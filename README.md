# Does Genre Make an Indian Film Pay Off?
### Studying the Relationship Between Genre, Budget, and Box Office Performance

[![Course](https://img.shields.io/badge/Course-CS%20215%3A%20Data%20Analysis%20%26%20Interpretation-blue)](#)
[![Institution](https://img.shields.io/badge/Institution-IIT%20Bombay-red)](#)
[![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen)](#)

---

## Overview

This repository hosts the code, datasets, and analysis for our **CS 215 (Data Analysis and Interpretation)** open project at **IIT Bombay**. 

We examine the commercial dynamics of Indian cinema by studying how a film's **genre** correlates with its financial returns relative to production costs. Specifically, we test whether the prevailing perception of **action films** holding superior commercial leverage holds true under rigorous statistical testing.

---

## Research Question & Hypotheses

### Primary Question
> Does the genre of an Indian film significantly impact its box-office performance—specifically its revenue-to-budget ratio—when controlling for scale, cast star-power, runtime, and release year?

* **Core Hypothesis:** Action films generate higher financial returns (revenue relative to budget) compared to other genres due to widespread commercial appeal and theatrical star-vehicle dynamics.
* **Alternative / Null Perspective:** When controlled for budget scale, cast prominence, and release environment, action films do not maintain a statistically significant return advantage over other genres.

---

## Methodology & Statistical Pipeline

1. **Sample Construction & Bias Auditing:**
   * Targeting a sample of **~500+ Indian films** across varying budget tiers.
   * Ensuring inclusion of low/mid-budget productions alongside blockbusters, actively tracking and documenting selection/survivorship bias.
2. **Metrics:**
   * Primary Target: **Revenue-to-Budget Ratio** (financial multiplier / return on investment proxy).
   * Secondary Metric: **IMDb Ratings & User Votes** (critical vs. commercial divergence).
3. **Statistical Techniques:**
   * **Bootstrapping & Confidence Intervals:** Evaluating genre-wise median revenue-to-budget distributions without assuming normality[cite: 1].
   * **Multivariate Regression & Controls:** Isolating genre coefficients while controlling for release year, runtime, star cast, and original language[cite: 1].
   * **Sensitivity Analysis:** Auditing genuine high-grossing outliers and testing model stability with and without extreme data points[cite: 1].

---

## Data Sources & Entity Resolution

Data is collected, harmonized, and cross-validated across multiple databases[cite: 1]:

* **[IMDb Non-Commercial Datasets](https://developer.imdb.com/non-commercial-datasets/):** Film title, release year, runtime, primary genres, average rating, votes, and principal cast/crew credits[cite: 1].
* **Curated Box-Office Repositories & Kaggle Datasets:**
  * [Bollywood Movies Box Office Collection (2022)](https://www.kaggle.com/datasets/shivanirana63/bollywood-movies-boxoffice-collection-2022)[cite: 1]
  * [Bollywood Release Movie Dataset](https://www.kaggle.com/datasets/slmsshk/bollywood-release-movie-dataset)[cite: 1]
  * [IMDb Dataset - All Indian Movies](https://www.kaggle.com/datasets/dhirajbembade/imdb-dataset-all-indian-movies)[cite: 1]
  * [Bollywood Movies IMDb Rating](https://www.kaggle.com/datasets/adrianmcmahon/bollywood-movies-imdb-rating)[cite: 1]
  * [IMDb Curated List](https://www.imdb.com/list/1s521560849/)[cite: 1]
* **Supplementary Industry Data:** TMDb and published trade reports for cross-verifying financial data[cite: 1].
* **Record Linkage:** Entity resolution via canonical `tconst` (IMDb ID) matched against normalized title strings and release years[cite: 1].

---

## Repository Structure

```text
├── data/
│   ├── raw/                # Unaltered source tables and scraped extracts
│   ├── processed/          # Cleaned, deduplicated, and inflation-adjusted datasets
│   └── data_dictionary.md  # Schema definitions, variable descriptions, units
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda_and_distributions.ipynb
│   ├── 03_hypothesis_testing.ipynb
│   └── 04_robustness_checks.ipynb
├── src/
│   ├── utils.py            # Helper scripts (currency standardization, matching)
│   └── stats_models.py     # Bootstrap functions and regression routines
├── reports/
│   ├── figures/            # Visualizations, boxplots, CI intervals
│   └── final_report.pdf
├── requirements.txt
└── README.md
