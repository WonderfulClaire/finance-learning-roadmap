#!/usr/bin/env python3
"""把入口文件里指向 docs/XX.md 的课程链接批量改为 lessons/XX.html"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = [ROOT / "index.html", ROOT / "README.md", ROOT / "README_EN.md", ROOT / "INDEX.md"]

pat = re.compile(r'docs/(\d{2}-[^)\s"]+)\.md')

def repl(m):
    return f"lessons/{m.group(1)}.html"

for f in FILES:
    if not f.exists():
        continue
    text = f.read_text(encoding="utf-8")
    new = pat.sub(repl, text)
    if new != text:
        f.write_text(new, encoding="utf-8")
        print("UPDATED", f.name)
    else:
        print("NO CHANGE", f.name)
