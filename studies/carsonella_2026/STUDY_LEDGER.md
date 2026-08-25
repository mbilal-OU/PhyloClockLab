# Study 01 — Carsonella 2026 Replication Ledger

## 1. Citation

Wu F, Deng K, Lin X, et al. **Time-resolved comparative genomics of ‘Candidatus Carsonella ruddii’ across psyllid lineages reveals a conserved core genome and contrasting secondary symbiont dynamics.** *Microbial Genomics*. 2026;12(6):001727. DOI: 10.1099/mgen.0.001727.

## 2. Why this study is our starting point

This study is small enough to inspect carefully but rich enough to teach real evolutionary genomics. It combines complete bacterial genomes, comparative genomics, phylogenomics, pangenome analysis and fossil-informed relaxed-clock dating.

Our objective is **not** to reproduce every figure blindly. The objective is to understand and reconstruct the temporal phylogenomic logic well enough to explain, modify, troubleshoot and later automate it.

## 3. Facts verified from the published article

- Seven complete *Candidatus Carsonella ruddii* genomes were generated.
- Genome sizes were approximately 165–174 kb.
- The hosts represent four psyllid families.
- The genomes are extremely AT-rich (>82% AT) and gene dense (>90% coding).
- The study reports a conserved core of 155 genes.
- The analysis integrates whole-genome phylogenomics, pangenome analysis and fossil-calibrated relaxed-clock dating.
- Two host fossil-informed soft calibrations were used for the dating analysis.
- Major inferred Carsonella divergences were concentrated from the Paleogene to Miocene.
- The reported crown diversification of Cacopsylla-associated Carsonella was approximately 15.95–18.99 Ma.
- The paper cites/uses the methodological ecosystem around OrthoFinder, ModelTest-NG, PhyML, MrBayes, PAML/MCMCTree, Tracer and FigTree; exact settings must be verified from the full Methods/Supplement before we reproduce them.

## 4. Candidate host panel — must be verified against the Carsonella Methods/Supplement

A closely related 2026 psyllid mitogenome study by overlapping authors used the following seven host species, also spanning four families:

1. *Blastopsylla occidentalis* — Aphalaridae
2. *Cornegenapsylla sinica* — Aphalaridae
3. *Macrohomotoma gladiata* — Carsidaridae
4. *Cacopsylla citrisuga* — Psyllidae
5. *Cacopsylla chinensis* — Psyllidae
6. *Diaphorina citri* — Psyllidae
7. *Bactericera cockerelli* — Triozidae

**Important:** this is currently a **candidate reconstruction**, not yet accepted as the exact Carsonella study panel until checked against the Carsonella article/supplementary material.

## 5. Published-method ledger — current status

| Component | Status | What we know now | What must still be verified |
|---|---|---|---|
| Biological question | ✅ verified | Time-resolved evolution of Carsonella across psyllid lineages | — |
| Number of new Carsonella genomes | ✅ verified | 7 | — |
| Host families | ✅ verified | 4 | Exact species/family assignments |
| Genome size range | ✅ verified | ~165–174 kb | Per-genome values |
| Core genome | ✅ verified | 155 genes | Exact orthology criteria |
| Orthology method | 🟡 partial | OrthoFinder is cited in the article | Version, parameters, inputs |
| Functional annotation | 🟡 partial | eggNOG-mapper is cited | Version, parameters |
| Phylogenetic model selection | 🟡 partial | ModelTest-NG is cited | Exact dataset/model per analysis |
| ML phylogeny | 🟡 partial | PhyML is cited | Version, model, support settings |
| Bayesian phylogeny | 🟡 partial | MrBayes 3.2 is cited | Generations, burn-in, partitions |
| Molecular-clock engine | 🟡 partial | PAML/MCMCTree methodology is cited | PAML version, exact control-file settings |
| Relaxed clock | ✅ broad concept verified | Fossil-calibrated relaxed-clock dating | Exact MCMCTree clock model |
| Calibrations | 🟡 partial | 2 host fossil-informed soft calibrations | Exact nodes, bounds/distributions, justification |
| MCMC diagnostics | 🟡 partial | Tracer is cited | Number of chains, chain length, sampling interval, ESS threshold |
| Tree visualization | 🟡 partial | FigTree v1.4.4 is cited | Exact plotting workflow |
| Genome accessions | ⬜ pending | Seven complete genomes exist | Exact accession for each taxon |
| Raw-read accessions | ⬜ pending | Not yet reconstructed | BioProject/SRA IDs if available |
| Published target node ages | 🟡 partial | Cacopsylla crown 15.95–18.99 Ma | Full node-age table and intervals |

## 6. Study 01 practical sequence

### Stage A — Methods reconstruction

- [ ] Obtain/read the full article Methods.
- [ ] Obtain/read Supplementary material 1.
- [ ] Build the exact seven-taxon/accession table.
- [ ] Record BioProject/SRA/GenBank identifiers.
- [ ] Record every software package and version.
- [ ] Record every important command-line or control-file parameter.
- [ ] Record the two calibration nodes and their mathematical prior definitions.
- [ ] Record MCMC chain length, sampling frequency, burn-in and diagnostic criteria.
- [ ] Record the exact published node ages we will use as replication targets.

### Stage B — Data provenance

- [ ] Download the exact published genomes.
- [ ] Save accession metadata in a TSV/CSV file.
- [ ] Verify genome lengths against the publication.
- [ ] Verify organism/host labels manually.
- [ ] Record download date and source.
- [ ] Compute checksums for local input files.

### Stage C — Manual phylogenomics

- [ ] Inspect genome annotations.
- [ ] Reconstruct ortholog/core-gene selection.
- [ ] Inspect the selected genes rather than accepting them blindly.
- [ ] Align genes manually/explicitly.
- [ ] Inspect alignment quality.
- [ ] Concatenate only after understanding the gene-level inputs.
- [ ] Reconstruct the published-style topology.
- [ ] Interpret branch lengths and support values.

### Stage D — Manual molecular-clock replication

- [ ] Prepare the dating topology/input manually.
- [ ] Encode the published calibrations manually.
- [ ] Understand every important MCMCTree control parameter before using it.
- [ ] Run the baseline analysis.
- [ ] Run at least two independent chains.
- [ ] Inspect convergence rather than trusting completion status.
- [ ] Compare posterior node ages with the publication.
- [ ] Explain discrepancies scientifically.

### Stage E — Sensitivity experiments

- [ ] Broaden/narrow a calibration prior.
- [ ] Test an alternative clock assumption where scientifically appropriate.
- [ ] Test a reduced gene sample.
- [ ] Test a reduced/altered taxon sample.
- [ ] Quantify how node ages and uncertainty change.
- [ ] Distinguish robust conclusions from calibration-sensitive conclusions.

### Stage F — Research engineering (only after manual mastery)

- [ ] Write a parser for MCMCTree outputs.
- [ ] Add structured configuration (YAML/JSON).
- [ ] Automate repeated sensitivity analyses.
- [ ] Add validation and clear error messages.
- [ ] Add a workflow engine.
- [ ] Add Slurm execution.
- [ ] Add Docker and Apptainer reproducibility.
- [ ] Add tests and CI.
- [ ] Generate a reproducible final report.

## 7. 10/10 mastery rubric

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

## 8. Current status

**Status: Stage A — methods reconstruction.**

No automated workflow should be added yet. The next earned artifact will be the exact taxa/accession/method/calibration ledger reconstructed from the paper and supplement.
