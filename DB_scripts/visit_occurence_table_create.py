import sqlite3

# Connect to the database
connection = sqlite3.connect('DB/mydb.db')
cursor = connection.cursor()

# SQL command to create the 'visit_occurence' table
create_table_query = '''
CREATE TABLE IF NOT EXISTS visit_occurence (
    visit_occurence_id INTEGER PRIMARY KEY,
    person_id INTEGER,
    visit_concept_id INTEGER,
    visit_start_date DATE,
    visit_start_datetime DATETIME,
    visit_end_date DATE,
    visit_end_datetime DATETIME,
    visit_type_concept_id INTEGER,
    provider_id INTEGER,
    care_site_id INTEGER,
    visit_source_value VARCHAR(100),
    visit_source_concept_id INTEGER,
    admitted_from_concept_id INTEGER,
    admitted_from_source_value VARCHAR(100),
    discharged_to_concept_id INTEGER,
    discharged_to_source_value VARCHAR(100),
    preceding_visit_occurence_id INTEGER,
    FOREIGN KEY (person_id) REFERENCES visit_detail (person_id),
    FOREIGN KEY (visit_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (visit_type_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (visit_source_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (admitted_from_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (discharged_to_concept_id) REFERENCES concept (concept_id)
)
'''

# Execute the command
cursor.execute(create_table_query)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Table 'visit_occurence' created successfully.")
