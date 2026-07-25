#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成仓库分享素材：二维码（SVG/PNG）+ 社交分享图（SVG/PNG）。
可复现：改 REPO_URL 后重跑即可。

依赖（已装于隔离 venv）：qrcode[pil]、Pillow
字体：Windows 自带微软雅黑 C:/Windows/Fonts/msyh.ttc
"""
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

REPO_URL = "https://github.com/WonderfulClaire/finance-learning-roadmap"
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
FONT = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑（含中文）


def build_qr():
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(REPO_URL)
    qr.make(fit=True)
    return qr


def qr_matrix(qr):
    return qr.get_matrix()  # list[list[bool]], 不含 quiet zone


def write_qr_svg(path, matrix):
    n = len(matrix)
    border = 4
    size_mod = n + 2 * border
    M = 10
    W = size_mod * M
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" '
        f'viewBox="0 0 {W} {W}" shape-rendering="crispEdges">',
        f'<rect width="{W}" height="{W}" fill="#ffffff"/>',
    ]
    for r in range(n):
        for c in range(n):
            if matrix[r][c]:
                x = (c + border) * M
                y = (r + border) * M
                parts.append(f'<rect x="{x}" y="{y}" width="{M}" height="{M}" fill="#0f172a"/>')
    parts.append("</svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


def write_share_svg(path, matrix):
    W, H = 1200, 630
    n = len(matrix)
    border = 4
    qr_mod = n + 2 * border
    M = 6  # 二维码模块像素
    qr_size = qr_mod * M  # 约 330
    qr_x = 1200 - 60 - qr_size
    qr_y = (H - qr_size) // 2 + 10

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Microsoft YaHei, sans-serif">')
    # 背景渐变
    s.append('''<defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#0f2027"/>
        <stop offset="55%" stop-color="#203a43"/>
        <stop offset="100%" stop-color="#2c5364"/>
      </linearGradient>
    </defs>''')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    # 左侧装饰条
    s.append(f'<rect x="0" y="0" width="10" height="{H}" fill="#22c55e"/>')
    # 标题
    s.append(f'<text x="70" y="150" fill="#ffffff" font-size="52" font-weight="700">个人理财系统学习路线</text>')
    s.append(f'<text x="72" y="210" fill="#7dd3fc" font-size="28">从复利到资产配置 · 零基础也能看懂的中文开源教程</text>')
    # 要点
    bullets = [
        "9 节系统课程：启航 → 基础 → 权益 → 策略 → 进阶",
        "5 个零依赖 Python 工具：复利 / 通胀 / 资产配置 / PE 分位 / 基金对比",
        "交互式复利计算器 + 30 天打卡计划 + 真实案例",
    ]
    y = 300
    for b in bullets:
        s.append(f'<circle cx="80" cy="{y-8}" r="6" fill="#22c55e"/>')
        s.append(f'<text x="104" y="{y}" fill="#e2e8f0" font-size="24">{b}</text>')
        y += 52
    # 底部口号
    s.append(f'<text x="72" y="560" fill="#facc15" font-size="26" font-weight="700">★ Star 让更多人少踩坑</text>')
    # 右侧二维码白卡
    card_x = qr_x - 24
    card_y = qr_y - 24
    s.append(f'<rect x="{card_x}" y="{card_y}" width="{qr_size+48}" height="{qr_size+90}" rx="18" fill="#ffffff"/>')
    s.append(f'<rect x="{card_x}" y="{card_y}" width="{qr_size+48}" height="6" rx="3" fill="#22c55e"/>')
    # 二维码模块
    s.append('<g shape-rendering="crispEdges">')
    for r in range(n):
        for c in range(n):
            if matrix[r][c]:
                x = qr_x + c * M
                y = qr_y + r * M
                s.append(f'<rect x="{x}" y="{y}" width="{M}" height="{M}" fill="#0f172a"/>')
    s.append('</g>')
    # 二维码下方 URL
    s.append(f'<text x="{card_x + (qr_size+48)/2}" y="{qr_y+qr_size+40}" fill="#0f172a" font-size="17" text-anchor="middle" font-family="Consolas, monospace">github.com/WonderfulClaire</text>')
    s.append(f'<text x="{card_x + (qr_size+48)/2}" y="{qr_y+qr_size+64}" fill="#334155" font-size="17" text-anchor="middle" font-family="Consolas, monospace">/finance-learning-roadmap</text>')
    s.append('</svg>')
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(s))


def vgradient(w, h, c1, c2):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / h
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


def write_share_png(path, qr_img):
    W, H = 1200, 630
    img = vgradient(W, H, (15, 32, 39), (44, 83, 100))
    d = ImageDraw.Draw(img)
    # 装饰条
    d.rectangle([0, 0, 10, H], fill=(34, 197, 94))
    font_big = ImageFont.truetype(FONT, 52)
    font_mid = ImageFont.truetype(FONT, 28)
    font_sm = ImageFont.truetype(FONT, 24)
    font_url = ImageFont.truetype(FONT, 18)
    # 标题
    d.text((70, 110), "个人理财系统学习路线", font=font_big, fill=(255, 255, 255))
    d.text((72, 178), "从复利到资产配置 · 零基础也能看懂的中文开源教程", font=font_mid, fill=(125, 211, 252))
    bullets = [
        "9 节系统课程：启航 → 基础 → 权益 → 策略 → 进阶",
        "5 个零依赖 Python 工具：复利 / 通胀 / 资产配置 / PE / 基金对比",
        "交互式计算器 + 30 天打卡 + 真实案例",
    ]
    y = 288
    for b in bullets:
        d.ellipse([74, y - 10, 86, y + 2], fill=(34, 197, 94))
        d.text((104, y - 16), b, font=font_sm, fill=(226, 232, 240))
        y += 52
    d.text((72, 540), "★ Star 让更多人少踩坑", font=font_mid, fill=(250, 204, 21))
    # 右侧二维码白卡
    qr_size = 300
    qr_resized = qr_img.resize((qr_size, qr_size))
    card_x, card_y = 810, 150
    d.rounded_rectangle([card_x - 24, card_y - 24, card_x + qr_size + 24, card_y + qr_size + 86],
                        radius=18, fill=(255, 255, 255))
    d.rectangle([card_x - 24, card_y - 24, card_x + qr_size + 24, card_y - 18], fill=(34, 197, 94))
    img.paste(qr_resized, (card_x, card_y))
    d.text((card_x + qr_size // 2, card_y + qr_size + 22), "github.com/WonderfulClaire",
           font=font_url, fill=(15, 23, 42), anchor="mm")
    d.text((card_x + qr_size // 2, card_y + qr_size + 50), "/finance-learning-roadmap",
           font=font_url, fill=(51, 65, 85), anchor="mm")
    img.save(path, "PNG")


def main():
    os.makedirs(ASSETS, exist_ok=True)
    qr = build_qr()
    matrix = qr_matrix(qr)
    write_qr_svg(os.path.join(ASSETS, "qrcode.svg"), matrix)
    write_share_svg(os.path.join(ASSETS, "share-card.svg"), matrix)
    # PNG
    qr_img = qr.make_image(fill_color="#0f172a", back_color="#ffffff").convert("RGB")
    write_share_png(os.path.join(ASSETS, "share-card.png"), qr_img)
    print("OK: qrcode.svg / share-card.svg / share-card.png 已生成于", ASSETS)


if __name__ == "__main__":
    main()
