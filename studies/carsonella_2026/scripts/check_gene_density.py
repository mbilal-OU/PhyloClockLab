#!/usr/bin/env python3

from Bio import SeqIO
import sys

gbff = sys.argv[1]

# Read the GenBank record
record = SeqIO.read(gbff, "genbank")

genome_length = len(record.seq)

# Collect coordinates of all features annotated as "gene"
intervals = []

for feature in record.features:
    if feature.type == "gene":
        start = int(feature.location.start)
        end = int(feature.location.end)
        intervals.append((start, end))

# Sort genes by genomic position
intervals.sort()

# Merge genes that overlap
merged = []

for start, end in intervals:
    if not merged or start > merged[-1][1]:
        merged.append([start, end])
    else:
        merged[-1][1] = max(merged[-1][1], end)

# Count unique genomic bases covered by genes
gene_covered_bp = sum(end - start for start, end in merged)

intergenic_bp = genome_length - gene_covered_bp

coding_density = (gene_covered_bp / genome_length) * 100

print(f"Accession: {record.id}")
print(f"Genome length: {genome_length:,} bp")
print(f"Annotated gene features: {len(intervals)}")
print(f"Merged gene intervals: {len(merged)}")
print(f"Gene-covered bases: {gene_covered_bp:,} bp")
print(f"Intergenic bases: {intergenic_bp:,} bp")
print(f"Gene coverage: {coding_density:.2f}%")
