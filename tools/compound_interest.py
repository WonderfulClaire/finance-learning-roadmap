#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复利 & 定投计算器（零依赖，标准库即可）

功能：
  - 一次性投入的复利终值
  - 每月定投的复利终值（年金）
  - 给出 72 法则翻倍年限参考

用法示例：
  python compound_interest.py --principal 100000 --years 30 --rate 0.08
  python compound_interest.py --monthly 1000 --years 20 --rate 0.08
  python compound_interest.py --principal 100000 --monthly 1000 --years 20 --rate 0.08
"""
import argparse


def future_value_lump(principal: float, rate: float, years: int) -> float:
    """一次性投入复利终值：P * (1+r)^n"""
    return principal * ((1 + rate) ** years)


def future_value_dca(monthly: float, rate: float, years: int) -> float:
    """每月月初定投终值（普通年金，按月复利）：
    PMT * [((1+i)^N - 1) / i]，i=月利率, N=月数
    """
    months = years * 12
    i = rate / 12.0
    if i == 0:
        return monthly * months
    return monthly * ((1 + i) ** months - 1) / i


def rule_of_72(rate: float) -> float:
    return 72.0 / (rate * 100) if rate > 0 else float("inf")


def main():
    p = argparse.ArgumentParser(description="复利 & 定投计算器")
    p.add_argument("--principal", type=float, default=0.0, help="一次性投入本金")
    p.add_argument("--monthly", type=float, default=0.0, help="每月定投金额")
    p.add_argument("--years", type=int, required=True, help="投资年限")
    p.add_argument("--rate", type=float, required=True, help="年化收益率，如 0.08 表示 8%")
    args = p.parse_args()

    if args.principal < 0 or args.monthly < 0 or args.rate < 0:
        print("参数不能为负")
        return

    fv_lump = future_value_lump(args.principal, args.rate, args.years) if args.principal else 0.0
    fv_dca = future_value_dca(args.monthly, args.rate, args.years) if args.monthly else 0.0
    total_invest = args.principal + args.monthly * args.years * 12
    total_fv = fv_lump + fv_dca
    gain = total_fv - total_invest

    print("=" * 48)
    print(f"投资年限 : {args.years} 年")
    print(f"年化收益 : {args.rate*100:.2f}%")
    if args.principal:
        print(f"一次性投入: {args.principal:,.0f}  →  终值 {fv_lump:,.0f}")
    if args.monthly:
        print(f"每月定投 : {args.monthly:,.0f}  →  终值 {fv_dca:,.0f}")
    print("-" * 48)
    print(f"累计投入 : {total_invest:,.0f}")
    print(f"预计终值 : {total_fv:,.0f}")
    print(f"复利收益 : {gain:,.0f}  (收益倍数 {total_fv/total_invest:.2f}x)")
    print(f"72法则  : 约 {rule_of_72(args.rate):.1f} 年本金翻倍")
    print("=" * 48)
    print("注：结果为数学推算，非收益承诺；实际有波动与费用。")


if __name__ == "__main__":
    main()
