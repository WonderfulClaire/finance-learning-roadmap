#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通胀侵蚀计算器（零依赖）

算：今天的一笔钱，在 N 年通胀后购买力剩多少；
以及：要维持购买力，目标名义收益需多少。

用法：
  python inflation_impact.py --amount 100000 --years 30 --inflation 0.03
"""
import argparse


def real_value(amount: float, inflation: float, years: int) -> float:
    return amount / ((1 + inflation) ** years)


def main():
    p = argparse.ArgumentParser(description="通胀侵蚀计算器")
    p.add_argument("--amount", type=float, required=True, help="今天的金额")
    p.add_argument("--years", type=int, required=True, help="年数")
    p.add_argument("--inflation", type=float, default=0.03, help="年化通胀率，默认 3%")
    args = p.parse_args()

    rv = real_value(args.amount, args.inflation, args.years)
    loss_ratio = 1 - rv / args.amount
    # 维持购买力所需名义年化
    need_rate = (1 + args.inflation) - 1  # 简化：至少跑赢通胀

    print("=" * 48)
    print(f"今天金额   : {args.amount:,.0f}")
    print(f"通胀假设   : {args.inflation*100:.1f}% / 年，共 {args.years} 年")
    print("-" * 48)
    print(f"{args.years}年后购买力 : {rv:,.0f}")
    print(f"购买力缩水   : {loss_ratio*100:.1f}%")
    print(f"要保值至少需 : 年化 > {need_rate*100:.1f}%")
    print("=" * 48)
    print("注：通胀率仅为假设，真实值每年不同。")


if __name__ == "__main__":
    main()
