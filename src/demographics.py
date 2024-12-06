import os
import redshift_connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import *
from queries import *

# Ensure the directory exists
os.makedirs('figs', exist_ok=True)

def create_tables():
    try:
        # Connect to Redshift
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

    try:
        # Fetch ischemic data
        cursor.execute(QUERY_FETCH_ISCHEMIC_ONLY_EDA.replace("schema_name", schema))
        df1 = cursor.fetch_dataframe()
        df1["stroke_type"] = "ischemic"

        cursor.execute(QUERY_FETCH_HAEMORRHAGIC_ONLY_EDA.replace("schema_name", schema))
        df2 = cursor.fetch_dataframe()
        df2["stroke_type"] = "hemorrhagic"

        # Combine data and process
        data = pd.concat([df1, df2], ignore_index=True)
        data["gender"] = data["gender_concept_id"].apply(
            lambda x: "male" if x == 8507 else "female"
        )

        # Process date columns
        date_cols = ['condition_start_date', 'condition_end_date']
        for col in date_cols:
            data[col] = pd.to_datetime(data[col], errors='coerce')

        # Plot 1: Age Distribution by Stroke Type
        plt.figure(figsize=(10, 6))
        sns.kdeplot(data=data, x='age', hue='stroke_type', fill=True)
        plt.title('Age Distribution by Stroke Type')
        plt.xlabel('Age')
        plt.ylabel('Density')
        plt.tight_layout()
        plt.savefig('figs/age_distribution_by_stroke_type.png')
        plt.show()

        # Process age groups
        age_bins = [18, 65, 85]
        age_labels = ['18-65', '65+']
        data['age_group'] = pd.cut(data['age'], bins=age_bins, labels=age_labels, right=False)

        # Table 1: Stroke distribution by age group
        age_group_counts = data.groupby(['age_group', 'stroke_type']).size().unstack(fill_value=0)
        total_age_group_counts = data.groupby('age_group').size()

        if '18-65' in total_age_group_counts.index and '65+' in total_age_group_counts.index:
            total_20_65 = total_age_group_counts['18-65']
            total_65_plus = total_age_group_counts['65+']
            percentage_20_65 = (total_20_65 / (total_20_65 + total_65_plus)) * 100
            percentage_65_plus = (total_65_plus / (total_20_65 + total_65_plus)) * 100

            ratio_data = pd.DataFrame({
                'Age Group': ['18-65', '65+'],
                'Stroke Possibility': [f'{percentage_20_65:.2f}%', f'{percentage_65_plus:.2f}%']
            })

            # Stroke type percentages
            total_strokes = data['stroke_type'].value_counts()
            total_stroke_count = total_strokes.sum()
            ischemic_percentage = (total_strokes['ischemic'] / total_stroke_count) * 100
            hemorrhagic_percentage = (total_strokes['hemorrhagic'] / total_stroke_count) * 100

            stroke_data = pd.DataFrame({
                'Stroke Type': ['Ischemic', 'Hemorrhagic'],
                'Count': [total_strokes['ischemic'], total_strokes['hemorrhagic']],
                'Percentage': [f'{ischemic_percentage:.2f}%', f'{hemorrhagic_percentage:.2f}%']
            })

            # Table 2: Stroke type distribution
            plt.figure(figsize=(12, 5))
            plt.axis('off')
            table = plt.table(
                cellText=stroke_data.values,
                colLabels=stroke_data.columns,
                loc='center',
                cellLoc='center',
                colColours=["#f2f2f2"] * 3
            )
            table.auto_set_font_size(False)
            table.set_fontsize(12)
            table.scale(1.5, 1.5)
            plt.tight_layout()
            plt.savefig('figs/stroke_type_distribution_table.png')
            plt.show()

            # Table 3: Stroke possibilities by age group
            plt.figure(figsize=(12, 5))
            plt.axis('off')
            ratio_table = plt.table(
                cellText=ratio_data.values,
                colLabels=ratio_data.columns,
                loc='center',
                cellLoc='center',
                colColours=["#f2f2f2"] * 2
            )
            ratio_table.auto_set_font_size(False)
            ratio_table.set_fontsize(12)
            ratio_table.scale(1.5, 1.5)
            plt.tight_layout()
            plt.savefig('figs/age_group_ratio_table.png')
            plt.show()
        else:
            print("Age groups '18-65' and/or '65+' are missing from the data!")

        # Plot 2: Gender Distribution by Stroke Type
        plt.figure(figsize=(12, 6))
        sns.countplot(data=data, x='gender', hue='stroke_type')
        plt.title('Gender Distribution by Stroke Type')
        plt.xlabel('Gender')
        plt.ylabel('Count')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(title='Stroke Type', loc='upper right', fontsize=10, title_fontsize=11)
        plt.tight_layout()
        plt.savefig('figs/gender_distribution_by_stroke_type.png')
        plt.show()

        # Plot 3: Age Distribution by Gender and Stroke Type
        fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharex=True)
        sns.kdeplot(data=data[data["gender"] == "male"], x="age", hue="stroke_type", fill=False, common_norm=False, alpha=0.6, linewidth=2, ax=axes[0])
        axes[0].set_title('Males: Age Distribution by Stroke Type')
        axes[0].set_xlabel('Age')
        axes[0].set_ylabel('Density')

        sns.kdeplot(data=data[data["gender"] == "female"], x="age", hue="stroke_type", fill=False, common_norm=False, alpha=0.6, linewidth=2, ax=axes[1])
        axes[1].set_title('Females: Age Distribution by Stroke Type')
        axes[1].set_xlabel('Age')
        axes[1].set_ylabel('Density')

        fig.suptitle('Age Distribution by Gender and Stroke Type (KDEs)', y=0.95)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig('figs/age_distribution_by_gender_and_stroke_type.png')
        plt.show()

    finally:
        # Ensure connection is closed
        conn.close()
        print("Connection closed.")

if __name__ == "__main__":
    create_tables()
