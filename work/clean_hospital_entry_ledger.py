from __future__ import annotations

import json
from pathlib import Path

import discover_hospital_entry_ledger as d


JSON_OUT = Path(r"D:\workspace\信息收集整理\work\pearl_delta_hospital_entry_ledger.json")
CSV_OUT = Path(r"D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院官网入口台账.csv")
REPORT_OUT = Path(r"D:\workspace\信息收集整理\医生画像仓库\99_资料来源\珠三角三甲医院官网入口台账_自动检索报告.md")


def is_bad_url(url: str) -> bool:
    host = d.canonical_host(url)
    return bool(url) and d.domain_is_bad(host)


def main() -> None:
    payload = json.loads(JSON_OUT.read_text(encoding="utf-8"))
    rows = payload["rows"]
    for row in rows:
        if is_bad_url(row["官网首页_候选"]):
            row["官网首页_候选"] = ""
            row["官网标题_自动识别"] = ""
        if is_bad_url(row["医生目录入口_候选"]):
            row["医生目录入口_候选"] = ""
            row["入口类型_自动判断"] = ""
        if not row["官网首页_候选"]:
            row["医生目录入口_候选"] = ""
            row["入口类型_自动判断"] = ""
            row["是否可按科室_初判"] = ""
            row["是否可全院采集_初判"] = ""
            if row["官方确认状态"] != "已试点确认":
                row["官方确认状态"] = "未找到-待人工补充"
                row["自动置信度"] = "未找到"
                row["采集难度_初判"] = "D-待人工补官网"
        else:
            if row["医生目录入口_候选"]:
                if row["官方确认状态"] != "已试点确认":
                    row["官方确认状态"] = "自动候选-待人工复核"
                if row["采集难度_初判"].startswith("D-"):
                    row["采集难度_初判"] = d.difficulty(
                        row["入口类型_自动判断"],
                        row["官网首页_候选"],
                        row["医生目录入口_候选"],
                    )
            elif row["官方确认状态"] != "已试点确认":
                row["官方确认状态"] = "已找到官网-待补医生入口"
                row["采集难度_初判"] = "C-仅官网待找入口"
        row["下一步动作"] = d.next_action(row)

    payload["city_summary"] = d.summarize_by_city(rows)
    JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    d.write_csv(rows)
    REPORT_OUT.write_text(d.build_report(rows, payload["city_summary"]), encoding="utf-8")
    print(f"cleaned_rows={len(rows)}")
    print(f"json={JSON_OUT}")
    print(f"csv={CSV_OUT}")
    print(f"report={REPORT_OUT}")


if __name__ == "__main__":
    main()
