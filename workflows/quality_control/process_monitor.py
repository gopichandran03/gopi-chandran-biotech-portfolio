#!/usr/bin/env python3
"""Descriptive statistical process monitoring over synthetic measurements.

WHAT THIS IS
    An educational demonstration of Shewhart control charts, run rules and
    process capability indices. It generates its own synthetic data.

WHAT THIS IS NOT
    A validated analytical method. A GMP release-control strategy. Software
    qualified for intended use. Anything that should inform a decision about
    real material. See README.md in this folder.

Usage
    python3 process_monitor.py                         # stable process
    python3 process_monitor.py --fault shift --size 1.5
    python3 process_monitor.py --fault drift --usl 54 --lsl 46
    python3 process_monitor.py --fault shift --plot chart.png
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

try:
    import numpy as np
except ImportError:  # pragma: no cover - dependency guidance
    sys.exit("numpy is required: python3 -m pip install -r requirements.txt")

FAULTS = ("none", "shift", "drift", "spread", "outlier")


@dataclass
class Baseline:
    """Control limits derived from a baseline period of a stable process."""

    mean: float
    sd: float
    n: int

    @property
    def ucl(self) -> float:
        return self.mean + 3 * self.sd

    @property
    def lcl(self) -> float:
        return self.mean - 3 * self.sd


def generate(n: int, baseline_n: int, target: float, noise: float,
             fault: str, size: float, seed: int) -> np.ndarray:
    """Generate synthetic measurements with an optional fault after baseline."""
    rng = np.random.default_rng(seed)
    values = rng.normal(target, noise, n)
    if fault == "none":
        return values
    post = np.arange(n - baseline_n)
    if fault == "shift":
        values[baseline_n:] += size * noise
    elif fault == "drift":
        values[baseline_n:] += size * noise * (post / max(1, len(post) - 1))
    elif fault == "spread":
        values[baseline_n:] += rng.normal(0, noise * size, len(post))
    elif fault == "outlier":
        idx = baseline_n + min(10, len(post) - 1)
        values[idx] += size * noise * 3
    return values


def fit_baseline(values: np.ndarray, baseline_n: int) -> Baseline:
    head = values[:baseline_n]
    return Baseline(mean=float(head.mean()), sd=float(head.std(ddof=1)), n=baseline_n)


def apply_rules(values: np.ndarray, base: Baseline, use_all: bool) -> dict[int, list[int]]:
    """Return {index: [rule numbers triggered]}.

    Rule 1  one point beyond 3 SD
    Rule 2  nine consecutive points on the same side of the centre line
    Rule 3  six consecutive points steadily increasing or decreasing
    Rule 4  two of three consecutive points beyond 2 SD on the same side
    """
    flags: dict[int, list[int]] = {}

    def add(i: int, rule: int) -> None:
        flags.setdefault(i, []).append(rule)

    for i, v in enumerate(values):
        if abs(v - base.mean) > 3 * base.sd:
            add(i, 1)

    if not use_all:
        return flags

    side = np.sign(values - base.mean)
    run = 0
    for i in range(len(values)):
        run = run + 1 if i > 0 and side[i] == side[i - 1] and side[i] != 0 else 1
        if run >= 9:
            add(i, 2)

    for i in range(5, len(values)):
        window = values[i - 5:i + 1]
        diffs = np.diff(window)
        if np.all(diffs > 0) or np.all(diffs < 0):
            add(i, 3)

    for i in range(2, len(values)):
        window = values[i - 2:i + 1]
        hi = np.sum(window - base.mean > 2 * base.sd)
        lo = np.sum(base.mean - window > 2 * base.sd)
        if hi >= 2 or lo >= 2:
            add(i, 4)

    return flags


def capability(values: np.ndarray, usl: float | None, lsl: float | None) -> dict | None:
    """Cp and Cpk. Only meaningful for a process that is already in control."""
    if usl is None or lsl is None:
        return None
    mean = float(values.mean())
    sd = float(values.std(ddof=1))
    if sd == 0:
        return None
    return {
        "mean": mean,
        "sd": sd,
        "cp": (usl - lsl) / (6 * sd),
        "cpk": min(usl - mean, mean - lsl) / (3 * sd),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=60, help="total observations (default 60)")
    ap.add_argument("--baseline", type=int, default=25, help="baseline observations (default 25)")
    ap.add_argument("--target", type=float, default=50.0)
    ap.add_argument("--noise", type=float, default=1.0, help="process SD")
    ap.add_argument("--fault", choices=FAULTS, default="none")
    ap.add_argument("--size", type=float, default=1.5, help="fault size in baseline SDs")
    ap.add_argument("--rules", choices=("1", "all"), default="all")
    ap.add_argument("--usl", type=float, default=None, help="upper specification limit")
    ap.add_argument("--lsl", type=float, default=None, help="lower specification limit")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--plot", metavar="PNG", default=None, help="write a chart to this path")
    args = ap.parse_args()

    if args.baseline >= args.n:
        sys.exit("--baseline must be smaller than --n")

    values = generate(args.n, args.baseline, args.target, args.noise,
                      args.fault, args.size, args.seed)
    base = fit_baseline(values, args.baseline)
    flags = apply_rules(values, base, args.rules == "all")

    print("=" * 68)
    print("SYNTHETIC DATA - educational demonstration, not a validated method")
    print("=" * 68)
    print(f"Observations      : {args.n} (baseline {args.baseline})")
    print(f"Fault injected    : {args.fault}"
          + (f" ({args.size} x baseline SD)" if args.fault != "none" else ""))
    print(f"Rule set          : {'1 only' if args.rules == '1' else 'rules 1-4'}")
    print()
    print("BASELINE STATISTICS")
    print(f"  mean (CL)       : {base.mean:.4f}")
    print(f"  sd              : {base.sd:.4f}")
    print(f"  UCL (+3 SD)     : {base.ucl:.4f}")
    print(f"  LCL (-3 SD)     : {base.lcl:.4f}")
    print()

    if flags:
        print(f"RULE VIOLATIONS ({len(flags)} points flagged)")
        print(f"  {'point':>6}  {'value':>9}  rules")
        for i in sorted(flags):
            rules = ", ".join(f"R{r}" for r in flags[i])
            marker = " *" if i >= args.baseline else ""
            print(f"  {i + 1:>6}  {values[i]:>9.3f}  {rules}{marker}")
        post = [i for i in flags if i >= args.baseline]
        if args.fault != "none":
            if post:
                print(f"\n  First detection after fault onset: "
                      f"{min(post) - args.baseline + 1} points")
            else:
                print("\n  Fault NOT detected by this rule set.")
    else:
        print("RULE VIOLATIONS: none - process appears in control")

    cap = capability(values[args.baseline:], args.usl, args.lsl)
    if cap:
        print()
        print("PROCESS CAPABILITY (post-baseline window)")
        print(f"  spec            : [{args.lsl}, {args.usl}]")
        print(f"  Cp              : {cap['cp']:.3f}")
        print(f"  Cpk             : {cap['cpk']:.3f}")
        if flags:
            print("  NOTE: capability indices assume a process in control. This process")
            print("        has rule violations, so these numbers describe nothing stable.")
        elif cap["cpk"] < cap["cp"] * 0.9:
            print("  NOTE: Cpk well below Cp - the process is off-centre rather than")
            print("        too variable. Re-centre the aim; do not chase variability.")

    if args.plot:
        write_plot(values, base, flags, args)
        print(f"\nChart written to {args.plot}")

    return 0


def write_plot(values, base, flags, args) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        sys.exit("matplotlib is required for --plot")

    # Series colours from the portfolio's validated categorical palette.
    series_1, series_2 = "#2a78d6", "#eb6834"
    x = np.arange(1, len(values) + 1)
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=140)
    ax.axvspan(1, args.baseline, color="#cde2fb", alpha=0.45, lw=0,
               label="baseline (sets limits)")
    ax.plot(x, values, color=series_1, lw=1.6, alpha=0.75, zorder=2)
    ax.scatter(x, values, s=18, color=series_1, zorder=3)
    if flags:
        fx = [i + 1 for i in sorted(flags)]
        fy = [values[i] for i in sorted(flags)]
        ax.scatter(fx, fy, s=58, color=series_2, zorder=4,
                   edgecolor="white", linewidth=1.4, label="flagged by a run rule")
    for y, label, style in ((base.ucl, "UCL +3 SD", "--"),
                            (base.mean, "CL", "-"),
                            (base.lcl, "LCL -3 SD", "--")):
        ax.axhline(y, color="#8c9a92", lw=1.2, ls=style, zorder=1)
        ax.annotate(label, xy=(len(values), y), xytext=(4, 0),
                    textcoords="offset points", va="center",
                    fontsize=8, color="#52616a")
    ax.set_xlabel("Observation (time order)", fontsize=9, color="#52616a")
    ax.set_ylabel("Value", fontsize=9, color="#52616a")
    ax.set_title(f"Synthetic process data - fault: {args.fault}", fontsize=11)
    ax.margins(x=0.02)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower left", fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(args.plot)
    plt.close(fig)


if __name__ == "__main__":
    sys.exit(main())
