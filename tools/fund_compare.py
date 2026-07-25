#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金对比表生成器（零依赖）

把两只基金的费率/收益做成对比表，辅助判断。
数据为手动填入（仓库不内置实时行情，避免过期误导）。

用法：
  python fund_compare.py \
    --name_a "纳指100 QDII A" --fee_a 0.65 --ret1y_a 15.8 --pe_a 34 --pct_a 77 \
    --name_b "中证A500 联接 A" --fee_b 0.20 --ret1y_b 5.0 --pe_b 15.5 --pct_b 45
费用单位：%/年；收益单位：%；PE 为估值；pct 为估值分位(%)。
"""
import argparse


def main():
    p = argparse.ArgumentParser(description="基金对比表生成器")
    for tag in ("a", "b"):
        g = p.add_argument_group(f"基金 {tag.upper()}")
        g.add_argument(f"--name_{tag}", default=f"基金{tag.upper()}")
        g.add_argument(f"--fee_{tag}", type=float, default=0.0, help="年费率 %")
        g.add_argument(f"--ret1y_{tag}", type=float, default=0.0, help="近1年收益 %")
        g.add_argument(f"--pe_{tag}", type=float, default=0.0, help="当前 PE")
        g.add_argument(f"--pct_{tag}", type=float, default=0.0, help="估值分位 %")
    args = p.parse_args()

    cols = ["项目", "A", "B"]
    rows = [
        ("名称", args.name_a, args.name_b),
        ("年费率(%)", f"{args.fee_a}", f"{args.fee_b}"),
        ("近1年收益(%)", f"{args.ret1y_a}", f"{args.ret1y_b}"),
        ("当前PE", f"{args.pe_a}", f"{args.pe_b}"),
        ("估值分位(%)", f"{args.pct_a}", f"{args.pct_b}"),
    ]
    w = 16
    print("=" * (w * 3 + 4))
    print(f"{cols[0]:<{w}}|{cols[1]:<{w}}|{cols[2]:<{w}}")
    print("-" * (w * 3 + 4))
    for r in rows:
        print(f"{str(r[0]):<{w}}|{str(r[1]):<{w}}|{str(r[2]):<{w}}")
    print("=" * (w * 3 + 4))
    print("提示：费用越低、估值分位越低通常越友好；收益会变化，勿当现状。")


if __name__ == "__main__":
    main()
