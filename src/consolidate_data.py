import pandas as pd
import numpy as np
import re

def normalize_title(s):
    if pd.isna(s):
        return ""
    return re.sub(r'[^a-z0-9]', '', str(s).lower())

def consolidate_movies(input_path="data/processed/master_movies_stacked.csv", output_path="data/processed/master_movies_final.csv"):
    df = pd.read_csv(input_path)
    
    # Create a normalized title key for grouping
    df['title_key'] = df['title'].apply(normalize_title)
    df = df[df['title_key'] != ""]

    # Define source reliability priority (Higher score = higher trust for financial figures)
    source_priority = {
        '06_shreyaumrao_bo2019_2023.csv': 3,
        '07_iima_bollywood.csv': 2,
        '05_ishajangir_bollywood.csv': 1
    }
    df['priority'] = df['source_file'].map(source_priority).fillna(1)

    # Sort by priority descending so the most reliable source comes first for each title
    df = df.sort_values(by=['title_key', 'priority'], ascending=[True, False])

    consolidated_rows = []

    for title_key, group in df.groupby('title_key'):
        # Combine all unique source files into an audit trail string
        sources_audit = " | ".join(group['source_file'].dropna().unique())
        
        # Take the best available values using the priority-sorted group
        # For numeric metrics, take the first non-null value (from highest priority source)
        # Or take median if you prefer blending. Here we take the highest priority source's numbers.
        best_row = group.iloc[0].copy()
        
        # If year, genres, rating, or votes are missing in top row but present in others, fill them
        best_row['year'] = group['year'].dropna().iloc[0] if len(group['year'].dropna()) > 0 else np.nan
        best_row['genres'] = group['genres'].dropna().iloc[0] if len(group['genres'].dropna()) > 0 else np.nan
        best_row['imdb_rating'] = group['imdb_rating'].dropna().iloc[0] if len(group['imdb_rating'].dropna()) > 0 else np.nan
        best_row['imdb_votes'] = group['imdb_votes'].dropna().iloc[0] if len(group['imdb_votes'].dropna()) > 0 else np.nan
        
        # Assign the audit trail to source_file
        best_row['source_file'] = sources_audit
        
        consolidated_rows.append(best_row)

    final_df = pd.DataFrame(consolidated_rows)

    # Recalculate final revenue and revenue-to-budget ratio to ensure mathematical consistency
    final_df['final_revenue_cr'] = (
        final_df['worldwide_rev_cr']
        .fillna(final_df['india_gross_rev_cr'])
        .fillna(final_df['india_net_rev_cr'])
    )

    final_df['rev_to_budget_ratio'] = np.where(
        (final_df['budget_cr'] > 0) & (final_df['final_revenue_cr'] > 0),
        (final_df['final_revenue_cr'] / final_df['budget_cr']).round(3),
        np.nan
    )

    # Clean up temporary columns and sort alphabetically by title
    cols_order = [
        'title', 'year', 'genres', 'imdb_rating', 'imdb_votes',
        'budget_cr', 'worldwide_rev_cr', 'india_gross_rev_cr',
        'india_net_rev_cr', 'overseas_rev_cr', 'final_revenue_cr',
        'rev_to_budget_ratio', 'source_file'
    ]
    
    final_master = final_df[cols_order].sort_values(by='title', ascending=True).reset_index(drop=True)
    final_master.to_csv(output_path, index=False)

    print("=" * 60)
    print(f"Successfully consolidated dataset saved to {output_path}")
    print(f"Total Unique Movies after merging duplicates: {len(final_master)}")
    print("=" * 60)
    print(final_master.notna().sum())

if __name__ == "__main__":
    consolidate_movies()
