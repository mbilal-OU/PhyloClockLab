# PhyloClockLab

A learning-first laboratory for reproducible molecular-clock and deep-time phylogenomics.

## Philosophy

**LEARN → APPLY → SHIP**

This repository is intentionally built from manual understanding toward automation. A workflow is not considered mastered merely because it runs. Each study should progress through biological understanding, manual analysis, result inspection, troubleshooting, sensitivity analysis, and only then research-software engineering.

## Study 01 — Carsonella (Wu et al., 2026)

**Paper:** Wu F. et al. *Time-resolved comparative genomics of ‘Candidatus Carsonella ruddii’ across psyllid lineages reveals a conserved core genome and contrasting secondary symbiont dynamics.* Microbial Genomics 12(6), 001727 (2026). DOI: 10.1099/mgen.0.001727

**Learning targets:**

- molecular evolution and substitution models
- phylogram vs chronogram
- strict vs relaxed molecular clocks
- calibration logic and uncertainty
- Bayesian priors, likelihoods, posteriors and MCMC
- MCMCTree/PAML interpretation
- convergence and independent-chain diagnostics
- calibration/model/sampling sensitivity
- Python/Bash automation after manual mastery
- workflow engineering, Slurm, containers, testing and CI

See [`studies/carsonella_2026/STUDY_LEDGER.md`](studies/carsonella_2026/STUDY_LEDGER.md) for the replication ledger.

## Study 02 — Alphaproteobacteria

Planned after Study 01. It will be used as the advanced methodological-sensitivity study once the Carsonella analysis can be explained and reproduced independently.

## Status

🟡 **Study 01: methods reconstruction and practical replication starting**

No automated pipeline is being added yet. Automation will be earned after the manual analysis is understood.
