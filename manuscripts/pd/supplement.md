# PD numerical supplement

Derived aggregate outputs only; original workbook must be obtained separately. All rows below are generated from the retained executed analysis, not invented examples. Units remain source rows or stated symbol/universe units, not independent animals. Public extensions.py regenerates these groups.

## Table S1. Fixed universe summaries

| Contrast | Universe | n | Mean delta | Population SD | Sample SD | Population up | Population down |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GS | all_rows | 8576 | 0.0512053644174 | 0.216470961605 | 0.21648358345 | 688 | 335 |
| GS | finite_FE | 8576 | 0.0512053644174 | 0.216470961605 | 0.21648358345 | 688 | 335 |
| GS | nonduplicated_symbols_only | 8533 | 0.051051543792 | 0.216655949658 | 0.216668645955 | 684 | 332 |
| GS | symbol_mean_delta | 8553 | 0.0511373268288 | 0.216551874836 | 0.216564535357 | 685 | 333 |
| GS | common_literal_ids | 8535 | 0.0516808047725 | 0.215137510635 | 0.215150114995 | 693 | 338 |
| GSDA | all_rows | 8576 | -0.0749916094781 | 0.173733460913 | 0.173743590848 | 313 | 631 |
| GSDA | finite_FE | 8576 | -0.0749916094781 | 0.173733460913 | 0.173743590848 | 313 | 631 |
| GSDA | nonduplicated_symbols_only | 8533 | -0.0749213075146 | 0.17375235982 | 0.173762541915 | 311 | 626 |
| GSDA | symbol_mean_delta | 8553 | -0.0749576009688 | 0.173667507587 | 0.17367766091 | 311 | 626 |
| GSDA | common_literal_ids | 8535 | -0.0752016036521 | 0.173355011427 | 0.173365167856 | 311 | 630 |
| KO | all_rows | 9561 | 0.0200397697292 | 0.272749185435 | 0.272763450186 | 596 | 576 |
| KO | finite_FE | 9561 | 0.0200397697292 | 0.272749185435 | 0.272763450186 | 596 | 576 |
| KO | nonduplicated_symbols_only | 9512 | 0.0193821020418 | 0.272155704041 | 0.272170011083 | 596 | 577 |
| KO | symbol_mean_delta | 9535 | 0.019689212468 | 0.272198779968 | 0.272213054755 | 597 | 577 |
| KO | common_literal_ids | 8535 | 0.0204443125765 | 0.257177874288 | 0.257192941685 | 527 | 520 |

## Table S2. Strict and inclusive comparison

| Contrast | Score | Direction | Inclusive | Strict | Different memberships |
| --- | --- | --- | --- | --- | --- |
| GS | source | up | 687 | 687 | 0 |
| GS | source | down | 335 | 335 | 0 |
| GS | sample | up | 687 | 687 | 0 |
| GS | sample | down | 335 | 335 | 0 |
| GS | population | up | 688 | 688 | 0 |
| GS | population | down | 335 | 335 | 0 |
| GSDA | source | up | 313 | 313 | 0 |
| GSDA | source | down | 631 | 631 | 0 |
| GSDA | sample | up | 313 | 313 | 0 |
| GSDA | sample | down | 631 | 631 | 0 |
| GSDA | population | up | 313 | 313 | 0 |
| GSDA | population | down | 631 | 631 | 0 |
| KO | source | up | 596 | 596 | 0 |
| KO | source | down | 576 | 576 | 0 |
| KO | sample | up | 596 | 596 | 0 |
| KO | sample | down | 576 | 576 | 0 |
| KO | population | up | 596 | 596 | 0 |
| KO | population | down | 576 | 576 | 0 |

## Table S3. Structure strata

| Contrast | Stratum | Rows | Mean | Median | Q25 | Q75 |
| --- | --- | --- | --- | --- | --- | --- |
| GS | complex_FE_lt_minus250 | 1150 | 0.0598184427118 | 0.029266504241 | -0.104998590267 | 0.191193502911 |
| GS | simple_FE_gt_minus20 | 1038 | 0.00414830351317 | -0.0203426201386 | -0.122629829624 | 0.121612248075 |
| GSDA | complex_FE_lt_minus250 | 1150 | -0.102719683301 | -0.078504797609 | -0.18923040746 | 0.0131722166604 |
| GSDA | simple_FE_gt_minus20 | 1038 | -0.0439869132596 | -0.0266892495842 | -0.118134005758 | 0.0505691911966 |
| KO | complex_FE_lt_minus250 | 1286 | -0.0379837495091 | -0.0396905866865 | -0.195580941639 | 0.115156986126 |
| KO | simple_FE_gt_minus20 | 1156 | 0.00918680925096 | 0.0190114305769 | -0.158483343393 | 0.176824924612 |

## Table S4. Matched-ID descriptive associations

| Pair | n | Pearson | Spearman | Median paired delta difference |
| --- | --- | --- | --- | --- |
| GS_GSDA | 8576 | -0.378502357029 | -0.301800329297 | 0.0710614710305 |
| GS_KO | 8535 | 0.135524935039 | 0.176643630436 | 0.0250606063804 |

All checks are descriptive and outcome-exposed. Caption-SD and original figure-universe correspondence remain unresolved.
