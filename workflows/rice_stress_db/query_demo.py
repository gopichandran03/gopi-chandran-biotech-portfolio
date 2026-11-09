#!/usr/bin/env python3
"""Load the RiceStressDB demonstration schema into SQLite and run the queries.

The schema and seed data are written for MySQL but use no MySQL-only syntax,
so they load straight into an in-memory SQLite database. That means this demo
runs with nothing installed and no database server - useful for reviewing the
data model, which is the part worth reviewing.

Usage
    python3 query_demo.py                       # run all demonstration queries
    python3 query_demo.py --search NAC          # synonym-tolerant gene lookup
    python3 query_demo.py --stress Salinity     # genes responding to a condition
    python3 query_demo.py --cross               # abiotic + biotic responders
    python3 query_demo.py --sqlite ricestress.db   # persist instead of in-memory
"""
from __future__ import annotations

import argparse
import pathlib
import sqlite3
import sys
import textwrap

HERE = pathlib.Path(__file__).resolve().parent


def build(conn: sqlite3.Connection) -> None:
    conn.executescript((HERE / "schema.sql").read_text(encoding="utf-8"))
    conn.executescript((HERE / "seed_data.sql").read_text(encoding="utf-8"))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.commit()


def show(conn: sqlite3.Connection, title: str, sql: str, params: tuple = ()) -> None:
    print("=" * 78)
    print(title)
    print("=" * 78)
    print(textwrap.indent(sql.strip(), "    "))
    print()
    cur = conn.execute(sql, params)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    if not rows:
        print("    (no rows)\n")
        return
    widths = [max(len(c), max(len(str(r[i])) for r in rows)) for i, c in enumerate(cols)]
    widths = [min(w, 46) for w in widths]
    header = "  ".join(c[:w].ljust(w) for c, w in zip(cols, widths))
    print("    " + header)
    print("    " + "  ".join("-" * w for w in widths))
    for r in rows:
        print("    " + "  ".join(str(v)[:w].ljust(w) for v, w in zip(r, widths)))
    print(f"\n    {len(rows)} row(s)\n")


Q_CROSS = """
SELECT g.primary_symbol, g.msu_locus, g.gene_family,
       COUNT(DISTINCT CASE WHEN s.category='abiotic' THEN s.stress_id END) AS abiotic_n,
       COUNT(DISTINCT CASE WHEN s.category='biotic'  THEN s.stress_id END) AS biotic_n
FROM genes g
JOIN gene_stress_response r ON r.gene_id   = g.gene_id
JOIN stress_conditions    s ON s.stress_id = r.stress_id
GROUP BY g.gene_id
HAVING abiotic_n > 0 AND biotic_n > 0
ORDER BY (abiotic_n + biotic_n) DESC
"""

Q_SEARCH = """
SELECT DISTINCT g.primary_symbol, g.msu_locus, g.rap_locus, g.gene_family,
       g.chromosome
FROM genes g
LEFT JOIN gene_synonyms y ON y.gene_id = g.gene_id
WHERE g.primary_symbol LIKE '%' || ? || '%'
   OR g.msu_locus      LIKE '%' || ? || '%'
   OR IFNULL(g.rap_locus,'') LIKE '%' || ? || '%'
   OR IFNULL(y.synonym,'')   LIKE '%' || ? || '%'
ORDER BY g.primary_symbol
"""

Q_CONDITIONS = """
SELECT s.stress_name, s.category,
       COUNT(DISTINCT r.gene_id) AS genes,
       SUM(CASE WHEN r.evidence='transgenic' THEN 1 ELSE 0 END) AS transgenic_evidence
FROM stress_conditions s
LEFT JOIN gene_stress_response r ON r.stress_id = s.stress_id
GROUP BY s.stress_id
ORDER BY genes DESC, s.stress_name
"""

Q_BY_STRESS = """
SELECT g.primary_symbol, g.msu_locus, g.gene_family,
       r.direction, r.evidence, IFNULL(r.notes,'') AS notes
FROM genes g
JOIN gene_stress_response r ON r.gene_id   = g.gene_id
JOIN stress_conditions    s ON s.stress_id = r.stress_id
WHERE s.stress_name = ?
ORDER BY r.evidence, g.primary_symbol
"""

Q_NEGATIVE = """
SELECT g.primary_symbol, s.stress_name, r.direction, IFNULL(r.notes,'') AS notes
FROM genes g
JOIN gene_stress_response r ON r.gene_id   = g.gene_id
JOIN stress_conditions    s ON s.stress_id = r.stress_id
WHERE r.direction = 'unchanged'
ORDER BY g.primary_symbol
"""

Q_SYNONYMS = """
SELECT g.primary_symbol, COUNT(y.synonym_id) AS synonyms,
       IFNULL(GROUP_CONCAT(y.synonym, ', '), '') AS also_known_as
FROM genes g
LEFT JOIN gene_synonyms y ON y.gene_id = g.gene_id
GROUP BY g.gene_id
HAVING synonyms > 0
ORDER BY synonyms DESC
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--search", metavar="TERM", help="synonym-tolerant gene lookup")
    ap.add_argument("--stress", metavar="NAME", help="genes responding to this condition")
    ap.add_argument("--cross", action="store_true",
                    help="only the abiotic + biotic cross-stress query")
    ap.add_argument("--sqlite", type=pathlib.Path, default=None,
                    help="write to this SQLite file instead of memory")
    args = ap.parse_args()

    target = str(args.sqlite) if args.sqlite else ":memory:"
    if args.sqlite and args.sqlite.exists():
        args.sqlite.unlink()
    conn = sqlite3.connect(target)
    try:
        build(conn)
    except sqlite3.Error as exc:
        sys.exit(f"failed to build the demo database: {exc}")

    n_genes = conn.execute("SELECT COUNT(*) FROM genes").fetchone()[0]
    n_resp = conn.execute("SELECT COUNT(*) FROM gene_stress_response").fetchone()[0]
    print(f"RiceStressDB demonstration extract: {n_genes} genes, {n_resp} "
          f"gene-stress records.")
    print("This is a sample for demonstrating the data model - not the "
          "production database.\n")

    if args.search:
        t = args.search
        show(conn, f"Synonym-tolerant lookup for {t!r}", Q_SEARCH, (t, t, t, t))
    elif args.stress:
        show(conn, f"Genes responding to {args.stress!r}", Q_BY_STRESS, (args.stress,))
    elif args.cross:
        show(conn, "Genes responding to BOTH abiotic and biotic stress", Q_CROSS)
    else:
        show(conn, "1. Genes responding to BOTH abiotic and biotic stress", Q_CROSS)
        show(conn, "2. Conditions ranked by how well characterised they are", Q_CONDITIONS)
        show(conn, "3. Synonym-tolerant lookup: every gene matching 'NAC'",
             Q_SEARCH, ("NAC",) * 4)
        show(conn, "4. Explicit negative results (direction = 'unchanged')", Q_NEGATIVE)
        show(conn, "5. Genes carrying the most synonyms", Q_SYNONYMS)
        print("Query 4 is the one that justifies putting `direction` on the")
        print("relationship rather than on the gene: 'OsLEA3 is NOT induced by cold'")
        print("is a real published finding, and a schema with one verdict per gene")
        print("has nowhere to record it.\n")

    if args.sqlite:
        conn.commit()
        print(f"Database written to {args.sqlite}")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
