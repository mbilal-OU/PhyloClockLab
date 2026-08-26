#!/usr/bin/env python3

import csv
import sys
from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

manifest = Path(sys.argv[1])
rawdir = Path(sys.argv[2])
outdir = Path(sys.argv[3])

protein_dir = outdir / "proteins"
cds_dir = outdir / "cds"

protein_dir.mkdir(parents=True, exist_ok=True)
cds_dir.mkdir(parents=True, exist_ok=True)

summary_file = outdir / "annotation_inventory.tsv"

summary = []

with manifest.open() as handle:
    reader = csv.DictReader(handle, delimiter="\t")

    for row in reader:

        sample = row["sample_id"]
        accession = row["ncbi_accession_version"]

        gbff = rawdir / f"{sample}_{accession}.gbff"

        record = SeqIO.read(gbff, "genbank")

        protein_records = []
        cds_records = []

        total_cds = 0
        translated_cds = 0
        no_translation = 0

        for feature in record.features:

            if feature.type != "CDS":
                continue

            total_cds += 1

            if "translation" not in feature.qualifiers:
                no_translation += 1
                continue

            translated_cds += 1

            locus_tag = feature.qualifiers.get(
                "locus_tag", ["NA"]
            )[0]

            protein_id = feature.qualifiers.get(
                "protein_id", ["NA"]
            )[0]

            seq_id = f"{sample}|{protein_id}|{locus_tag}"

            protein_seq = Seq(feature.qualifiers["translation"][0])

            cds_seq = feature.extract(record.seq)

            protein_records.append(
                SeqRecord(
                    protein_seq,
                    id=seq_id,
                    description=""
                )
            )

            cds_records.append(
                SeqRecord(
                    cds_seq,
                    id=seq_id,
                    description=""
                )
            )

        SeqIO.write(
            protein_records,
            protein_dir / f"{sample}.faa",
            "fasta"
        )

        SeqIO.write(
            cds_records,
            cds_dir / f"{sample}.fna",
            "fasta"
        )

        summary.append({
            "sample_id": sample,
            "accession": accession,
            "total_CDS_features": total_cds,
            "translated_CDS": translated_cds,
            "CDS_without_translation": no_translation,
        })

with summary_file.open("w", newline="") as handle:

    fields = [
        "sample_id",
        "accession",
        "total_CDS_features",
        "translated_CDS",
        "CDS_without_translation",
    ]

    writer = csv.DictWriter(
        handle,
        fieldnames=fields,
        delimiter="\t"
    )

    writer.writeheader()
    writer.writerows(summary)

print(f"Processed taxa: {len(summary)}")
print(f"Protein FASTA directory: {protein_dir}")
print(f"CDS FASTA directory: {cds_dir}")
print(f"Inventory: {summary_file}")
