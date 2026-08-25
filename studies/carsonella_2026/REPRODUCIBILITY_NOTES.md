# Study 01 Reproducibility Notes

## CP197248 genome and annotation check

Accession inspected: CP197248.1  
Host: Diaphorina citri  
Symbiont: Candidatus Carsonella ruddii  
BioProject: PRJNA1303861

### Values independently reproduced

- Current sequence length: 174,020 bp
- CDS features: 207
- tRNA features: 27
- rRNA features: 3
- GC content: 17.64%
- AT content: 82.36%

The CDS, tRNA, rRNA and nucleotide-composition values agree with the publication after rounding.

### Sequence-length discrepancy

The publication reports a genome length of 174,018 bp, whereas the current GenBank record CP197248.1 contains 174,020 bp.

### Intergenic/gene-density discrepancy

Applying the gene-feature merging and circular-gap logic described in Supplementary Code S1 to the current CP197248.1 PGAP annotation produced:

- gene features: 237
- merged gene intervals: 64
- intergenic regions: 64
- intergenic length range: 1–244 bp
- total intergenic length: 2,524 bp
- gene-covered length: 171,496 bp
- gene-covered fraction: 98.55%

Table 1 of the publication reports:

- intergenic regions: 96
- intergenic length range: 1–1,036 bp
- total gene coverage: 160,507 bp
- coding density: 92.24%

Therefore, the Table 1 intergenic/gene-density values cannot currently be reproduced from the deposited CP197248.1 PGAP annotation using the calculation logic supplied with the paper.

This observation is recorded as a reproducibility discrepancy, not as evidence of an error in the biological conclusions. Possible causes include differences in annotation snapshots, undocumented feature definitions/preprocessing, or manuscript/table-level differences.

### Annotation metadata inspected

- annotation provider: NCBI
- pipeline: PGAP
- PGAP revision: 6.10
- annotation date: 2025-08-14
- genes total: 237
- CDS total: 207
- coding genes: 206
- pseudogenes: 1
