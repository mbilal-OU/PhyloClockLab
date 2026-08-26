#!/usr/bin/env python3

import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("qc_table")
parser.add_argument("output")
args = parser.parse_args()

df = pd.read_csv(args.qc_table, sep="\t")

metrics = [
    "min_unaligned_aa",
    "max_unaligned_aa",
    "max_min_length_ratio",
    "alignment_length_aa",
    "pct_columns_100pct",
    "pct_columns_ge95pct",
    "pct_columns_ge90pct",
    "pct_columns_ge80pct",
    "mean_gap_percent",
    "max_gap_percent",
]

with open(args.output, "w") as out:

    out.write("Canonical single-copy orthogroup QC summary\n")
    out.write("=" * 42 + "\n")
    out.write(f"Orthogroups: {len(df)}\n\n")

    for col in metrics:

        out.write(
            f"{col}: "
            f"min={df[col].min():.2f}, "
            f"median={df[col].median():.2f}, "
            f"mean={df[col].mean():.2f}, "
            f"max={df[col].max():.2f}\n"
        )

print(f"Created: {args.output}")
