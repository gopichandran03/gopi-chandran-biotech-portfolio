-- RiceStressDB - sample seed data (15 genes)
--
-- SCOPE: this is a demonstration extract, NOT the production database
-- developed at TNAU. Every locus identifier, synonym and stress association
-- below is taken from public curated resources - funRiceGenes
-- (https://funricegenes.github.io/), Oryzabase, and the primary literature
-- they index - so the records are real and checkable rather than invented.
--
-- Load after schema.sql.

-- ---------------------------------------------------------------------------
INSERT INTO stress_conditions (stress_id, stress_name, category, description) VALUES
 (1, 'Salinity',        'abiotic', 'High soil or water salt concentration; ion toxicity and osmotic stress'),
 (2, 'Drought',         'abiotic', 'Water deficit; includes dehydration and PEG-simulated osmotic stress'),
 (3, 'Cold',            'abiotic', 'Low temperature and chilling stress'),
 (4, 'Heat',            'abiotic', 'High temperature stress'),
 (5, 'Submergence',     'abiotic', 'Flooding and complete or partial submergence'),
 (6, 'Oxidative stress','abiotic', 'Reactive oxygen species accumulation'),
 (7, 'Blast disease',   'biotic',  'Infection by the fungal pathogen Magnaporthe oryzae'),
 (8, 'Wounding',        'biotic',  'Mechanical wounding and herbivory-associated damage');

-- ---------------------------------------------------------------------------
INSERT INTO genes (gene_id, msu_locus, rap_locus, primary_symbol, gene_family, chromosome, description) VALUES
 (1,  'LOC_Os01g20160', NULL,             'OsHKT1;5',  'HKT transporter',        1,  'Na+-selective transporter mediating Na+ exclusion and K+/Na+ homeostasis under salt stress; corresponds to the SKC1 salt-tolerance QTL'),
 (2,  'LOC_Os12g44360', 'Os12g0641100',   'OsSOS1',    'Na+/H+ antiporter',      12, 'Plasma-membrane Na+/H+ exchanger; upregulated in shoots and roots under salt stress but not induced by drought'),
 (3,  'LOC_Os09g35030', 'Os09g0522200',   'OsDREB1A',  'AP2/ERF (DREB)',         9,  'DRE-binding transcription factor; expression induced by cold'),
 (4,  'LOC_Os03g60080', NULL,             'SNAC1',     'NAC',                    3,  'Stress-responsive NAC transcription factor; overexpression raised seed setting 22-34% under severe reproductive-stage drought in the field with no yield penalty'),
 (5,  'LOC_Os01g66120', 'Os01g0884300',   'OsNAC6',    'NAC',                    1,  'Induced by cold, drought, salinity and ABA, and also by wounding and blast disease - integrates abiotic and biotic stress signals'),
 (6,  'LOC_Os11g08210', NULL,             'OsNAC5',    'NAC',                    11, 'Abiotic stress-responsive NAC; overexpression improved high-salinity tolerance; salt induction abolished by an inhibitor of ABA effects'),
 (7,  'LOC_Os01g09550', NULL,             'SNAC3',     'NAC',                    1,  'Positive regulator of drought and oxidative stress response; significantly activated by rice blast infection'),
 (8,  'LOC_Os05g46480', 'Os05g0542500',   'OsLEA3',    'LEA group 3',            5,  'Group 3 late-embryogenesis-abundant protein; induced by drought, salt and ABA but not by cold; overexpression raised relative yield under field drought'),
 (9,  'LOC_Os05g38150', 'Os05g0455500',   'OsP5CS1',   'P5C synthetase',         5,  'Proline biosynthesis enzyme; induced by high salt, dehydration, ABA and cold, but not by heat treatment'),
 (10, 'LOC_Os07g05940', NULL,             'OsNCED4',   'NCED (ABA biosynthesis)',7,  '9-cis-epoxycarotenoid dioxygenase in ABA biosynthesis; regulated downstream of stress-responsive MYB and DUF966 factors'),
 (11, 'LOC_Os09g11480', 'Os09g0287000',   'Sub1B',     'AP2/ERF',                9,  'One of three ERF genes at the Sub1 locus (Sub1A, Sub1B, Sub1C); Sub1A was identified as the major determinant of submergence tolerance'),
 (12, 'LOC_Os03g20790', NULL,             'OsEIL1',    'EIN3-like',              3,  'Ethylene-insensitive-3-like transcription factor associated with submergence stress response'),
 (13, 'LOC_Os01g64970', NULL,             'OsSAPK4',   'SnRK2 kinase',           1,  'Stress/ABA-activated protein kinase associated with salt stress response'),
 (14, 'LOC_Os11g06720', NULL,             'OsASR5',    'ASR',                    11, 'Abscisic acid stress and ripening protein 5; associated with drought stress response'),
 (15, 'LOC_Os06g41010', NULL,             'OsiSAP8',   'Zinc-finger (SAP)',      6,  'Stress-associated protein 8; associated with cold stress response');

-- ---------------------------------------------------------------------------
INSERT INTO gene_synonyms (synonym_id, gene_id, synonym, source) VALUES
 (1,  1, 'SKC1',      'funRiceGenes'),
 (2,  1, 'OsHKT8',    'funRiceGenes'),
 (3,  1, 'OsHK1;5',   'funRiceGenes'),
 (4,  2, 'OsNHA1',    'funRiceGenes'),
 (5,  3, 'OsCBF3',    'Oryzabase'),
 (6,  3, 'OsDREBL',   'Oryzabase'),
 (7,  3, 'OsERF024',  'Oryzabase'),
 (8,  3, 'DREB1A',    'Oryzabase (CGSNL)'),
 (9,  4, 'OsNAC19',   'funRiceGenes'),
 (10, 4, 'OsNAC9',    'funRiceGenes'),
 (11, 5, 'SNAC2',     'funRiceGenes'),
 (12, 5, 'ONAC048',   'Oryzabase'),
 (13, 5, 'OsNAC2',    'Oryzabase'),
 (14, 5, 'OsSOG71',   'Oryzabase'),
 (15, 7, 'ONAC066',   'funRiceGenes'),
 (16, 7, 'OsNAC006',  'funRiceGenes'),
 (17, 8, 'OsLEA3-1',  'funRiceGenes'),
 (18, 9, 'OsP5CS',    'funRiceGenes');

-- ---------------------------------------------------------------------------
-- The junction table. Note gene 5 (OsNAC6) and gene 7 (SNAC3), which carry
-- both abiotic and biotic associations - the cross-stress case the schema
-- exists to make queryable.
INSERT INTO gene_stress_response (response_id, gene_id, stress_id, direction, evidence, notes) VALUES
 (1,  1,  1, 'induced',   'qtl',        'SKC1 salt-tolerance QTL corresponds to this gene'),
 (2,  2,  1, 'induced',   'expression', 'Upregulated in shoots and roots under salt; not induced by drought'),
 (3,  3,  3, 'induced',   'expression', 'Cold induction reported'),
 (4,  3,  2, 'induced',   'transgenic', 'Drought-inducible promoter activation reported'),
 (5,  4,  2, 'induced',   'transgenic', 'Field drought at reproductive stage; 22-34% higher seed setting'),
 (6,  4,  1, 'induced',   'expression', NULL),
 (7,  5,  3, 'induced',   'expression', NULL),
 (8,  5,  2, 'induced',   'transgenic', 'Root-specific overexpression improved grain yield under multiyear field drought'),
 (9,  5,  1, 'induced',   'expression', NULL),
 (10, 5,  7, 'induced',   'expression', 'Induced by blast disease'),
 (11, 5,  8, 'induced',   'expression', 'Induced by wounding and by jasmonic acid'),
 (12, 6,  1, 'induced',   'transgenic', 'Overexpression improved high-salinity tolerance'),
 (13, 7,  2, 'induced',   'transgenic', 'Positive regulator of drought response'),
 (14, 7,  6, 'induced',   'expression', 'Positive regulator of oxidative stress response'),
 (15, 7,  7, 'induced',   'expression', 'Significantly activated by rice blast infection'),
 (16, 8,  2, 'induced',   'transgenic', 'Higher relative yield under field drought'),
 (17, 8,  1, 'induced',   'expression', NULL),
 (18, 8,  3, 'unchanged', 'expression', 'Explicitly reported as NOT induced by cold'),
 (19, 9,  1, 'induced',   'expression', NULL),
 (20, 9,  2, 'induced',   'expression', 'Induced by dehydration'),
 (21, 9,  3, 'induced',   'expression', NULL),
 (22, 9,  4, 'unchanged', 'expression', 'Explicitly reported as NOT induced by heat treatment'),
 (23, 10, 2, 'induced',   'expression', NULL),
 (24, 10, 1, 'induced',   'expression', NULL),
 (25, 11, 5, 'induced',   'qtl',        'Sub1 locus; Sub1A is the major determinant'),
 (26, 12, 5, 'induced',   'expression', NULL),
 (27, 13, 1, 'induced',   'transgenic', NULL),
 (28, 14, 2, 'induced',   'transgenic', NULL),
 (29, 15, 3, 'induced',   'transgenic', NULL);
