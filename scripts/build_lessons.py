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

# 每章开篇名人名言 / 本章为什么重要
QUOTES = {
    "m00": {
        "text": "Rule No. 1: Never lose money. Rule No. 2: Never forget rule No. 1.",
        "author": "—— Warren Buffett（沃伦·巴菲特）",
        "why": "本章先给你泼一盆冷水：理财不是暴富，而是先守住本金、跑赢通胀。巴菲特的第一条规则，正是本章的底层逻辑。"
    },
    "m01": {
        "text": "Diversification is the only free lunch in finance.",
        "author": "—— Harry Markowitz（哈里·马科维茨，现代投资组合理论之父）",
        "why": "本章绘制“资产地图”：不同资产就像不同食材，单吃一种会营养不良，合理搭配才能免费降低风险。"
    },
    "m02": {
        "text": "The individual investor should act consistently as an investor and not as a speculator.",
        "author": "—— Benjamin Graham（本杰明·格雷厄姆）",
        "why": "现金与固收是账户的“压舱石”。格雷厄姆提醒我们：先当投资者，再谈收益；稳钱管不好，长钱难安心。"
    },
    "m03": {
        "text": "Don't look for the needle in the haystack. Just buy the haystack.",
        "author": "—— John C. Bogle（约翰·博格，指数基金之父）",
        "why": "本章讲指数基金：不必费尽心思选股，买下整个市场，让时间和复利为你工作。"
    },
    "m04": {
        "text": "Invest in what you know.",
        "author": "—— Peter Lynch（彼得·林奇）",
        "why": "主动基金与个股是“认知变现”的重灾区。林奇说：只投你看得懂的生意，不懂的不碰。"
    },
    "m05": {
        "text": "Asset allocation is the overwhelmingly dominant contributor to total return.",
        "author": "—— David F. Swensen（大卫·斯文森，耶鲁捐赠基金首席投资官）",
        "why": "本章进入实战：配多少股票、多少债券、定投多少钱，这些决策决定了你绝大部分长期收益。"
    },
    "m06": {
        "text": "We cannot predict, but we can prepare.",
        "author": "—— Howard Marks（霍华德·马克斯）",
        "why": "估值与择时不是为了猜顶底，而是为了在市场极端时保持清醒。马克斯的话，是本章的核心心法。"
    },
    "m07": {
        "text": "Price is what you pay. Value is what you get.",
        "author": "—— Warren Buffett（沃伦·巴菲特）",
        "why": "财报与量化初探：学会读数字背后的生意，才能判断你付的价格是否物有所值。"
    },
    "m08": {
        "text": "In this world nothing can be said to be certain, except death and taxes.",
        "author": "—— Benjamin Franklin（本杰明·富兰克林）",
        "why": "保险、养老、税务看不见摸不着，却决定你人生下半场是否体面。本章把“不得不面对”的事提前安排好。"
    },
}


# 每章延伸观看视频（B站搜索入口为主，兼顾 YouTube 国际读者；链接稳定不失效）
# 每章顶部点亮勋章（游戏化成就）
BADGES = {
    "m00": {"icon": "🛡️", "name": "防坑守卫", "desc": "识别销售套路，把守住本金放在第一位"},
    "m01": {"icon": "🧭", "name": "资产罗盘", "desc": "建立“钱能去哪”的全景图，不再盲目跟风"},
    "m02": {"icon": "🏦", "name": "现金管家", "desc": "把稳的钱放在对的地方，睡好觉比高收益更重要"},
    "m03": {"icon": "📈", "name": "指数先锋", "desc": "用宽基指数撬动长期复利，不赌个股"},
    "m04": {"icon": "🎯", "name": "选股猎手", "desc": "理性看待主动基金与个股，只投看得懂的生意"},
    "m05": {"icon": "⚖️", "name": "配置大师", "desc": "用股债配比平衡波动与收益，把焦虑变成纪律"},
    "m06": {"icon": "🔭", "name": "估值侦探", "desc": "用数据辅助决策，而不是被情绪牵着走"},
    "m07": {"icon": "📊", "name": "财报量化师", "desc": "把“感觉”变成可验证的数据，看懂生意再出价"},
    "m08": {"icon": "🛡️", "name": "人生护城河", "desc": "用保险和养老提前安排好人生的底线"},
}


VIDEOS = {
    "m00": [
        {"title": "🔍 B站：理财入门与防坑（搜“理财入门 防坑”）", "url": "https://search.bilibili.com/all?keyword=理财入门防坑", "note": "挑播放量高、有系列输出的 UP 主看"},
        {"title": "🎬 YouTube：Investing for Beginners — The Plain Bagel", "url": "https://www.youtube.com/@ThePlainBagel", "note": "英文，讲得清楚不忽悠；需梯子"},
    ],
    "m01": [
        {"title": "🔍 B站：资产配置入门（搜“资产配置 入门”）", "url": "https://search.bilibili.com/all?keyword=资产配置入门", "note": "先看“钱有哪些去处”再动手"},
        {"title": "🎬 YouTube：Asset Allocation Explained — Ben Felix", "url": "https://www.youtube.com/@BenFelixCSI", "note": "英文，数据派；需梯子"},
    ],
    "m02": [
        {"title": "🔍 B站：货币基金与债券入门（搜“货币基金 债券 入门”）", "url": "https://search.bilibili.com/all?keyword=货币基金债券入门", "note": "搞懂“稳钱”为什么稳"},
        {"title": "🎬 YouTube：Bonds Explained — The Plain Bagel", "url": "https://www.youtube.com/@ThePlainBagel", "note": "英文；需梯子"},
    ],
    "m03": [
        {"title": "🔍 B站：指数基金与定投（搜“指数基金 定投 银行螺丝钉”）", "url": "https://search.bilibili.com/all?keyword=指数基金定投银行螺丝钉", "note": "银行螺丝钉是 index 流派代表"},
        {"title": "🎬 YouTube：Index Funds — Ben Felix", "url": "https://www.youtube.com/@BenFelixCSI", "note": "英文；需梯子"},
    ],
    "m04": [
        {"title": "🔍 B站：股票与基本面入门（搜“股票入门 基本面分析”）", "url": "https://search.bilibili.com/all?keyword=股票入门基本面分析", "note": "先懂生意再谈买股"},
        {"title": "🎬 YouTube：Stock Picking — The Plain Bagel", "url": "https://www.youtube.com/@ThePlainBagel", "note": "英文；需梯子"},
    ],
    "m05": [
        {"title": "🔍 B站：定投与资产配置（搜“定投 资产配置”）", "url": "https://search.bilibili.com/all?keyword=定投资产配置", "note": "落地“怎么买、买多少”"},
        {"title": "🎬 YouTube：Passive Investing — Ben Felix", "url": "https://www.youtube.com/@BenFelixCSI", "note": "英文；需梯子"},
    ],
    "m06": [
        {"title": "🔍 B站：市盈率与估值（搜“市盈率 估值 定投”）", "url": "https://search.bilibili.com/all?keyword=市盈率估值定投", "note": "学会看贵还是便宜"},
        {"title": "🎬 YouTube：Valuation — Ben Felix", "url": "https://www.youtube.com/@BenFelixCSI", "note": "英文；需梯子"},
    ],
    "m07": [
        {"title": "🔍 B站：财报三张表入门（搜“财报 三张表 入门”）", "url": "https://search.bilibili.com/all?keyword=财报三张表入门", "note": "读得懂报表才看得懂生意"},
        {"title": "🎬 YouTube：Financial Statements — The Plain Bagel", "url": "https://www.youtube.com/@ThePlainBagel", "note": "英文；需梯子"},
    ],
    "m08": [
        {"title": "🔍 B站：保险与养老规划（搜“保险入门 养老规划”）", "url": "https://search.bilibili.com/all?keyword=保险入门养老规划", "note": "先把“万一”安排好"},
        {"title": "🎬 YouTube：Insurance & Retirement — The Plain Bagel", "url": "https://www.youtube.com/@ThePlainBagel", "note": "英文；需梯子"},
    ],
}


def video_html(module_id: str) -> str:
    items = VIDEOS.get(module_id)
    if not items:
        return ""
    lis = "\n".join(
        f'<li><a href="{v["url"]}" target="_blank" rel="noopener">{v["title"]}</a>'
        f'<span class="vnote">{v.get("note", "")}</span></li>'
        for v in items
    )
    return f'''<section class="card videos" id="videos">
  <h2>📺 延伸观看</h2>
  <p class="note">挑播放量高、UP主有系统输出的看；视频只作辅助，投资决策请以你自己的判断为准。</p>
  <ul class="vlist">{lis}</ul>
</section>'''


def quote_html(module_id: str) -> str:
    q = QUOTES.get(module_id)
    if not q:
        return ""
    return f'''<div class="quote-hero">
  <p class="quote-text">{q['text']}</p>
  <p class="quote-author">{q['author']}</p>
  <p class="quote-why">💡 本章为什么重要：{q['why']}</p>
</div>'''


def badge_html(module_id: str) -> str:
    b = BADGES.get(module_id)
    if not b:
        return ""
    return f'''<div class="badge-hero" id="chapterBadge">
  <div class="badge-icon">{b['icon']}</div>
  <div class="badge-body">
    <div class="badge-title">🏅 本章成就：{b['name']}</div>
    <div class="badge-desc">{b['desc']}</div>
  </div>
  <div class="badge-status">✨ 已点亮</div>
</div>'''


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
    quote = quote_html(module["id"])
    badge = badge_html(module["id"])
    video = video_html(module["id"])
    if next_mod:
        next_href = html_filename(next_mod["file"])
        next_label = "📖 下一章 →"
    else:
        next_href = "../learn.html"
        next_label = "🎉 查看结业证书"

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
body{{margin:0;font-family:-apple-system,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--fg);line-height:1.75;font-size:16px}}
a{{color:var(--brand);text-decoration:none}}
a:hover{{text-decoration:underline}}
header.hero{{background:linear-gradient(135deg,#1f2a44,#32507a);color:#fff;padding:36px 24px 28px}}
header.hero .hwrap{{max-width:1400px;margin:0 auto}}
header.hero h1{{margin:0;font-size:clamp(26px,3vw,38px)}}
header.hero .meta{{margin-top:10px;font-size:14px;color:#cbd5e1}}
nav.top{{max-width:1400px;margin:0 auto;padding:16px 24px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;font-size:14px}}
nav.top a.back{{color:var(--muted)}}
nav.top .stage{{margin-left:auto;color:var(--muted)}}
nav.lesson-nav{{max-width:1400px;margin:0 auto;padding:0 24px 32px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}}
nav.lesson-nav a{{padding:12px 16px;border:1px solid var(--line);border-radius:8px;background:var(--card);font-size:14px;max-width:48%}}
main.wrap{{max-width:1400px;margin:0 auto;padding:0 24px 48px;display:grid;grid-template-columns:minmax(0,1fr);gap:28px}}
@media(min-width:1100px){{
  main.wrap{{grid-template-columns:260px 1fr}}
}}
aside.toc{{display:none}}
@media(min-width:1100px){{
  aside.toc{{display:block;position:sticky;top:24px;align-self:start;font-size:14px}}
  aside.toc ul{{list-style:none;padding:0;margin:0;border-left:2px solid var(--line);padding-left:14px}}
  aside.toc li{{margin:10px 0}}
  aside.toc a{{color:var(--muted)}}
  aside.toc a:hover{{color:var(--brand)}}
}}
article{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:clamp(24px,3vw,44px);box-shadow:var(--shadow);font-size:clamp(16px,1.6vw,18px)}}
article h1{{font-size:clamp(28px,3.2vw,42px);margin-top:0}}
article h2{{font-size:clamp(22px,2.4vw,30px);margin-top:36px;padding-bottom:10px;border-bottom:1px solid var(--line)}}
article h3{{font-size:clamp(18px,2vw,22px);margin-top:28px}}
article p{{margin:.8em 0}}
article blockquote{{margin:1.2em 0;padding:16px 20px;border-left:4px solid var(--brand);background:var(--bg);border-radius:0 10px 10px 0;color:var(--muted)}}
.quote-hero{{margin:0 0 28px 0;padding:clamp(20px,2.5vw,32px);border-radius:14px;background:linear-gradient(135deg,rgba(78,121,167,.10),rgba(242,142,43,.08));border:1px solid var(--line);position:relative;overflow:hidden}}
.quote-hero::before{{content:"“";position:absolute;top:-10px;left:14px;font-size:72px;color:var(--brand);opacity:.18;line-height:1}}
.quote-hero .quote-text{{font-size:clamp(18px,2vw,24px);font-weight:600;line-height:1.6;color:var(--fg);position:relative;z-index:1;margin:0;padding-left:12px}}
.quote-hero .quote-author{{margin-top:14px;font-size:14px;color:var(--muted);font-style:italic;padding-left:12px}}
.quote-hero .quote-why{{margin-top:10px;font-size:13px;color:var(--muted);padding-left:12px;border-top:1px dashed var(--line);padding-top:10px}}
.badge-hero{{display:flex;align-items:center;gap:16px;margin:0 0 28px 0;padding:16px 20px;border-radius:14px;background:linear-gradient(135deg,rgba(59,130,246,.10),rgba(139,92,246,.10));border:1px solid var(--line);box-shadow:0 0 0 1px rgba(255,215,0,.25),0 6px 20px rgba(0,0,0,.08);position:relative;overflow:hidden}}
.badge-hero::after{{content:"";position:absolute;top:0;right:0;width:80px;height:80px;background:radial-gradient(circle at top right,rgba(255,215,0,.18),transparent 60%);pointer-events:none}}
.badge-icon{{font-size:38px;line-height:1;flex-shrink:0}}
.badge-title{{font-size:17px;font-weight:700;color:var(--fg);margin-bottom:4px}}
.badge-desc{{font-size:13px;color:var(--muted);line-height:1.5}}
.badge-status{{margin-left:auto;font-size:12px;font-weight:700;color:var(--gold);background:rgba(255,215,0,.12);padding:6px 12px;border-radius:20px;white-space:nowrap;border:1px solid rgba(255,215,0,.35)}}
@media(max-width:600px){{
  .badge-hero{{flex-wrap:wrap;gap:12px}}
  .badge-status{{margin-left:0}}
}}
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
.complete-bar .next-btn{{padding:12px 20px;border:0;border-radius:8px;background:var(--brand);color:#fff;font-size:15px;font-weight:700;cursor:pointer;display:inline-block;transition:filter .15s,box-shadow .15s;box-shadow:var(--shadow)}}
.complete-bar .next-btn:hover{{filter:brightness(1.08);text-decoration:none}}
.complete-bar .next-btn.done{{background:var(--gold)}}
.complete-bar .msg{{font-size:13px;color:var(--muted)}}
.quiz,.videos{{max-width:900px;margin-left:auto;margin-right:auto}}
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
.videos .vlist{{list-style:none;padding:0;margin:12px 0 0}}
.videos .vlist li{{padding:12px 14px;border:1px solid var(--line);border-radius:10px;margin:10px 0;background:var(--bg)}}
.videos .vlist a{{font-weight:600;font-size:15px}}
.videos .vnote{{display:block;margin-top:4px;font-size:13px;color:var(--muted)}}
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
    {quote}
    {badge}
    {body}
  </article>
</main>
<section class="card" style="max-width:1400px;margin:0 auto 24px;">
  <div class="complete-bar">
    <button id="markBtn" onclick="toggleComplete()">✅ 标记本节为「已完成」</button>
    <a class="next-btn" id="nextBtn" href="{next_href}">{next_label}</a>
    <span class="msg" id="completeMsg"></span>
  </div>
  <p class="note">进度保存在浏览器 localStorage，返回<a href="../learn.html">🎮 里程碑页</a>可查看徽章与证书。学完点「下一章」即可继续。</p>
</section>
{video}
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
  const nextBtn = document.getElementById('nextBtn');
  if (done.has(MODULE_ID)) {{
    btn.textContent = '✓ 本节已完成（点击取消）';
    btn.classList.add('done');
    msg.textContent = '进度已同步到 milestones 页，点「下一章」继续 →';
    if (nextBtn) nextBtn.classList.add('done');
  }} else {{
    btn.textContent = '✅ 标记本节为「已完成」';
    btn.classList.remove('done');
    msg.textContent = '';
    if (nextBtn) nextBtn.classList.remove('done');
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
