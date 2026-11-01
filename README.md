# Translation-table replay: AD, PD and PDAC

Offline, standard-library Python code for bounded reconstructions of three published processed workbooks. The new code is released under the MIT license with the responsible author's authorization. Original publications and source data retain their own licenses; no workbooks, full source matrices, private records or credentials are included.

Associated manuscripts remain subject to author factual declarations and journal-specific finalization. This repository is not evidence of submission, acceptance, human peer review, independent biological replication or re-fitting the original statistical models.

## Run

Python 3.10 or later. Obtain the original workbook separately and use its exact bytes; resaving it changes its SHA-256 and is deliberately rejected. Output directories must not already exist.

```
python -I -S -B extensions.py --study ad --input /external/41398_2020_882_MOESM3_ESM.xlsx --output ./ad_output
python -I -S -B extensions.py --study pd --input /external/figure1_2.xls --output ./pd_output
python -I -S -B extensions.py --study pdac --input /external/Supplementary_Table_S1.xlsx --output ./pdac_output
```

The /external paths are illustrative, not distributed files. SHA validation, archive/XML safety checks and exact core membership/row-anchor checks precede extension computation and output creation. Runtime makes no internet requests. extensions.json contains recomputed extensions; core_membership.csv is generated from the externally supplied source. Do not redistribute source-like exports without checking source rights.

## Sources

- AD: Ghosh et al., Translational Psychiatry (2020), https://doi.org/10.1038/s41398-020-00882-7 — Supplementary Table 2.
- PD: Kim et al., eNeuro (2021), https://www.eneuro.org/content/8/6/ENEURO.0310-21.2021 — Extended Data Figure 1-2. The .xls file is actually OOXML. Preserve its original 1904 date epoch and date-formatted corrupted symbols; this software does not infer repairs.
- PDAC: Nguyen et al., Cancers (2023), https://doi.org/10.3390/cancers15051444 — Supplementary Table S1.

Input hashes and headers are in expectations.json. Caption SDs and reported structure counts are explicitly source-transcribed constants, not workbook discoveries. Scope and exact coverage are detailed in coverage.md. References contain aggregate results, sparse collision/boundary examples and identity digests, not full source gene tables.

## Isolated verification

```
python -I -S -B build_test.py --build --ad /external/AD.xlsx --pd /external/figure1_2.xls --pdac /external/Supplementary_Table_S1.xlsx --work ./verification
```

The test builds an allowlisted ZIP, cold-extracts it, runs all three actual external workbooks with isolated Python, and compares extensions against frozen reference outputs. It also rejects wrong-input hashes, corrupted core expectations and identity-digest mutations before treating outputs as valid. Explicit artificial numerical fixtures test ties, linear quartiles, correlations and Decimal boundaries; they are not empirical research data.

Exact identifiers, integers, row anchors and identity digests are compared exactly. Floating summaries allow relative/absolute 1e-12, with 1e-14 absolute tolerance for boundary distances. Decimal cell-string comparisons allow relative 2e-15 / absolute 1e-25 for the development parser's float-to-string conversion; threshold membership itself uses original XML decimal strings. The core retains its original absolute TE/z tolerance below 1e-10. Reference capture used existing reviewed outputs and a development-only openpyxl parser; portable runtime and tests use only the standard library.

Local parent verification of the preceding author-review bundle passed 13 test groups, 1975 reference leaves and 26 source hashes. The release bundle must have its own generated hash and test report because its README/license changed. These are same-host software checks, not external human interpretation or cross-platform empirical validation. No remote CI result is claimed here.

## Boundaries

The PD frozen population-SD primary remains GS688, while source/sample-SD GS is687; Eif2b3 is the explicit boundary member. GS/GSDA caption-SD and structure-universe correspondence remain unresolved. PDAC results are conditional on a preselected1815-row table. AD name-based reconstruction is not proof of original feature-ID membership or author error. No disease mechanism, therapeutic efficacy or full sequencing-pipeline reproduction is claimed.

AI tools contributed substantially to implementation and analysis; actual Claude Code provided read-only critique and Hermes adjudicated findings and reran computations. AI critique is not accountable human peer review. Separate manuscript licensing, author declarations and any journal submission are documented outside this software release.
