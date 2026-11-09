# Gopi Chandran | Biotechnology · Bioinformatics · Operations

MPS Biotechnology student at the University of Maryland, Baltimore County
(UMBC), with a B.Tech. in Biotechnology from Tamil Nadu Agricultural University
(TNAU). Interests span biotechnology R&D, reproducible bioinformatics,
mammalian cell culture operations, and biotechnology commercialization.

**Portfolio:** <https://gopichandran03.github.io/gopi-chandran-biotech-portfolio/>
**Project walkthroughs:** <https://gopichandran03.github.io/gopi-chandran-biotech-portfolio/projects/>

- GitHub: <https://github.com/gopichandran03>
- LinkedIn: <https://www.linkedin.com/in/gopichandran03/>
- Email: gopic2@umbc.edu

---

## Portfolio integrity note

Code in this repository consists of reproducible demonstrations and workflow
templates. It does not reproduce proprietary employer work or unpublished
research results.

Where a demonstration needs data, it runs on **clearly labelled synthetic or
example input**, and every page that uses such data says so. Published findings
from the literature are cited to their source on each walkthrough's final
slide. Replace example inputs with authorized data before using any of these
workflows for research, and never upload confidential, patient-identifiable,
employer-owned or otherwise restricted data.

---

## Project walkthroughs

Eight projects, each as a short slide deck you can click through. Most carry a
demo that runs in the browser, reachable with one click from the top of the
page.

| # | Project | What you can do with it |
|---|---------|------------------------|
| 01 | [Pivot Bio commercialization strategy](projects/pivot-bio/) | Grower unit-economics calculator; market, competitive and exit analysis |
| 02 | [Quality & process monitoring](projects/process-monitoring/) | Live Shewhart control chart — inject a shift, drift or excursion and watch the run rules |
| 03 | [HTB-182 culture operations](projects/htb182-cell-culture/) | Culture planning calculator: passage and split, plan backwards from an experiment, size a cell bank |
| 04 | [Computational & quantum antibody design](projects/computational-antibody/) | TRACE platform context across filovirus, Lassa and SARS-CoV-2; scorecard for quantum claims |
| 05 | [CR6261 and the influenza HA stem](projects/cr6261-influenza/) | Structural and immunogenetic analysis of a broadly neutralizing antibody |
| 06 | [RiceStressDB](projects/ricestressdb/) | Query console over the sample extract, with the generated SQL shown |
| 07 | [*Moringa oleifera* RNA-seq profiling](projects/moringa-rnaseq/) | Stage-by-stage pipeline inspector: commands, checkpoints, failure modes |
| 08 | [*Dalbergia latifolia* genome characterization](projects/dalbergia-genomics/) | Working microsatellite finder — paste in any sequence |

## Runnable code

Each tool is self-contained and documented in its own README.

```bash
git clone https://github.com/gopichandran03/gopi-chandran-biotech-portfolio.git
cd gopi-chandran-biotech-portfolio
python3 -m pip install -r requirements.txt    # Python 3.10+
```

| Folder | Tool | Needs |
|--------|------|-------|
| [`workflows/quality_control/`](workflows/quality_control/) | Shewhart charts, run rules, Cp/Cpk over synthetic data | numpy (matplotlib for plots) |
| [`workflows/rice_stress_db/`](workflows/rice_stress_db/) | Database schema, sample data and query demo | nothing — standard library |
| [`workflows/rnaseq/`](workflows/rnaseq/) | Count-matrix QC summary | numpy, pandas, matplotlib |
| [`workflows/ssr_finder/`](workflows/ssr_finder/) | Perfect tandem repeat (SSR) detection | nothing — standard library |

```bash
python3 workflows/ssr_finder/find_ssrs.py --demo
python3 workflows/rice_stress_db/query_demo.py
python3 workflows/quality_control/process_monitor.py --fault shift --size 1.5
python3 workflows/rnaseq/qc_summary.py --counts workflows/rnaseq/data/example_counts.tsv
```

---

## Areas of focus

- **Bioinformatics** — RNA-seq workflow design, transcriptome analysis,
  functional annotation, comparative genomics, biological databases.
- **Biopharmaceutical operations** — laboratory readiness, mammalian cell
  culture, documentation, process consistency, quality-conscious work.
- **Commercialization and coordination** — partner screening, competitive
  intelligence, market landscape analysis, project coordination, scientific
  communication.
- **Computing** — Python, R, Linux, MySQL, PHP.

## Selected work

### RiceStressDB — agricultural biotechnology database
A relational database organising rice stress gene information: 1,200+ genes
across 17 biotic and abiotic stress conditions, with functional annotations and
stress metadata. MySQL and PHP. Government of India software copyright
registration `SW-35001/2025-CO`, associated with TNAU.

This repository contains a demonstration schema and a 15-record sample extract
drawn from public curated resources — not the production database.

### *Moringa oleifera* RNA-seq transcript profiling
Transcript profiling for phytochemical biosynthesis genes using HISAT2,
StringTie, TransDecoder, eggNOG-mapper, InterProScan, BLAST and KEGG. Run
against the public dataset NCBI BioProject `PRJNA394193`. Metrics recorded for
my run: 79.79 Mb assembly, N50 2,094 bp, 66,079 transcripts over 200 bp — the
N50 matching the published assembly for the same dataset.

### *Dalbergia latifolia* genome characterization
SSR and SNP marker discovery, genome alignment and variant analysis during a
bioinformatics internship at the Forest Research Institute, Dehradun, with
application to diversity assessment and conservation genetics for a species
listed on CITES Appendix II.

### Pivot Bio commercialization strategy
Market opportunity, competitive positioning, customer segments, value
proposition, go-to-market and exit analysis. The team was a finalist in a
simulated investment exercise and received the highest simulated investment
allocation ($1 million) among five finalist teams.

### HTB-182 cell culture operations
Continuous maintenance of HTB-182 (NCI-H520) lung squamous carcinoma cells at
UMBC: passaging and split planning, caffeine treatment design, scaling the
culture up and down to meet experiments, cryopreservation and cell banking, and
contingency planning for incubator, power and contamination failures.

### Computational and quantum antibody design — Regenova
Business development and operations support across broadly neutralizing
antibody programmes for pan-filovirus, Lassa and SARS-CoV-2 targets, built on
TRACE, a hybrid quantum-classical platform. Includes partner screening,
competitive landscape work, scientific-commercial due diligence, and a
conference abstract in preparation for the SARS-CoV-2 programme. Public pages
carry no confidential technical detail.

## Experience highlights

### Regenova Pharmaceuticals — Business Development & Operations Management Intern
- Screened 20+ potential industry and academic partners; five advanced to the
  next evaluation stage. 50+ academic outreach activities.
- Prepared market landscape and competitive-intelligence materials across
  biotherapeutics, AI-enabled drug discovery, oncology and infectious disease.
- Translated scientific programmes into partnership, proposal, commercialization
  and funding materials.

### UMBC — Graduate Assistant / Teaching Assistant
- Supported coordination across 13+ biotechnology and life-science courses,
  100+ class sessions and 60+ guest speakers.
- Mammalian cell culture: HEK293 and HTB-182, internally modified laboratory
  protocols, CO₂ incubators, biosafety cabinets, microscopy, automated and
  manual cell counting.
- Contributed literature review and preliminary investigation to a
  xenotransplantation-related project examining flow-cytometry approaches for
  chimerism detection.

## Technical toolkit

**Bioinformatics:** HISAT2, StringTie, TransDecoder, eggNOG-mapper,
InterProScan, BLAST, MEGA, KEGG
**Data:** Python, R, Linux, MySQL, PHP
**Biotechnology:** mammalian cell culture, molecular biology, genomics, RNA-seq,
functional annotation
**Operations:** documentation, project coordination, stakeholder communication,
market research, competitive intelligence

## Education

- **MPS Biotechnology**, University of Maryland, Baltimore County (UMBC) —
  expected May 2027
- **B.Tech. Biotechnology**, Tamil Nadu Agricultural University (TNAU) —
  GPA 3.70/4.00

---

## Repository layout

```
index.html                  portfolio site
projects/                   eight project walkthroughs (generated)
  index.html                walkthrough hub
  <slug>/index.html
scripts/
  build_pages.py            renders projects/ from content modules
  content/<slug>.py         slide content, one module per project
workflows/                  runnable demonstration code
assets/
  css/deck.css              shared styling for walkthrough pages
  js/deck.js                slide navigation
```

Walkthrough pages are generated. Edit the content module in `scripts/content/`,
then rebuild:

```bash
python3 scripts/build_pages.py            # write pages
python3 scripts/build_pages.py --check    # render without writing
```
