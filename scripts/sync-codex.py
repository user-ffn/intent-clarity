#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步脚本：以 skill/SKILL.md（Claude 版）为唯一源，生成 codex/SKILL.md（Codex 版）。

为什么需要转换而不是直接复制：
- Claude Code 的 SKILL.md frontmatter 支持 name / description / whenToUse 三个字段。
- Codex 只识别 name / description，不认识 whenToUse —— 触发条件必须合并进 description，
  否则 Codex 侧完全不知道什么时候该用这个 skill。
- 正文中"给Claude"这类只对 Claude Code 有意义的措辞，在 Codex 版里改成中性表述。

用法：
    python scripts/sync-codex.py

改完 skill/SKILL.md 后跑一次这个脚本，codex/SKILL.md 就会自动跟上，
不需要手动逐段搬运，避免两份文件慢慢漂移。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "skill" / "SKILL.md"
DST = ROOT / "codex" / "SKILL.md"


def convert(text: str) -> str:
    # 1. 解析并重写 frontmatter：把 whenToUse 的内容合并进 description，去掉 whenToUse 字段。
    fm_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not fm_match:
        raise ValueError("SKILL.md 缺少 frontmatter，无法转换")

    frontmatter = fm_match.group(1)
    body = text[fm_match.end():]

    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    when_match = re.search(
        r"^whenToUse:\s*\|\n((?:^[ \t]+.*\n?)*)", frontmatter, re.MULTILINE
    )

    if not name_match or not desc_match:
        raise ValueError("frontmatter 缺少 name 或 description，无法转换")

    name = name_match.group(1).strip()
    description = desc_match.group(1).strip()

    if when_match:
        when_lines = [
            line.strip().lstrip("- ").strip()
            for line in when_match.group(1).splitlines()
            if line.strip()
        ]
        # 触发条件本身有一行说明性文字（"用户的表达包含以下任一特征时自动触发："），
        # 剩下的是具体特征列表，拼接成一句话接在 description 后面。
        trigger_items = [line for line in when_lines if not line.endswith("：") and not line.endswith(":")]
        if trigger_items:
            # 触发条件原文可能已经自带中英文引号（如 "想做X但..."），不再重复包一层，
            # 避免生成 “"..."” 这种双重引号。
            description = (
                f"{description}当用户表达出现以下任一特征时触发："
                + "、".join(trigger_items)
                + "。"
            )

    new_frontmatter = f"---\nname: {name}\ndescription: {description}\n---\n"

    # 2. 正文里把只对 Claude Code 有意义的措辞改成中性表述。
    body = body.replace("## 实现提示（给Claude）", "## 实现提示")

    return new_frontmatter + body


def main() -> int:
    if not SRC.exists():
        print(f"找不到源文件：{SRC}", file=sys.stderr)
        return 1

    text = SRC.read_text(encoding="utf-8")
    converted = convert(text)

    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(converted, encoding="utf-8", newline="\n")

    print(f"已生成：{DST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
