#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 docs/*.md 渲染成 lessons/*.html
用法：在仓库根目录执行
    python scripts/build_lessons.py
依赖：pip install markdown
"""
import json
import re
from pathlib import Path

try:
    import markdown
    from markdown.extensions import fenced_code, tables, toc
except ImportError as e:
    raise SystemExit("请先安装 markdown：pip install markdown") from e

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
LESSONS = ROOT / "lessons"
DATA = ROOT / "data"
ASSETS = ROOT / "assets"

LESSONS.mkdir(exist_ok=True)

# 课程顺序与阶段信息（与 learn.html 保持一致）
STAGES = [
    {"id": "s1", "name": "阶段一 · 启航", "badge": "🚀 启航者"},
    {"id": "s2", "name": "阶段二 · 基础", "badge": "💰 资产管家"},
    {"id": "s3", "name": "阶段三 · 权益", "badge": "📈 权益投资人"},
    {"id": "s4", "name": "阶段四 · 策略", "badge": "🎯 策略大师"},
    {"id": "s5", "name": "阶段五 · 进阶", "badge": "🏆 理财宗师"},
]

MODULES = [
    {"id": "m00", "stage": 0, "title": "M00 启航：为什么理财与防坑", "file": "00-启航-为什么理财与防坑.md"},
    {"id": "m01", "stage": 1, "title": "M01 资产地图与工具箱", "file": "01-资产地图与工具箱.md"},
    {"id": "m02", "stage": 1, "title": "M02 现金与固收", "file": "02-现金与固收.md"},
    {"id": "m03", "stage": 2, "title": "M03 指数基金入门", "file": "03-指数基金入门.md"},
    {"id": "m04", "stage": 2, "title": "M04 主动基金与股票入门", "file": "04-主动基金与股票入门.md"},
    {"id": "m05", "stage": 3, "title": "M05 资产配置与定投", "file": "05-资产配置与定投.md"},
    {"id": "m06", "stage": 3, "title": "M06 估值指标与择时", "file": "06-估值指标与择时.md"},
    {"id": "m07", "stage": 4, "title": "M07 进阶：财报与量化初探", "file": "07-进阶-财报与量化初探.md"},
    {"id": "m08", "stage": 4, "title": "M08 保险与养老税务", "file": "08-保险与养老税务.md"},
]

MD_FILE_TO_MODULE = {m["file"]: m for m in MODULES}


def load_quizzes():
    qf = DATA / "quizzes.json"
    if qf.exists():
        return json.loads(qf.read_text(encoding="utf-8"))
    return {}


QUIZZES = load_quizzes()


def slug_for(filename: str) -> str:
    return Path(filename).stem


def html_filename(md_file: str) -> str:
    return Path(md_file).with_suffix(".html").name


def md_to_html(md_path: Path) -> tuple[str, str]:
    md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])
    body = md.convert(md_path.read_text(encoding="utf-8"))
    return body, md.toc


def fix_links_and_wikilinks(body: str, current_md: str) -> str:
    # wikilinks like [[资产配置]] -> styled span
    body = re.sub(r"\[\[([^\]]+)\]\]", r'<span class="wikilink">\1</span>', body)

    # markdown links: docs/XX.md -> lessons/XX.html
    def repl_docs(m):
        text, url = m.group(1), m.group(2)
        if url.startswith("docs/") and url.endswith(".md"):
            # lesson pages live in the same lessons/ folder
            return f'[{text}]({html_filename(Path(url).name)})'
        if url == "README.md":
            return f'[{text}](../index.html)'
        return m.group(0)

    body = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_docs, body)
    return body


def quiz_html(module_id: str) -> str:
    quiz = QUIZZES.get(module_id)
    if not quiz or not quiz.get("questions"):
        return ""
    items = []
    for i, q in enumerate(quiz["questions"], 1):
        opts = "\n".join(
            f'<label class="opt" data-q="{i}" data-opt="{j}">'
            f'<input type="radio" name="q{i}" value="{j}"> <span>{chr(0x41+j)}. {opt}</span>'
            f'</label>'
            for j, opt in enumerate(q["options"])
        )
        items.append(
            f'<div class="q" id="quiz-q{i}">'
            f'<p class="qt"><b>Q{i}.</b> {q["question"]}</p>'
            f'<div class="opts">{opts}</div>'
            f'<div class="feedback" id="fb-q{i}"></div>'
            f'</div>'
        )
    questions_block = "\n".join(items)
    answers_js = json.dumps([q["answer"] for q in quiz["questions"]], ensure_ascii=False)
    explanations_js = json.dumps([q.get("explanation", "") for q in quiz["questions"]], ensure_ascii=False)
    return f'''
<section class="quiz card" id="quiz">
  <h2>🧩 课后小测验</h2>
  <p class="note">答完立刻出答案与解析，巩固本节要点。</p>
  {questions_block}
</section>
<script>
(function(){{
  const answers = {answers_js};
  const explanations = {explanations_js};
  document.querySelectorAll('.opt').forEach(label => {{
    label.addEventListener('click', function(e){{
      if(e.target.tagName === 'INPUT') e.preventDefault();
      const qIdx = parseInt(this.dataset.q) - 1;
      const chosen = parseInt(this.dataset.opt);
      const correct = answers[qIdx];
      const fb = document.getElementById('fb-q' + (qIdx+1));
      const all = this.closest('.opts').querySelectorAll('.opt');
      all.forEach(l => l.classList.add('disabled'));
      if (chosen === correct) {{
        this.classList.add('correct');
        fb.innerHTML = '<span class="ok">✅ 正确！</span> ' + explanations[qIdx];
      }} else {{
        this.classList.add('wrong');
        all[correct].classList.add('correct');
        fb.innerHTML = '<span class="bad">❌ 不对。</span> ' + explanations[qIdx];
      }}
    }});
  }});
}})();
</script>
'''


def build_page(md_path: Path, module: dict, prev_mod: dict | None, next_mod: dict | None) -> str:
    body_raw, toc_html = md_to_html(md_path)
    body = fix_links_and_wikilinks(body_raw, md_path.name)

    stage = STAGES[module["stage"]]
    prev_link = f'<a class="navprev" href="{html_filename(prev_mod["file"])}">← {prev_mod["title"]}</a>' if prev_mod else '<span></span>'
    next_link = f'<a class="navnext" href="{html_filename(next_mod["file"])}">{next_mod["title"]} →</a>' if next_mod else '<span></span>'

    quiz = quiz_html(module["id"])

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="description" content="{module['title']} · 个人理财系统学习路线"/>
<meta property="og:title" content="{module['title']}"/>
<meta property="og:description" content="从零基础到资产配置的中文开源理财教程"/>
<meta property="og:image" content="https://wonderfulclaire.github.io/finance-learning-roadmap/assets/share-card.png"/>
<title>{module['title']} · 理财学习路线</title>
<style>
:root{{
  --bg:#ffffff;--fg:#1f2a44;--muted:#6b7280;--line:#e5e7eb;
  --brand:#4e79a7;--brand2:#f28e2b;--ok:#59a14f;--bad:#e15759;--gold:#c8a24a;
  --card:#f8fafc;--shadow:0 8px 30px rgba(15,23,42,.08);
}}
@media(prefers-color-scheme:dark){{
  :root{{--bg:#0f172a;--fg:#e2e8f0;--muted:#94a3b8;--line:#233044;--card:#111c33;--shadow:0 8px 30px rgba(0,0,0,.4);}}
}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--fg);line-height:1.7}}
a{{color:var(--brand);text-decoration:none}}
a:hover{{text-decoration:underline}}
header.hero{{background:linear-gradient(135deg,#1f2a44,#32507a);color:#fff;padding:32px 20px 24px}}
header.hero .hwrap{{max-width:980px;margin:0 auto}}
header.hero h1{{margin:0;font-size:26px}}
header.hero .meta{{margin-top:8px;font-size:13px;color:#cbd5e1}}
nav.top{{max-width:980px;margin:0 auto;padding:14px 20px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;font-size:13px}}
nav.top a.back{{color:var(--muted)}}
nav.top .stage{{margin-left:auto;color:var(--muted)}}
nav.lesson-nav{{max-width:980px;margin:0 auto;padding:0 20px 28px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}}
nav.lesson-nav a{{padding:10px 14px;border:1px solid var(--line);border-radius:8px;background:var(--card);font-size:13px;max-width:48%}}
main.wrap{{max-width:980px;margin:0 auto;padding:0 20px 40px;display:grid;grid-template-columns:minmax(0,1fr);gap:24px}}
@media(min-width:900px){{
  main.wrap{{grid-template-columns:220px 1fr}}
}}
aside.toc{{display:none}}
@media(min-width:900px){{
  aside.toc{{display:block;position:sticky;top:24px;align-self:start;font-size:13px}}
  aside.toc ul{{list-style:none;padding:0;margin:0;border-left:2px solid var(--line);padding-left:12px}}
  aside.toc li{{margin:8px 0}}
  aside.toc a{{color:var(--muted)}}
  aside.toc a:hover{{color:var(--brand)}}
}}
article{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:28px;box-shadow:var(--shadow)}}
article h1{{font-size:28px;margin-top:0}}
article h2{{font-size:20px;margin-top:32px;padding-bottom:8px;border-bottom:1px solid var(--line)}}
article h3{{font-size:17px;margin-top:24px}}
article p{{margin:.8em 0}}
article blockquote{{margin:1em 0;padding:12px 16px;border-left:4px solid var(--brand);background:var(--bg);border-radius:0 8px 8px 0;color:var(--muted)}}
article img{{max-width:100%;height:auto;border-radius:8px;margin:12px 0}}
article table{{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px}}
article th,article td{{border:1px solid var(--line);padding:10px;text-align:left}}
article th{{background:var(--bg);font-weight:700}}
article code{{background:rgba(0,0,0,.06);padding:2px 6px;border-radius:4px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.9em}}
article pre{{background:#0f172a;color:#e2e8f0;padding:16px;border-radius:10px;overflow:auto}}
article pre code{{background:transparent;color:inherit;padding:0}}
article ul,article ol{{padding-left:22px}}
article li{{margin:.35em 0}}
.wikilink{{background:rgba(78,121,167,.12);color:var(--brand);padding:1px 6px;border-radius:4px;font-weight:600}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px;box-shadow:var(--shadow);margin:22px 0}}
.complete-bar{{display:flex;gap:12px;flex-wrap:wrap;align-items:center}}
.complete-bar button{{padding:12px 20px;border:0;border-radius:8px;background:var(--ok);color:#fff;font-size:15px;font-weight:700;cursor:pointer}}
.complete-bar button:hover{{filter:brightness(1.08)}}
.complete-bar button.done{{background:var(--gold)}}
.complete-bar .msg{{font-size:13px;color:var(--muted)}}
.quiz .q{{margin:18px 0;padding:16px;border:1px solid var(--line);border-radius:10px;background:var(--bg)}}
.quiz .qt{{margin-top:0}}
.quiz .opts{{display:flex;flex-direction:column;gap:8px}}
.quiz .opt{{padding:10px 12px;border:1px solid var(--line);border-radius:8px;cursor:pointer;background:var(--card);display:flex;align-items:flex-start;gap:8px}}
.quiz .opt:hover{{border-color:var(--brand)}}
.quiz .opt.disabled{{pointer-events:none}}
.quiz .opt.correct{{border-color:var(--ok);background:rgba(89,161,79,.12)}}
.quiz .opt.wrong{{border-color:var(--bad);background:rgba(225,87,89,.12)}}
.quiz .opt input{{margin-top:3px;flex:none}}
.quiz .feedback{{margin-top:10px;font-size:14px}}
.quiz .feedback .ok{{color:var(--ok);font-weight:700}}
.quiz .feedback .bad{{color:var(--bad);font-weight:700}}
.note{{font-size:13px;color:var(--muted);margin-top:8px}}
footer{{text-align:center;color:var(--muted);font-size:13px;padding:20px}}
#toast{{position:fixed;left:50%;top:24px;transform:translateX(-50%) translateY(-120%);background:linear-gradient(135deg,var(--gold),var(--brand2));color:#fff;font-weight:700;padding:14px 22px;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.25);z-index:9999;transition:transform .4s cubic-bezier(.2,1.2,.4,1);font-size:15px}}
#toast.show{{transform:translateX(-50%) translateY(0)}}
</style>
</head>
<body>
<div id="toast"></div>
<header class="hero">
  <div class="hwrap">
    <h1>{module['title']}</h1>
    <div class="meta">{stage['name']} · {stage['badge']} · 个人理财系统学习路线</div>
  </div>
</header>
<nav class="top">
  <a class="back" href="../index.html">← 交互式计算器</a>
  <a class="back" href="../learn.html">🎮 里程碑</a>
  <span class="stage">{stage['badge']}</span>
</nav>
<nav class="lesson-nav">
  {prev_link}
  {next_link}
</nav>
<main class="wrap">
  <aside class="toc">
    <b>目录</b>
    {toc_html}
  </aside>
  <article>
    {body}
  </article>
</main>
<section class="card" style="max-width:980px;margin:0 auto 24px;">
  <div class="complete-bar">
    <button id="markBtn" onclick="toggleComplete()">✅ 标记本节为「已完成」</button>
    <span class="msg" id="completeMsg"></span>
  </div>
  <p class="note">进度保存在浏览器 localStorage，返回<a href="../learn.html">🎮 里程碑页</a>可查看徽章与证书。</p>
</section>
{quiz}
<footer>
  ⚠️ 本项目仅供学习，不构成投资建议 · <a href="https://github.com/WonderfulClaire/finance-learning-roadmap">GitHub</a>
</footer>
<script>
const MODULE_ID = '{module['id']}';
const STORE = 'flr_progress_v1';
const STAGE_ID = '{stage['id']}';
function getDone(){{ return new Set(JSON.parse(localStorage.getItem(STORE) || '[]')); }}
function saveDone(s){{ localStorage.setItem(STORE, JSON.stringify([...s])); }}
function toast(msg){{
  const t = document.getElementById('toast'); t.textContent = msg; t.classList.add('show');
  clearTimeout(t._tm); t._tm = setTimeout(() => t.classList.remove('show'), 3000);
}}
function updateBtn(){{
  const done = getDone();
  const btn = document.getElementById('markBtn');
  const msg = document.getElementById('completeMsg');
  if (done.has(MODULE_ID)) {{
    btn.textContent = '✓ 本节已完成（点击取消）';
    btn.classList.add('done');
    msg.textContent = '进度已同步到 milestones 页';
  }} else {{
    btn.textContent = '✅ 标记本节为「已完成」';
    btn.classList.remove('done');
    msg.textContent = '';
  }}
}}
function toggleComplete(){{
  const done = getDone();
  const wasDone = done.has(MODULE_ID);
  if (wasDone) done.delete(MODULE_ID); else done.add(MODULE_ID);
  saveDone(done);
  updateBtn();
  toast(wasDone ? '已取消完成标记' : '🎉 本节已标记完成！');
}}
updateBtn();
</script>
</body>
</html>
'''


def main():
    for i, mod in enumerate(MODULES):
        md_path = DOCS / mod["file"]
        if not md_path.exists():
            print(f"SKIP (missing): {mod['file']}")
            continue
        prev_mod = MODULES[i - 1] if i > 0 else None
        next_mod = MODULES[i + 1] if i < len(MODULES) - 1 else None
        html = build_page(md_path, mod, prev_mod, next_mod)
        out = LESSONS / html_filename(mod["file"])
        out.write_text(html, encoding="utf-8")
        print(f"WROTE {out.relative_to(ROOT)}")
    print("DONE")


if __name__ == "__main__":
    main()
