import pandas as pd
import great_expectations as ge
import pyarrow
import os
from ge_init import get_context

context = get_context()
print(f"Loaded GX context: {type(context).__name__}")


#location of file
#DO NOT USE BACKLASHES ****
#csv = open("C:\Users\Kameleon\Downloads\supermarket_sales.csv", "r")
#*******
csv = "C:/Users/Kameleon/Downloads/supermarket_sales.csv"

try:                    #attempt and if runs into issues do this instead
    de = pd.read_csv(
                    csv,
                    on_bad_lines="error",
                    delimiter=",",
                    encoding="utf-8",   #language of the gods(english only characters)
                    dtype={"gross income": "float64"}
                   )   #loads into Dataframe
    print(de.head())      #prints only first 5 rows

except FileNotFoundError as e:
    print(f"Error: The file was not found. Check the file path. {e}")

except pd.errors.EmptyDataError as e:
    print(f"Error: The CSV file is empty. {e}")
    
except pd.errors.ParserError as e:
    print(f"Error: Malformed CSV file (delimiter or structure issue, {e}")

except UnicodeDecodeError as e:
    print(f"Error: Encoding issue. Try using 'ISO-8859-1' or detecting encoding, {e}")

if 'de' in locals(): #locals is temp place of variables stored while script is ran
    
    #data.to_parquet('convert.parquet')
  #  print(de.head())      #prints only first 5 rows
 #   print(de.tail())      #prints only last 5 rows
  #  print(de.dtypes)      #print data types from csv

    #Great Expecatations sample transfer for validating
    context = ge.get_context()                                                  # create workspace for managing data, validating rules and results
    print(type(context))  #test to see if im running this on RAM(EphemeralDataContext) or File-Based(On Disk)
    data_source_name = "supermarket_sales"                                      # Name of database on GX
    data_sources = context.data_sources.add_pandas(name=data_source_name)       # add pandas to datasource
    data_asset = data_sources.add_dataframe_asset(name="my_dataframe_asset")    # adds dataframe to validate
    batch_request = data_asset.build_batch_request(options ={"dataframe":de})                # Inform which pandas database is being validated -*-*-*-*-*
    expectation_suite_name = "my_expectation_suite"                             #Great Expextations Workspace for all Databases in GE to be accessible


    #Expectation Suite is where the rules you wish to test againsnt your databases    
    try:
    # Try to load the suite by name
        expectation_suite = context.get_expectation_suite("my_expectation_suite")
        print("✅ Loaded existing expectation suite.")
    except ge.exceptions.DataContextError:
    # If it doesn't exist, create it
        expectation_suite = context.create_expectation_suite("my_expectation_suite")
        print("🆕 Created a new expectation suite.")  #load "Rules" named my_expectation_suite, otherwise create for suite called my_expectation_suite


   #Generates Validator for checking if data is correct on Expactation Suite Pass/Fail
    validator = context.get_validator(                                          
    batch_request=batch_request,
    expectation_suite=expectation_suite
                                      )
            
    #this is a rule just added to check against database, example ensures "Invoice ID" column has no null values and all are populated
    validator.expect_column_values_to_not_be_null(column="Invoice ID")

    #Saves Results in Expecatations Suites to have for future usage. ^^^^this up here before^^^^
    validator.save_expectation_suite()


    #runs Validator again rules in Expectation Suite and the creates a checkpoint to save results for view later
    checkpoint = context.add_or_update_checkpoint(  #creates Checkpoint and validates info
    name="my_validation_checkpoint",
    validations=[{
        "batch_request": batch_request,             #calls on Panda database from above*-*-*-*-*-*-*
        "expectation_suite_name": suite_name        #checks rules from Expectations Suite
                }]
                                                )

    #retrieve Results from Checkpoint variable
    result = checkpoint.run()

    print(result)

    

    
