## Sales Tax Calculator

### Pre-requisite

- Python >= 3.9.0

### Tests

Unit tests are located in `$WORKING_DIR/salesTax/test_receipt.py`

To run all the unit tests use the following command:
    
    python -m unittest test_receipt.py

### Executing Code with default data

The default data for testing our the project is located under `$WORKING_DIR/salesTax/data.json`

To execute the code with the default data and check the printed receipt, use the following command:

    python receipt.py

To run the code with a different set of tests:

1. Please add or replace the new test data to `$WORKING_DIR/salesTax/data.json`
2. Save the data files
3. Run the following command to check your receipt print out, `python receipt.py`
