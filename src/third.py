import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os
from reuse import render_plot, plot_selection_terminal

# Database connection and data retrieval
conn = sqlite3.connect('DB/mydb.db')

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

# Validate data for male and female groups
filtered_male_data = data[(data["gender"] == "male") & (data["stroke_type"].notnull())]
filtered_female_data = data[(data["gender"] == "female") & (data["stroke_type"].notnull())]

fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharex=True)

# KDE for males (if data exists)
if not filtered_male_data.empty:
    sns.kdeplot(
        data=filtered_male_data, 
        x="age", 
        hue="stroke_type", 
        fill=False, 
        common_norm=False, 
        alpha=0.6, 
        linewidth=2, 
        ax=axes[0]
    )
    axes[0].set_title('Males: Age Distribution by Stroke Type')
    axes[0].set_xlabel('Age')
    axes[0].set_ylabel('Density')
else:
    axes[0].text(0.5, 0.5, 'No data for males', horizontalalignment='center', verticalalignment='center')
    axes[0].set_title('Males: No Data Available')

# KDE for females (if data exists)
if not filtered_female_data.empty:
    sns.kdeplot(
        data=filtered_female_data, 
        x="age", 
        hue="stroke_type", 
        fill=False, 
        common_norm=False, 
        alpha=0.6, 
        linewidth=2, 
        ax=axes[1]
    )
    axes[1].set_title('Females: Age Distribution by Stroke Type')
    axes[1].set_xlabel('Age')
    axes[1].set_ylabel('Density')
else:
    axes[1].text(0.5, 0.5, 'No data for females', horizontalalignment='center', verticalalignment='center')
    axes[1].set_title('Females: No Data Available')

# Finalizing layout and saving
fig.suptitle('Age Distribution by Gender and Stroke Type (KDEs)', y=0.95)
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save plot
os.makedirs('figs/TEST_DB', exist_ok=True)
plt.savefig('figs/TEST_DB/third.png', dpi=300, bbox_inches='tight')

conn.close()

# Plot paths dictionary
plot_paths = {
    "test_db": "figs/TEST_DB/third.png", 
    "ohdsi": "figs/OHDSI/third.png"
}

# Run terminal-based selection
plot_selection_terminal(plot_paths)
