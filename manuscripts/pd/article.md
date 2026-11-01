# [Re] A source-bound partial replication of translation-efficiency summaries in LRRK2 mouse brain

## Abstract

**Objective:** To determine which published LRRK2 mouse-brain translation-efficiency results are recoverable from a public processed table, without claiming replication of sequencing or biological experiments. **Methods:** We independently implemented log-ratio reconstruction and membership verification across three contrasts, preserved a previously frozen population-standard-deviation primary analysis, and distinguished inherited sample-SD sensitivity from new post-hoc universe and structure analyses. **Results:** All 26,713 supplied rows supported reconstruction. Source z-scores matched sample-SD standardization within 1.5 × 10⁻¹³. Source memberships were GS 687 up/335 down, GSDA 313/631, and KO 596/576; population-SD primary GS membership retained 688 up, with Eif2b3 crossing the boundary. Table sample SDs were 0.216484, 0.173744, and 0.272763 versus caption values 0.226, 0.179, and 0.273. Fixed universe alternatives did not reconcile GS/GSDA SDs. Structure-stratum directions were compatible with the source narrative, but denominators differed and gene-wide GS–KO changes were not inversely correlated. **Conclusions:** The processed arithmetic and selected memberships are recoverable; the SD and structure-universe correspondence remains unresolved. This is a partial computational replication candidate, not evidence of original-study failure, biological replication, or clinical benefit.

## Introduction

Ribosome profiling measures ribosome-protected RNA fragments, while RNA sequencing measures transcript abundance. Their ratio is often interpreted as translation efficiency (TE), but reconstruction of a reported ratio is distinct from validating the biological mechanism inferred from it. Kim and colleagues studied G2019S LRRK2 (GS), kinase-dead G2019S/D1994A LRRK2 (GSDA), and LRRK2 knockout (KO) mouse brains [1]. They reported altered TE distributions, associations with predicted 5′ untranslated-region structure, and separate reporter and electrophysiological observations. A supplementary expression workbook provides an opportunity to ask exactly which computational results a reader can independently recover.

This question matters because agreement has several levels. Matching a figure’s gene count does not establish that the same identifiers were selected. Matching standardized scores does not establish that a caption summarizes the same analysis universe. Neither validates the original normalization, preparation-level replication, or causal account. A faithful partial replication should identify its successful components as specifically as its unresolved ones, rather than treating the original article as either wholly reproduced or wholly failed.

The present work extends an already exposed retrospective pilot. That pilot reconstructed processed TE arithmetic and identified a small SD-convention boundary difference together with larger caption–table SD differences. We preserve its frozen primary specification. Our additional contribution is a bounded investigation of plausible universe definitions, an explicit link between threshold membership and literal source identifiers, descriptive checks of structure-dependent patterns, and artificial software controls demonstrating why count agreement alone is insufficient. We do not present this as a systematic literature review or a newly blinded experiment.

## Methods

### Source, provenance, and experimental scope

We used the cached publisher HTML, Extended Data Figure 1-2 workbook, and cached source text of Kim et al. [1,2]. No new internet requests were made. The workbook is an OOXML ZIP despite its .xls suffix; it was opened from bytes rather than interpreted by extension. Its SHA-256 is 08a9bbc3fa8696426c02fe9f725a44b69d9b2927532a8c5f727a1260ac894c3d. A preservation ledger records hashes of pre-existing scope artifacts. Input files were read only; generated outputs reside in a separate candidate directory.

The underlying experiment used caudate putamen from three- to four-month-old mice. Methods describe pooling tissue from three mixed-sex mice per preparation; Figure 1 describes two independent results combined with DESeq. We leave the independent biological sample count unresolved rather than equating thousands of gene rows, pools, or libraries with independent animals. GS and GSDA are contrasted against non-transgenic controls; KO is contrasted against WT. The source reports CDS-only counting using a union-of-isoforms annotation, discarding low-read transcripts, and DESeq 1.20 normalization [1,3]. We did not rerun alignment, the <128-read filter, DESeq, isoform annotation, or replicate-level inference.

### Caption and column audit

The actual cached HTML Figure 1 caption maps panels B, C, and D to GS, KO, and GSDA, respectively. It explicitly describes log2 values, one transcript per point, standard z-scores, ±1.5 selection, and SDs of 0.226, 0.179, and 0.273 for GS, GSDA, and KO. The published review/response contains a C/D labeling correction; that history is not evidence that the SDs were corrected or that a particular SD belongs to another universe. Figure 2 reports GS 687/335 and KO 596/576 selected groups, and complex/simple structure groups of 1,145/1,036 without a complete, unambiguous contrast-specific universe mapping.

The table columns contain literal identifiers, symbols, description, control and treated footprint and RNA baseMeans, minimum isoform 5′UTR folding energy, log2 TE values, delta-TE, and z-score. A minimum over isoforms is not isoform-resolved translation. Gene-level union counting, caption “transcript” language, and duplicated symbols cannot be assumed interchangeable. All fields needed for arithmetic were finite and the four abundance inputs were positive. Minimum folding energy was present for every row.

### Inherited primary analysis and agreement targets

For each row we calculated delta = log2(RPF_t/RNA_t) − log2(RPF_c/RNA_c). The frozen primary z-score subtracts the within-sheet delta mean and divides by population SD (ddof=0). Up/down membership uses inclusive thresholds of +1.5/−1.5. The previously specified sample-SD sensitivity uses ddof=1; strict-versus-inclusive selection is also inherited. We did not promote sample SD to primary because it better matches the source. Numerical agreement with source arithmetic was assessed at absolute error below 10⁻¹⁰, while caption agreement was assessed at its displayed three-decimal precision. Literal identifiers plus workbook row anchors define membership; symbols are not unique keys.

### New post-hoc analyses

All new checks were specified after the initial discrepancies were known and recorded as post-hoc in the timestamped local protocol before execution. Five universes were examined: all source rows; finite-folding-energy rows; rows whose symbol occurs exactly once; arithmetic mean delta per literal symbol; and literal-ID intersection across all three contrasts. Omitting every duplicated-symbol row avoids an arbitrary representative choice. Symbol averaging changes the estimand and is not a repair of the primary analysis. No universe was selected for proximity to a caption value. We did not impose the source’s raw-read threshold on normalized baseMeans.

We compared reconstructed log ratios, subtraction of stored log2 TE columns, and stored delta. Natural-log scaling was checked as a standardized-score invariant; a raw linear TE difference was evaluated only to demonstrate a different scale, not as an admissible replacement for a caption explicitly describing log2. We used fixed source structure thresholds: folding energy below −250 kcal/mol and above −20 kcal/mol. Means, medians, and interquartile ranges summarize delta in these strata. Spearman correlations describe continuous folding-energy/delta association. Matched-ID correlations between GS and GSDA and between GS and KO assess whether a broad inverse gene-wise pattern follows from the table.

No gene-level p-values or animal-level confidence intervals were calculated. Gene rows share biological preparations, and the processed table cannot support independent-animal inference. We did not reconstruct randomly sampled reference groups, reproduce source ANOVA or Wilcoxon tests, or synthesize unavailable icSHAPE measurements. The public code regenerates derived summaries and row-anchored memberships from the external source; it does not distribute source abundance matrices or publisher figures.

### Verification and software controls

The verifier independently rereads workbook cells, recomputes TE and sample/population memberships, checks frozen hashes and saved summaries, and checks document content and embedded images. An independently reconstructed source membership is compared with the exported row-anchored set as a positive check; artificial negative controls include a count-preserving member replacement, omission, and a wrong-contrast set. These tests assess enumerated software behavior, not sensitivity/specificity on empirical scientific errors. A successful verifier does not establish the correctness of every biological interpretation. The public standalone code and extension runner are supplied for inspection and execution under MIT; source data retain their original rights.

## Results

### Processed arithmetic and membership are recoverable

The workbook contains 8,576 GS, 8,576 GSDA, and 9,561 KO rows, with no duplicate literal identifiers or arithmetic exclusions. Across all 26,713 rows, reconstructed delta agrees with the stored delta within 2.5 × 10⁻¹⁴. Subtracting the stored log2 TE columns gives the same result within 2.6 × 10⁻¹⁴. Sample-standardized delta agrees with every source z-score within 1.5 × 10⁻¹³. This identifies the source table’s standardization convention numerically, conditional on the supplied universe; it does not reconstruct DESeq.

| Contrast | Rows | Frozen primary up/down | Source/sample-SD up/down | Table sample SD | Caption SD |
|---|---:|---:|---:|---:|---:|
| GS | 8,576 | 688 / 335 | 687 / 335 | 0.216484 | 0.226 |
| GSDA | 8,576 | 313 / 631 | 313 / 631 | 0.173744 | 0.179 |
| KO | 9,561 | 596 / 576 | 596 / 576 | 0.272763 | 0.273 |

The GS and KO source counts reproduce Figure 2’s reported counts. Sample-SD membership also matches every source selected identifier, not merely the totals. Figure 2 does not report corresponding GSDA selected counts. Strict versus inclusive comparisons change no source membership. This inherited check is explicitly recomputed for every contrast and source/sample/population score in the public runner's extensions.json; membership differences are verified from row anchors rather than counts alone.

Only one primary-versus-source boundary difference occurs: GS workbook row 689, uc008uhu.2, Eif2b3. Its population z-score is 1.5000822877711095, while its sample/source score is approximately 1.4999948270657. Its delta lies 0.0000178129 above the population upper boundary and 0.00000111986 below the sample upper boundary. Thus 688 remains the prespecified primary GS-up count and 687 remains the source/sample sensitivity. These are not two competing estimates selected by apparent success.

### Plausible table universes do not close the SD correspondence

The caption GS and GSDA SDs exceed table sample SDs by 4.396% and 3.025%, respectively; KO agrees at three decimals. Population-versus-sample scaling is far too small to account for the first two differences. All rows have finite UTR folding energies, so UTR-availability eligibility leaves the results unchanged.

GS and GSDA each have 20 duplicated-symbol groups involving 43 rows, corresponding to 23 excess symbol rows. KO has 23 groups involving 49 rows and 26 excess rows. These quantities distinguish affected rows from excess rows. Removing all duplicated-symbol rows gives sample SDs 0.216669, 0.173763, and 0.272170. Averaging deltas by symbol gives 0.216565, 0.173678, and 0.272213. Restricting to 8,535 literal IDs common to all contrasts gives 0.215150, 0.173365, and 0.257193. None reconciles the GS or GSDA caption value at reported precision (Figure 1; Supplement S1).

Natural-log rescaling leaves standardized scores unchanged within numerical tolerance, but changes the units of an SD; it is not a reconciliation of log2 values. Linear TE differences have sample SDs 0.229701, 0.187948, and 0.191340, also failing to explain the three-caption pattern and contradicting its stated scale. No cutoff, pseudocount, or row-ranking search was performed. A figure-generation universe or historical workbook version remains possible but unverified.

### Structure directions recur, but denominators remain non-identical

Applying the caption’s strict structure thresholds to all supplied GS rows yields 1,150 complex and 1,038 simple rows, rather than 1,145/1,036. GSDA has the same stratum counts; KO has 1,286/1,156. Counting unique symbols in GS produces 1,145 complex but 1,037 simple symbols. Removing every duplicated-symbol row produces 1,142/1,036. The all-contrast ID intersection yields 1,145 complex but 1,030 simple rows. Several individual numbers can therefore be matched by different rules; no single tested rule matches both caption denominators. Selecting one rule per stratum would be outcome-driven and is not justified.

Nevertheless, all-row descriptive structure patterns are compatible with the source narrative (Figure 2). GS median delta is 0.02927 in complex and −0.02034 in simple rows; KO medians are −0.03969 and 0.01901, respectively. GSDA medians are −0.07850 and −0.02669. Continuous folding-energy/delta Spearman correlations are −0.0831 (GS), 0.1141 (GSDA), and 0.0735 (KO). These modest associations do not identify structure as a causal mediator or reproduce the source’s inferential tests.

### Reciprocal structure patterns are not genome-wide inversion

Across the 8,576 matched GS/GSDA IDs, delta correlations are Pearson −0.3785 and Spearman −0.3018. Across 8,535 matched GS/KO IDs they are Pearson 0.1355 and Spearman 0.1766. Thus the structure-stratified reciprocal tendency does not imply a global negative correlation between GS and KO gene-wise changes. Shared controls, normalization, tissue composition, and genotype-specific perturbations prevent interpreting these descriptive correlations as an interaction estimate or an inhibitor-response prediction.

## Discussion

### What this partial replication establishes

The strongest recoverable finding is unusually specific: every supplied z-score is consistent with centered, sample-standardized log2 footprint/RNA differences, and the source memberships can be recovered exactly from that definition. The one-member population-primary discrepancy is explained by a known convention at a sharply resolved boundary. It is not evidence that the table is numerically unstable in a broad biological sense. Preserving both conventions prevents an apparently successful reconstruction from rewriting the analysis plan.

The SD audit reaches a different conclusion: two caption summaries are not recovered from the supplied all-row table or the fixed semantic alternatives examined. This is an unresolved correspondence, not a demonstrated error in the original experiment or a declaration of non-replicability. Exact figure inputs, plotting code, or version history could resolve it. The caption’s panel-label correction does not supply that missing information. Likewise, partial matches to Figure 2 denominators are insufficient without a consistent rule defining both strata.

### Counterarguments and alternative explanations

First, the original authors may have used a legitimate figure-specific universe absent from the workbook. That would explain why internally consistent table scores coexist with different caption SDs. We cannot exclude this and therefore report both values without choosing an authority by numerical convenience. Second, a symbol-based interpretation might be appropriate for some annotations. Our checks show that symbol deduplication can alter counts, but do not identify which representative or aggregation the original figure used. Third, the observed structure tendencies might reflect UTR length, expression-related selection, or isoform annotation rather than structural complexity itself. Minimum isoform folding energy is particularly unsuitable for a strong isoform-mechanistic claim without further annotation.

Fourth, gene-wise GS–KO correlations might be weakly positive while conditional structure effects reverse. These are different statistical questions; the correlation is a guard against overgeneralization, not a refutation of the source’s stratified observation. Fifth, bulk protein synthesis measurements may differ from normalized relative TE. The original discussion acknowledges a report of suppressed bulk synthesis in other models [1]. We have not independently reassessed that cited study and do not treat it as adjudicated counterevidence.

### Added methodological value and publication form

This work goes beyond replaying four counts by joining numerical reconstruction to literal membership, identifying a boundary member, separating duplicated-symbol excess from affected rows, auditing consistent universe rules, and showing that qualitative structure reversal is not equivalent to genome-wide inversion. The controlled substitutions demonstrate a verification-layer distinction only; they are not a benchmark of error detection or an estimate of the prevalence of published mistakes.

For a general novel-methods article, a single exposed source and artificial controls would offer limited evidence of transfer or utility. A coordinated three-case paper could be stronger if it asks the same falsifiable audit question across the AD, PD, and PDAC branches while preserving their different assays and models. Neither the other branches’ experiments nor a three-case validation are results of this manuscript. Related TSC audit work must be disclosed and overlap assessed before any submission.

A different publication rationale applies to ReScience C. Its saved official guidance explicitly permits partial replication and does not require novelty [4–6]. Therefore the absence of a new method or an independent external expert is not itself a disqualifying gate. The present submission is a successful partial replication of processed arithmetic and memberships with unresolved summary correspondence. Editorial judgment is still needed on whether this limited computational subset is substantial enough under the journal’s field-specific criteria. It must not be reframed as a negative replication merely to increase impact.

### Limits and next evidence requirement

This study cannot establish original model reconstruction, raw-read reproducibility, DESeq uncertainty, biological independence, original p-values, RNA-structure causality, protein-output effects, or treatment benefit. Source-figure images were not downloaded or visually digitized; actual cached HTML legends and captions were inspected. There was no human duplicate scientific review. New analyses are post-hoc, not preregistered or confirmatory. No claim of author endorsement or failed-author-contact history is made.

The next scientific clarification is the exact row/identifier universe and version used for Figure 1 GS/GSDA SDs and Figure 2 complex/simple groups. Supplying the original figure-input lists and the SD convention would be more decisive than additional arbitrary sensitivity searches. That clarification would improve scope closure; its absence need not prohibit a narrowly stated successful partial replication. If pursuing a negative-replication claim, the saved writing guidance expects attempted author contact while editing guidance describes it as encouraged rather than mandatory [5,6]; this difference should be resolved with the journal only after user authorization. No contact has occurred in this task.

## Conclusion

Processed-table arithmetic and selected memberships are recoverable with an explicit sample-SD convention. The frozen population-SD primary retains its one-member difference. Fixed universe, annotation, and scale checks narrow but do not resolve two caption SD differences and the structure-denominator correspondence. A transparent partial-replication article is supportable for editorial consideration; a full biological replication, a negative-replication judgment, and a validated cross-disease method are not.

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
## Figure legends

**Figure 1. SD agreement across fixed universes.** Original derived plot, not a reproduced publisher figure. Points show sample SD of log2 delta-TE for all rows, finite-FE rows, singleton-symbol rows, symbol-mean delta, and common literal-ID rows; vertical lines show the source Figure 1 caption SD. These are post-hoc semantic sensitivities, not selected alternative primaries. KO caption agreement is specific to the supplied full universe. No interval denotes biological uncertainty.

**Figure 2. Structure-stratum delta-TE distributions.** Original derived plot of fixed complex (FE < −250) and simple (FE > −20) strata. Boxes show interquartile ranges and internal lines show medians. Counts are supplied table rows, not independent animals. The plot does not reproduce original random control selection, original p-values, or Figure 2’s unresolved exact denominator universe.

## References

1. Kim JW, Yin X, Martin I, Xiong Y, Eacker SM, Ingolia NT, Dawson TM, Dawson VL. Dysregulated mRNA Translation in the G2019S LRRK2 and LRRK2 Knock-Out Mouse Brains. eNeuro. 2021;8(6):ENEURO.0310-21.2021. doi:10.1523/ENEURO.0310-21.2021. PMID:34759048. https://www.eneuro.org/content/8/6/ENEURO.0310-21.2021
2. Kim et al. Extended Data Figure 1-2: Ribosome profiling expression analysis results. Publisher-linked workbook. https://www.eneuro.org/content/eneuro/8/6/ENEURO.0310-21.2021/DC2/embed/inline-supplementary-material-2.xls?download=true
3. Anders S, Huber W. Differential expression analysis for sequence count data. Genome Biology. 2010;11:R106. doi:10.1186/gb-2010-11-10-r106. Method citation verified in reference 1; not independently re-read here.
4. ReScience C. Frequently Asked Questions. https://rescience.github.io/faq/ . Official guidance supplied locally as submission_review/venue_1.md; inspected for this candidate.
5. ReScience C. Writing a ReScience C article / submission overview. https://rescience.github.io/write/ . Official guidance supplied locally as submission_review/venue_2.md; inspected for this candidate.
6. ReScience C. Reviewing and editing guidance. https://rescience.github.io/edit/ . Official guidance supplied locally as submission_review/venue_3.md; inspected for this candidate.
