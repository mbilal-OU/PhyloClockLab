#!/usr/bin/env python3

import argparse
import csv
from pathlib import Path
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument("manifest", type=Path)
parser.add_argument("rawdir", type=Path)
parser.add_argument("sample")
parser.add_argument("protein_id")
parser.add_argument("--flank", type=int, default=3)
args = parser.parse_args()

accession = None

with args.manifest.open() as handle:
    reader = csv.DictReader(handle, delimiter="\t")

    for row in reader:
        if row["sample_id"] == args.sample:
            accession = row["ncbi_accession_version"]
            break

if accession is None:
    raise SystemExit(f"ERROR: sample not found: {args.sample}")

gbff = args.rawdir / f"{args.sample}_{accession}.gbff"
record = SeqIO.read(gbff, "genbank")

cds = []

for feature in record.features:
    if feature.type != "CDS":
        continue

    protein_id = feature.qualifiers.get("protein_id", ["NA"])[0]
    locus_tag = feature.qualifiers.get("locus_tag", ["NA"])[0]
    product = feature.qualifiers.get("product", ["NA"])[0]

    start = int(feature.location.start) + 1
    end = int(feature.location.end)
    strand = feature.location.strand
    nt_length = len(feature.location)

    aa = feature.qualifiers.get("translation", [""])[0]
    aa_length = len(aa) if aa else "NA"

    pseudo = (
        "yes"
        if "pseudo" in feature.qualifiers
        or "pseudogene" in feature.qualifiers
        else "no"
    )

    cds.append({
        "start": start,
        "end": end,
        "strand": strand,
        "protein_id": protein_id,
        "locus_tag": locus_tag,
        "nt_length": nt_length,
        "aa_length": aa_length,
        "pseudo": pseudo,
        "product": product,
    })

cds.sort(key=lambda x: x["start"])

target_index = None

for i, row in enumerate(cds):
    if row["protein_id"] == args.protein_id:
        target_index = i
        break

if target_index is None:
    raise SystemExit(
        f"ERROR: protein {args.protein_id} not found in {args.sample}"
    )

lo = max(0, target_index - args.flank)
hi = min(len(cds), target_index + args.flank + 1)

print(
    "relative\tstart\tend\tstrand\tprotein_id\tlocus_tag\t"
    "nt_length\taa_length\tpseudo\tproduct"
)

for i in range(lo, hi):
    row = cds[i]
    relative = i - target_index

    print(
        f"{relative:+d}\t"
        f"{row['start']}\t"
        f"{row['end']}\t"
        f"{row['strand']}\t"
        f"{row['protein_id']}\t"
        f"{row['locus_tag']}\t"
        f"{row['nt_length']}\t"
        f"{row['aa_length']}\t"
        f"{row['pseudo']}\t"
        f"{row['product']}"
    )
