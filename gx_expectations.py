#custom rules to set on GX Cloud to import

def customer_rules(validator):
    validator.expect_column_values_to_not_be_null("Invoice ID")