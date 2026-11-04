import pandas as pd


df = pd.read_csv("data/processed/master_movies_stacked.csv")
print("Total movies in raw data:", len(df))


cols_to_keep = ["title", "genres", "imdb_rating", "budget_cr", "india_net_rev_cr", "rev_to_budget_ratio"]
df = df[cols_to_keep]
clean_df = df.dropna()
print("After removing empty values:", len(clean_df))


clean_df = clean_df[(clean_df["rev_to_budget_ratio"] >= 0.5) & (clean_df["rev_to_budget_ratio"] <= 20)]
clean_df = clean_df.reset_index(drop=True)
print("After ratio filter:", len(clean_df))


clean_df.to_csv("data/processed/clean_movies.csv", index=False)
print("Done! Saved as data/processed/clean_movies.csv")