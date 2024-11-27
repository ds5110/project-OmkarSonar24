import os
import sqlite3
import pandas as pd

def csv_to_sqlite(csv_folder, sqlite_db_path):
    """
    Reads all CSV files in the given folder and pushes their content to an SQLite3 database.
    Each table name matches the CSV file name (lowercase).
    
    Args:
        csv_folder (str): Path to the folder containing CSV files.
        sqlite_db_path (str): Path to the SQLite database file.
    """
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    
    # Loop through all CSV files in the folder
    for file in os.listdir(csv_folder):
        if file.endswith('.csv'):
            table_name = os.path.splitext(file)[0].lower()  # Extract file name and convert to lowercase
            
            # Read the CSV file into a DataFrame
            file_path = os.path.join(csv_folder, file)
            df = pd.read_csv(file_path)
            
            # Push data to SQLite database (create table if not exists)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Data from {file} inserted into table '{table_name}'")
    
    # Close the connection
    conn.commit()
    conn.close()
    print("All CSV files have been processed.")

# Example usage
csv_folder = "DB\DB_CSV_FILES"  
sqlite_db_path = "DB\mydb.db"  
csv_to_sqlite(csv_folder, sqlite_db_path)
