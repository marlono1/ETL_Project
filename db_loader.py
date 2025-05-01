# Import the pandas library so we can work with DataFrames
import pandas as pd

# psycopg2 is the PostgreSQL driver used under the hood
import psycopg2

# SQLAlchemy lets us connect to and interact with the database
from sqlalchemy import create_engine

def load_to_postgres(df, table_name, db_url):
    """
    Loads a pandas DataFrame into a PostgreSQL table.

    Parameters:
        df : Data that was imported from API/CSV/Excel and stored on Pandas
        table_name: The name of the table to write to in PostgreSQL
        db_url: The connection URL for the PostgreSQL database with user creadentials and database that is being accessed
                      
    """
    try:
        # Create a database engine (this manages the actual connection)
        engine = create_engine(db_url) # db_url is being retrieved from Main.py 
        
        # Use the engine to open a connection
        with engine.connect() as connection:
            # Write the DataFrame to a table in the database
            # if_exists='append' means: add more data if the current table does not have the latest info
            # index=False avoids writing DataFrame index as a column
            df.to_sql(table_name, con=connection, if_exists='append', index=False)

        print(f"✅ Data loaded into table '{table_name}' successfully!")

    except Exception as e:
        # Print an error message if anything goes wrong
        print(f"❌ Error loading data to PostgreSQL: {e}")

