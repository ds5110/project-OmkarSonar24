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
cursor.execute(QUERY_FETCH_EDA_1.replace("schema_name", schema))
df1 = cursor.fetch_dataframe()
cursor.execute(QUERY_FETCH_EDA_2.replace("schema_name", schema))
df2 = cursor.fetch_dataframe()

sns.set_theme(style="whitegrid")

# Plotting a bar chart
plt.figure(figsize=(10, 6))
sns.barplot(data=df1, x="stroke_type", y="count", hue="stroke_type", palette="Blues_d")
plt.xticks(rotation=45, ha="right")
plt.title("Counts of Different Types of Strokes")
plt.xlabel("Stroke Type")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("figs/counts_of_different_types_of_strokes.png", bbox_inches="tight")

plt.figure(figsize=(8, 4))
sns.barplot(data=df2, x="stroke_type", y="count", hue="stroke_type", palette="Blues_d")
plt.xticks(rotation=45, ha="right")
plt.title("Counts of Different Types of Strokes")
plt.xlabel("Stroke Type")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("figs/counts_of_different_types_of_strokes_plot_2.png", bbox_inches="tight")
plt.show()

cursor.close()

conn.close()
