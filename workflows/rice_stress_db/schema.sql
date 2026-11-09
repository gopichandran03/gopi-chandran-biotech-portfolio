-- RiceStressDB - demonstration schema
--
-- This is the relational model for a stress-responsive rice gene database:
-- genes, the stress conditions they respond to, the many-to-many relationship
-- between them, and the synonyms that make a gene findable under any of its
-- historical names.
--
-- This file is the SCHEMA ONLY, with a small sample of seed data in
-- seed_data.sql. It is not the production database developed at TNAU.
--
-- Written for MySQL 8 / MariaDB 10.5+. It also loads in SQLite with the ENUM
-- columns treated as TEXT, which is how query_demo.py runs it with no server.

DROP TABLE IF EXISTS gene_stress_response;
DROP TABLE IF EXISTS gene_synonyms;
DROP TABLE IF EXISTS stress_conditions;
DROP TABLE IF EXISTS genes;

-- ---------------------------------------------------------------------------
-- genes: one row per gene, keyed on the MSU locus identifier.
-- ---------------------------------------------------------------------------
CREATE TABLE genes (
    gene_id         INTEGER      PRIMARY KEY,
    msu_locus       VARCHAR(32)  NOT NULL UNIQUE,   -- e.g. LOC_Os01g20160
    rap_locus       VARCHAR(32),                    -- e.g. Os01g0884300
    primary_symbol  VARCHAR(64)  NOT NULL,
    gene_family     VARCHAR(96),
    chromosome      SMALLINT,
    description     TEXT
);

CREATE INDEX idx_genes_symbol ON genes (primary_symbol);
CREATE INDEX idx_genes_rap    ON genes (rap_locus);
CREATE INDEX idx_genes_family ON genes (gene_family);

-- ---------------------------------------------------------------------------
-- stress_conditions: the controlled list of conditions.
-- Keeping this as a table rather than a free-text column is what makes
-- "all biotic stresses" a query instead of a string match.
-- ---------------------------------------------------------------------------
CREATE TABLE stress_conditions (
    stress_id    INTEGER     PRIMARY KEY,
    stress_name  VARCHAR(64) NOT NULL UNIQUE,
    category     VARCHAR(16) NOT NULL,              -- 'abiotic' | 'biotic'
    description  TEXT,
    CHECK (category IN ('abiotic', 'biotic'))
);

-- ---------------------------------------------------------------------------
-- gene_synonyms: a gene has unboundedly many historical names.
-- This is the table that lets a search for SNAC2 and a search for OsNAC6
-- land on the same record.
-- ---------------------------------------------------------------------------
CREATE TABLE gene_synonyms (
    synonym_id  INTEGER     PRIMARY KEY,
    gene_id     INTEGER     NOT NULL,
    synonym     VARCHAR(64) NOT NULL,
    source      VARCHAR(64),
    FOREIGN KEY (gene_id) REFERENCES genes (gene_id) ON DELETE CASCADE
);

CREATE INDEX idx_syn_gene    ON gene_synonyms (gene_id);
CREATE INDEX idx_syn_synonym ON gene_synonyms (synonym);

-- ---------------------------------------------------------------------------
-- gene_stress_response: the junction table, and the heart of the model.
--
-- direction and evidence live HERE and not on `genes`, because "responds to
-- drought" is a property of the gene-stress PAIR. A gene can be induced by one
-- stress and unchanged under another; putting a single verdict on the gene row
-- would silently destroy exactly those cases.
-- ---------------------------------------------------------------------------
CREATE TABLE gene_stress_response (
    response_id     INTEGER     PRIMARY KEY,
    gene_id         INTEGER     NOT NULL,
    stress_id       INTEGER     NOT NULL,
    direction       VARCHAR(16) NOT NULL,   -- induced|repressed|both|unchanged
    evidence        VARCHAR(16) NOT NULL,   -- expression|transgenic|qtl|mutant
    reference_pmid  VARCHAR(16),
    notes           TEXT,
    UNIQUE (gene_id, stress_id),
    FOREIGN KEY (gene_id)   REFERENCES genes (gene_id)             ON DELETE CASCADE,
    FOREIGN KEY (stress_id) REFERENCES stress_conditions (stress_id) ON DELETE RESTRICT,
    CHECK (direction IN ('induced', 'repressed', 'both', 'unchanged')),
    CHECK (evidence  IN ('expression', 'transgenic', 'qtl', 'mutant'))
);

CREATE INDEX idx_resp_gene   ON gene_stress_response (gene_id);
CREATE INDEX idx_resp_stress ON gene_stress_response (stress_id);
CREATE INDEX idx_resp_dir    ON gene_stress_response (direction);
