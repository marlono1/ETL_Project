from ge_init import get_context
from data_loader import load_csv
from gx_validator import setup_validator, run_validation
from gx_expectations import customer_rules
from db_loader import load_to_postgres

def validate_csv(filepath, suite_name):   #Calls Function to Load CSV via Panda, push to GX cloud, launch Rules and Add, then validates rules vs dataAsset(CSV)

    context = get_context()     # connect to GX Cloud
    df = load_csv(filepath)     # Loads CSV to Panda to parse

    
    validator = setup_validator(                    #creates two variables, Validator to add rules to Expectaution Suite. 2nd is for GX to be able to store in there workspace
        context=context,                            #Connects to GX cloud
        df=df,                                      #reference of Database from Panda
        suite_name=suite_name,                      #Name of the Suite we are either generating or creating
        rules_func=customer_rules,                   #add rules from GX_Expectation Suite to add rules to GX Cloud Suite
        asset_name="Superstore_sales"                 #give our data asset a unique name in our data source for future reference
    )

    # Run checkpoint
    result = run_validation(validator)
    #result = run_checkpoint(context, batch_request, suite_name)     #Run Rules(Expectation Suite(validator) vs GX workspace(batch_request)) to verify data
    return result


#This functions runs if only this Script is ran first
if __name__ == "__main__":
    #Manually set the file path and suite name here
    filepath = "/home/mar/Downloads/CSV_ETL_without_checkpoint/supermarket_sales.csv"
    suite_name = "customer_expectation_suite"

    # Run validation process
    result = validate_csv(filepath, suite_name)
    print("Validation complete! Check GX Cloud for the results.")


# Inside your if __name__ == "__main__" block:

if result["success"]:   # GE validation success
    print("✅ Validation passed, now loading into PostgreSQL...")
    db_url = "postgresql+psycopg2://etl_user:etl@localhost:5432/etl_db"
    load_to_postgres(df, table_name="customer_data", db_url=db_url)
else:
    print("❌ Validation failed. Skipping load to PostgreSQL.")

