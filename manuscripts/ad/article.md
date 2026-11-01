# [Re] When a gene name is not a row: a source-bound reconstruction of ribosome-enriched RNA results in an Alzheimer-related neuronal model

## Abstract

**Background:** Reproducibility of gene-set summaries depends on the measurement, contrast and identifier unit, not simply matching totals. **Methods:** We recovered the publisher-hosted Supplementary Table 2 for an Alzheimer-related neuronal study (DOI: 10.1038/s41398-020-00882-7), froze a source-column interpretation after prior outcome exposure, and reconstructed within-treatment ribosome-enriched versus total RNA lists using literal gene names. We audited duplicate identifiers and performed subset-only sensitivity analyses. **Results:** The workbook contained 2,980 vehicle and 3,760 amyloid-beta selected rows, but 2,973 and 3,752 distinct gene names. Literal-name comparison yielded 349 vehicle-only, 1,128 amyloid-beta-only and 2,624 shared names, compared with reported summaries of 356, 1,136 and 2,624. Seven and eight excess rows respectively account arithmetically for the differences in unique-category totals, without resolving the original identifier-level membership. **Conclusions:** A recoverable distinction between selected rows and gene names changes reconstruction while preserving the reported overlap. This does not establish a scientific error or overturn the biological findings. Independent interpretation, original identifiers and cross-case evaluation remain necessary.

## Introduction

Public supplementary tables make biological studies inspectable, but they do not always expose the exact unit used to construct a figure. A table can contain several rows carrying the same gene name while retaining distinct effects or adjusted probabilities. Counting rows, counting names and counting original stable gene identifiers then answer different questions. An apparently small numerical disagreement may therefore be a mapping problem rather than a biological contradiction. Conversely, reproducing a published number does not establish that the same underlying members were recovered.

An Alzheimer-related experimental study by Ghosh and colleagues provides a useful bounded example [1]. The study investigated amyloid-beta exposure in primary rat cortical neurons and separate age-related phenotypes in Cyfip2 mice. Its RNA experiment compared total cytoplasmic and ribosome-enriched fractions within vehicle and amyloid-beta treatment conditions. The reported Figure 1d summary comprised 356 vehicle-unique, 1,136 amyloid-beta-unique and 2,624 shared genes. These quantities had already been inspected before this reconstruction was designed; they are not held-out targets.

The measurement boundary is especially important. A sucrose-cushion preparation of ribosome-enriched RNA is not RNase-protected footprint sequencing. Differential representation in an enriched fraction is not automatically a model-based treatment effect on translation efficiency, nor direct quantification of each gene's protein output. The paper also reports protein-synthesis and mouse experiments; neither supplies independent gene-set membership for this particular comparison.

We asked whether the publicly supplied selected lists support a transparent literal-name reconstruction and whether data-unit choices explain differences from the reported totals. We did not ask whether amyloid-beta causes Alzheimer's disease, whether CYFIP2 is a validated therapeutic target, or whether the original sequencing inference can be independently replicated. This distinction keeps an executable documentation result from becoming an unsupported disease claim.

## Methods

### Design, provenance and prior exposure

This was a purposively selected retrospective methodological application, not a systematic review, prospective registration or unused transfer test. The parent cross-disease scope included three exposed experimental sources and an earlier TSC development case. The present work is a separate local branch, not a reset of that programme's selection or acquisition history. Earlier AD acquisition exhausted eight requests and retained an unrecoverable redirect-body measurement gap. A newly authorized recovery amendment was recorded before any additional request. Historical accounting remains uncertified.

The recovery phase allowed at most 12 individually prelogged first-party requests and 15,000,000 decoded response-body bytes. Automatic redirects and retries were disabled. Response bodies, including HTML errors, were streamed; no browser, external extraction service, authentication or access-control bypass was used. The successful file came from the publisher's public media endpoint. Network provenance was recorded in the local acquisition ledger; source hashes and executable mapping are provided in the public code repository. Sources outside this branch were read-only.

### Source validation and experiment definition

The acquisition pipeline ran inspect_table.py to check ZIP signatures, archive paths, member counts, expansion sizes and compression ratios before workbook parsing. This inspection is a prerequisite for the internal analyze.py script, not an inline guard in that script; the standalone reviewer replay embeds its guards before parsing. The archive was not extracted to disk. An inert printer-settings member was identified explicitly rather than executed. The local archived article states a Creative Commons Attribution 4.0 licence with exceptions for separately credited third-party material. Derived outputs preserve source attribution; no external redistribution was performed.

The source describes primary rat cortical neurons exposed to 100 nM synthetic rat amyloid-beta 1–42 preparation or vehicle for 24 hours. Ribosome-associated material was pelleted through a 20% sucrose cushion, using an RNase inhibitor; polyadenylated RNA libraries were prepared [1, Methods: Ribosomal RNA extraction; RNA sequencing and analysis]. We therefore describe the assay as ribosome-enriched RNA, not footprints. The target contrast is enriched versus total RNA within each treatment, followed by comparison of selected lists. Separate Cyfip2 mouse pathology and behavioural experiments were excluded.

The official GSE149540 full text record [2] was retrieved to map sample identifiers. Twelve library records describe three libraries for each treatment-by-fraction cell. Neither that arrangement nor the sample titles establishes donor independence, pooling or pairing. Independent biological sample size was left unknown; twelve libraries were not treated as twelve independent animals or patients.

### Frozen interpretation and primary reconstruction

After inspecting workbook labels but before set calculations, we froze the mapping in a timestamped local source-column freeze; the exact sheet mapping is stated below. The four sheets are log_control_non_fmrp, log_ab_non_fmrp, log_control_fmrp and log_ab_fmrp. Each exposes Associated_Gene_Name, log2FoldChange and padj. We interpreted these as source-selected lists separated by treatment and FMRP label, not a complete tested universe.

For vehicle, we united the two control sheets; for amyloid-beta, we united the two ab sheets. Primary identifiers were nonblank, literal, case-sensitive names. We did not resolve aliases, strip accession suffixes or convert names to modern annotations. Every selected source row was retained with workbook hash, sheet and one-based Excel-row anchor. Set operations deduplicated identical names within treatment and exported shared and treatment-only membership. No effect-size filter was imposed on the primary enumeration. Published DESeq/BH processing was not rerun, and a generic statistical p-value statement was not used to reconstruct an unavailable complete selection pipeline.

### Sensitivity and audit procedures

The source-column freeze specified whitespace-trimmed enumeration, restriction of supplied rows to numeric adjusted p-values below 0.05 and 0.01, and restriction to finite numeric fold changes. These are subset analyses of already-selected lists, not a new genome-wide differential analysis. We audited blank identifiers, duplicate names, numeric failures and overlap between FMRP-labelled and other sheets. The selected FMRP fraction is descriptive; no enrichment test was performed without a verified full background.

After the primary output revealed duplicate names, a separately disclosed explanatory audit retained both row totals and name totals and inspected duplicate row effects. This post-result arithmetic check is not a prespecified biological endpoint. The verifier independently reads worksheet XML rather than relying only on the workbook library, compares exported membership and anchors, and checks input hashes. Agreement between these implementations constrains parsing and computational errors under the same interpretation; it does not independently establish the original authors' identifier mapping or figure-construction choices. Artificial software controls are labelled tests, not empirical observations or an estimate of detection accuracy.

## Results

### Genuine source recovery and dataset boundaries

The fourth recovery request returned a 229,758-byte workbook from the publisher media endpoint; earlier static/media candidates failed DNS resolution or returned HTML 404 responses. Its SHA-256 was 3dc2f0d2b36e003c18a90e57dc9655f60640bd0de2b500a42e1431b785368140. The validated archive contained 15 members with 1,276,313 expanded bytes. A fifth request returned the official GEO record, allowing all twelve library identifiers to be mapped. No raw reads were acquired. These are actual access and reconstruction results, not restoration of the historical accounting gap.

### Selected rows and literal-name membership

The vehicle non-FMRP sheet contained 2,631 data rows representing 2,624 distinct names; its FMRP sheet contained 349 rows and names. The amyloid-beta non-FMRP sheet contained 3,341 rows representing 3,334 names; its FMRP sheet contained 419 rows representing 418 names. There were no blank names, and the FMRP and non-FMRP name sets were disjoint within each treatment.

Combined selected-row totals were therefore 2,980 for vehicle and 3,760 for amyloid-beta, whereas distinct-name totals were 2,973 and 3,752. Literal-name reconstruction returned 349 vehicle-only names, 1,128 amyloid-beta-only names and 2,624 shared names, a union of 4,101 names. The overlap agrees numerically with the published figure, but the treatment-only categories do not. All reconstructed members and source anchors can be regenerated as core_membership.csv from the separately obtained source workbook; agreement of overlap counts alone is not independent confirmation of the figure's original membership.

### Duplicate-name audit

Seven vehicle and eight amyloid-beta rows were excess relative to distinct names. Repeated vehicle names included Coro7, Cox6b1, Hspa8, Klf7, Rpl21, Tbca and Uqcrb. In amyloid-beta lists, Coro7, Cox6b1, Hspa8, Klf7, Lrp1b, Rpl21, Uqcrb and Nr3c1 were repeated. Their differing numerical entries demonstrate that these are not simply identical repeated lines. Lrp1b and Nr3c1 each have opposite-signed fold changes among amyloid-beta rows. A single gene-name direction would discard information.

Subtracting the observed 2,624 shared names from the selected-row totals gives 356 and 1,136, exactly the reported treatment-only summaries. This arithmetic compatibility is an explanatory observation, not proof of the original plotting procedure. Missing original identifiers prevent determination of whether repeated names represent distinct annotation records, collapsed mappings or another source-specific structure. We therefore classify the discrepancy as identifier-unit unresolved rather than an established author error.

### Sensitivity and missing inference

Trimming whitespace and retaining supplied rows with padj below 0.05 left primary name-set counts unchanged. Restriction to padj below 0.01 yielded 280 vehicle-only, 832 amyloid-beta-only and 1,697 shared names. Restriction to finite fold changes yielded 349, 1,127 and 2,622 respectively. Two vehicle and three amyloid-beta rows had nonfinite or nonnumeric effect fields, including Inf and an Excel error token; their identifiers were retained in the primary membership analysis.

The FMRP-labelled selected-name fractions were 349/2,973 and 418/3,752. These describe the selected lists only and do not estimate enrichment relative to all tested genes. Neither the full gene universe, a treatment-by-fraction interaction estimate, independent biological n nor an independent biological replication was established.

## Discussion

The substantive result is a reproducible distinction between selected records and literal gene names in a real supplementary workbook. The source's overlap count is recovered, while its treatment-only totals are arithmetically compatible with subtracting a name-level overlap from row-level totals. This is more informative than reporting access failure or comparing three summary numbers without source membership. It nevertheless remains narrower than reproduction of the original statistical analysis.

Several explanations remain plausible. The original inference may have operated on stable identifiers subsequently mapped to nonunique names. Different records may therefore legitimately share a displayed name. Alternatively, a plotting or export step may have mixed units. Without stable identifiers and the original comparison code, these explanations cannot be distinguished. Repeated names with opposite signs reinforce the need for mapping provenance, but do not by themselves demonstrate false biological conclusions. A correction request would be premature without source-specific human adjudication and, if authorized later, a bounded factual query to the original investigators.

The threshold sensitivity illustrates another boundary. Applying a stricter cutoff to selected rows changes overlap substantially, but it cannot test whether omitted rows would enter under a different original model. It cannot reconstruct library normalization, model design, outlier handling or multiple-testing correction. The selected lists support a reproducible membership audit; they do not support an invented complete DESeq input. Likewise, FMRP labels can describe strata without licensing a new enrichment probability.

A methodological paper would be strengthened by a source-linked comparison across assay technologies, using this example together with the PD and PDAC branches. Those cases would need their own validated tables and measurement-specific interpretation. Combining diseases should test a transferable question about analysis units and membership, not imply shared therapeutic efficacy. The existing TSC case is an exposed development source; re-enumerating a second workbook alone does not establish a distinct paper's originality. We currently favour evaluating a single integrated methods paper over claiming separate AD-paper novelty.

This case also identifies a falsifiable methodological proposition: where original stable identifiers and plotting code are supplied, a fully specified identifier mapping should reconcile record-level and name-level summaries or expose a residual discrepancy. Exact reconciliation would disconfirm an interpretation that the published totals necessarily arose from erroneous gene counting. A residual difference after source-authoritative mapping would justify further investigation, not immediate generalization to literature-wide error rates.

## Limitations and conclusion

The analysis was outcome-exposed, purposively selected and performed with substantive AI assistance. No independent human second interpretation was completed. Independent sample size, original feature identifiers, complete tested statistics and original code remain missing. Software integrity checks cannot settle those scientific questions. The exercise establishes a transparent selected-list reconstruction and a concrete identifier-unit ambiguity, not failed biological replication, disease discovery or clinical utility. Submission readiness requires source interpretation review, an explicit overlap decision and journal-specific author approval.

## Declarations

**Author and correspondence:** ByungGyu Yoo, Independent Researcher, Incheon, Republic of Korea. ORCID: 0009-0009-8158-758X. Correspondence: ppitu009@gmail.com.

**Funding:** The author received no external funding for this work.

**Competing interests:** The author declares no competing interests and no close collaborative relationship with the authors of the original study.

**Contributions and accountability:** The accountable author authorized the research direction, public release and submission, and accepts responsibility for the work. The computational implementation, analysis, drafting and critique received substantive AI assistance as disclosed below; these tasks are not falsely attributed to an independent human reviewer. AI systems are not authors.

**Ethics:** This work reanalyses publicly available processed experimental tables. It involved no new human participants, patient-level data collection or animal experiments. No original-study animal ethics approval is represented as approval for this secondary analysis.

**Data and code:** Source workbooks remain with their original publishers and must be obtained separately; original source licenses and third-party exceptions are unchanged. Public code, input hashes, headers, source attribution, numerical reference summaries, coverage map and isolated tests are available at https://github.com/poilcer/translation-table-replay/tree/e1133cdd3d14705bdc88623f64773b885b6e87c9. The extensions.py runner reproduces the workbook-derived numerical extensions from one external workbook per study; it does not require a private sibling directory or prior CSV exports. Original workbooks and full source matrices are not redistributed. No archival DOI for this new work has been assigned.

**Related work and exclusivity:** This is one of three distinct-source partial reconstructions from an outcome-exposed, purposively selected research programme, not a new held-out validation. A related TSC manuscript entitled "Tracing analytical targets before comparing gene counts: a reproducibility case study in tuberous sclerosis research" was submitted to Science Editing (temporary reference 20260133). This statement records that submission history, not acceptance or a freshly certified editorial status. The other companion manuscripts use different original studies; shared conceptual and software elements are disclosed and no independent cross-disease validation is claimed. These three current manuscripts have not been submitted elsewhere by this programme. Each must be considered as a bounded partial reconstruction, not as a newly validated general methodology.

**AI-use disclosure:** OpenAI gpt-6.1-sol operating through Hermes assisted source inspection, analysis design, code development, numerical work, original figures, verification and substantial manuscript drafting. Anthropic Claude through the authenticated Claude Code CLI subsequently provided read-only scientific and code critique. Hermes checked the critique against actual artifacts, applied supported revisions and reran computations. Actual runtime records are retained. These AI checks are not independent human peer review or biological validation, and no source-author endorsement is claimed.

**License and approval:** The author approved public release and submission. This manuscript and its newly created figures are licensed CC BY 4.0; the new computational software is MIT-licensed. These grants do not relicense the original publications, workbooks or source data.
## References

1. Ghosh A, Mizuno K, Tiwari SS, Proitsi P, Gomez Perez-Nievas B, Glennon E, Martinez-Nunez RT, Giese KP. Alzheimer's disease-related dysregulation of mRNA translation causes key pathological features with ageing. Translational Psychiatry. 2020;10:192. doi:10.1038/s41398-020-00882-7. PMCID: PMC7297996. Supplementary Table 2: 41398_2020_882_MOESM3_ESM.xlsx.
2. NCBI Gene Expression Omnibus. GSE149540. Official full text record retrieved during the disclosed recovery phase. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE149540
