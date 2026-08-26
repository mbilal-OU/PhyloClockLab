#!/usr/bin/env python3

import argparse
import csv
from pathlib import Path

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


parser = argparse.ArgumentParser()

parser.add_argument("protein_alignment_dir", type=Path)
parser.add_argument("cds_dir", type=Path)
parser.add_argument("output_dir", type=Path)
parser.add_argument("summary", type=Path)

args = parser.parse_args()


args.output_dir.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load all CDS sequences
# --------------------------------------------------

cds_lookup = {}

for f in sorted(args.cds_dir.glob("*.fna")):

    for rec in SeqIO.parse(f, "fasta"):

        if rec.id in cds_lookup:
            raise SystemExit(
                f"ERROR: duplicate CDS identifier: {rec.id}"
            )

        cds_lookup[rec.id] = str(rec.seq).upper()


print(f"CDS sequences loaded: {len(cds_lookup)}")


rows = []


# --------------------------------------------------
# Back-translate every protein alignment
# --------------------------------------------------

alignment_files = sorted(
    args.protein_alignment_dir.glob(
        "*_protein_aligned.faa"
    )
)

print(f"Protein alignments found: {len(alignment_files)}")


for number, protein_file in enumerate(
    alignment_files,
    start=1
):

    og = protein_file.name.replace(
        "_protein_aligned.faa",
        ""
    )

    protein_records = list(
        SeqIO.parse(protein_file, "fasta")
    )

    nucleotide_records = []


    for protein_record in protein_records:

        seq_id = protein_record.id

        if seq_id not in cds_lookup:
            raise SystemExit(
                f"ERROR: CDS not found for {seq_id}"
            )

        protein_alignment = str(
            protein_record.seq
        ).upper()

        ungapped_protein = (
            protein_alignment.replace("-", "")
        )

        cds = cds_lookup[seq_id]

        if len(cds) % 3 != 0:
            raise SystemExit(
                f"ERROR: CDS length not divisible by 3: "
                f"{seq_id} ({len(cds)} nt)"
            )

        codons = [
            cds[i:i+3]
            for i in range(0, len(cds), 3)
        ]

        terminal_stop_removed = False

        # GenBank CDS may contain terminal stop codon
        if (
            len(codons) == len(ungapped_protein) + 1
            and str(
                Seq(codons[-1]).translate(table=11)
            ) == "*"
        ):
            codons = codons[:-1]
            terminal_stop_removed = True


        if len(codons) != len(ungapped_protein):

            raise SystemExit(
                "\n".join([
                    "ERROR: protein/CDS length mismatch",
                    f"Orthogroup: {og}",
                    f"Sequence: {seq_id}",
                    f"Protein residues: {len(ungapped_protein)}",
                    f"CDS codons: {len(codons)}",
                ])
            )


        codon_index = 0
        aligned_nt = []


        for aa in protein_alignment:

            if aa == "-":
                aligned_nt.append("---")

            else:
                aligned_nt.append(
                    codons[codon_index]
                )

                codon_index += 1


        if codon_index != len(codons):

            raise SystemExit(
                f"ERROR: not all codons consumed for "
                f"{seq_id}"
            )


        nucleotide_sequence = "".join(
            aligned_nt
        )


        if len(nucleotide_sequence) != (
            3 * len(protein_alignment)
        ):

            raise SystemExit(
                f"ERROR: nucleotide alignment length "
                f"incorrect for {seq_id}"
            )


        nucleotide_records.append(

            SeqRecord(
                Seq(nucleotide_sequence),
                id=seq_id,
                description=""
            )
        )


        rows.append({
            "orthogroup": og,
            "sequence_id": seq_id,
            "protein_residues": len(
                ungapped_protein
            ),
            "cds_nt_used": len(codons) * 3,
            "protein_alignment_aa": len(
                protein_alignment
            ),
            "nucleotide_alignment_nt": len(
                nucleotide_sequence
            ),
            "terminal_stop_removed":
                terminal_stop_removed,
        })


    output = (
        args.output_dir /
        f"{og}_codon_aligned.fna"
    )


    SeqIO.write(
        nucleotide_records,
        output,
        "fasta"
    )


    print(
        f"[{number:02d}/{len(alignment_files)}] "
        f"{og}"
    )


# --------------------------------------------------
# Write validation summary
# --------------------------------------------------

args.summary.parent.mkdir(
    parents=True,
    exist_ok=True
)

fields = [
    "orthogroup",
    "sequence_id",
    "protein_residues",
    "cds_nt_used",
    "protein_alignment_aa",
    "nucleotide_alignment_nt",
    "terminal_stop_removed",
]


with args.summary.open(
    "w",
    newline=""
) as handle:

    writer = csv.DictWriter(
        handle,
        fieldnames=fields,
        delimiter="\t"
    )

    writer.writeheader()
    writer.writerows(rows)


print()
print(f"Orthogroups processed: {len(alignment_files)}")
print(f"Sequence records validated: {len(rows)}")
print(f"Summary: {args.summary}")
