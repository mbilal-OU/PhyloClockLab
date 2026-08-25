# Study 01 — Carsonella 2026 Replication Ledger

## 1. Citation

Wu F, Deng K, Lin X, et al. **Time-resolved comparative genomics of ‘Candidatus Carsonella ruddii’ across psyllid lineages reveals a conserved core genome and contrasting secondary symbiont dynamics.** *Microbial Genomics*. 2026;12:001727. DOI: 10.1099/mgen.0.001727.

## 2. Learning objective

This study is our first **LEARN → APPLY → SHIP** project in molecular evolution, phylogenomics and divergence-time estimation.

The goal is not to reproduce figures blindly. We will understand the biological question, reconstruct the published analysis manually, inspect intermediate outputs, diagnose discrepancies, test sensitivity to assumptions, and only then engineer automation around the analysis.

## 3. Biological questions from the paper

The authors ask three connected questions:

1. How structurally and functionally conserved are Carsonella genomes across divergent psyllid hosts?
2. To what extent are Carsonella phylogeny and inferred divergence times congruent with host diversification?
3. How does the long-term stability of the primary Carsonella symbiosis compare with the more labile distribution of secondary symbionts?

For our learning project, the main focus is **Question 2**, while Questions 1 and 3 provide biological context.

## 4. Dataset architecture

### 4.1 Seven newly generated complete Carsonella genomes

All seven were deposited under **BioProject PRJNA1303861**.

| ID | Psyllid host | Family used in paper | Carsonella accession | Genome size (bp) |
|---|---|---|---|---:|
| A | *Diaphorina citri* | Psyllidae | CP197248 | 174,018 |
| B | *Bactericera cockerelli* | Triozidae | CP197249 | 173,966 |
| C | *Cacopsylla citrisuga* | Psyllidae | CP197250 | 169,003 |
| D | *Cacopsylla chinensis* | Psyllidae | CP197251 | 168,970 |
| E | *Cornegenapsylla sinica* | Aphalaridae (Phacopteroninae) | CP197252 | 172,068 |
| F | *Macrohomotoma gladiata* | Carsidaridae | CP197253 | 165,724 |
| G | *Blastopsylla occidentalis* | Aphalaridae | CP197254 | 166,875 |

Important taxonomy note from the supplement: the paper treats *Diaphorina* as Psyllidae despite historical instability in its placement, and treats *Cornegenapsylla sinica* as Aphalaridae (Phacopteroninae).

### 4.2 Eleven previously published Carsonella genomes used in the phylogeny

| Paper ID | Host | Family | Carsonella accession |
|---|---|---|---|
| J01 | *Heteropsylla cubana* | Psyllidae | NC_018416.1 |
| J02 | *Cacopsylla melanoneura* | Psyllidae | CP092147.1 |
| J03 | *Diaphorina citri* | Psyllidae | CP146469.1 |
| J04 | *Heteropsylla texana* | Psyllidae | CP003544.1 |
| J05 | *Cacopsylla picta* | Psyllidae | CP102598.1 |
| J06 | *Cacopsylla pyri* | Psyllidae | CP116500.1 |
| J07 | *Bactericera trigonica* | Triozidae | CP024798.1 |
| J08 | *Bactericera cockerelli* | Triozidae | CP019943.1 |
| J09 | *Ctenarytaina eucalypti* | Aphalaridae | CP003541.1 |
| J10 | *Pachypsylla* sp. 'celtidis' | Aphalaridae | CP003545.1 |
| J11 | *Pachypsylla venusta* | Aphalaridae | AP009180.1 |

### 4.3 Outgroups

The 18 Carsonella lineages were rooted with two obligate primary symbionts:

| Label | Taxon | Host context | GenBank accession |
|---|---|---|---|
| CaNd | *Candidatus Nardonella dryophthoridicola* strain NardRF | red palm weevil *Rhynchophorus ferrugineus* | CP069383 |
| CaPal | *Candidatus Portiera aleyrodidarum* strain AF-CAI | whitefly *Aleurodicus floccissimus* | LN734649 |

**Phylogenetic dataset = 18 Carsonella lineages + 2 outgroups.**

## 5. Genome-generation and comparative-genomics methods

These steps are part of the published study, but they are not all required for our first molecular-clock replication because the completed genomes are already deposited.

### Sequencing / assembly

- Illumina HiSeq, 150-bp paired-end reads.
- >20 GB raw data per sample.
- CLC Genomics Workbench v21 for initial de novo assembly.
- Initial CLC assembly parameters:
  - word size = 20
  - bubble size = 50
  - minimum contig length = 1,000 bp
- BLAST+ local database built from 11 published Carsonella genomes.
- Candidate Carsonella contigs identified by blastn.
- Hybrid reconstruction combined reference-guided mapping and de novo assembly.
- CLC mapping parameters:
  - mismatch cost = 2
  - insertion cost = 3
  - deletion cost = 3
  - length fraction = 0.9
  - similarity fraction = 0.9
- Ambiguous joins were resolved by PCR/Sanger sequencing when needed.
- Circularity was experimentally checked with outward-facing primers.
- Reads were remapped to final assemblies for coverage QC.

### Annotation / genome comparison

- NCBI PGAP for annotation.
- BRIG for circular genome visualization; CP197248 (*D. citri*) used as reference.
- FastANI v1.33; fragment length = 1,000 bp.
- Whole-genome multiple alignment in CLC Genomics Workbench, “Very accurate” setting:
  - gap open cost = 28.0
  - gap extension cost = 1.0
  - end gap cost = “as any other”
- `genbank-to` v0.42 to convert GenBank files into ORF/protein FASTA files.
- OrthoFinder v2.5.4, default settings, on predicted amino-acid sequences.
- Gene present in all seven new genomes = core under this study's seven-genome pangenome definition.
- Remaining genes = accessory.
- Accessory-gene presence/absence checked using BLAST+ with E-value < 1e-5.
- R v4.4.1 + `pheatmap` used for accessory-gene heatmap.
- eggNOG-mapper / COG used for provisional functional classification.

Published pangenome result for the seven new genomes:

- **Core: 155 genes**
- **Accessory: 40 genes**

## 6. Carsonella phylogenetic reconstruction

### Dataset

- 18 Carsonella lineages + 2 outgroups.
- Paper describes the analysis as genome-based / whole-genome phylogenomics.
- A concatenated nucleotide alignment was analysed as a single partition.

### Model selection

- ModelTest-NG v0.1.7.
- Single-partition analysis.
- Best-fitting nucleotide substitution model selected for the full alignment.

**Reproducibility note:** the exact winning substitution model for the Carsonella genome alignment is not stated in the supplied main article or supplement. We must not invent it. We will either recover it from deposited analysis files if available or rerun ModelTest-NG ourselves and document our result.

### Maximum-likelihood tree

- PhyML 3.3.3.20220408.
- 100 nonparametric bootstrap replicates.

### Bayesian tree

- MrBayes v3.2.7a.
- Two independent runs.
- Four chains per run.
- 1,000,000 generations.
- Sampling every 100 generations.
- First 25% discarded as burn-in.
- Convergence criteria:
  - average standard deviation of split frequencies < 0.01
  - potential scale reduction factors approximately 1.0

The paper reports identical ML and Bayesian topologies with maximal or near-maximal support at internal nodes.

## 7. Published MCMCtree divergence-dating design

### Engine and data

- MCMCtree in **PAML v4.10.9**.
- Concatenated Carsonella nucleotide alignment.
- `seqtype = 0` (DNA).
- Relaxed clock: `clock = 2`.
- Paper describes this as an **independent-rates / uncorrelated** model.
- Birth-death-sampling prior: `BDparas = 1 1 0`.
  - lambda = 1
  - mu = 1
  - rho = 0

### Approximate-likelihood workflow

The paper used the standard two-stage approximate-likelihood strategy:

1. `usedata = 3` to calculate gradients/Hessians.
2. `usedata = 2` for posterior sampling using the approximate likelihood.

### MCMC schedule

- Two independent MCMCtree runs.
- 100,000,000 steps per run.
- Sampling every 10,000 steps.
- First 10% discarded as burn-in.
- Tracer v1.7.2 used for convergence/mixing assessment.
- Required ESS > 200 for key parameters.
- Replicate logs combined using LogCombiner from the BEAST package.
- FigTree used to visualize the time tree.
- Chronogram summarized with median node ages and 95% HPD intervals.

### Important settings not reported in supplied paper/supplement

The following are **not yet verified** and must not be guessed:

- exact selected nucleotide substitution model for the Carsonella alignment
- exact construction procedure/file for the 18-lineage concatenated alignment beyond the paper's genome-alignment description
- `rgene_gamma`
- `sigma2_gamma`
- `alpha`
- `ncatG`
- `cleandata`
- `finetune`
- starting values / seed settings
- any additional MCMCtree control-file parameters not explicitly listed in Methods
- raw-read SRA run accessions (BioProject is reported, individual SRA IDs are not listed in the supplied article/supplement)

These are now explicit **reproducibility questions** for us rather than hidden assumptions.

## 8. Fossil calibrations

The dating analysis used only two host fossil-informed soft calibrations. The authors explicitly caution that these are host-derived calibrations and therefore depend on broad host–symbiont codivergence at the calibrated nodes.

### CAL-01 — Aphalaridae crown

- Calibrated node: crown of Carsonella lineages associated with Aphalaridae sensu lato.
- Fossil context: *Eogyropsylla* spp. from Eocene/Baltic amber plus *Eogyropsylla paveloctogenarius* from the Kishenehn Formation.
- Time context: Lutetian / middle Eocene.
- MCMCtree prior: **`B(0.412, 0.478)`**.
- On the paper's 100-Myr tree time scale: **41.2–47.8 Ma**.
- Implemented as a **soft bound**, not a fixed age.

### CAL-02 — Cacopsylla crown

- Calibrated node: crown of Carsonella lineages hosted by *Cacopsylla*.
- Fossil: *Cacopsylla trigona*.
- Geological context: Garang Formation, eastern Tibetan Plateau, China.
- Published formation age: Middle Miocene, **16–19 Ma**.
- MCMCtree prior: **`B(0.16, 0.19)`**.
- Implemented as a **soft bound**, not a fixed age.

### Interpretation rule

These calibrations do **not** assert that the bacterial nodes are exactly 41.2–47.8 Ma and 16–19 Ma. They place probabilistic temporal information on host-defined symbiont nodes under the assumption of broad codivergence. This assumption will later become one of our sensitivity-analysis targets.

## 9. Published divergence-time targets

The main article reports the following 95% HPD intervals. These are our first numerical replication targets:

| Evolutionary split / node | Published 95% HPD (Ma) |
|---|---:|
| sampled Psyllidae-associated Carsonella vs remaining Carsonella | 50.40–68.32 |
| Aphalaridae + Carsidaridae vs Triozidae + *D. citri* | 46.88–62.39 |
| *D. citri* Carsonella vs other Triozidae-associated Carsonella | 31.82–55.38 |
| *M. gladiata* vs sampled Aphalaridae | 25.15–41.11 |
| sampled Aphalaridae crown | 31.32–44.01 |
| *Heteropsylla* vs *Cacopsylla* | 24.98–50.29 |
| sampled *Cacopsylla* crown | **15.95–18.99** |

We will compare **posterior medians and full HPD intervals**, not merely ask whether our tree “looks similar.”

## 10. Host-tree context

This is not our first replication target, but it matters because the calibrations are host-informed.

- Host tree used mitochondrial `cox1` because it was the only marker consistently available across sampled host taxa.
- 18 psyllid species + host outgroups.
- Alignment in CLC Genomics Workbench.
- PhyML host ML tree used **GTR+G+I** with 1,000 bootstrap replicates.
- MrBayes v3.2.7a:
  - two runs of four chains
  - 1,500,000 generations
  - sampling every 100 generations
- Host–symbiont congruence assessed with ParaFit using patristic distances.
- `ParaFitGlobal = 18.59`, `P = 0.001`, 999 permutations.

Important biological caution: *D. citri* is a localized host–symbiont topological incongruence in this dataset. Its Carsonella groups with Triozidae-associated lineages even though the host is treated as Psyllidae. The authors therefore interpret codivergence as broad rather than strict.

## 11. Stage A completion checklist

- [x] Main article obtained and read.
- [x] Supplement obtained and read.
- [x] Exact seven new taxa identified.
- [x] Exact seven new GenBank accessions identified.
- [x] Eleven published Carsonella phylogenetic accessions identified.
- [x] Two outgroups identified.
- [x] BioProject identified: PRJNA1303861.
- [x] Major software packages and reported versions recorded.
- [x] Reported phylogenetic run settings recorded.
- [x] Reported MCMCtree workflow/settings recorded.
- [x] Both calibration nodes and priors reconstructed.
- [x] Main published dating intervals recorded.
- [x] Unreported/ambiguous settings explicitly identified rather than guessed.
- [ ] Recover individual raw-read/SRA run identifiers if needed.
- [ ] Determine whether deposited analysis files contain the exact ModelTest-NG winning model and MCMCtree control file.

## 12. Stage B — next: data provenance

We will next obtain the **already assembled genomes**, not the very large raw Illumina libraries. This is deliberate: our first learning objective is phylogenomics and molecular-clock inference, not genome assembly.

### Stage B tasks

- [ ] Download the seven newly deposited genomes CP197248–CP197254.
- [ ] Download the eleven published Carsonella genomes used in Fig. 5.
- [ ] Download the two outgroup genomes.
- [ ] Save accession, organism, host/family and source metadata in a machine-readable TSV/CSV.
- [ ] Verify accession labels manually against the paper.
- [ ] Verify the seven new genome lengths against Table 1.
- [ ] Record retrieval date and source.
- [ ] Compute SHA256 checksums for local input files.
- [ ] Inspect at least one GenBank record manually before automation.

## 13. Manual phylogenomics stage after data retrieval

- [ ] Inspect genome annotations and sequence composition.
- [ ] Reconstruct the exact sequence representation used for the published 18-lineage phylogeny as closely as the reporting permits.
- [ ] Understand why the paper used nucleotide data and a single concatenated partition.
- [ ] Run model selection rather than assuming a model.
- [ ] Infer ML topology and inspect support.
- [ ] Compare our topology with Fig. 5 / Fig. S2.
- [ ] Only after understanding the topology, prepare the dating tree.

## 14. Manual molecular-clock stage

- [ ] Prepare the MCMCtree tree file manually.
- [ ] Encode CAL-01 manually and explain it.
- [ ] Encode CAL-02 manually and explain it.
- [ ] Build the control file with every parameter annotated in our notes.
- [ ] Perform the approximate-likelihood preparation step.
- [ ] Run two independent posterior chains.
- [ ] Inspect convergence, trace behavior and ESS.
- [ ] Compare medians and HPDs with the published chronogram.
- [ ] Explain any disagreement before changing settings.

## 15. Sensitivity experiments after baseline replication

- [ ] Prior-only run to see what calibrations/tree prior imply without sequence likelihood.
- [ ] Broader calibration bounds.
- [ ] Alternative scientifically defensible calibration treatment.
- [ ] Alternative clock model if appropriate.
- [ ] Reduced gene/alignment sample.
- [ ] Reduced/altered taxon sample.
- [ ] Quantify movement in node medians and HPD widths.
- [ ] Classify conclusions as robust or calibration/model-sensitive.

## 16. Research engineering — only after manual mastery

- [ ] Python parser for MCMCtree outputs.
- [ ] Structured YAML/JSON configuration.
- [ ] Input validation and helpful failures.
- [ ] Automated repeated sensitivity experiments.
- [ ] Workflow engine (Nextflow or Snakemake, chosen after manual workflow is stable).
- [ ] Slurm execution and resource benchmarking.
- [ ] Docker environment.
- [ ] Apptainer/HPC execution.
- [ ] Unit/integration tests.
- [ ] GitHub Actions CI.
- [ ] Reproducible report and provenance metadata.

## 17. 10/10 mastery rubric

A point is earned only when it can be explained and demonstrated.

- [ ] 1/10 Biological question and symbiosis understood
- [ ] 2/10 Study design and data provenance understood
- [ ] 3/10 Phylogenomic reconstruction understood
- [ ] 4/10 Substitution models and branch lengths understood
- [ ] 5/10 Molecular-clock theory understood
- [ ] 6/10 Calibration and Bayesian prior logic understood
- [ ] 7/10 Published dating analysis substantially replicated
- [ ] 8/10 MCMC diagnostics and sensitivity analyses interpreted independently
- [ ] 9/10 Workflow can be modified/debugged without blindly copying commands
- [ ] 10/10 Reproducible engineering layer built and scientific conclusions communicated clearly

## 18. Current status

**Stage A — published-method reconstruction: essentially complete.**

We now have enough verified information to begin **Stage B: accession-controlled data retrieval and inspection**.

No automated analysis pipeline has been added yet. That is intentional.
