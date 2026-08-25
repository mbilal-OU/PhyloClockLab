#!/usr/bin/env python3

import csv
import sys
from pathlib import Path
from Bio import SeqIO

manifest = Path(sys.argv[1])
rawdir = Path(sys.argv[2])
output = Path(sys.argv[3])

results = []

with manifest.open() as handle:
    reader = csv.DictReader(handle, delimiter="\t")

    for row in reader:
        sample_id = row["sample_id"]
        expected = row["ncbi_accession_version"]

        fasta_file = rawdir / f"{sample_id}_{expected}.fasta"
        gbff_file = rawdir / f"{sample_id}_{expected}.gbff"

        status = "OK"
        notes = []

        if not fasta_file.exists():
            status = "FAIL"
            notes.append("missing FASTA")

        if not gbff_file.exists():
            status = "FAIL"
            notes.append("missing GBFF")

        if status == "OK":
            fasta = SeqIO.read(fasta_file, "fasta")
            gbff = SeqIO.read(gbff_file, "genbank")

            if fasta.id != expected:
                status = "FAIL"
                notes.append(f"FASTA id={fasta.id}")

            if gbff.id != expected:
                status = "FAIL"
                notes.append(f"GBFF id={gbff.id}")

            if len(fasta.seq) != len(gbff.seq):
                status = "FAIL"
                notes.append("length mismatch")

            if str(fasta.seq).upper() != str(gbff.seq).upper():
                status = "FAIL"
                notes.append("sequence mismatch")

            length = len(fasta.seq)

        else:
            length = "NA"

        results.append({
            "sample_id": sample_id,
            "expected_accession": expected,
            "sequence_length_bp": length,
            "status": status,
            "notes": "; ".join(notes) if notes else "",
        })

with output.open("w", newline="") as handle:
    fieldnames = [
        "sample_id",
        "expected_accession",
        "sequence_length_bp",
        "status",
        "notes",
    ]

    writer = csv.DictWriter(
        handle,
        fieldnames=fieldnames,
        delimiter="\t"
    )

    writer.writeheader()
    writer.writerows(results)

print(f"Validated taxa: {len(results)}")

failures = [r for r in results if r["status"] != "OK"]

if failures:
    print(f"FAIL: {len(failures)} taxa failed validation")
    for row in failures:
        print(
            row["sample_id"],
            row["expected_accession"],
            row["notes"],
            sep="\t"
        )
    sys.exit(1)

print("PASS: all FASTA and GenBank records are internally consistent")
