import pandas as pd
import numpy as np

def filter_and_strip_year(input_path="data/processed/master_movies_compact.csv", output_path="data/processed/master_movies_analysis_ready.csv"):
    # Load the compact dataset
    df = pd.read_csv(input_path)
    
    # Define columns that must be fully available
    required_cols = ['title', 'genres', 'budget_cr', 'india_net_rev_cr', 'source_file']
    
    # Keep only rows where all required columns have non-null values
    df_filtered = df.dropna(subset=required_cols).copy()
    
    # Strip away the 'year' column
    if 'year' in df_filtered.columns:
        df_filtered = df_filtered.drop(columns=['year'])
        
    # Recalculate rev_to_budget_ratio based on india_net_rev_cr and budget_cr for consistency
    df_filtered['rev_to_budget_ratio'] = (df_filtered['india_net_rev_cr'] / df_filtered['budget_cr']).round(3)

    # Sort alphabetically by movie title (A to Z)
    df_filtered = df_filtered.sort_values(by='title', ascending=True).reset_index(drop=True)
    
    # Save to processed folder
    df_filtered.to_csv(output_path, index=False)
    
    print("=" * 60)
    print(f"Analysis-ready subset saved to {output_path}")
    print(f"Total fully available rows: {len(df_filtered)}")
    print("=" * 60)
    print(df_filtered.notna().sum())

if __name__ == "__main__":
    filter_and_strip_year()
