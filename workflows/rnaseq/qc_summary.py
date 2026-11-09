#!/usr/bin/env python3
"""Quality-control summary for an RNA-seq count matrix.

WHAT THIS IS
    The checks worth running on a gene-level count matrix before any
    differential-expression analysis: library sizes, detection rates, the
    share of reads taken by the most abundant genes, and sample-sample
    correlation. It reads a plain TSV, so it runs anywhere in seconds.

WHAT THIS IS NOT
    A replacement for read-level QC (FastQC/MultiQC), alignment, transcript
    assembly, differential expression or functional annotation. See README.md
    for where this sits in a full HISAT2/StringTie workflow.

Usage
    python3 qc_summary.py --counts data/example_counts.tsv
    python3 qc_summary.py --counts data/example_counts.tsv --out qc/
"""
from __future__ import annotations

import argparse
import pathlib
import sys

try:
    import numpy as np
    import pandas as pd
except ImportError:  # pragma: no cover
    sys.exit("numpy and pandas are required: python3 -m pip install -r requirements.txt")


def load_counts(path: pathlib.Path) -> pd.DataFrame:
    if not path.exists():
        sys.exit(f"no such file: {path}")
    df = pd.read_csv(path, sep="\t", index_col=0)
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        sys.exit("no numeric count columns found - is this a count matrix?")
    if (numeric < 0).any().any():
        sys.exit("negative values found - this does not look like a count matrix")
    return numeric


def cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0)
    return counts.divide(lib.replace(0, np.nan), axis=1) * 1e6


def library_summary(counts: pd.DataFrame, min_count: int) -> pd.DataFrame:
    lib = counts.sum(axis=0)
    detected = (counts >= min_count).sum(axis=0)
    top10 = counts.apply(lambda c: c.nlargest(10).sum() / c.sum() * 100 if c.sum() else np.nan)
    top50 = counts.apply(lambda c: c.nlargest(50).sum() / c.sum() * 100 if c.sum() else np.nan)
    return pd.DataFrame({
        "library_size": lib.astype("int64"),
        "genes_detected": detected.astype("int64"),
        "pct_genes_detected": (detected / len(counts) * 100).round(2),
        "pct_reads_top10_genes": top10.round(2),
        "pct_reads_top50_genes": top50.round(2),
        "median_nonzero_count": counts.replace(0, np.nan).median(axis=0).round(1),
    })


def flag_outliers(summary: pd.DataFrame, corr: pd.DataFrame) -> list[str]:
    """Plain-language warnings. Thresholds are conventional, not authoritative."""
    notes: list[str] = []
    lib = summary["library_size"]
    median_lib = lib.median()
    for sample, size in lib.items():
        if median_lib and size < 0.5 * median_lib:
            notes.append(
                f"{sample}: library size {size:,} is under half the median "
                f"({median_lib:,.0f}) - under-sequenced relative to the rest."
            )
    for sample, pct in summary["pct_reads_top10_genes"].items():
        if pct > 40:
            notes.append(
                f"{sample}: top 10 genes hold {pct:.1f}% of reads - check for rRNA "
                f"or other contamination dominating the library."
            )
    det = summary["pct_genes_detected"]
    if len(det) > 1 and det.max() - det.min() > 25:
        notes.append(
            f"detection rate ranges {det.min():.1f}%-{det.max():.1f}% across samples - "
            f"a spread this wide usually means uneven depth or input quality."
        )
    if len(corr) > 2:
        worst = corr.where(~np.eye(len(corr), dtype=bool)).max()
        for sample, best in worst.items():
            if best < 0.7:
                notes.append(
                    f"{sample}: best correlation with any other sample is {best:.2f} - "
                    f"this sample does not group with the rest; investigate before including it."
                )
    return notes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--counts", type=pathlib.Path, required=True,
                    help="TSV count matrix: genes in rows, samples in columns")
    ap.add_argument("--min-count", type=int, default=1,
                    help="counts at or above this mark a gene as detected (default 1)")
    ap.add_argument("--out", type=pathlib.Path, default=None,
                    help="directory for summary tables and the plot")
    args = ap.parse_args()

    counts = load_counts(args.counts)
    print(f"Loaded {counts.shape[0]:,} genes x {counts.shape[1]} samples "
          f"from {args.counts}")
    print()

    summary = library_summary(counts, args.min_count)
    print("PER-SAMPLE SUMMARY")
    print(summary.to_string())
    print()

    logc = np.log2(cpm(counts).fillna(0) + 1)
    corr = logc.corr(method="spearman").round(3)
    print("SAMPLE-SAMPLE CORRELATION (Spearman on log2 CPM)")
    print(corr.to_string())
    print()

    zero_everywhere = int((counts.sum(axis=1) == 0).sum())
    print("MATRIX-LEVEL")
    print(f"  genes with zero counts in every sample : {zero_everywhere:,} "
          f"({zero_everywhere / len(counts) * 100:.1f}%)")
    print(f"  genes detected in all samples          : "
          f"{int((counts >= args.min_count).all(axis=1).sum()):,}")
    print(f"  total counts                           : {int(counts.values.sum()):,}")
    print()

    notes = flag_outliers(summary, corr)
    if notes:
        print("WARNINGS")
        for n in notes:
            print(f"  - {n}")
    else:
        print("WARNINGS: none at the default thresholds.")
    print()
    print("Reminder: these are descriptive QC checks. They do not validate the")
    print("upstream alignment or assembly, and passing them does not make a")
    print("differential-expression result correct.")

    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        summary.to_csv(args.out / "sample_summary.tsv", sep="\t")
        corr.to_csv(args.out / "sample_correlation.tsv", sep="\t")
        write_plot(summary, logc, args.out / "qc_overview.png")
        print(f"\nWrote sample_summary.tsv, sample_correlation.tsv and "
              f"qc_overview.png to {args.out}/")

    return 0


def write_plot(summary: pd.DataFrame, logc: pd.DataFrame, path: pathlib.Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available - skipping the plot", file=sys.stderr)
        return

    series_1 = "#2a78d6"
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=140)

    ax = axes[0]
    lib = summary["library_size"] / 1e6
    bars = ax.barh(lib.index, lib.values, color=series_1, height=0.6)
    ax.bar_label(bars, fmt="%.1fM", padding=4, fontsize=8, color="#10212b")
    ax.set_xlabel("Library size (million counts)", fontsize=9, color="#52616a")
    ax.set_title("Library size by sample", fontsize=10)
    ax.margins(x=0.16)
    ax.spines[["top", "right"]].set_visible(False)

    ax = axes[1]
    box_kw = dict(
        patch_artist=True,
        boxprops=dict(facecolor="#cde2fb", edgecolor=series_1),
        medianprops=dict(color="#0d366b"),
        flierprops=dict(markersize=2, markerfacecolor="#8c9a92",
                        markeredgecolor="none", alpha=0.4),
    )
    data = [logc[c].values for c in logc.columns]
    names = list(logc.columns)
    # matplotlib renamed boxplot's `labels` to `tick_labels` in 3.9.
    try:
        ax.boxplot(data, tick_labels=names, **box_kw)
    except TypeError:
        ax.boxplot(data, labels=names, **box_kw)
    ax.set_ylabel("log2(CPM + 1)", fontsize=9, color="#52616a")
    ax.set_title("Expression distribution by sample", fontsize=10)
    ax.tick_params(axis="x", rotation=30, labelsize=8)
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


if __name__ == "__main__":
    sys.exit(main())
