# -*- coding: utf-8 -*-
"""将 test-cases.md 转成可重复使用的结构化验收集。

保留原始期望文本，避免机械解析时丢失产品语义；路由和轮数只作为
验收初始标签，后续允许在评审时人工修正。
"""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "test-cases.md"
OUTPUT = ROOT / "evaluation" / "cases.json"


def infer_route(expected_lines):
    text = " ".join(expected_lines)
    if "深度探索" in text:
        return "deep_exploration"
    if any(token in text for token in ("直接开始", "直接分析", "直接执行")):
        return "direct_execution"
    return "quick_clarify"


def infer_task_type(case_id, expected_lines):
    text = " ".join(expected_lines)
    if case_id.startswith("B"):
        return "辅助决策"
    if case_id.startswith("C"):
        return "制定路径"
    if case_id.startswith("D7") or "问题诊断" in text:
        return "问题诊断"
    if case_id.startswith("D"):
        return "创造设计"
    if case_id.startswith("E"):
        return "生成内容"
    return "状态探索"


def parse_cases(markdown):
    category = None
    current = None
    cases = []

    def finish():
        if not current:
            return
        expected = current["expected_behavior"]
        forbidden = current["forbidden_behavior"]
        route = infer_route(expected)
        current.update(
            {
                "task_type": infer_task_type(current["id"], expected),
                "expected_route": route,
                "max_turns": 5 if route == "deep_exploration" else 0 if route == "direct_execution" else 3,
                "first_question": None,
                "review": {
                    "route_correct": None,
                    "first_question_effective": None,
                    "over_questioning": None,
                    "actual_turns": None,
                    "failure_reason": "",
                },
                "forbidden_behavior": forbidden,
            }
        )
        cases.append(current)

    for line in markdown.splitlines():
        category_match = re.match(r"^##\s+(.+?)（10条）", line)
        if category_match:
            finish()
            current = None
            category = category_match.group(1)
            continue

        case_match = re.match(r"^###\s+([A-Z]\d+)$", line)
        if case_match:
            finish()
            current = {
                "id": case_match.group(1),
                "category": category,
                "input": "",
                "expected_behavior": [],
                "forbidden_behavior": [],
                "_section": None,
            }
            continue

        if not current:
            continue

        if line.startswith("**用户输入**："):
            current["input"] = line.split("：", 1)[1].strip()
            current["_section"] = "expected_behavior"
        elif line.startswith("**期望行为**："):
            current["_section"] = "expected_behavior"
        elif line.startswith("**不应该**："):
            current["forbidden_behavior"].append(line.split("：", 1)[1].strip())
            current["_section"] = "forbidden_behavior"
        elif line.startswith("- ") and current["_section"]:
            current[current["_section"]].append(line[2:].strip())

    finish()
    for item in cases:
        item.pop("_section", None)
    return cases


def main():
    cases = parse_cases(SOURCE.read_text(encoding="utf-8"))
    if len(cases) != 50:
        raise SystemExit(f"expected 50 cases, got {len(cases)}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(cases, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"generated {len(cases)} cases -> {OUTPUT}")


if __name__ == "__main__":
    main()
