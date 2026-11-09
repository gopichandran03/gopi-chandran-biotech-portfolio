#!/usr/bin/env python3
"""Detect perfect tandem repeats (microsatellites / SSRs) in DNA sequences.

This is the first step of SSR marker development: scan a sequence for perfect
tandem repeats of motif length 1-6 that meet a minimum repeat count, then
report the ones with enough flanking sequence to design primers against.

The algorithm is the standard one used by tools in the MISA family:
  * scan for each period p from 6 down to 1 (longest first, so a (AGGT)n is
    not consumed as overlapping di-repeats),
  * reject motifs that are themselves repeats of a shorter unit,
  * accept runs meeting the per-period minimum repeat count,
  * mark accepted spans as covered so hits never overlap.

Usage
    python3 find_ssrs.py sequence.fasta
    python3 find_ssrs.py sequence.fasta --min 1:12,2:6,3:5,4:5,5:4,6:4
    python3 find_ssrs.py sequence.fasta --flank 100 --tsv ssrs.tsv
    python3 find_ssrs.py --demo

Works on real FASTA input. `--demo` generates a synthetic sequence with known
repeats inserted, so the detector's behaviour can be checked against a known
answer; that sequence is NOT from any real organism.
"""
from __future__ import annotations

import argparse
import pathlib
import random
import sys
from dataclasses import dataclass, asdict

DEFAULT_MIN = {1: 12, 2: 6, 3: 5, 4: 5, 5: 4, 6: 4}
CLASS_NAME = {1: "mono", 2: "di", 3: "tri", 4: "tetra", 5: "penta", 6: "hexa"}


@dataclass
class SSR:
    seq_id: str
    start: int          # 1-based inclusive
    end: int            # 1-based inclusive
    motif: str
    motif_class: str
    repeats: int
    length: int
    normalised: str     # lexicographically smallest rotation
    left_flank: int
    right_flank: int

    @property
    def primer_ready(self) -> bool:
        return self.left_flank >= 100 and self.right_flank >= 100


def read_fasta(path: pathlib.Path) -> list[tuple[str, str]]:
    """Return [(id, sequence)]. Non-ACGT characters are stripped."""
    records: list[tuple[str, list[str]]] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                records.append((line[1:].split()[0] or f"seq{len(records) + 1}", []))
            else:
                if not records:
                    records.append(("sequence_1", []))
                records[-1][1].append(line)
    cleaned = []
    for name, chunks in records:
        seq = "".join(chunks).upper()
        seq = "".join(c for c in seq if c in "ACGT")
        if seq:
            cleaned.append((name, seq))
    return cleaned


def normalise(motif: str) -> str:
    """Lexicographically smallest rotation, so (AG)n and (GA)n group together."""
    return min(motif[i:] + motif[:i] for i in range(len(motif)))


def is_primitive(motif: str) -> bool:
    """False if the motif is itself a repeat of a shorter unit (e.g. 'ATAT')."""
    n = len(motif)
    for p in range(1, n):
        if n % p:
            continue
        if motif == motif[:p] * (n // p):
            return False
    return True


def find_ssrs(seq_id: str, seq: str, minimums: dict[int, int]) -> list[SSR]:
    n = len(seq)
    covered = bytearray(n)
    hits: list[SSR] = []

    for period in range(6, 0, -1):
        need = minimums.get(period, 0)
        if need < 2:
            continue
        i = 0
        while i + period <= n:
            motif = seq[i:i + period]
            if not is_primitive(motif):
                i += 1
                continue
            count, j = 1, i + period
            while j + period <= n and seq[j:j + period] == motif:
                count += 1
                j += period
            if count >= need:
                if not any(covered[i:j]):
                    covered[i:j] = b"\x01" * (j - i)
                    hits.append(SSR(
                        seq_id=seq_id,
                        start=i + 1,
                        end=j,
                        motif=motif,
                        motif_class=CLASS_NAME[period],
                        repeats=count,
                        length=j - i,
                        normalised=normalise(motif),
                        left_flank=i,
                        right_flank=n - j,
                    ))
                i = j
            else:
                i += 1

    hits.sort(key=lambda h: h.start)
    return hits


def synthetic_sequence(seed: int = 20261109) -> str:
    """Random background with known repeats inserted - for checking the detector.

    NOT a real sequence from any organism.
    """
    rng = random.Random(seed)
    parts: list[str] = []

    def background(k: int) -> None:
        parts.append("".join(rng.choice("ACGT") for _ in range(k)))

    plan = [(120, None), (0, ("AG", 14)), (95, None), (0, ("AAT", 9)),
            (140, None), (0, ("A", 16)), (80, None), (0, ("GATA", 7)),
            (110, None), (0, ("CT", 11)), (130, None), (0, ("AGGT", 6)),
            (75, None), (0, ("TTAGG", 5)), (160, None), (0, ("ACGTCA", 4)),
            (90, None), (0, ("TA", 8)), (145, None), (0, ("CCG", 7)), (100, None)]
    for bg, rep in plan:
        if bg:
            background(bg)
        if rep:
            parts.append(rep[0] * rep[1])
    return "".join(parts)


def parse_minimums(spec: str | None) -> dict[int, int]:
    if not spec:
        return dict(DEFAULT_MIN)
    out = dict(DEFAULT_MIN)
    for pair in spec.split(","):
        period, _, count = pair.partition(":")
        try:
            p, c = int(period), int(count)
        except ValueError:
            sys.exit(f"bad --min entry {pair!r}; expected forms like 2:6")
        if p not in CLASS_NAME:
            sys.exit(f"--min period must be 1-6, got {p}")
        out[p] = c
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fasta", nargs="?", type=pathlib.Path,
                    help="input FASTA file (omit with --demo)")
    ap.add_argument("--demo", action="store_true",
                    help="run on a synthetic sequence with known repeats")
    ap.add_argument("--min", dest="minimums", default=None,
                    help="minimum repeats per period, e.g. 1:12,2:6,3:5,4:5,5:4,6:4")
    ap.add_argument("--flank", type=int, default=100,
                    help="flank in bp required on each side to call a hit primer-ready")
    ap.add_argument("--tsv", type=pathlib.Path, default=None, help="write results as TSV")
    args = ap.parse_args()

    if args.demo:
        records = [("synthetic_demo", synthetic_sequence())]
    elif args.fasta:
        if not args.fasta.exists():
            sys.exit(f"no such file: {args.fasta}")
        records = read_fasta(args.fasta)
        if not records:
            sys.exit("no usable sequence found in the input")
    else:
        ap.error("give a FASTA file or use --demo")

    minimums = parse_minimums(args.minimums)
    print("Minimum repeats per period: "
          + ", ".join(f"{CLASS_NAME[p]}={minimums[p]}" for p in sorted(minimums)))
    if args.demo:
        print("INPUT: synthetic sequence with known inserted repeats - not a real organism.")
    print()

    all_hits: list[SSR] = []
    for seq_id, seq in records:
        hits = find_ssrs(seq_id, seq, minimums)
        all_hits.extend(hits)
        gc = sum(c in "GC" for c in seq) / len(seq) * 100
        print(f"{seq_id}  length={len(seq):,} bp  GC={gc:.1f}%  "
              f"SSRs={len(hits)}  density={len(hits) / (len(seq) / 1000):.2f}/kb")
        if not hits:
            print("  (no repeats met these thresholds)")
            continue
        print(f"  {'start':>7} {'end':>7} {'motif':<14} {'class':<6} "
              f"{'rep':>4} {'len':>5} {'L-flank':>8} {'R-flank':>8}  usable")
        for h in hits:
            ready = "yes" if (h.left_flank >= args.flank and h.right_flank >= args.flank) else "no"
            print(f"  {h.start:>7} {h.end:>7} {f'({h.motif}){h.repeats}':<14} "
                  f"{h.motif_class:<6} {h.repeats:>4} {h.length:>5} "
                  f"{h.left_flank:>8} {h.right_flank:>8}  {ready}")
        print()

    by_class: dict[str, int] = {}
    for h in all_hits:
        by_class[h.motif_class] = by_class.get(h.motif_class, 0) + 1
    if by_class:
        print("Motif class distribution: "
              + ", ".join(f"{k}={v}" for k, v in sorted(by_class.items())))
        usable = sum(1 for h in all_hits
                     if h.left_flank >= args.flank and h.right_flank >= args.flank)
        print(f"Primer-ready (>= {args.flank} bp both flanks): {usable} of {len(all_hits)}")

    if args.tsv:
        cols = list(asdict(all_hits[0]).keys()) if all_hits else [
            f.name for f in SSR.__dataclass_fields__.values()]  # type: ignore[attr-defined]
        with args.tsv.open("w", encoding="utf-8") as fh:
            fh.write("\t".join(cols) + "\n")
            for h in all_hits:
                row = asdict(h)
                fh.write("\t".join(str(row[c]) for c in cols) + "\n")
        print(f"\nTSV written to {args.tsv}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
