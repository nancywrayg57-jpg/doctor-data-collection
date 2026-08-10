import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const jsonPath = "D:/workspace/信息收集整理/work/sysu5_doctors_auto_base.json";
const outputPath =
  "D:/workspace/信息收集整理/医生画像仓库/99_资料来源/中山大学附属第五医院_全院医生自动采集底表.xlsx";
const previewPath =
  "D:/workspace/信息收集整理/work/sysu5_doctors_auto_base_preview.png";

const payload = JSON.parse(await fs.readFile(jsonPath, "utf8"));
payload.rows.forEach((row, index) => {
  row["序号"] = index + 1;
});
await fs.writeFile(jsonPath, JSON.stringify(payload, null, 2), "utf8");

const csvPath =
  "D:/workspace/信息收集整理/医生画像仓库/99_资料来源/中山大学附属第五医院_全院医生自动采集底表.csv";

function csvEscape(value) {
  const text = value === null || value === undefined ? "" : String(value);
  if (/[",\r\n]/.test(text)) {
    return `"${text.replaceAll('"', '""')}"`;
  }
  return text;
}

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

function writeTable(workbook, name, headers, rows, tableName, widths = {}) {
  const sheet = workbook.worksheets.add(safeSheetName(name));
  const matrix = [headers, ...rows.map((row) => headers.map((header) => row[header] ?? ""))];
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
    fill: "#1F6F78",
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

  headers.forEach((header, idx) => {
    const columnRange = sheet.getRange(`${colLetter(idx + 1)}:${colLetter(idx + 1)}`);
    columnRange.format.columnWidth = widths[header] ?? 16;
  });
  sheet.getRange(`A1:${lastCol}1`).format.rowHeight = 26;
  return sheet;
}

const workbook = Workbook.create();

const baseHeaders = [
  "序号",
  "医院",
  "姓名",
  "科室_分类页",
  "科室_列表卡片",
  "职称_关键词",
  "职称身份原文",
  "重点优先级",
  "重点关注范围",
  "重点疾病标签",
  "擅长诊疗方向摘录",
  "亮眼经历线索",
  "列表简介",
  "详情正文摘录",
  "来源类型",
  "来源链接",
  "采集入口",
  "采集方式",
  "采集日期",
  "详情页状态",
  "已建画像",
  "异常提示",
  "复核状态",
];

const csvText = [
  baseHeaders.join(","),
  ...payload.rows.map((row) => baseHeaders.map((header) => csvEscape(row[header])).join(",")),
].join("\r\n");
await fs.writeFile(csvPath, `\uFEFF${csvText}`, "utf8");

const baseSheet = writeTable(
  workbook,
  "自动采集底表",
  baseHeaders,
  payload.rows,
  "DoctorAutoBaseTable",
  {
    序号: 8,
    医院: 18,
    姓名: 12,
    科室_分类页: 24,
    科室_列表卡片: 24,
    职称_关键词: 30,
    职称身份原文: 42,
    重点优先级: 12,
    重点关注范围: 22,
    重点疾病标签: 34,
    擅长诊疗方向摘录: 56,
    亮眼经历线索: 56,
    列表简介: 44,
    详情正文摘录: 70,
    来源类型: 12,
    来源链接: 58,
    采集入口: 58,
    采集方式: 24,
    采集日期: 14,
    详情页状态: 12,
    已建画像: 12,
    异常提示: 28,
    复核状态: 14,
  },
);
baseSheet.getRange(`A2:W${payload.rows.length + 1}`).format.rowHeight = 64;

const reviewRows = payload.rows.filter((row) => row["异常提示"]);
writeTable(workbook, "复核清单", baseHeaders, reviewRows, "DoctorReviewTable", {
  序号: 8,
  医院: 18,
  姓名: 12,
  科室_分类页: 24,
  科室_列表卡片: 24,
  职称_关键词: 30,
  职称身份原文: 42,
  重点优先级: 12,
  重点关注范围: 22,
  重点疾病标签: 34,
  擅长诊疗方向摘录: 56,
  亮眼经历线索: 56,
  列表简介: 44,
  详情正文摘录: 70,
  来源类型: 12,
  来源链接: 58,
  采集入口: 58,
  采集方式: 24,
  采集日期: 14,
  详情页状态: 12,
  已建画像: 12,
  异常提示: 28,
  复核状态: 14,
});

const deptRows = payload.category_counts.map(([department, count]) => ({
  科室分类: department,
  医生数: count,
}));
writeTable(workbook, "科室统计", ["科室分类", "医生数"], deptRows, "DepartmentStatsTable", {
  科室分类: 28,
  医生数: 12,
});

const groupRows = Object.entries(payload.group_counts).map(([group, count]) => ({
  重点关注范围: group,
  医生数: count,
}));
writeTable(workbook, "重点范围统计", ["重点关注范围", "医生数"], groupRows, "FocusStatsTable", {
  重点关注范围: 24,
  医生数: 12,
});

const metaRows = [
  { 项目: "医院", 内容: payload.meta.hospital },
  { 项目: "官网入口", 内容: payload.meta.entry_url },
  { 项目: "采集日期", 内容: payload.meta.collected_at },
  { 项目: "官网分类数", 内容: payload.meta.category_count },
  { 项目: "原始医生卡片记录", 内容: payload.meta.raw_card_rows },
  { 项目: "唯一医生详情页", 内容: payload.meta.unique_doctor_count },
  { 项目: "分类页失败数", 内容: payload.meta.category_error_count },
  { 项目: "详情页失败数", 内容: payload.meta.detail_error_count },
  { 项目: "已建画像匹配数", 内容: payload.meta.existing_profile_count },
  {
    项目: "合规边界",
    内容:
      "仅使用医院官网公开网页；不采集私人联系方式、患者隐私、第三方评价；自动亮点仅作线索，必须人工复核后再对外包装。",
  },
];
writeTable(workbook, "采集说明", ["项目", "内容"], metaRows, "CollectionNotesTable", {
  项目: 24,
  内容: 90,
});

const inspect = await workbook.inspect({
  kind: "region",
  sheetId: "自动采集底表",
  range: "A1:W5",
  maxChars: 2500,
});
console.log(inspect.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

const preview = await workbook.render({
  sheetName: "自动采集底表",
  range: "A1:W18",
  scale: 1,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));

const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);
console.log(JSON.stringify({ outputPath, previewPath }, null, 2));
process.exit(0);
