import sqlite3

# Connect to the database
connection = sqlite3.connect('mydb.db')
cursor = connection.cursor()

# SQL command to create the 'visit_detail' table
create_table_query = '''
CREATE TABLE IF NOT EXISTS visit_detail (
    visit_detail_id INTEGER PRIMARY KEY,
    person_id INTEGER,
    visit_detail_concept_id INTEGER,
    visit_detail_start_date DATE,
    visit_detail_start_datetime DATETIME,
    visit_detail_end_date DATE,
    visit_detail_end_datetime DATETIME,
    visit_detail_type_concept_id INTEGER,
    provider_id INTEGER,
    care_site_id INTEGER,
    visit_detail_source_value VARCHAR(100),
    visit_detail_source_concept_id INTEGER,
    admitted_from_concept_id INTEGER,
    admitted_from_source_value VARCHAR(100),
    discharged_to_source_value VARCHAR(100),
    discharged_to_concept_id INTEGER,
    preceding_visit_detail_id INTEGER,
    parent_visit_detail_id INTEGER,
    visit_occurence_id INTEGER,
    FOREIGN KEY (visit_detail_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (visit_detail_type_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (visit_detail_source_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (admitted_from_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (discharged_to_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (visit_occurence_id) REFERENCES visit_occurence (visit_occurence_id)
)
'''

# Execute the command
cursor.execute(create_table_query)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Table 'visit_detail' created successfully.")
