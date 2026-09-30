import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Global style settings for scientific publication
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'figure.dpi': 300
})

# Create directory to save individual figures if needed
output_dir = 'figures'
os.makedirs(output_dir, exist_ok=True)

# 1. Load dataset
df = pd.read_csv('dataset.csv')
features = ['L_LAB_AVG', 'A_LAB_AVG', 'B_LAB_AVG']
X = df[features].copy()

# 2. Standardize features for KMeans clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Perform KMeans clustering with k=3
kmeans = KMeans(n_clusters=3, random_state=42, n_init=20)
clusters = kmeans.fit_predict(X_scaled)
df['Cluster_Raw'] = clusters

# Order clusters based on average a* value (green -> yellowish/intermediate -> red)
# In CIELAB space, a* indicates redness (positive) vs greenness (negative)
cluster_order = df.groupby('Cluster_Raw')['A_LAB_AVG'].mean().sort_values().index

stage_names = {
    cluster_order[0]: 'Unripe',
    cluster_order[1]: 'Medium',
    cluster_order[2]: 'Ripe'
}

stage_levels = ['Unripe', 'Medium', 'Ripe']
df['Maturity_Stage'] = df['Cluster_Raw'].map(stage_names)

# Save updated dataset with 3-class classification
output_csv = 'dataset_classificado.csv'
df.to_csv(output_csv, index=False)
print("Classification complete. Updated CSV saved to:", output_csv)

# Print descriptive statistics per maturity group
summary = df.groupby('Maturity_Stage')[features].agg(['count', 'mean', 'std']).round(2)
print("\n--- Summary Statistics by Maturity Stage ---")
print(summary.to_string())

# Color palette corresponding to tomato maturity: Unripe (green), Medium (orange-amber), Ripe (red)
palette = {
    'Unripe': '#2ca02c',
    'Medium': '#ff7f0e',
    'Ripe': '#d62728'
}

# --- 4. Individual Figures Generation (High-Resolution 300 DPI) ---

# Figure 1: 3D Scatter Plot in CIELAB Color Space
fig1 = plt.figure(figsize=(8, 6))
ax1 = fig1.add_subplot(1, 1, 1, projection='3d')
for stage in stage_levels:
    subset = df[df['Maturity_Stage'] == stage]
    ax1.scatter(
        subset['A_LAB_AVG'], subset['B_LAB_AVG'], subset['L_LAB_AVG'],
        c=palette[stage], label=stage, s=50, alpha=0.85, edgecolors='k', linewidth=0.4
    )
ax1.set_xlabel('a* (Green [-] to Red [+])', labelpad=8)
ax1.set_ylabel('b* (Blue [-] to Yellow [+])', labelpad=8)
ax1.set_zlabel('L* (Lightness)', labelpad=8)
ax1.set_title('3D CIELAB Color Space Representation by Maturity Stage', fontweight='bold', pad=15)
ax1.legend(title='Maturity Stage', loc='upper left', framealpha=0.9)
ax1.view_init(elev=20, azim=130)
fig1.tight_layout()
fig1.savefig(os.path.join(output_dir, 'fig1_cielab_3d_scatter.png'), dpi=300, bbox_inches='tight')
fig1.savefig(os.path.join(output_dir, 'fig1_cielab_3d_scatter.pdf'), bbox_inches='tight')
plt.close(fig1)

# Figure 2: Chromaticity Diagram (a* vs b*)
fig2, ax2 = plt.subplots(figsize=(7, 6))
sns.scatterplot(
    data=df, x='A_LAB_AVG', y='B_LAB_AVG', hue='Maturity_Stage',
    hue_order=stage_levels, palette=palette, style='Maturity_Stage',
    s=75, alpha=0.9, edgecolor='black', linewidth=0.5, ax=ax2
)
ax2.set_xlabel('a* Coordinate (Redness)')
ax2.set_ylabel('b* Coordinate (Yellowness)')
ax2.set_title('Chromaticity Projection (a* vs. b*)', fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(title='Maturity Stage', frameon=True)
fig2.tight_layout()
fig2.savefig(os.path.join(output_dir, 'fig2_chromaticity_a_vs_b.png'), dpi=300, bbox_inches='tight')
fig2.savefig(os.path.join(output_dir, 'fig2_chromaticity_a_vs_b.pdf'), bbox_inches='tight')
plt.close(fig2)

# Figure 3: Boxplot of CIELAB Coordinates across Stages
fig3, ax3 = plt.subplots(figsize=(8, 6))
df_melted = pd.melt(
    df, id_vars=['Maturity_Stage'], value_vars=features,
    var_name='CIELAB_Parameter', value_name='Value'
)
sns.boxplot(
    data=df_melted, x='CIELAB_Parameter', y='Value', hue='Maturity_Stage',
    hue_order=stage_levels, palette=palette, ax=ax3, fliersize=3
)
ax3.set_xlabel('CIELAB Color Coordinates')
ax3.set_ylabel('Measured Coordinate Value')
ax3.set_title('Distribution of CIELAB Coordinates across Maturity Stages', fontweight='bold')
ax3.grid(True, linestyle='--', alpha=0.5)
ax3.legend(title='Maturity Stage', frameon=True)
fig3.tight_layout()
fig3.savefig(os.path.join(output_dir, 'fig3_cielab_boxplot.png'), dpi=300, bbox_inches='tight')
fig3.savefig(os.path.join(output_dir, 'fig3_cielab_boxplot.pdf'), bbox_inches='tight')
plt.close(fig3)

# Figure 4: Lightness vs Redness (L* vs a*)
fig4, ax4 = plt.subplots(figsize=(7, 6))
sns.scatterplot(
    data=df, x='A_LAB_AVG', y='L_LAB_AVG', hue='Maturity_Stage',
    hue_order=stage_levels, palette=palette, style='Maturity_Stage',
    s=75, alpha=0.9, edgecolor='black', linewidth=0.5, ax=ax4
)
ax4.set_xlabel('a* Coordinate (Redness)')
ax4.set_ylabel('L* Coordinate (Lightness)')
ax4.set_title('Lightness vs. Redness Correlation (L* vs. a*)', fontweight='bold')
ax4.grid(True, linestyle='--', alpha=0.5)
ax4.legend(title='Maturity Stage', frameon=True)
fig4.tight_layout()
fig4.savefig(os.path.join(output_dir, 'fig4_lightness_vs_redness.png'), dpi=300, bbox_inches='tight')
fig4.savefig(os.path.join(output_dir, 'fig4_lightness_vs_redness.pdf'), bbox_inches='tight')
plt.close(fig4)

print("\nAll individual figures saved successfully in PNG (300 DPI) and PDF vector formats in 'figures/' folder.")
