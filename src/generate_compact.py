import pandas as pd

def generate_compact_dataset(input_path="data/processed/master_movies_final.csv", output_path="data/processed/master_movies_compact.csv"):
    # Load the consolidated final dataset
    df = pd.read_csv(input_path)

    # Define the exact columns you want to keep
    target_columns = [
        'title', 
        'year', 
        'genres', 
        'budget_cr', 
        'india_net_rev_cr', 
        'source_file', 
        'rev_to_budget_ratio'
    ]

    # Filter and reorder columns, sorting alphabetically by title
    compact_df = df[target_columns].sort_values(by='title', ascending=True).reset_index(drop=True)

    # Save to processed folder
    compact_df.to_csv(output_path, index=False)

    print("=" * 60)
    print(f"Successfully generated compact dataset at {output_path}")
    print(f"Total Unique Movies: {len(compact_df)}")
    print("=" * 60)
    print(compact_df.notna().sum())

if __name__ == "__main__":
    generate_compact_dataset()
