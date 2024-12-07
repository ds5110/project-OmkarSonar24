import json
import os

import matplotlib.pyplot as plt
import numpy as np
import redshift_connector
import seaborn as sns

from queries import *
from utils import *

# Ensure the directory exists
os.makedirs("figs", exist_ok=True)


def create_tables():
    try:
        # Connect to Redshift
        conn = redshift_connector.connect(
            host=host, port=port, database=dbname, user=user, password=password
        )
        print("Connected to Redshift")
        cursor = conn.cursor()
    except Exception as e:
        print(f"Error connecting to Redshift: {e}")
        return

    # Define filters
    unwanted_visit_concept_ids = {581458, 8809, 8668, 8650, 8850}
    target_set = {8782, 8717, 8920, 8870, 9201, 8971, 8546}  # Inpatient concept IDs

    try:
        print(f"Starting data fetch from OHDSI database")
        # Fetch data
        cursor.execute(
            QUERY_FETCH_HAEMORRHAGIC_ONLY_VISITS.replace("schema_name", schema)
        )
        haem_df = cursor.fetch_dataframe()
        print(f"Fetched Haemorrhagic Data")

        cursor.execute(QUERY_FETCH_ISCHEMIC_ONLY_VISITS.replace("schema_name", schema))
        isc_df = cursor.fetch_dataframe()
        print(f"Fetched Ischemic Data")

        # Drop unwanted visit types
        haem_df = haem_df.drop(
            haem_df[haem_df["visit_concept_id"].isin(unwanted_visit_concept_ids)].index
        )
        isc_df = isc_df.drop(
            isc_df[isc_df["visit_concept_id"].isin(unwanted_visit_concept_ids)].index
        )

        # Calculate First Discharges
        haem_first_discharges_df, haem_stats = get_first_admission_durations(haem_df)
        isc_first_discharges_df, isc_stats = get_first_admission_durations(isc_df)

        # Display statistics
        print(f"Haemorrhagic Stroke Stats-")
        print(json.dumps(haem_stats, indent=4))
        print(f"Ischemic Stroke Stats-")
        print(json.dumps(isc_stats, indent=4))

        # Filter for visualization (durations <= 100 days)
        hdf = haem_first_discharges_df[haem_first_discharges_df["duration"] <= 100]
        idf = isc_first_discharges_df[isc_first_discharges_df["duration"] <= 100]

        # Plot: First Discharge Duration Comparison
        plt.figure(figsize=(10, 6))
        plt.rcParams["figure.dpi"] = 150
        sns.kdeplot(hdf, x="duration", label="Haemorrhagic Stroke", color="orange")
        sns.kdeplot(idf, x="duration", label="Ischemic Stroke", color="blue")
        plt.legend()
        plt.title(f"Ischemic Vs Haemorrhagic First Discharge Duration (KDE Plot)")
        plt.xticks(np.arange(0, 110, 10))
        plt.xlabel("First Discharge Duration (days)")
        plt.tight_layout()
        plt.savefig("figs/ischemic_vs_haemorrhagic_discharge_duration_kde.png")
        plt.show()

    finally:
        # Close the connection
        cursor.close()
        conn.close()
        print("Connection closed.")


# Run the script
if __name__ == "__main__":
    create_tables()
