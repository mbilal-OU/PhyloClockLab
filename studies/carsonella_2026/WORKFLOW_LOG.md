# Carsonella 2026 Workflow Log

This file records important development-stage analyses and decisions.
Exploratory commands are converted into reusable scripts before the final workflow is automated.

## Stage B — Data provenance

- Built a 20-taxon manifest: 18 Carsonella + 2 outgroups.
- Validated all accessions against NCBI.
- Downloaded FASTA and GenBank records.
- Verified FASTA and GenBank sequence identity.
- Recorded exact accession versions.
- Generated SHA256 checksums for 40 raw files.
- Recorded NCBI retrieval date.
- Raw downloaded sequence files are excluded from Git.

## Stage C — Phylogenomic reconstruction

### CDS/protein extraction

Script:
studies/carsonella_2026/scripts/extract_cds_proteins.py

Protein-producing CDSs were extracted from all 20 GenBank records.

Total translated proteins entering orthology analysis:
3988

### Orthology inference

Software:
OrthoFinder 3.1.5

Command:
orthofinder -f studies/carsonella_2026/data/derived/proteins -t 8

Results:
- Species: 20
- Genes: 3988
- Genes assigned to orthogroups: 3874 (97.1%)
- Orthogroups: 251
- Orthogroups containing all 20 species: 80
- Single-copy orthogroups: 60

Important reproducibility note:
OrthoFinder 3.1.5 is used for our reconstruction.
The publication reports OrthoFinder 2.5.4 for its seven-genome comparative analysis, but does not explicitly report how the 20-taxon concatenated nucleotide phylogenetic alignment was constructed.

### Manual QC locus — OG0000032

Functional interpretation:
Valyl-tRNA synthetase / class I tRNA ligase family protein.

Members:
20 sequences, one per taxon.

Unaligned protein lengths:
- Carsonella: approximately 604–638 aa
- Nardonella: 828 aa
- Portiera: 884 aa

Protein alignment:
MAFFT 7.526 --auto

MAFFT selected:
L-INS-i

Aligned length:
939 amino-acid columns

Occupancy:
- 20/20 taxa: 544 columns (57.93%)
- >=19/20 taxa: 595 columns (63.37%)
- >=18/20 taxa: 604 columns (64.32%)
- >=16/20 taxa: 616 columns (65.60%)
- >=10/20 taxa: 626 columns (66.67%)

Interpretation:
Most Carsonella sequences span almost the entire alignment coordinate range but contain many internal gaps. OG0000032 therefore requires additional QC before inclusion in a concatenated phylogenomic dataset.

## Automation principle

Development follows:

EXPLORE -> UNDERSTAND -> SCRIPT -> VALIDATE -> AUTOMATE

Scientifically meaningful analyses should not remain only in shell history.

### 60 single-copy orthogroup alignment/QC checkpoint

Status: RECONSTRUCTED analysis; this locus-selection procedure is not explicitly reported in the publication.

OrthoFinder identified 60 single-copy orthogroups across all 20 taxa.

All 60 protein orthogroups were aligned with MAFFT --auto and evaluated for:
- protein-length variation
- alignment length
- complete-column occupancy
- >=95%, >=90%, and >=80% taxon occupancy
- mean gap burden
- maximum per-taxon gap burden

Overall QC distribution:
- orthogroups: 60
- median max/min protein-length ratio: 1.20
- median complete-column occupancy: 79.53%
- mean complete-column occupancy: 73.67%
- median >=90%-taxon occupancy: 87.11%
- median mean-gap percentage: 11.45%
- median maximum gap percentage: 19.12%

Clean examples include:
OG0000077, OG0000058, OG0000081, OG0000069 and OG0000089.

Strong outliers include:
OG0000056, OG0000044 and OG0000049.

Important interpretation:
Low 100%-taxon occupancy does not necessarily indicate a globally poor alignment.
For example, OG0000056 and OG0000044 retain >90% occupancy across >=18/20 taxa,
suggesting one or a few strongly truncated/outlier sequences.

Potentially globally problematic loci such as OG0000049 show low occupancy even
after allowing missing sequence in multiple taxa.

Reproducibility issue identified:
The initial manual OG0000032 MAFFT alignment was 939 aa long, whereas the automated
MAFFT --thread 8 analysis produced a 949-aa alignment. MAFFT threading behavior must
therefore be tested before the 60-locus QC dataset is treated as canonical.

### MAFFT reproducibility test

A reproducibility test was performed on OG0000032 using MAFFT 7.526.

Results:

- --thread 1 replicate A: 938 aa
- --thread 1 replicate B: 938 aa
- single-thread SHA256 hashes were identical

- --thread 8 replicate A: 938 aa
- --thread 8 replicate B: 947 aa
- multithread SHA256 hashes differed

All runs selected L-INS-i.

Interpretation:
Multithreaded iterative refinement produced non-identical alignments across
independent runs. The initial 60-locus QC dataset generated with --thread 8
is therefore considered DEVELOPMENTAL rather than canonical.

MAFFT documentation states that iterative refinement may return different
results when multiple threads are used and recommends --threadit 0 for
run-to-run reproducibility.

Canonical MAFFT parameters will be fixed only after testing --threadit 0.

### MAFFT reproducibility issue resolved

Canonical protein-alignment configuration:

mafft --auto --thread 8 --threadit 0

Evidence from OG0000032:

- deterministic replicate A: 939 aa
- deterministic replicate B: 939 aa
- both deterministic SHA256 hashes were identical
- deterministic alignment SHA256:
  5adfda9507e588d65c9e1af300232698d2d88805bbc9678824ab3f0e30eeb4b8

The deterministic alignment was also byte-for-byte identical to the original
manual OG0000032 alignment.

By contrast:

- explicit --thread 1 was reproducible but generated a different 938-aa alignment
- --thread 8 without --threadit 0 produced different results between runs

Decision:
All canonical single-copy protein alignments for this reconstruction will use
--auto --thread 8 --threadit 0.

The previous 60-locus --thread 8 QC run is retained as DEVELOPMENTAL output
and will not be used for the canonical phylogenomic dataset.

### Development issue — canonical MAFFT script argument order

The first attempt to rerun the 60 canonical alignments failed at OG0000032.

Cause:
The script-editing command inserted `--threadit 0` between the `--thread`
option and its numeric argument, producing the invalid command structure:

mafft --auto --thread --threadit 0 8 INPUT

Resolution:
The saved script was corrected to:

mafft --auto --thread 8 --threadit 0 INPUT

This was a workflow-development error and did not alter any biological input data.
The failed canonical alignment attempt was not used for downstream analysis.

### Canonical 60-locus protein alignment completed

All 60 single-copy orthogroups were regenerated using the locked deterministic MAFFT configuration:

mafft --auto --thread 8 --threadit 0

Canonical orthogroups aligned:
60

Validation:
The scripted canonical OG0000032 alignment was compared with the original manually validated alignment.

Both files had identical SHA256:

5adfda9507e588d65c9e1af300232698d2d88805bbc9678824ab3f0e30eeb4b8

Interpretation:
The saved alignment workflow reproduces the manually validated teaching locus exactly.

The canonical 60-locus dataset supersedes the previous developmental multithreaded MAFFT dataset for downstream phylogenomic reconstruction.

### Problematic orthogroup neighborhood inspection

OG0000056:
- CaNd member QTJ62935.1 is 58 aa and hypothetical.
- Other 19 members are approximately 445–474 aa and mostly GatA/amidase-family proteins.
- QTJ62935.1 lies immediately upstream of and overlaps the CaNd TilS CDS.
- Working classification: likely fragmentary/spurious orthogroup member or annotation artifact.
- Targeted homology search required before excluding the locus.

OG0000044:
- Sample E member YDA14889.1 is 91 aa and hypothetical.
- Remaining members are approximately 605–675 aa transketolase-like proteins.
- Immediate neighboring CDSs do not reveal an obvious second transketolase fragment.
- Working classification: possible severe truncation, annotation failure, or missing homolog.
- Targeted homology search required.

OG0000049:
- Most Carsonella members are approximately 156–175 aa.
- Outgroup TilS proteins are substantially longer: CaNd 477 aa and CaPal 417 aa.
- Carsonella members occur in a conserved-looking genomic neighborhood downstream of dnaE.
- Working classification: probable lineage-structured reductive remodeling of TilS rather than a single isolated bad sequence.
- Sample D is unusually short at 94 aa and requires additional scrutiny.

No locus has yet been accepted or rejected from the phylogenomic dataset.

### Targeted protein homology searches — initial DIAMOND screen

DIAMOND 2.2.5 protein searches were performed to investigate three
problematic single-copy orthogroups.

OG0000056:
A normal GatA/amidase-family member was searched against the complete
translated CaNd proteome.
Result: 0 reported pairwise alignments.

Interpretation:
No alternative recognizable full-length GatA homolog was detected in the
current translated CaNd annotation under the initial DIAMOND settings.
The 58-aa CaNd member remains suspicious as a fragmentary or erroneous
orthogroup assignment.

OG0000044:
A normal transketolase member from sample A was searched against the
complete translated E proteome.
Result: 0 reported pairwise alignments.

Interpretation:
No alternative recognizable full-length transketolase homolog was detected
in the current translated E annotation under the initial DIAMOND settings.
The 91-aa E member remains suspicious.

OG0000049:
The 477-aa CaNd TilS protein was searched against the complete A and D
translated proteomes.
Result: 0 reported pairwise alignments.

Interpretation:
Direct protein similarity between full-length CaNd TilS and the short A/D
OG0000049 members was not detected under the initial DIAMOND settings.
Therefore the previous hypothesis of lineage-wide TilS reduction is not yet
considered established. Orthology remains unresolved.

Important:
Absence of a DIAMOND protein hit is not equivalent to biological gene absence.
More-sensitive protein searches and, if necessary, translated nucleotide
searches are required.

### Sensitive DIAMOND interpretation of problematic orthogroups

Very-sensitive DIAMOND searches were repeated with permissive E-value reporting.
Because this produces numerous weak background similarities, individual matches
were interpreted using target identity, query coverage, subject identity and
whether the expected orthogroup member itself was recovered.

OG0000044:
The 635-aa sample-A transketolase query recovered the exact E orthogroup member
YDA14889.1 (91 aa):
- identity = 36.3%
- alignment length = 113 aa
- E-value = 3.85e-05
- query length = 635 aa
- subject length = 91 aa

Interpretation:
YDA14889.1 has detectable transketolase homology but represents only a small
fraction of the full-length protein. This supports classification as a
severely truncated/fragmentary homolog rather than a normal complete
transketolase.

OG0000056:
The 451-aa GatA query did not recover the 58-aa CaNd orthogroup member
QTJ62935.1. Other CaNd hits were weak partial similarities and did not reveal
an obvious full-length GatA homolog.

Interpretation:
Protein-level evidence for a CaNd GatA orthologue remains absent.
The QTJ62935.1 assignment remains suspicious and requires genome-level search.

OG0000049:
The 477-aa CaNd TilS query returned several weak partial similarities in
A and D, but the actual OG0000049 members A/YDA14095.1 and D/YDA14693.1
were not recovered.

Interpretation:
The current search does not independently support TilS orthology for the
short Carsonella OG0000049 members. The earlier hypothesis of lineage-wide
TilS reduction is therefore not established.

Current working classifications:
OG0000044 = fragmentary homolog supported
OG0000056 = orthology/annotation problem unresolved
OG0000049 = orthology unresolved; potentially unsuitable for phylogenetic use

No locus has yet been removed from the reconstructed dataset.

### OG0000056 genome-level GatA search

The 451-aa sample-A GatA protein was searched against the complete CaNd
CP069383.1 nucleotide genome using TBLASTN.

The strongest reported match:
- identity: 34.8%
- aligned length: 66 aa
- E-value: 0.94
- bit score: 25.0

All remaining matches were similarly weak or weaker.

Interpretation:
No convincing genomic GatA homolog was detected in CaNd. Therefore the absence
of a recognizable full-length GatA in the translated annotation is not readily
explained by a simple missed protein annotation.

Combined protein-level and genome-level evidence increases concern that the
58-aa CaNd member assigned to OG0000056 is not a reliable GatA orthologue.

Status:
OG0000056 remains under review and has not yet been removed from the
phylogenomic dataset.

### First formal locus decisions after protein- and genome-level validation

OG0000056 — EXCLUDE from primary phylogenomic matrix

Evidence:
- CaNd member QTJ62935.1 is only 58 aa.
- Other orthogroup members are approximately 445–474 aa GatA/amidase proteins.
- Protein-level GatA search did not recover QTJ62935.1 or a convincing alternative CaNd GatA.
- TBLASTN against the complete CaNd genome found no convincing GatA locus.
- Best genomic match: 66 aa, E=0.94, bitscore=25.0.

Decision:
The CaNd member is not sufficiently supported as a homologous GatA sequence.
OG0000056 will therefore not be used in the primary strict 20-taxon
phylogenomic reconstruction.

OG0000049 — EXCLUDE from primary phylogenomic matrix

Evidence:
- Carsonella members and outgroup TilS proteins show extreme length disparity.
- Full-length CaNd TilS did not recover the A or D OG0000049 proteins by
  protein-level search.
- TBLASTN against complete A and D genomes did not find convincing genomic
  TilS homology at the candidate OG0000049 loci.
- A D-genome match close to the candidate region covered only 20 aa with
  E=7.2 and is not considered meaningful evidence.

Decision:
Orthology across all 20 taxa is insufficiently supported.
OG0000049 will not be used in the primary strict phylogenomic reconstruction.

OG0000044 — PENDING FINAL RECIPROCAL CHECK

Evidence:
- E member YDA14889.1 is only 91 aa versus approximately 605–675 aa in most
  other taxa.
- Sensitive protein search detected transketolase similarity in the exact
  E fragment.
- Genome-level search did not reveal a convincing hidden full-length
  transketolase around the annotated E locus.

Working interpretation:
YDA14889.1 is probably a genuine but severely truncated transketolase homolog.
A reciprocal orthogroup-specific similarity test will be performed before
deciding whether the locus can remain with partial data.

### Stage C locus sets frozen for nucleotide reconstruction

Two reconstructed phylogenomic locus sets were defined.

PRIMARY CONSERVATIVE:
57 loci.
Excluded:
- OG0000056: unsupported CaNd GatA orthology
- OG0000049: unsupported 20-taxon orthology / TilS assignment
- OG0000044: genuine but severely truncated E transketolase fragment

SENSITIVITY:
58 loci.
Excluded:
- OG0000056
- OG0000049

OG0000044 is retained only in the sensitivity dataset because reciprocal
similarity searches support homology of the 91-aa E fragment to the
C-terminal region of transketolase proteins, but the sequence is severely
incomplete.

These locus sets are RECONSTRUCTED because the publication does not report
the exact loci used to construct its 20-taxon concatenated nucleotide
alignment.

### Codon-aware nucleotide reconstruction completed

Canonical protein alignments were back-translated using the original CDS
sequences.

Validation results:
- CDS sequences available: 3,988
- protein alignments processed: 60
- sequence records validated: 1,200
- codon-aware nucleotide alignments created: 60

For every sequence:
- CDS length was checked for codon compatibility
- protein/CDS residue counts were required to match
- protein alignment gaps were converted to nucleotide triplet gaps
- nucleotide alignment length was required to equal 3 × protein alignment length

Manual validation locus OG0000032:
- protein alignment = 939 aa
- nucleotide alignment = 2,817 nt
- 20 taxa present in both

Result:
All 60 loci passed protein-to-CDS back-translation validation.
