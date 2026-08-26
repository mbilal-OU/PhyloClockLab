#!/usr/bin/env python3

import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("developmental")
parser.add_argument("canonical")
parser.add_argument("output")
args = parser.parse_args()

dev = pd.read_csv(args.developmental, sep="\t")
can = pd.read_csv(args.canonical, sep="\t")

metrics = [
    "alignment_length_aa",
    "pct_columns_100pct",
    "pct_columns_ge90pct",
    "mean_gap_percent",
    "max_gap_percent",
]

merged = dev.merge(
    can,
    on="orthogroup",
    suffixes=("_developmental", "_canonical")
)

for metric in metrics:
    merged[f"delta_{metric}"] = (
        merged[f"{metric}_canonical"]
        - merged[f"{metric}_developmental"]
    )

columns = ["orthogroup"]

for metric in metrics:
    columns += [
        f"{metric}_developmental",
        f"{metric}_canonical",
        f"delta_{metric}",
    ]

merged[columns].to_csv(
    args.output,
    sep="\t",
    index=False
)

print(f"Compared orthogroups: {len(merged)}")
print(f"Created: {args.output}")
