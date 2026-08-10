import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const jsonPath = "D:/workspace/信息收集整理/work/pearl_delta_hospital_entry_ledger.json";
const outputPath =
  "D:/workspace/信息收集整理/医生画像仓库/99_资料来源/珠三角三甲医院官网入口台账.xlsx";
const previewMainPath =
  "D:/workspace/信息收集整理/work/pearl_delta_hospital_entry_ledger_preview_main.png";
const previewSummaryPath =
  "D:/workspace/信息收集整理/work/pearl_delta_hospital_entry_ledger_preview_summary.png";

const payload = JSON.parse(await fs.readFile(jsonPath, "utf8"));

function colLetter(n) {
  let s = "";
  while (n > 0) {
    const m = (n - 1) % 26;
    s = String.fromCharCode(65 + m) + s;
    n = Math.floor((n - 1) / 26);
  }
  return s;
}

function safeSheetName(name) {
  return name.slice(0, 31);
}

function matrixFromRows(headers, rows) {
  return [headers, ...rows.map((row) => headers.map((header) => row[header] ?? ""))];
}

function writeTable(workbook, name, headers, rows, tableName, widths = {}) {
  const sheet = workbook.worksheets.add(safeSheetName(name));
  const matrix = matrixFromRows(headers, rows);
  const lastCol = colLetter(headers.length);
  const lastRow = matrix.length;
  sheet.getRangeByIndexes(0, 0, matrix.length, headers.length).values = matrix;

  const used = sheet.getRange(`A1:${lastCol}${lastRow}`);
  used.format = {
    font: { name: "Microsoft YaHei", size: 10, color: "#111827" },
    wrapText: true,
    verticalAlignment: "top",
  };
  sheet.getRange(`A1:${lastCol}1`).format = {
    fill: "#155E75",
    font: { bold: true, color: "#FFFFFF", name: "Microsoft YaHei", size: 10 },
    horizontalAlignment: "center",
    verticalAlignment: "middle",
  };
  used.format.borders = {
    insideHorizontal: { style: "thin", color: "#E5E7EB" },
    top: { style: "thin", color: "#CBD5E1" },
    bottom: { style: "thin", color: "#CBD5E1" },
  };
  sheet.tables.add(`A1:${lastCol}${lastRow}`, true, tableName);
  sheet.freezePanes.freezeRows(1);
  sheet.showGridLines = false;
  headers.forEach((header, index) => {
    sheet.getRange(`${colLetter(index + 1)}:${colLetter(index + 1)}`).format.columnWidth =
      widths[header] ?? 16;
  });
  sheet.getRange(`A1:${lastCol}1`).format.rowHeight = 28;
  return sheet;
}

const workbook = Workbook.create();

const mainWidths = {
  序号: 7,
  推进批次: 8,
  城市: 10,
  区县: 12,
  医院名称: 28,
  医院别名: 18,
  医院等级: 12,
  医院类型: 12,
  官网首页_候选: 38,
  官网标题_自动识别: 30,
  医生目录入口_候选: 46,
  入口类型_自动判断: 16,
  是否可按科室_初判: 14,
  是否可全院采集_初判: 16,
  采集难度_初判: 18,
  官方确认状态: 18,
  自动置信度: 12,
  检索关键词: 28,
  搜索依据链接: 24,
  排除或注意事项: 34,
  下一步动作: 28,
  人工复核结果: 16,
  人工备注: 28,
  更新时间: 12,
};

const mainSheet = writeTable(
  workbook,
  "入口台账",
  payload.headers,
  payload.rows,
  "HospitalEntryLedger",
  mainWidths,
);
const mainRows = payload.rows.length + 1;
mainSheet.freezePanes.freezeColumns(5);
["I", "K", "R"].forEach((col) => {
  mainSheet.getRange(`${col}2:${col}${mainRows}`).format.wrapText = false;
});
mainSheet.getRange(`A2:X${mainRows}`).format.rowHeight = 42;

mainSheet.getRange(`V2:V${mainRows}`).dataValidation = {
  rule: { type: "list", values: ["确认可采集", "需修正链接", "暂缓", "排除"] },
};
mainSheet.getRange(`P2:P${mainRows}`).dataValidation = {
  rule: {
    type: "list",
    values: ["已试点确认", "自动候选-待人工复核", "已找到官网-待补医生入口", "未找到-待人工补充"],
  },
};
mainSheet.getRange(`O2:O${mainRows}`).conditionalFormats.add("containsText", {
  text: "A-",
  format: { fill: "#DCFCE7", font: { color: "#166534" } },
});
mainSheet.getRange(`O2:O${mainRows}`).conditionalFormats.add("containsText", {
  text: "B-",
  format: { fill: "#FEF9C3", font: { color: "#854D0E" } },
});
mainSheet.getRange(`O2:O${mainRows}`).conditionalFormats.add("containsText", {
  text: "C-",
  format: { fill: "#E0F2FE", font: { color: "#075985" } },
});
mainSheet.getRange(`O2:O${mainRows}`).conditionalFormats.add("containsText", {
  text: "D-",
  format: { fill: "#FEE2E2", font: { color: "#991B1B" } },
});
mainSheet.getRange(`Q2:Q${mainRows}`).conditionalFormats.add("containsText", {
  text: "高",
  format: { fill: "#DCFCE7", font: { color: "#166534" } },
});
mainSheet.getRange(`Q2:Q${mainRows}`).conditionalFormats.add("containsText", {
  text: "未找到",
  format: { fill: "#FEE2E2", font: { color: "#991B1B" } },
});

const summaryHeaders = ["城市", "医院数", "官网候选数", "医生入口候选数", "A级", "B级", "C级", "D级"];
const summarySheet = writeTable(
  workbook,
  "城市汇总",
  summaryHeaders,
  payload.city_summary,
  "CitySummary",
  {
    城市: 12,
    医院数: 10,
    官网候选数: 12,
    医生入口候选数: 16,
    A级: 10,
    B级: 10,
    C级: 10,
    D级: 10,
  },
);

const reviewRows = payload.rows.filter((row) => row["官方确认状态"] !== "已试点确认");
writeTable(
  workbook,
  "人工复核清单",
  [
    "城市",
    "医院名称",
    "官网首页_候选",
    "医生目录入口_候选",
    "采集难度_初判",
    "自动置信度",
    "下一步动作",
    "人工复核结果",
    "人工备注",
  ],
  reviewRows,
  "ManualReviewList",
  {
    城市: 10,
    医院名称: 30,
    官网首页_候选: 42,
    医生目录入口_候选: 46,
    采集难度_初判: 18,
    自动置信度: 12,
    下一步动作: 30,
    人工复核结果: 16,
    人工备注: 30,
  },
);

writeTable(
  workbook,
  "字段说明",
  ["字段", "说明"],
  payload.field_notes,
  "FieldNotes",
  { 字段: 24, 说明: 80 },
);

writeTable(
  workbook,
  "检索说明",
  ["项目", "内容"],
  [
    { 项目: "生成日期", 内容: payload.generated_at },
    { 项目: "源文件", 内容: payload.source_xlsx },
    { 项目: "源页签", 内容: payload.source_sheet },
    { 项目: "合规边界", 内容: "仅用于发现医院官网、官方医生/专家/科室入口；医生资料采集仍只允许医院官方公开渠道。" },
    { 项目: "人工复核原则", 内容: "自动候选链接必须人工打开确认后，才能进入正式医生数据采集。" },
    { 项目: "推进方式", 内容: "按城市分批推进；优先处理采集难度为 A 或 B 的医院。" },
  ],
  "SearchNotes",
  { 项目: 18, 内容: 100 },
);

const mainPreview = await workbook.render({
  sheetName: "入口台账",
  range: "A1:X18",
  scale: 1,
  format: "png",
});
await fs.writeFile(previewMainPath, new Uint8Array(await mainPreview.arrayBuffer()));

const summaryPreview = await workbook.render({
  sheetName: "城市汇总",
  autoCrop: "all",
  scale: 1,
  format: "png",
});
await fs.writeFile(previewSummaryPath, new Uint8Array(await summaryPreview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(`XLSX: ${outputPath}`);
console.log(`PREVIEW_MAIN: ${previewMainPath}`);
console.log(`PREVIEW_SUMMARY: ${previewSummaryPath}`);
