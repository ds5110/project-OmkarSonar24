import pandas as pd
import os
import sqlite3  
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to local SQLite database 
conn = sqlite3.connect('DB/mydb.db')  
cursor = conn.cursor()

# Sample query to fetch data from the local database 
query = """
SELECT * from concept ;
"""

# Fetch the data into a pandas DataFrame
df = pd.read_sql(query, conn)

print(df)