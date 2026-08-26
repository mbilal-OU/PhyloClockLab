#!/usr/bin/env python3

import sys
from Bio import SeqIO

alignment = sys.argv[1]

records = list(SeqIO.parse(alignment, "fasta"))

if not records:
    raise SystemExit("ERROR: alignment contains no sequences")

seqs = [str(r.seq) for r in records]

lengths = {len(s) for s in seqs}

if len(lengths) != 1:
    raise SystemExit("ERROR: sequences do not have equal aligned lengths")

n_taxa = len(seqs)
alignment_length = len(seqs[0])

occupancy = []

for column in range(alignment_length):
    present = sum(seq[column] != "-" for seq in seqs)
    occupancy.append(present)

print(f"Taxa: {n_taxa}")
print(f"Alignment columns: {alignment_length}")
print()

thresholds = [
    n_taxa,
    max(n_taxa - 1, 1),
    max(n_taxa - 2, 1),
    max(int(n_taxa * 0.8), 1),
    max(int(n_taxa * 0.5), 1),
]

for threshold in dict.fromkeys(thresholds):
    count = sum(value >= threshold for value in occupancy)

    print(
        f"Columns with >= {threshold}/{n_taxa} taxa present: "
        f"{count} ({100 * count / alignment_length:.2f}%)"
    )

print()
print(
    "sample\talignment_length\tresidues\tgaps\tgap_percent\t"
    "first_residue_column\tlast_residue_column\tspan"
)

for rec in records:

    seq = str(rec.seq)
    sample = rec.id.split("|")[0]

    gaps = seq.count("-")
    residues = len(seq) - gaps

    occupied = [
        i for i, residue in enumerate(seq)
        if residue != "-"
    ]

    if occupied:
        first = occupied[0] + 1
        last = occupied[-1] + 1
        span = last - first + 1
    else:
        first = "NA"
        last = "NA"
        span = "NA"

    print(
        f"{sample}\t{len(seq)}\t{residues}\t{gaps}\t"
        f"{100 * gaps / len(seq):.2f}\t"
        f"{first}\t{last}\t{span}"
    )
