import os
import pandas as pd
import redshift_connector
from queries import *
from utils import *
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap

# Ensure the directory exists
os.makedirs('figs', exist_ok=True)

# Connect to Redshift
try:
    conn = redshift_connector.connect(
        host=host,
        port=port,
        database=dbname,
        user=user,
        password=password
    )
    print("Connected to Redshift")
    cursor = conn.cursor()
except Exception as e:
    print(f"Error connecting to Redshift: {e}")
    exit()

# Fetch data
df1 = pd.read_sql(QUERY_FETCH_PROCEDURE_PLOT1_1.replace("schema_name", schema), conn)
df2 = pd.read_sql(QUERY_FETCH_PROCEDURE_PLOT1_2.replace("schema_name", schema), conn)

# Map procedure names
procedure_name_map_1 = {
    2314284: 'Strength exercises',
    2314294: 'Dynamic Activities',
    4203780: 'Respiratory Therapy',
    2314285: 'Neuromuscular Reeducation',
    2314287: 'Gait Training',
    2314297: 'Self-Care/Home Management Training',
    42627910: 'Occupational Therapy Evaluation, Medium Complexity',
    42627954: 'Occupational Therapy Evaluation, Low Complexity',
    2313701: 'Individual Speech/Language/Communication Treatment',
    2314290: 'Manual Therapy'
}
df1['concept_name'] = df1['procedure_concept_id'].map(procedure_name_map_1)

procedure_name_map_2 = {
    2314284  : 'Strength exercises',
    2314294    : 'Dynamic Activities',
    4203780    : 'Respiratory Therapy',
    2314285  : 'Neuromuscular Reeducation',
    2314287  : 'Gait Training',
    2314297  : 'Self-Care/Home Management Training',
    42627910  : 'Occupational Therapy Evaluation, Medium Complexity',
    42627954 : 'Occupational Therapy Evaluation, Low Complexity',
    2313701  : 'Individual Speech/Language/Communication Treatment',
    2314290  : 'Manual Therapy'
}
df2['concept_name'] = df2['procedure_concept_id'].map(procedure_name_map_2)
 
# Custom sum values for distinct person counts
sum_df1 = 30478  # Sum of distinct person count for df1
sum_df2 = 130604  # Sum of distinct person count for df2
 
# Calculate percentage for Haemorrhagic (df1) based on custom sum
df1['percentage'] = (df1['distinct_person_count'] / sum_df1) * 100
 
# Calculate percentage for Ischemic (df2) based on custom sum
df2['percentage'] = (df2['distinct_person_count'] / sum_df2) * 100
 
# Create a figure with two subplots (one for each stroke type) with independent y-axes
fig, axes = plt.subplots(1, 2, figsize=(18, 8), sharey=False)  # Increased figure size for better label space
 
# Plot for Haemorrhagic Stroke Procedures
sns.barplot(data=df1, x='concept_name', y='percentage', ax=axes[0], palette='Blues')  # Concept name on x, percentage on y
axes[0].set_title('Haemorrhagic Stroke Procedures', fontsize=18)  # Increased title font size
axes[0].set_xlabel('Procedure Name', fontsize=14)  # Increased x-axis label font size
axes[0].set_ylabel('Percentage of Distinct Person (%)', fontsize=14)  # Increased y-axis label font size
 
# Add distinct person count labels on top of the bars for Haemorrhagic
for idx, row in df1.iterrows():
    axes[0].text(idx, row['percentage'] + 0.05, f'{row["distinct_person_count"]}', ha='center', fontsize=12)  # Increased label font size
 
# Plot for Ischemic Stroke Procedures
sns.barplot(data=df2, x='concept_name', y='percentage', ax=axes[1], palette='Reds')  # Concept name on x, percentage on y
axes[1].set_title('Ischemic Stroke Procedures', fontsize=18)  # Increased title font size
axes[1].set_xlabel('Procedure Name', fontsize=14)  # Increased x-axis label font size
axes[1].set_ylabel('Percentage of Distinct Person (%)', fontsize=12)  # Increased y-axis label font size
 
# Add distinct person count labels on top of the bars for Ischemic
for idx, row in df2.iterrows():
    axes[1].text(idx, row['percentage'] + 0.05, f'{row["distinct_person_count"]}', ha='center', fontsize=12)  # Increased label font size
 
# Rotate x-axis labels for readability (Procedure names)
axes[0].tick_params(axis='x', rotation=45, labelsize=12)  # Increased font size for x-tick labels
axes[1].tick_params(axis='x', rotation=45, labelsize=12)  # Increased font size for x-tick labels
 
# Explicitly set x-tick labels for both subplots to avoid misalignment issues
axes[0].set_xticklabels(df1['concept_name'], rotation=45, ha='right', fontsize=14)  # Increased font size for x-tick labels
axes[1].set_xticklabels(df2['concept_name'], rotation=45, ha='right', fontsize=14)  # Increased font size for x-tick labels
 
# Adjust layout to ensure proper spacing for the x-axis labels
plt.tight_layout(pad=3.0)  # Added padding for better spacing around labels
 
# Save the plot to a file (high-quality output) without cutting off labels
plt.savefig("figs/stroke_procedures_plot_with_percentage_and_count.jpg", format='jpg', dpi=300, bbox_inches='tight', pad_inches=0.5)
 
# Show the plot
plt.show()