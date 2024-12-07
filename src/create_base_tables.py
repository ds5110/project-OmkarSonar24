import redshift_connector

from queries import *
from utils import *


def create_tables():
    try:
        conn = redshift_connector.connect(
            host=host, port=port, database=dbname, user=user, password=password
        )
        print("Connected to Redshift")
        cursor = conn.cursor()
    except Exception as e:
        print(f"Error connecting to Redshift: {e}")
        return

    # Check existence and create cohorts
    for table_name, query in CREATE_TABLE_QUERY_MAP.items():
        try:
            # Check if the table exists
            check_query = f"""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = '{schema}' AND table_name = '{table_name}'
            );
            """
            cursor.execute(check_query)
            exists = cursor.fetchone()[0]

            if exists:
                print(
                    f"Table '{schema}.{table_name}' already exists. Skipping creation."
                )
            else:
                print(f"Table '{table_name}' does not exist. Creating it...")
                query = query.replace("schema_name", schema)
                cursor.execute(query)
                conn.commit()
                print(f"Table '{table_name}' created successfully.")

        except Exception as e:
            print(f"Error creating table '{table_name}': {e}")

    # Close the connection
    cursor.close()
    conn.close()
    print("Connection closed.")


# Run the script
if __name__ == "__main__":
    create_tables()
