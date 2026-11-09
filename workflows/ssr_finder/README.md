# SSR (microsatellite) finder

Detects perfect tandem repeats in DNA sequences — the first step of
microsatellite marker development.

**Walkthrough with a browser version of this tool:**
[projects/dalbergia-genomics/](../../projects/dalbergia-genomics/index.html)

---

## What it does

Scans a sequence for perfect tandem repeats of motif length 1–6 that meet a
minimum repeat count, and reports each hit with its position, motif, repeat
number, normalised motif and available flanking sequence.

This runs on **real FASTA input** — point it at any sequence you have. The
`--demo` mode generates a synthetic sequence with known repeats inserted so the
detector can be checked against a known answer; that sequence is not from any
organism.

## Run it

```bash
python3 find_ssrs.py --demo                        # synthetic check sequence
python3 find_ssrs.py sequence.fasta
python3 find_ssrs.py sequence.fasta --min 1:12,2:6,3:5,4:5,5:4,6:4
python3 find_ssrs.py sequence.fasta --flank 100 --tsv ssrs.tsv
```

No dependencies — standard library only.

## The algorithm

The standard approach used by tools in the MISA family:

1. Scan for each period *p* from 6 down to 1. **Longest first** matters: a
   `(AGGT)n` run scanned as di-nucleotides first would be consumed as
   overlapping junk.
2. Reject motifs that are themselves repeats of a shorter unit — `ATAT` is a
   di-nucleotide `(AT)2`, not a tetra-nucleotide.
3. Accept runs meeting the minimum repeat count for that period.
4. Mark accepted spans as covered, so reported hits never overlap.
5. Normalise each motif to its lexicographically smallest rotation, so `(AG)n`
   and `(GA)n` group into one motif class.

## Thresholds are not a detail

Default minimum repeats: mono 12, di 6, tri 5, tetra 5, penta 4, hexa 4.

Lower the di-nucleotide threshold from 6 to 3 and the count explodes. The
thresholds *decide what counts as a microsatellite* — which is why an SSR count
quoted without them is uninterpretable, and why tools in this family require
them to be declared up front.

Mononucleotide repeats are frequently excluded from marker panels entirely,
because they are hard to genotype reliably (polymerase slippage makes allele
calling noisy). Set `--min 1:999` to drop them.

## From repeat to usable marker

Detection is the easy step. The `usable` column applies the first real filter:
primer design needs roughly 100 bp of unique sequence on each side, so repeats
near a contig end are detected but not usable.

What follows, outside this script:

1. Design primers in the flanks (Primer3), with Tm and GC constraints
2. Check primer specificity against the genome; discard multi-locus hits
3. Wet-lab validation — does it amplify, consistently, across individuals?
4. Polymorphism screening on a diversity panel

**Attrition is severe and normal.** Most detected repeats never become markers:
flanking sequence is repetitive, primers amplify multiple loci, amplification
fails, or — most often — the locus turns out monomorphic in the populations of
interest. A marker that does not vary tells you nothing. Report "n loci
screened, m polymorphic", not the number the scan found.

## Limitations

- **Perfect repeats only.** Imperfect and compound SSRs (interrupted repeats,
  adjacent different motifs) are common in real genomes and are not detected.
  MISA handles compound repeats within a distance threshold; this does not.
- **No primer design** — use Primer3 on the flanks.
- **Memory-resident.** Fine for contigs and small genomes; a whole large genome
  wants streaming.
- **No masking.** Running on unmasked sequence will return repeats inside
  transposable elements, which make poor markers.

## Context

Written for the *Dalbergia latifolia* (Indian rosewood) marker-discovery
walkthrough. The species is assessed as globally Vulnerable on the IUCN Red
List and listed on CITES Appendix II, which creates a legal need to tell legal
material from illegal — and that need is answered with genetics or not at all.
