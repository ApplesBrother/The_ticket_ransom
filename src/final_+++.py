import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

FIG_DIR = "figures"  # saved outside data/, at the project root
os.makedirs(FIG_DIR, exist_ok=True)

# ==========================================
# 1. LOAD & CLEAN DATA
# ==========================================
df = pd.read_csv("data/processed/recalculated_data.csv")
df.columns = df.columns.str.strip()

df = df.rename(columns={
    "imdb_rating": "rating", 
    "budget_cr": "budget",
    "india_net_rev_cr": "revenue"
})

for col in ["rating", "budget", "revenue", "year"]:
    if df[col].dtype == 'object':
        df[col] = df[col].astype(str).str.replace(r'[₹$, ]', '', regex=True)
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["ratio"] = np.where(df["budget"] > 0, df["revenue"] / df["budget"], 0)
df = df.dropna(subset=["rating", "budget", "ratio", "year", "genres"])
df = df[df["budget"] > 0].copy()
df["year"] = df["year"].astype(int)

# ==========================================
# 2. APPLY HARDCODED FILTERS
# ==========================================
MIN_BUDGET, MAX_BUDGET = 0.5, 5000.0     # in Crores
MIN_REVENUE, MAX_REVENUE = 0.5, 5000.0  # in Crores
MIN_RATIO, MAX_RATIO = 0.05, 20.0

df = df[
    (df['budget'] >= MIN_BUDGET) & (df['budget'] <= MAX_BUDGET) &
    (df['revenue'] >= MIN_REVENUE) & (df['revenue'] <= MAX_REVENUE) &
    (df['ratio'] >= MIN_RATIO) & (df['ratio'] <= MAX_RATIO)
].copy()

# Sort genres by frequency to grab the top 7 for our 8-panel grids
top_7_genres = df['genres'].value_counts().head(7).index.tolist()
grid_panels = ['Overall'] + top_7_genres

# Sort all genres by median ratio for the single-panel charts
genre_order = df.groupby('genres')['ratio'].median().sort_values(ascending=False).index
df_log = df[df['ratio'] > 0].copy()

# Global min/max year for consistent X-axis across the time grid
min_yr, max_yr = df['year'].min(), df['year'].max()

sns.set_theme(style="whitegrid")

# ==========================================
# 3. PLOT 1 & 2: Bar Graphs (Median & Mean)
# ==========================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.barplot(data=df, x='genres', y='ratio', estimator=np.median, order=genre_order, errorbar=None, color='#4C72B0', ax=axes[0])
axes[0].set_title('Median ROI Ratio by Genre', fontweight='bold')
axes[0].axhline(1, color='red', linestyle='--')
axes[0].tick_params(axis='x', rotation=45)

sns.barplot(data=df, x='genres', y='ratio', estimator=np.mean, order=genre_order, errorbar=None, color='#DD8452', ax=axes[1])
axes[1].set_title('Average (Mean) ROI Ratio by Genre', fontweight='bold')
axes[1].axhline(1, color='red', linestyle='--')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "01_median_mean_roi_by_genre.png"), dpi=300, bbox_inches="tight")
plt.show()

# ==========================================
# 4. PLOT 3: 8-Panel Histogram (ROI Number Density)
# ==========================================
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
fig.suptitle('Number Density Distribution of ROI (Log Scale)', fontsize=16, fontweight='bold')
axes = axes.flatten()

for i, panel in enumerate(grid_panels):
    ax = axes[i]
    if panel == 'Overall':
        subset = df_log
        color = '#937860'
    else:
        subset = df_log[df_log['genres'] == panel]
        color = '#4C72B0'
        
    if not subset.empty:
        sns.histplot(data=subset, x='ratio', bins=20, log_scale=True, color=color, kde=True, ax=ax)
        
    ax.set_title(panel, fontweight='bold')
    ax.set_xlabel('ROI Ratio')
    ax.set_ylabel('Movies')
    ax.axvline(1, color='red', linestyle='--')

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "02_roi_histogram_by_genre.png"), dpi=300, bbox_inches="tight")
plt.show()

# ==========================================
# 5. PLOT 4: 8-Panel Bar Chart (Average ROI by Budget)
# ==========================================
bins = [0, 10, 30, 50, 100, 250, np.inf]
labels = ['0-10', '10-30', '30-50', '50-100', '100-250', '250+']
df['budget_section'] = pd.cut(df['budget'], bins=bins, labels=labels)

fig, axes = plt.subplots(2, 4, figsize=(20, 10))
fig.suptitle('Average ROI Ratio by Budget Section (in Crores)', fontsize=16, fontweight='bold')
axes = axes.flatten()

for i, panel in enumerate(grid_panels):
    ax = axes[i]
    if panel == 'Overall':
        subset = df
        color = '#55A868'
    else:
        subset = df[df['genres'] == panel]
        color = '#DD8452'
        
    if not subset.empty:
        sns.barplot(data=subset, x='budget_section', y='ratio', estimator=np.mean, errorbar=None, color=color, ax=ax)
        
    ax.set_title(panel, fontweight='bold')
    ax.set_xlabel('Budget Tiers')
    ax.set_ylabel('Mean ROI')
    ax.axhline(1, color='red', linestyle='--')
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "03_avg_roi_by_budget_section.png"), dpi=300, bbox_inches="tight")
plt.show()

# ==========================================
# 6. PLOT 5: Box Plot (Log Scale)
# ==========================================
plt.figure(figsize=(11, 6))
sns.boxplot(data=df_log, x='genres', y='ratio', order=genre_order, color='#8172B3', fliersize=4)
plt.title('Distribution of ROI Ratio by Genre (Log Scale)', fontsize=14, fontweight='bold')
plt.yscale('log')
plt.xticks(rotation=45)
plt.axhline(1, color='red', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "04_roi_boxplot_by_genre.png"), dpi=300, bbox_inches="tight")
plt.show()

# ==========================================
# 7. PLOT 6: Scatter (Rating vs Ratio - Log Scale)
# ==========================================
plt.figure(figsize=(11, 6))
sns.scatterplot(data=df_log, x='rating', y='ratio', hue='genres', alpha=0.7)
plt.title('ROI Ratio vs IMDb Rating (Log Scale)', fontsize=14, fontweight='bold')
plt.yscale('log')
plt.axhline(1, color='gray', linestyle='--')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "05_roi_vs_imdb_rating.png"), dpi=300, bbox_inches="tight")
plt.show()

# ==========================================
# 8. PLOT 7: 8-Panel Line Graph (Year vs Average Ratio - Log Scale)
# ==========================================
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
fig.suptitle('Average ROI Ratio Over Time (Log Scale)', fontsize=16, fontweight='bold')
axes = axes.flatten()

for i, panel in enumerate(grid_panels):
    ax = axes[i]
    if panel == 'Overall':
        subset = df_log
        color = 'black'
    else:
        subset = df_log[df_log['genres'] == panel]
        color = '#C44E52'
        
    if not subset.empty:
        sns.lineplot(data=subset, x='year', y='ratio', estimator=np.mean, errorbar=None, color=color, marker='o', linewidth=2, ax=ax)
        
    ax.set_title(panel, fontweight='bold')
    ax.set_xlabel('Release Year')
    ax.set_ylabel('Mean ROI (Log Scale)')
    ax.set_yscale('log')
    ax.axhline(1, color='red', linestyle='--')
    
    # Lock the X-axis across all panels so the timelines perfectly align
    ax.set_xlim(min_yr - 0.5, max_yr + 0.5)
    ax.set_xticks(range(min_yr, max_yr + 1))
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "06_avg_roi_over_time.png"), dpi=300, bbox_inches="tight")
plt.show()