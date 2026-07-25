#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PE 历史百分位计算器（零依赖）

输入一串历史 PE（逗号分隔或文件），给出当前 PE 在历史中的分位。
分位越低越"便宜"（相对历史）。

用法：
  python pe_percentile.py --current 15 --history 12,13,14,15,18,20,22,16,14,13
  python pe_percentile.py --current 15 --file pes.txt     # 文件每行一个 PE
"""
import argparse


def percentile(current: float, history: list) -> float:
    if not history:
        raise ValueError("历史数据为空")
    below = sum(1 for x in history if x <= current)
    return below / len(history) * 100.0


def main():
    p = argparse.ArgumentParser(description="PE 历史百分位计算器")
    p.add_argument("--current", type=float, required=True, help="当前 PE")
    p.add_argument("--history", type=str, default="", help="历史 PE，逗号分隔")
    p.add_argument("--file", type=str, default="", help="历史 PE 文件，每行一个")
    args = p.parse_args()

    history = []
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            history = [float(x.strip()) for x in f if x.strip()]
    elif args.history:
        history = [float(x.strip()) for x in args.history.split(",") if x.strip()]

    if not history:
        print("请提供 --history 或 --file")
        return

    pct = percentile(args.current, history)
    band = ("低估区(<30%)" if pct < 30
            else "正常区(30%-70%)" if pct < 70
            else "高估区(70%-90%)" if pct < 90
            else "泡沫区(>90%)")
    print("=" * 48)
    print(f"当前 PE      : {args.current}")
    print(f"历史样本数   : {len(history)}")
    print(f"历史区间     : {min(history)} ~ {max(history)}")
    print(f"当前分位     : {pct:.1f}%  →  {band}")
    print("=" * 48)
    print("注：分位只给赔率不给时点；低估值也可能长期更低。")


if __name__ == "__main__":
    main()
