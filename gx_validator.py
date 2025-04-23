import great_expectations as gx
import os

    

def setup_validator(context, df, suite_name, asset_name, rules_func=None):
    #uploads batch request from Pandas(lame terms, moves Pandas data frame to GX cloud workspace
    # Use built-in GX Cloud fluent API for reading a DataFrame
    if df.empty:
        raise ValueError("❌ The provided DataFrame is empty. Please check the input file.")

    try:
        datasource = context.data_sources.get("pandas_default")
    except gx.exceptions.DataContextError:
        datasource = context.data_sources.add_pandas(name="pandas_default")
        
    batch = datasource.read_dataframe(df)
    validator = context.get_validator(batch=batch)
    
    try:
        suite = context.suites.get(suite_name)
        print(f"📂 Found existing suite in GX Cloud: '{suite_name}'")
        suite_already_exists = True
    except gx.exceptions.DataContextError:
        print(f"🆕 Creating new suite at GX Cloud path: '{suite_name}'")
        suite = context.suites.add(gx.core.ExpectationSuite(name=suite_name))
        suite_already_exists = False

    validator.expectation_suite_name = suite_name

    if rules_func:
        rules_func(validator)
        if not suite_already_exists:
            validator.save_expectation_suite()

    return validator        
            

def run_validation(validator):
    """
    Runs validation directly using the Fluent Validator object.
    Returns a result dictionary.
    """
    return validator.validate()
    """
    Runs validation using a temporary one-off checkpoint (GX Cloud compatible).
    This does NOT require batch_request and uses validator directly.
    """
    
#    context = validator._data_context
#    checkpoint = Checkpoint(
#        name="runtime_customer_checkpoint",
#        data_context=context,
#        validations=[
#            {
#                "batch": validator.active_batch,
#                "expectation_suite_name": validator.expectation_suite_name,
#            }
#        ],
#    )
#    return checkpoint.run()


def run_checkpoint(context, batch_request, suite_name, checkpoint_name="my_checkpoint"):
    checkpoint = context.add_or_update_checkpoint(	#creates a place to store results and runs validator
        name=checkpoint_name,
        validations=[{
            "batch_request": batch_request,			#Panda Database added to GX
            "expectation_suite_name": suite_name	#Great Expectations suite for rules to test against
        }]
    )
    return checkpoint.run()