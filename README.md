# Does Genre Make an Indian Film Pay Off?
### Studying the Relationship Between Genre, Budget, and Box Office Performance
---

## Overview

This repository hosts the code, datasets, and analysis for our **CS 215 (Data Analysis and Interpretation)** open project at **IIT Bombay**.

We examine the commercial dynamics of Indian cinema by studying how a film's **genre** relates to its financial returns relative to production cost. Specifically, we test whether the prevailing perception that **action films** hold a commercial advantage holds up when we look at capital efficiency (revenue relative to budget) rather than absolute box-office gross.

Throughout, **ROI** means the **Revenue-to-Budget ratio** = `India Net Revenue / Budget` (both in ₹ Crores). An ROI of 1 is break-even.

## Team Members (IIT Bombay)
* Rujul (25B0937)
* Kavya (25B0947)
* Arnav Jindal (25B1087)
* Rajit Gupta (25B0938)

---

## Research Question & Hypotheses

### Primary Question
> Does the genre of an Indian film significantly impact its box-office performance, specifically its revenue-to-budget ratio?

* **Core Hypothesis:** Action films generate higher ROI than other genres.
* **Null / Alternative Perspective:** Action films do not hold a significant ROI advantage; lower-budget genres (e.g. Comedy, Drama) may offer comparable or better multipliers.

> **Status:** The pipeline and exploratory visual analysis are complete. Formal hypothesis tests (e.g. Kruskal-Wallis across genres) and any regression controlling for budget, rating, and year are **not yet implemented** in this repository.

---

## Project Evolution & Implementation Process

Our data pipeline evolved iteratively to handle messy, multi-source records, currency discrepancies, and conflicting figures across independent archives.

### Phase 1: Ingestion & Unit Standardization (`src/clean_data.py`)
* **The Challenge:** Raw files used different formats, scattered date notations, and mixed units (e.g. raw INR integers like `5000000` vs. figures already in Crores).
* **The Fix:** Regex parsers extract 4-digit release years and clean numeric strings; all financial metrics are standardized to **₹ Crores** (Source 05 is divided by `1e7`).

### Phase 2: Stacking with Source Provenance
* **Initial Plan:** Merge everything and collapse duplicates into a single master row.
* **Pivot:** Different scrapers report conflicting figures for the same film, so `clean_data.py` instead **stacks** sources `05`, `06`, and `07` and keeps a mandatory `source_file` column on every row for auditability.
* IMDb rating, votes, and fallback genres (from sources `03` and `04`) are joined on a normalized alphanumeric title key.
* `final_revenue_cr` falls back through worldwide → India gross → India net revenue.
* **Output:** `data/processed/master_movies_stacked.csv` (2,185 rows: 1,698 from `05`, 338 from `06`, 149 from `07`).

### Phase 3: Filtering to a Complete Subset (`src/filter_movies.py`)
* Keeps `title`, `genres`, `imdb_rating`, `budget_cr`, `india_net_rev_cr`, `rev_to_budget_ratio`.
* Drops rows with any missing value, then keeps only films with ROI between **0.5 and 20**.
* **Output:** `data/processed/clean_movies.csv` (1,034 rows).

### Phase 4: Recalculated Dataset (`data/processed/recalculated_data.csv`)
* Building on the filtered subset, we produced a revised dataset (1,046 rows) with a `year` column restored and **genre labels consolidated into 7 categories**: Comedy, Drama, Thriller, Action, Romance, Horror, and Biopic/Historical/Sports (replacing the many raw labels such as `Rom__Com`, `Love_Story`, `Suspense`, `Masala`, and multi-genre strings).
* Budget and revenue values were rechecked and the ROI ratio recomputed.
* This file is the input to the final analysis.
* **Note:** this step was done outside the scripts in `src/`, so there is no script that regenerates this file.

### Phase 5: Exploratory Visual Analysis (`src/final_+++.py`)
Loads `recalculated_data.csv`, applies hard-coded sanity filters, and writes six figures to `figures/`:

* **Filters applied:** budget and revenue each between ₹0.5 and ₹5,000 Cr; ROI between 0.05 and 20; rows missing rating, budget, year, or genre are dropped.
* **Resulting sample:** about **826 films** (2003–2026): Comedy 254, Drama 172, Action 128, Thriller 125, Romance 73, Biopic/Historical/Sports 38, Horror 36.
* **Panel grids** show "Overall" plus the 7 most frequent genres.

| Figure | Description |
|---|---|
| `01_median_mean_roi_by_genre.png` | Median and mean ROI by genre |
| `02_roi_histogram_by_genre.png` | ROI distribution (log scale), overall and per genre |
| `03_avg_roi_by_budget_section.png` | Mean ROI across budget tiers (0-10, 10-30, 30-50, 50-100, 100-250, 250+ Cr) |
| `04_roi_boxplot_by_genre.png` | ROI box plot by genre (log scale) |
| `05_roi_vs_imdb_rating.png` | ROI vs IMDb rating, colored by genre |
| `06_avg_roi_over_time.png` | Mean ROI by release year, overall and per genre |

---

## Data Sources

Seven open-source datasets are included in `data/raw/`:

| # | File | Contents | Used in pipeline? |
|---|---|---|---|
| 01 | `01_shivanirana63_bo2022.csv` | 2022 box office supplement | No |
| 02 | `02_slmsshk_release_data.csv` | Historical lifetime collections | No |
| 03 | `03_dhirajbembade_imdb_india.csv` | IMDb catalog: genres, ratings, votes | Yes (IMDb enrichment) |
| 04 | `04_adrianmcmahon_imdb_950.csv` | Top 950 Bollywood ratings | Yes (IMDb enrichment) |
| 05 | `05_ishajangir_bollywood.csv` | ~1,700 historical films, raw INR | Yes (stacked) |
| 06 | `06_shreyaumrao_bo2019_2023.csv` | Modern box office collections | Yes (stacked) |
| 07 | `07_iima_bollywood.csv` | IIM Ahmedabad case study dataset | Yes (stacked) |

---

## Repository Structure

```text
├── data/
│   ├── raw/                          # Unaltered source tables (Sources 01 to 07)
│   └── processed/
│       ├── master_movies_stacked.csv # Stacked sources with source_file tag (clean_data.py)
│       ├── clean_movies.csv          # Complete rows, ROI in [0.5, 20] (filter_movies.py)
│       └── recalculated_data.csv     # Consolidated genres, year added, ROI recomputed
├── src/
│   ├── clean_data.py                 # Ingestion, unit standardization, stacking, IMDb enrichment
│   ├── filter_movies.py              # Missing-value and ROI-range filtering
│   └── final_+++.py                  # Final filters and generation of all figures
├── figures/                          # Six generated plots (01 to 06)
├── report/                           # Project reports and ppt
├── requirements.txt                  # Python dependencies
└── README.md
```

## How to Reproduce

Run from the repository root:

```bash
pip install -r requirements.txt
python src/clean_data.py      # -> data/processed/master_movies_stacked.csv
python src/filter_movies.py   # -> data/processed/clean_movies.csv
python "src/final_+++.py"     # -> figures/01 ... 06 (reads recalculated_data.csv)
```

`data/raw/` is listed in `.gitignore`, so the raw CSVs must be present locally before running `clean_data.py`.
