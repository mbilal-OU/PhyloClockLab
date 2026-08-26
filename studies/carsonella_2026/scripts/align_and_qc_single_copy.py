#!/usr/bin/env python3

import argparse
import csv
import subprocess
from pathlib import Path
from statistics import mean

from Bio import SeqIO


def summarize_alignment(records):
    seqs = [str(r.seq) for r in records]

    if not seqs:
        raise ValueError("No sequences found")

    lengths = {len(s) for s in seqs}

    if len(lengths) != 1:
        raise ValueError("Aligned sequences do not have equal lengths")

    n_taxa = len(seqs)
    aln_len = len(seqs[0])

    occupancy = [
        sum(seq[i] != "-" for seq in seqs)
        for i in range(aln_len)
    ]

    gap_percentages = [
        100 * seq.count("-") / aln_len
        for seq in seqs
    ]

    return {
        "alignment_length_aa": aln_len,
        "columns_100pct": sum(x == n_taxa for x in occupancy),
        "columns_ge95pct": sum(x >= 0.95 * n_taxa for x in occupancy),
        "columns_ge90pct": sum(x >= 0.90 * n_taxa for x in occupancy),
        "columns_ge80pct": sum(x >= 0.80 * n_taxa for x in occupancy),
        "pct_columns_100pct": 100 * sum(x == n_taxa for x in occupancy) / aln_len,
        "pct_columns_ge95pct": 100 * sum(x >= 0.95 * n_taxa for x in occupancy) / aln_len,
        "pct_columns_ge90pct": 100 * sum(x >= 0.90 * n_taxa for x in occupancy) / aln_len,
        "pct_columns_ge80pct": 100 * sum(x >= 0.80 * n_taxa for x in occupancy) / aln_len,
        "mean_gap_percent": mean(gap_percentages),
        "max_gap_percent": max(gap_percentages),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("single_copy_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("summary_tsv", type=Path)
    parser.add_argument("--threads", type=int, default=4)

    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.summary_tsv.parent.mkdir(parents=True, exist_ok=True)

    input_files = sorted(args.single_copy_dir.glob("*.fa"))

    print(f"Single-copy orthogroups found: {len(input_files)}")

    results = []

    for number, infile in enumerate(input_files, start=1):

        orthogroup = infile.stem

        alignment_file = (
            args.output_dir / f"{orthogroup}_protein_aligned.faa"
        )

        log_file = (
            args.output_dir / f"{orthogroup}_mafft.log"
        )

        unaligned_records = list(SeqIO.parse(infile, "fasta"))

        unaligned_lengths = [
            len(record.seq)
            for record in unaligned_records
        ]

        print(
            f"[{number:02d}/{len(input_files)}] "
            f"{orthogroup}"
        )

        with alignment_file.open("w") as aln_out, \
             log_file.open("w") as log_out:

            subprocess.run(
                [
                    "mafft",
                    "--auto",
                    "--thread",
                    str(args.threads),
                    "--threadit",
                    "0",
                    str(infile),
                ],
                stdout=aln_out,
                stderr=log_out,
                check=True,
            )

        aligned_records = list(
            SeqIO.parse(alignment_file, "fasta")
        )

        metrics = summarize_alignment(aligned_records)

        min_len = min(unaligned_lengths)
        max_len = max(unaligned_lengths)

        results.append({
            "orthogroup": orthogroup,
            "n_taxa": len(unaligned_records),
            "min_unaligned_aa": min_len,
            "max_unaligned_aa": max_len,
            "mean_unaligned_aa": f"{mean(unaligned_lengths):.2f}",
            "max_min_length_ratio": f"{max_len / min_len:.3f}",
            "alignment_length_aa": metrics["alignment_length_aa"],
            "columns_100pct": metrics["columns_100pct"],
            "pct_columns_100pct": f"{metrics['pct_columns_100pct']:.2f}",
            "columns_ge95pct": metrics["columns_ge95pct"],
            "pct_columns_ge95pct": f"{metrics['pct_columns_ge95pct']:.2f}",
            "columns_ge90pct": metrics["columns_ge90pct"],
            "pct_columns_ge90pct": f"{metrics['pct_columns_ge90pct']:.2f}",
            "columns_ge80pct": metrics["columns_ge80pct"],
            "pct_columns_ge80pct": f"{metrics['pct_columns_ge80pct']:.2f}",
            "mean_gap_percent": f"{metrics['mean_gap_percent']:.2f}",
            "max_gap_percent": f"{metrics['max_gap_percent']:.2f}",
        })

    fields = list(results[0].keys())

    with args.summary_tsv.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t"
        )

        writer.writeheader()
        writer.writerows(results)

    print()
    print(f"Aligned orthogroups: {len(results)}")
    print(f"Summary: {args.summary_tsv}")


if __name__ == "__main__":
    main()
