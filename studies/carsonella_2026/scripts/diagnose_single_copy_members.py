#!/usr/bin/env python3

import argparse
import csv
from pathlib import Path
from Bio import SeqIO


parser = argparse.ArgumentParser()

parser.add_argument("manifest", type=Path)
parser.add_argument("rawdir", type=Path)
parser.add_argument("single_copy_dir", type=Path)
parser.add_argument("alignment_dir", type=Path)
parser.add_argument("output", type=Path)

args = parser.parse_args()


# --------------------------------------------------
# Build annotation lookup from original GenBank files
# --------------------------------------------------

annotation = {}

with args.manifest.open() as handle:
    reader = csv.DictReader(handle, delimiter="\t")

    for row in reader:

        sample = row["sample_id"]
        accession = row["ncbi_accession_version"]

        gbff = args.rawdir / f"{sample}_{accession}.gbff"

        record = SeqIO.read(gbff, "genbank")

        annotation[sample] = {}

        for feature in record.features:

            if feature.type != "CDS":
                continue

            protein_id = feature.qualifiers.get(
                "protein_id", ["NA"]
            )[0]

            locus_tag = feature.qualifiers.get(
                "locus_tag", ["NA"]
            )[0]

            product = feature.qualifiers.get(
                "product", ["NA"]
            )[0]

            annotation[sample][protein_id] = {
                "locus_tag": locus_tag,
                "product": product,
            }


rows = []


# --------------------------------------------------
# Inspect every single-copy orthogroup
# --------------------------------------------------

for infile in sorted(args.single_copy_dir.glob("*.fa")):

    orthogroup = infile.stem

    aligned_file = (
        args.alignment_dir /
        f"{orthogroup}_protein_aligned.faa"
    )

    original = {
        rec.id: rec
        for rec in SeqIO.parse(infile, "fasta")
    }

    aligned = {
        rec.id: rec
        for rec in SeqIO.parse(aligned_file, "fasta")
    }

    for seq_id, rec in original.items():

        sample, protein_id, locus_tag = seq_id.split("|")

        aligned_seq = str(aligned[seq_id].seq)

        alignment_length = len(aligned_seq)
        gap_count = aligned_seq.count("-")

        gap_percent = (
            100 * gap_count / alignment_length
        )

        info = annotation.get(
            sample, {}
        ).get(
            protein_id,
            {
                "locus_tag": locus_tag,
                "product": "NOT_FOUND",
            }
        )

        rows.append({
            "orthogroup": orthogroup,
            "sample": sample,
            "protein_id": protein_id,
            "locus_tag": info["locus_tag"],
            "protein_length_aa": len(rec.seq),
            "alignment_length_aa": alignment_length,
            "gap_count": gap_count,
            "gap_percent": f"{gap_percent:.2f}",
            "product": info["product"],
        })


args.output.parent.mkdir(
    parents=True,
    exist_ok=True
)

with args.output.open("w", newline="") as handle:

    fields = [
        "orthogroup",
        "sample",
        "protein_id",
        "locus_tag",
        "protein_length_aa",
        "alignment_length_aa",
        "gap_count",
        "gap_percent",
        "product",
    ]

    writer = csv.DictWriter(
        handle,
        fieldnames=fields,
        delimiter="\t"
    )

    writer.writeheader()
    writer.writerows(rows)


print(f"Member records: {len(rows)}")
print(f"Orthogroups: {len(set(r['orthogroup'] for r in rows))}")
print(f"Output: {args.output}")
