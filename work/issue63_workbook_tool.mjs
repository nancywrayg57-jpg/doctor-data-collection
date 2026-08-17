import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const MASTER_SHEETS = [
  ["自动采集底表", "A1:Y8"],
  ["复核清单", "A1:Y8"],
  ["科室统计", "A1:B12"],
  ["重点范围统计", "A1:B12"],
  ["医院统计", "A1:F12"],
  ["采集说明", "A1:B30"],
];
const LEDGER_SHEETS = [
  ["入口台账", "A1:X18"],
  ["城市汇总", "A1:H20"],
  ["人工复核清单", "A1:I12"],
  ["字段说明", "A1:B30"],
  ["检索说明", "A1:B12"],
];
const LEDGER_SEQUENCE = "15";
const LEDGER_HOSPITAL = "南部战区空军医院";
const LEDGER_SKIP_NOTE = "管理员裁决跳过（军队医院，2026-08-17）";

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    args[key] = argv[i + 1] ?? true;
    i += 1;
  }
  return args;
}

async function importWorkbook(filePath) {
  return SpreadsheetFile.importXlsx(await FileBlob.load(filePath));
}

function safeName(value) {
  return value.replace(/[\\/:*?"<>|]/g, "_");
}

async function renderSheets(workbook, sheets, outputDir, prefix) {
  await fs.mkdir(outputDir, { recursive: true });
  const outputs = [];
  for (const [sheetName, range] of sheets) {
    const image = await workbook.render({
      sheetName,
      range,
      scale: 1,
      format: "png",
    });
    const output = path.join(outputDir, `${prefix}_${safeName(sheetName)}.png`);
    await fs.writeFile(output, new Uint8Array(await image.arrayBuffer()));
    outputs.push(output);
  }
  return outputs;
}

async function inspectWorkbook(workbook, label, sheets) {
  const sheetSummary = await workbook.inspect({
    kind: "sheet",
    include: "id,name",
    maxChars: 4000,
  });
  const formulaErrors = await workbook.inspect({
    kind: "match",
    searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
    options: { useRegex: true, maxResults: 100 },
    summary: `${label} formula error scan`,
    maxChars: 4000,
  });
  const keyRange = label === "ledger" ? "A1:X18" : "A1:Y8";
  const keySheet = label === "ledger" ? "入口台账" : "自动采集底表";
  const keyValues = await workbook.inspect({
    kind: "region",
    sheetId: keySheet,
    range: keyRange,
    maxChars: 6000,
    tableMaxRows: 18,
    tableMaxCols: 25,
    tableMaxCellChars: 100,
  });
  const keyStyles = await workbook.inspect({
    kind: "computedStyle",
    sheetId: keySheet,
    range: label === "ledger" ? "T15:U17" : "Q1:R4",
    maxChars: 3000,
  });
  return {
    sheets: sheetSummary.ndjson,
    formulaErrors: formulaErrors.ndjson,
    keyValues: keyValues.ndjson,
    keyStyles: keyStyles.ndjson,
    expectedSheets: sheets.map(([name]) => name),
  };
}

function updateLedgerRow(workbook) {
  const sheet = workbook.worksheets.getItem("入口台账");
  const used = sheet.getUsedRange();
  const values = used.values;
  if (!Array.isArray(values) || values.length < 2) {
    throw new Error("入口台账工作表为空");
  }
  const headers = values[0].map((value) => String(value ?? ""));
  const sequenceCol = headers.indexOf("序号");
  const hospitalCol = headers.indexOf("医院名称");
  const noteCol = headers.indexOf("排除或注意事项");
  const actionCol = headers.indexOf("下一步动作");
  if ([sequenceCol, hospitalCol, noteCol, actionCol].some((index) => index < 0)) {
    throw new Error("入口台账缺少 Issue #63 附带条款所需列");
  }
  const matches = [];
  for (let rowIndex = 1; rowIndex < values.length; rowIndex += 1) {
    if (
      String(values[rowIndex][sequenceCol] ?? "") === LEDGER_SEQUENCE &&
      String(values[rowIndex][hospitalCol] ?? "") === LEDGER_HOSPITAL
    ) {
      matches.push(rowIndex);
    }
  }
  if (matches.length !== 1) {
    throw new Error(`入口台账序号 15 目标行不唯一：${matches.length}`);
  }
  const rowIndex = matches[0];
  const oldNote = String(values[rowIndex][noteCol] ?? "").trim();
  const noteParts = oldNote.split("；").map((item) => item.trim()).filter(Boolean);
  if (!noteParts.includes(LEDGER_SKIP_NOTE)) noteParts.push(LEDGER_SKIP_NOTE);
  const newNote = noteParts.join("；");
  sheet.getCell(rowIndex, noteCol).values = [[newNote]];
  sheet.getCell(rowIndex, actionCol).values = [["跳过"]];
  return {
    worksheetRow: rowIndex + 1,
    oldNote,
    newNote,
    oldAction: String(values[rowIndex][actionCol] ?? ""),
    newAction: "跳过",
  };
}

async function readLedgerRow(workbook) {
  const sheet = workbook.worksheets.getItem("入口台账");
  const values = sheet.getUsedRange().values;
  const headers = values[0].map((value) => String(value ?? ""));
  const sequenceCol = headers.indexOf("序号");
  const hospitalCol = headers.indexOf("医院名称");
  const noteCol = headers.indexOf("排除或注意事项");
  const actionCol = headers.indexOf("下一步动作");
  const matches = values
    .map((row, rowIndex) => ({ row, rowIndex }))
    .filter(
      ({ row, rowIndex }) =>
        rowIndex > 0 &&
        String(row[sequenceCol] ?? "") === LEDGER_SEQUENCE &&
        String(row[hospitalCol] ?? "") === LEDGER_HOSPITAL,
    );
  if (matches.length !== 1) {
    throw new Error(`入口台账序号 15 目标行不唯一：${matches.length}`);
  }
  const { row, rowIndex } = matches[0];
  const errors = await workbook.inspect({
    kind: "match",
    searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
    options: { useRegex: true, maxResults: 100 },
    summary: "ledger formula error scan",
    maxChars: 4000,
  });
  return {
    worksheetRow: rowIndex + 1,
    sequence: String(row[sequenceCol] ?? ""),
    hospital: String(row[hospitalCol] ?? ""),
    note: String(row[noteCol] ?? ""),
    action: String(row[actionCol] ?? ""),
    formulaErrors: errors.ndjson,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.mode === "inspect") {
    if (!args.master || !args.ledger || !args["preview-dir"]) {
      throw new Error("inspect 需要 --master --ledger --preview-dir");
    }
    const master = await importWorkbook(args.master);
    const ledger = await importWorkbook(args.ledger);
    const masterInspect = await inspectWorkbook(master, "master", MASTER_SHEETS);
    const ledgerInspect = await inspectWorkbook(ledger, "ledger", LEDGER_SHEETS);
    const masterPreviews = await renderSheets(
      master,
      MASTER_SHEETS,
      args["preview-dir"],
      "master",
    );
    const ledgerPreviews = await renderSheets(
      ledger,
      LEDGER_SHEETS,
      args["preview-dir"],
      "ledger",
    );
    console.log(JSON.stringify({ masterInspect, ledgerInspect, masterPreviews, ledgerPreviews }));
    return;
  }

  if (args.mode === "edit-ledger") {
    if (!args.input || !args.output || !args["preview-dir"]) {
      throw new Error("edit-ledger 需要 --input --output --preview-dir");
    }
    const workbook = await importWorkbook(args.input);
    const change = updateLedgerRow(workbook);
    const errors = await workbook.inspect({
      kind: "match",
      searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
      options: { useRegex: true, maxResults: 100 },
      summary: "ledger post-edit formula error scan",
      maxChars: 4000,
    });
    const previews = await renderSheets(
      workbook,
      LEDGER_SHEETS,
      args["preview-dir"],
      "ledger_post",
    );
    const output = await SpreadsheetFile.exportXlsx(workbook);
    await output.save(args.output);
    console.log(JSON.stringify({ change, formulaErrors: errors.ndjson, previews }));
    return;
  }

  if (args.mode === "read-ledger") {
    if (!args.input) throw new Error("read-ledger 需要 --input");
    const workbook = await importWorkbook(args.input);
    console.log(JSON.stringify(await readLedgerRow(workbook)));
    return;
  }

  throw new Error("--mode 必须为 inspect、edit-ledger 或 read-ledger");
}

await main();
