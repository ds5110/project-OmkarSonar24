import redshift_connector
import pandas as pd
import numpy as np
import redshift_connector
import matplotlib.pyplot as plt
import seaborn as sns
import json
from utils import *
from queries import *

def create_tables():
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
        return
    
    unwanted_visit_concept_ids = {581458, 8809, 8668, 8650, 8850}
    target_set = {8782, 8717, 8920, 8870, 9201, 8971, 8546} # Inpatient concept ids

    print(f"Starting data fetch from OHDSI database")
    cursor.execute(QUERY_FETCH_HAEMORRHAGIC_ONLY_VISITS.replace("schema_name", schema))
    haem_df = cursor.fetch_dataframe()
    print(f"Fetched Haemorrhagic Data")
    cursor.execute(QUERY_FETCH_ISCHEMIC_ONLY_VISITS.replace("schema_name", schema))
    isc_df = cursor.fetch_dataframe()
    print(f"Fetched complete data from OHDSI database")

    # Drop unwanted visit_types - Pharmacy Visit, Independent Laboratory, Ambulance - Land, Birthing Center, Ambulance - Air or Water
    haem_df = haem_df.drop(haem_df[haem_df["visit_concept_id"].isin(unwanted_visit_concept_ids)].index)
    isc_df = isc_df.drop(isc_df[isc_df["visit_concept_id"].isin(unwanted_visit_concept_ids)].index)

    # Calculate First Discharges
    haem_first_discharges_df, haem_stats = get_first_admission_durations(haem_df)
    isc_first_discharges_df, isc_stats = get_first_admission_durations(isc_df)    

    print(f"Haemorrhagic Stroke Stats-")
    print(json.dumps(haem_stats, indent=4))
    print(f"Ischemic Stroke Stats-")
    print(json.dumps(isc_stats, indent=4))

    hdf = haem_first_discharges_df[haem_first_discharges_df["duration"]<=100]
    idf = isc_first_discharges_df[isc_first_discharges_df["duration"]<=100]

    # First Discharge Duration Comparison
    plt.figure(figsize=(10, 6))
    plt.rcParams["figure.dpi"] = 150
    sns.kdeplot(hdf, x="duration", label="Haemorrhagic Stroke", color="orange")
    sns.kdeplot(idf, x="duration", label="Ischemic Stroke", color="blue")
    plt.legend()
    plt.title(f"Ischemic Vs Haemorrhagic KDE Plot")
    plt.xticks(np.arange(0, 110, 10))
    plt.xlabel("first_discharge_duration(days)");

    haem_discharges_df = haem_df.groupby("discharge_to_concept_name", as_index=False).agg(person_count=("person_id", pd.Series.nunique))
    haem_discharges_df = haem_discharges_df.sort_values("person_count", ascending=False)
    isc_discharges_df = isc_df.groupby("discharge_to_concept_name", as_index=False).agg(person_count=("person_id", pd.Series.nunique))
    isc_discharges_df = isc_discharges_df.sort_values("person_count", ascending=False)
    

    

    # Close the connection
    cursor.close()
    conn.close()
    print("Connection closed.")

# Run the script
if __name__ == "__main__":
    create_tables()
