import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os
from reuse import render_plot, plot_selection_terminal

# Database connection and data retrieval
conn = sqlite3.connect('DB/mydb.db')
cursor = conn.cursor()

query1 = """
SELECT * from final_stroke_cohort;
"""

df1 = pd.read_sql(query1, conn)

data = pd.DataFrame(df1, columns=["condition_occurrence_id", "person_id", "condition_concept_id", "condition_start_date", 
                                  "condition_end_date", "age", "gender_concept_id", "condition_descendant_concept_id", 
                                  "observation_start_date", "observation_end_date", "observation_period_id", "stroke_type", "gender"])

data['age'] = pd.to_numeric(data['age'], errors='coerce')
data = data.dropna(subset=['age', 'stroke_type'])


if len(data[data['stroke_type'] == 'ischemic']) == 0 or len(data[data['stroke_type'] == 'hemorrhagic']) == 0:
    print("One of the stroke types is missing in the dataset")

# Plotting gender distribution by stroke type
plt.figure(figsize=(12, 6))
sns.countplot(data=data, x='gender', hue='stroke_type')
plt.title('Gender Distribution by Stroke Type')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Gridlines for readability
plt.legend(title='Stroke Type', loc='upper right', fontsize=10, title_fontsize=11)

# Save plot
os.makedirs('figs/TEST_DB', exist_ok=True)
plt.savefig('figs/TEST_DB/second.png', dpi=300, bbox_inches='tight')

conn.close()

# Dictionary for plot paths
plot_paths = {
    "test_db": "figs/TEST_DB/second.png",
    "ohdsi": "figs/OHDSI/second.png"
}

# Run terminal-based selection
plot_selection_terminal(plot_paths)
