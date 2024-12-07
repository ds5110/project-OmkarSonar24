import os

import matplotlib.pyplot as plt
import pandas as pd
import redshift_connector
import seaborn as sns

from queries import *
from utils import *

# Ensure the directory exists
os.makedirs("figs", exist_ok=True)

# Connect to Redshift
try:
    conn = redshift_connector.connect(
        host=host, port=port, database=dbname, user=user, password=password
    )
    print("Connected to Redshift")
    cursor = conn.cursor()
except Exception as e:
    print(f"Error connecting to Redshift: {e}")
    exit()

# Fetch data
cursor.execute(QUERY_FETCH_PROCEDURE_PLOT2_1.replace("schema_name", schema))
df1 = cursor.fetch_dataframe()
cursor.execute(QUERY_FETCH_PROCEDURE_PLOT2_2.replace("schema_name", schema))
df2 = cursor.fetch_dataframe()

# Aggregating data by procedure category for Haemorrhagic Stroke Cohort
df1_category_count = df1.groupby("procedure_category")["procedure_count"].sum()

# Aggregating data by procedure category for Ischemic Stroke Cohort
df2_category_count = df2.groupby("procedure_category")["procedure_count"].sum()

# Create a figure for Haemorrhagic Stroke Cohort Pie Chart
colors_haemorrhagic = sns.light_palette("seagreen", n_colors=len(df1_category_count))

plt.figure(figsize=(10, 7))
plt.pie(
    df1_category_count,
    labels=df1_category_count.index,
    autopct="%.2f%%",
    colors=colors_haemorrhagic,
    textprops={"fontsize": 14},
)
plt.title("Distribution of Procedures for Haemorrhagic Stroke Cohort", fontsize=16)
plt.savefig(
    "figs/procedures_distribution_haemorrhagic_stroke_pie_chart.png",
    format="png",
    bbox_inches="tight",
    dpi=300,
)
plt.tight_layout()
plt.show()

# Create a figure for Ischemic Stroke Cohort Pie Chart
colors_ischemic = sns.light_palette("#79C", n_colors=len(df2_category_count))

plt.figure(figsize=(10, 7))
plt.pie(
    df2_category_count,
    labels=df2_category_count.index,
    autopct="%.2f%%",
    colors=colors_ischemic,
    textprops={"fontsize": 14},
)
plt.title("Distribution of Procedures for Ischemic Stroke Cohort", fontsize=16)
plt.savefig(
    "figs/procedures_distribution_ischemic_stroke_pie_chart.png",
    format="png",
    bbox_inches="tight",
    dpi=300,
)
plt.tight_layout()
plt.show()
