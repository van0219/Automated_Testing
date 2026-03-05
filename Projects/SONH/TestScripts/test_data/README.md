# Test Data Files

This folder contains CSV, XML, and JSON test data files used for interface testing.

## File Naming Convention
- `{INTERFACE_ID}_valid.csv` - Valid data for successful import
- `{INTERFACE_ID}_invalid_format.csv` - Invalid format/structure
- `{INTERFACE_ID}_duplicate.csv` - Duplicate records
- `{INTERFACE_ID}_empty.csv` - Empty file
- `{INTERFACE_ID}_business_error.csv` - Business rule violations

## Generating Test Data
Use the "Interface Step 0: Generate Test Data" hook to create fresh test data files with:
- Current dates (YYYYMMDD format)
- Correct FSM field names (queried from FSM API)
- Appropriate test scenarios (valid, invalid, duplicate, etc.)

## Usage
Test data files are referenced in test scenario JSON files via the `test_data_file` field.
