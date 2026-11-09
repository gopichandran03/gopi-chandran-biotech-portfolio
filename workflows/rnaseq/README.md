# RNA-seq count-matrix QC

Quality-control checks on a gene-level count matrix, before any
differential-expression analysis.

**Full workflow walkthrough with a stage-by-stage inspector:**
[projects/moringa-rnaseq/](../../projects/moringa-rnaseq/index.html)

---

## Scope

This script covers **one honest piece** of a transcriptome workflow: the checks
worth running on a count matrix once alignment and quantification are done. It
is not a replacement for read-level QC, alignment, transcript assembly,
differential expression or functional annotation.

It ships with `data/example_counts.tsv`, a **clearly labelled example matrix**
(4,000 genes × 5 tissues) generated for this demonstration, so the script runs
anywhere in seconds. One sample in it is deliberately under-sequenced so the
warnings have something real to catch.

The project this belongs to ran against the publicly deposited *Moringa
oleifera* RNA-seq dataset, NCBI BioProject
[`PRJNA394193`](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA394193) — not
private or unpublished data.

## Run it

```bash
python3 -m pip install -r ../../requirements.txt

python3 qc_summary.py --counts data/example_counts.tsv
python3 qc_summary.py --counts data/example_counts.tsv --out qc/
```

Input is a TSV with genes in rows and samples in columns, first column the
gene identifier.

## What it checks

| Check | Why it matters |
|-------|----------------|
| Library size per sample | A sample at a fraction of the others' depth will look "low-expressing" everywhere |
| Genes detected per sample | A detection rate far off the rest means uneven depth or input quality |
| % of reads in the top 10 and 50 genes | A high share is the signature of rRNA or other contamination dominating the library |
| Median non-zero count | Depth sanity check that is not distorted by the zeros |
| Sample-sample Spearman correlation on log2 CPM | Samples should group as the biology predicts; one that correlates with nothing needs investigating |
| Genes with zero counts everywhere | Filtering candidates, and a sanity check on the annotation used |

Warnings use conventional thresholds (half the median library size, 40% of
reads in the top 10 genes, a 25-point spread in detection rate, best
correlation below 0.7). They are prompts to look, not verdicts.

## Where this sits in the full pipeline

```
1. Raw read QC            FastQC + MultiQC
2. Trim and filter        Trimmomatic / fastp
3. Align                  HISAT2  (--dta for downstream assembly)
4. Assemble transcripts   StringTie, then --merge, then gffcompare
5. Quantify               StringTie -e -B, then prepDE.py   <-- produces the matrix
6. QC the matrix          *** this script ***
7. Find coding regions    TransDecoder
8. Annotate               BLAST + InterProScan + eggNOG-mapper
9. Pathway mapping        KEGG (KAAS / KofamScan)
```

The walkthrough linked above has the actual command for each stage, the
checkpoint that decides whether to continue, and the failure mode that
checkpoint exists to catch.

## One interpretation trap worth naming

Transcripts are not genes. An assembly reporting 66,079 transcripts over 200 bp
does not describe ~66,000 genes — isoforms and fragments collapse to a far
smaller number of gene models. Quoting the transcript count as a gene count
inflates the result several-fold, and it is one of the most common errors in
transcriptome reporting.

## Reproducibility

What this script does well: fixed inputs, no hidden state, deterministic output.

What a production workflow needs that this does not have: a workflow manager
(Nextflow or Snakemake) so dependencies and resumption are declared rather than
hand-managed, containers pinning exact tool versions, a single config file for
paths and parameters, and checksums on reference inputs.
