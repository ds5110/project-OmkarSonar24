import os
import pandas as pd
import redshift_connector
from queries import *
from utils import *
import matplotlib.pyplot as plt
import seaborn as sns

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
df1 = pd.read_sql(QUERY_FETCH_EDA_1.replace("schema_name", schema), conn)
df2 = pd.read_sql(QUERY_FETCH_EDA_2.replace("schema_name", schema), conn)

sns.set(style="whitegrid")

# Plotting a bar chart
plt.figure(figsize=(12, 6))
sns.barplot(data=df1, x='stroke_type', y='count', palette='Blues_d')
plt.xticks(rotation=45, ha='right')
plt.title("Counts of Different Types of Strokes")
plt.xlabel("Stroke Type")
plt.ylabel("Count")
plt.savefig("figs/counts_of_different_types_of_strokes.png", bbox_inches='tight')
plt.show()

sns.set(style="whitegrid")


plt.figure(figsize=(12, 6))
sns.barplot(data=df2, x='stroke_type', y='count', palette='Blues_d')
plt.xticks(rotation=45, ha='right')
plt.title("Counts of Different Types of Strokes")
plt.xlabel("Stroke Type")
plt.ylabel("Count")


plt.savefig("figs/counts_of_different_types_of_strokes_plot_2.png", bbox_inches='tight')


plt.show()

cursor.close()

conn.close()