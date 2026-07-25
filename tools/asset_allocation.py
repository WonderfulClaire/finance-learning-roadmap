#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资产配置建议器（零依赖）

根据风险问卷（年龄 + 风险承受等级）给出股/债/现金目标配比。
采用「权益 ≈ 100 − 年龄」的入门法则，再按风险偏好微调。

用法：
  python asset_allocation.py --age 28 --risk 中   # 风险: 低/中/高
  python asset_allocation.py --age 28 --risk 高 --amount 100000
"""
import argparse

RISK_SHIFT = {"低": -15, "中": 0, "高": 15}


def suggest(age: int, risk: str) -> dict:
    equity = 100 - age + RISK_SHIFT.get(risk, 0)
    equity = max(10, min(90, equity))          # 夹在 10%~90%
    bond = max(5, 90 - equity)                 # 剩余大部分给债券
    cash = 100 - equity - bond
    if cash < 0:
        cash = 0
        bond = 100 - equity
    return {"equity": equity, "bond": bond, "cash": cash}


def main():
    p = argparse.ArgumentParser(description="资产配置建议器")
    p.add_argument("--age", type=int, required=True, help="你的年龄")
    p.add_argument("--risk", choices=["低", "中", "高"], default="中", help="风险承受：低/中/高")
    p.add_argument("--amount", type=float, default=0.0, help="可投资总资产（可选，用于金额拆分）")
    args = p.parse_args()

    s = suggest(args.age, args.risk)
    print("=" * 48)
    print(f"年龄 {args.age}、风险偏好「{args.risk}」的建议配比：")
    print(f"  权益(股/指数) : {s['equity']}%")
    print(f"  固收(债/存款) : {s['bond']}%")
    print(f"  现金(货基)   : {s['cash']}%")
    if args.amount > 0:
        print("-" * 48)
        print(f"  按总资产 {args.amount:,.0f} 拆分：")
        print(f"    权益 : {args.amount*s['equity']/100:,.0f}")
        print(f"    固收 : {args.amount*s['bond']/100:,.0f}")
        print(f"    现金 : {args.amount*s['cash']/100:,.0f}")
    print("=" * 48)
    print("注：仅为教学框架，非投资建议；实际还要看资金期限。")


if __name__ == "__main__":
    main()
