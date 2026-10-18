import os
import re
import pandas as pd
import numpy as np

def normalize_title(s):
    if pd.isna(s):
        return ""
    return re.sub(r'[^a-z0-9]', '', str(s).lower())

def extract_year(s):
    if pd.isna(s):
        return np.nan
    s_str = str(s).strip()
    match = re.search(r'(19\d{2}|20\d{2})', s_str)
    if match:
        return int(match.group(1))
    dt = pd.to_datetime(s_str, errors='coerce')
    return int(dt.year) if pd.notna(dt) else np.nan

def clean_num(val):
    if pd.isna(val):
        return np.nan
    s = str(val).lower().replace(',', '').strip()
    if 'n.a' in s or s == '':
        return np.nan
    match = re.search(r'(\d+\.?\d*)', s)
    if not match:
        return np.nan
    num = float(match.group(1))
    return num if num > 0 else np.nan

def build_combined_master():
    os.makedirs("data/processed", exist_ok=True)

    # 1. Build IMDb Metadata Lookup (from sources 03 & 04) to enrich rows
    df3 = pd.read_csv("data/raw/03_dhirajbembade_imdb_india.csv", encoding_errors="ignore")
    meta3 = pd.DataFrame({
        'title_key': df3['Name'].apply(normalize_title),
        'year_meta': df3['Year'].apply(extract_year),
        'genres_meta': df3['Genre'].astype(str).str.strip().replace('nan', np.nan),
        'imdb_rating': pd.to_numeric(df3['Rating'], errors='coerce'),
        'imdb_votes': df3['Votes'].apply(clean_num)
    })

    df4 = pd.read_csv("data/raw/04_adrianmcmahon_imdb_950.csv", encoding_errors="ignore")
    meta4 = pd.DataFrame({
        'title_key': df4['Name'].apply(normalize_title),
        'year_meta': df4['Year'].apply(extract_year),
        'genres_meta': np.nan,
        'imdb_rating': pd.to_numeric(df4['Rating'], errors='coerce'),
        'imdb_votes': pd.to_numeric(df4['Votes'], errors='coerce')
    })

    meta_all = pd.concat([meta3, meta4], ignore_index=True)
    meta_all = meta_all[meta_all['title_key'] != ""]
    meta_title_only = meta_all.drop_duplicates(subset=['title_key'])

    # 2. Load Source 05: ishajangir (Values in raw INR -> divide by 1e7 for Crores)
    df5 = pd.read_csv("data/raw/05_ishajangir_bollywood.csv", encoding_errors="ignore")
    s5 = pd.DataFrame({
        'title': df5['Movie_Name'].astype(str).str.strip(),
        'year': np.nan,
        'genres': df5['Genre'].astype(str).str.strip().str.title().replace('Nan', np.nan),
        'budget_cr': (pd.to_numeric(df5['Budget(INR)'], errors='coerce') / 1e7).round(4),
        'worldwide_rev_cr': np.nan,
        'india_gross_rev_cr': np.nan,
        'india_net_rev_cr': (pd.to_numeric(df5['Revenue(INR)'], errors='coerce') / 1e7).round(4),
        'overseas_rev_cr': np.nan,
        'source_file': '05_ishajangir_bollywood.csv'
    })

    # 3. Load Source 06: shreyaumrao (2019-2023 Box Office in Crores)
    df6 = pd.read_csv("data/raw/06_shreyaumrao_bo2019_2023.csv", encoding_errors="ignore")
    s6 = pd.DataFrame({
        'title': df6['Movie'].astype(str).str.strip(),
        'year': df6['Released Date'].apply(extract_year),
        'genres': np.nan,
        'budget_cr': df6['Budget'].apply(clean_num),
        'worldwide_rev_cr': df6['Worldwide'].apply(clean_num),
        'india_gross_rev_cr': df6['India Gross'].apply(clean_num),
        'india_net_rev_cr': df6['India Hindi Net'].apply(clean_num),
        'overseas_rev_cr': df6['Overseas'].apply(clean_num),
        'source_file': '06_shreyaumrao_bo2019_2023.csv'
    })

    # 4. Load Source 07: IIMA bollywood (149 rows, in Crores)
    df7 = pd.read_csv("data/raw/07_iima_bollywood.csv", encoding_errors="ignore")
    s7 = pd.DataFrame({
        'title': df7['MovieName'].astype(str).str.strip(),
        'year': df7['Release Date'].apply(extract_year),
        'genres': df7['Genre'].astype(str).str.strip().str.title().replace('Nan', np.nan),
        'budget_cr': df7['Budget'].apply(clean_num),
        'worldwide_rev_cr': np.nan,
        'india_gross_rev_cr': np.nan,
        'india_net_rev_cr': df7['BoxOfficeCollection'].apply(clean_num),
        'overseas_rev_cr': np.nan,
        'source_file': '07_iima_bollywood.csv'
    })

    # Combine all rows without dropping duplicates
    combined = pd.concat([s5, s6, s7], ignore_index=True)
    combined['title_key'] = combined['title'].apply(normalize_title)
    combined = combined[combined['title_key'] != ""]

    # Enrich with IMDb ratings and votes
    combined = pd.merge(
        combined,
        meta_title_only[['title_key', 'genres_meta', 'imdb_rating', 'imdb_votes']],
        on='title_key',
        how='left'
    )

    combined['genres'] = combined['genres'].fillna(combined['genres_meta'])
    combined.drop(columns=['title_key', 'genres_meta'], inplace=True)

    # Compute Final Revenue & Revenue-to-Budget Ratio
    combined['final_revenue_cr'] = (
        combined['worldwide_rev_cr']
        .fillna(combined['india_gross_rev_cr'])
        .fillna(combined['india_net_rev_cr'])
    )

    combined['rev_to_budget_ratio'] = np.where(
        (combined['budget_cr'] > 0) & (combined['final_revenue_cr'] > 0),
        (combined['final_revenue_cr'] / combined['budget_cr']).round(3),
        np.nan
    )

    cols_order = [
        'title', 'year', 'genres', 'imdb_rating', 'imdb_votes',
        'budget_cr', 'worldwide_rev_cr', 'india_gross_rev_cr',
        'india_net_rev_cr', 'overseas_rev_cr', 'final_revenue_cr',
        'rev_to_budget_ratio', 'source_file'
    ]

    # Sort alphabetically by title (A to Z)
    master = combined[cols_order].sort_values(by='title', ascending=True)
    master.to_csv("data/processed/master_movies_stacked.csv", index=False)

    print("=" * 60)
    print(f"Created data/processed/master_movies_stacked.csv | Total Rows: {len(master)}")
    print("=" * 60)
    print("\nRows per Source File:")
    print(master['source_file'].value_counts())
    print("\nNon-Empty Counts Per Column:")
    print(master.notna().sum())

if __name__ == "__main__":
    build_combined_master()
