# Does Genre Make an Indian Film Pay Off?
### Studying the Relationship Between Genre, Budget, and Box Office Performance
---

## Overview

This repository hosts the code, datasets, and analysis for our **CS 215 (Data Analysis and Interpretation)** open project at **IIT Bombay**. 

We examine the commercial dynamics of Indian cinema by studying how a film's **genre** correlates with its financial returns relative to production costs. Specifically, we test whether the prevailing perception of **action films** holding superior commercial leverage holds true under rigorous statistical testing.

## Team Members (IIT Bombay)
* Rujul (25B0937)
* Kavya (25B0947)
* Arnav Jindal (25B1087)
* Rajit Gupta (25B0938)

---

## Research Question & Hypotheses

### Primary Question
> Does the genre of an Indian film significantly impact its box-office performance—specifically its revenue-to-budget ratio—when controlling for scale, cast star-power, runtime, and release year?

* **Core Hypothesis:** Action films generate higher financial returns (revenue relative to budget) compared to other genres due to widespread commercial appeal and theatrical star-vehicle dynamics.
* **Alternative / Null Perspective:** When controlled for budget scale, cast prominence, and release environment, action films do not maintain a statistically significant return advantage over other genres.

---

## Project Evolution & Implementation Process

Our data pipeline evolved iteratively to handle messy, multi-source records, currency discrepancies, and conflicting box office figures across independent archives. Below is how our workflow transitioned from raw ingestion to analysis-ready models:

### Phase 1: Ingestion & Unit Standardization
* **The Challenge:** Raw data dumps utilized vastly different formatting standards, scattered date notations, and mixed currency representations (e.g., raw INR integers like `5000000` vs. pre-computed Crores).
* **The Fix:** We ingested 7 distinct source files, built regex parsers to extract standard 4-digit release years, and unified all financial metrics into standardized **₹ Crores** (`1e7` scaling applied where necessary).

### Phase 2: From Blind Deduplication to Source Provenance Tracking
* **Initial Plan:** Merge all datasets immediately by collapsing duplicates into a single master row.
* **Real-World Pivot:** Recognizing that different scrapers (e.g., historical archives vs. modern box office trackers) report conflicting figures, we modified our pipeline (`src/clean_data.py`) to **stack** core sources (`05`, `06`, `07`) side-by-side. This ensures overlapping movies appear repeatedly with a mandatory `source_file` tag for complete auditability.

### Phase 3: Hierarchical Conflict Resolution & Consolidation
* **The Challenge:** Overlapping films frequently presented conflicting budgets or revenues across scrapers.
* **The Fix:** We implemented a prioritized conflict-resolution pipeline (`src/consolidate_data.py`). Grouping by normalized title keys, we established a reliability hierarchy (**Modern Box Office (`06_shreyaumrao`) $\rightarrow$ Case Studies (`07_iima`) $\rightarrow$ General Archives (`05_ishajangir`)**). Source audit trails are concatenated (e.g., `source1 | source2`), and final records are sorted alphabetically.

### Phase 4: Compact Views & Analysis-Ready Filtering
* **Compact Mapping (`src/generate_compact.py`):** Extracted a streamlined 7-column view focusing strictly on `title`, `year`, `genres`, `budget_cr`, `india_net_rev_cr`, `source_file`, and `rev_to_budget_ratio`.
* **Strict Filtering (`src/filter_subset.py`):** Stripped away release year noise and filtered out rows with missing vital signs, yielding a clean subset of fully verified films ready for statistical testing.

### Phase 5: Automated Exploratory Data Analysis (EDA)
* **Statistical Rigor (`src/eda_analysis.py`):** Built automated scripts to compute median/mean ROI, success rates (% profitable films), and execute non-parametric **Kruskal-Wallis H-tests** to verify whether genre-based return variances are statistically significant.

---

## Data Sources & Entity Resolution

Data was collected, harmonized, and cross-validated across 7 open-source repositories:
1. `01_shivanirana63_bo2022.csv` (2022 Box Office supplement)
2. `02_slmsshk_release_data.csv` (Historical lifetime collections)
3. `03_dhirajbembade_imdb_india.csv` (IMDb catalog: genres, ratings, votes)
4. `04_adrianmcmahon_imdb_950.csv` (Top 950 Bollywood ratings)
5. `05_ishajangir_bollywood.csv` (~1,700 historical films in raw INR)
6. `06_shreyaumrao_bo2019_2023.csv` (Modern box office collections)
7. `07_iima_bollywood.csv` (IIM Ahmedabad case study dataset)

---

## Repository Structure

```text
├── data/
│   ├── raw/                      # Unaltered source tables (Sources 01 to 07)
│   └── processed/                # Cleaned, stacked, consolidated, and analysis-ready CSVs
├── notebooks/                    # Exploratory notebooks and hypothesis testing workflows
├── src/
│   ├── clean_data.py             # Stacking, currency standardization, and IMDb enrichment
│   ├── consolidate_data.py       # Hierarchical conflict resolution and deduplication
│   ├── generate_compact.py       # Compact 7-column projection generator
│   ├── filter_subset.py          # Strict completeness filtering and year stripping
│   └── eda_analysis.py           # Statistical summary generation and Kruskal-Wallis tests
├── figures/                      # Generated multi-panel visual analyses and distribution plots
├── requirements.txt              # Project Python dependencies
└── README.md                     # Project documentation and process evolution
