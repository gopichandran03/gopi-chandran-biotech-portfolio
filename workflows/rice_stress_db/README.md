# RiceStressDB - demonstration schema and query layer

The relational data model behind RiceStressDB, a database of stress-responsive
rice genes with functional annotations and biotic/abiotic stress metadata.

**Walkthrough with a live query console:**
[projects/ricestressdb/](../../projects/ricestressdb/index.html)

---

## Scope

This folder contains the **schema** and a **15-record sample extract**. It is
not the production database developed at TNAU, which holds 1,200+ gene records
across 17 stress conditions.

Every locus identifier, synonym and stress association in the sample is taken
from public curated resources — [funRiceGenes](https://funricegenes.github.io/),
[Oryzabase](https://shigen.nig.ac.jp/rice/oryzabase/), and the primary
literature they index — so the records are real and checkable rather than
invented. Sources are listed on the walkthrough's final slide.

The production database is registered as a software copyright with the
Government of India, associated with Tamil Nadu Agricultural University:
`SW-35001/2025-CO`. A copyright registration covers the software as an original
work of authorship; it is not a patent and not a claim of novelty over the
underlying biology.

## Run it

No database server and no dependencies required — the demo loads the MySQL
schema into in-memory SQLite:

```bash
python3 query_demo.py                   # all demonstration queries
python3 query_demo.py --search NAC      # synonym-tolerant lookup
python3 query_demo.py --search SNAC2    # ...finds OsNAC6, under its old name
python3 query_demo.py --stress Salinity # genes responding to one condition
python3 query_demo.py --cross           # abiotic + biotic responders
python3 query_demo.py --sqlite rice.db  # persist to a file
```

For MySQL or MariaDB:

```bash
mysql -u USER -p -e "CREATE DATABASE ricestressdb;"
mysql -u USER -p ricestressdb < schema.sql
mysql -u USER -p ricestressdb < seed_data.sql
```

## The data model

```
genes ──┬── gene_synonyms          (a gene has many historical names)
        └── gene_stress_response ──── stress_conditions
                                      (many-to-many, with direction
                                       and evidence on the relationship)
```

Four tables. The design decisions worth defending:

**The gene-stress relationship is its own table.** A flat sheet forces one row
per gene and crams the conditions into a comma-separated cell — at which point
"which genes respond to both salinity and blast?" stops being answerable.

**`direction` and `evidence` live on the relationship, not on the gene.**
"Responds to drought" is a property of the gene-stress *pair*. `OsLEA3` is
induced by drought and salt and explicitly **not** induced by cold; `OsP5CS1`
is induced by salt, dehydration and cold and explicitly **not** by heat. A
schema with one verdict per gene has nowhere to put those published negative
results — and negative results are exactly what stops someone repeating an
experiment that has already been done.

**Synonyms get their own table.** A gene can appear in the literature as
`OsNAC6`, `SNAC2`, `ONAC048`, `OsNAC2` or `OsSOG71`. A biologist who read a
2005 paper and one who read a 2016 paper should land on the same record.

**Two identifier systems are reconciled.** MSU (`LOC_Os...`) and RAP-DB
(`Os...g...`) are both in active use, and papers cite either.

## Files

| File | Contents |
|------|----------|
| `schema.sql` | Table definitions, constraints and indexes |
| `seed_data.sql` | 15-gene sample extract with 29 gene-stress records |
| `query_demo.py` | Loads both into SQLite and runs the demonstration queries |

## What I would change in a rebuild

- **Controlled vocabulary for stress terms** — map to Plant Ontology / PECO so
  "drought", "dehydration" and "water deficit" collapse properly instead of
  being three strings.
- **Full-text or trigram index** on synonyms. The current `LIKE '%term%'`
  cannot use a B-tree index because of the leading wildcard, so every synonym
  search scans the table. Invisible at this scale; not invisible at ten times it.
- **A JSON API**, so the data is programmatically reachable rather than only
  browsable.
- **Per-row provenance** — curator, date, confidence — so records can be
  re-reviewed.
- **Automated identifier validation** against MSU/RAP releases, to catch
  retired loci.

## Attribution

The data model, schema, query layer, web interface and curation work are mine.
Every gene-stress association originates in a published study by other
researchers. A curated database is a work of organisation, and its value
depends on citing what it organises.
