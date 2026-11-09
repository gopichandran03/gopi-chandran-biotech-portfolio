# Quality and process-monitoring demonstration

Statistical process control over **synthetic** measurements: Shewhart control
limits, run rules, and process capability indices.

**Walkthrough with a live interactive chart:**
[projects/process-monitoring/](../../projects/process-monitoring/index.html)

---

## What this is, and is not

**Is:** an educational demonstration of descriptive process monitoring. It
generates its own data, derives control limits from a baseline period, applies
four run rules, and computes Cp/Cpk against specification limits you supply.

**Is not:** a validated analytical method, a GMP release-control strategy,
software qualified for intended use, or anything that should inform a decision
about real material. No real laboratory or employer data appears here.

## Run it

```bash
python3 -m pip install -r ../../requirements.txt

# a stable process - expect no violations
python3 process_monitor.py

# a step shift of 1.5 baseline SD after the baseline period
python3 process_monitor.py --fault shift --size 1.5

# the point of run rules: a 1 SD shift is nearly invisible to rule 1 alone
python3 process_monitor.py --fault shift --size 1.0 --rules 1
python3 process_monitor.py --fault shift --size 1.0 --rules all

# capability against a specification, plus a chart
python3 process_monitor.py --fault drift --usl 54 --lsl 46 --plot chart.png
```

`--fault` accepts `none`, `shift`, `drift`, `spread` or `outlier`.
`--seed` makes any run reproducible.

## The rules implemented

| Rule | Pattern | Typically means |
|------|---------|-----------------|
| 1 | One point beyond 3 SD from the centre line | A gross excursion - bad sample, transcription error, large real event |
| 2 | Nine consecutive points on the same side of the centre line | The process mean has moved |
| 3 | Six consecutive points steadily increasing or decreasing | Drift - calibration, temperature, reagent degradation |
| 4 | Two of three consecutive points beyond 2 SD on the same side | An emerging shift, caught earlier than rule 1 |

A subset of the Nelson rules, which descend from the Western Electric handbook.
Clinical laboratories use the closely related Westgard rules for the same job.

Adding rules increases sensitivity to real change **and** increases false
alarms. The engineering decision is choosing a rule set proportionate to the
cost of each, and then holding to it.

## Control limits are not specification limits

The most common error in this area, so it is worth stating plainly:

- **Control limits** come from the process data (mean ± 3 SD of a stable
  baseline). They describe what the process *does*.
- **Specification limits** come from requirements. They describe what is
  *acceptable*.

A process can be wildly unstable and still inside spec, or perfectly stable
and entirely outside it. The script keeps them separate: control limits are
derived, specification limits are only used if you pass `--usl` and `--lsl`.

Capability indices assume a process already in control. The script says so when
it computes them on a process with rule violations, because `Cpk` on an
out-of-control process is a confident number describing nothing.

## Known limitations

- Assumes **independent** observations. Real in-process measurements are often
  autocorrelated, which inflates false alarms badly; an EWMA or time-series
  approach suits that case better.
- Assumes approximate **normality**. Many bioprocess measurements are skewed or
  bounded (counts, percentages, titres), where symmetric limits mislead.
- Assumes a genuinely **stable baseline**. If the baseline already contained a
  shift, the limits are inflated and will hide the next one.
- Charts **individual** measurements. With rational subgroups, X-bar/R or
  X-bar/S charts separate within- from between-subgroup variation.
- Monitors **one variable**. Real processes have many correlated parameters.

## Further reading

- Shewhart, *Economic Control of Quality of Manufactured Product* (1931)
- Nelson, "The Shewhart Control Chart - Tests for Special Causes," *Journal of
  Quality Technology* 16(4), 1984
- Westgard et al., "A multi-rule Shewhart chart for quality control in clinical
  chemistry," *Clinical Chemistry* 27(3), 1981
- Montgomery, *Introduction to Statistical Quality Control*
- ICH Q8-Q10 for the regulatory framing of in-process controls
