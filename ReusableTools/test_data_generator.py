# -*- coding: utf-8 -*-
"""
Test Data Generator

Generate test data files for FSM interface testing.
Creates valid, invalid, and edge-case data files for comprehensive testing.

IMPORTANT: This tool generates data using field names provided by Kiro (AI).
The field selection process is:
1. fsm_field_discovery.py queries FSM API for valid field names
2. Kiro analyzes the fields and selects which to include
3. This tool generates test data with Kiro's selected fields

Usage:
    from test_data_generator import generate_all_test_scenarios
    
    # Kiro provides the field list after analyzing FSM API response
    selected_fields = [
        'FinanceEnterpriseGroup',
        'AccountingEntity',
        'PostingDate',
        'Account',
        'Amount',
        'DebitCredit',
        'Description',
        'Reference',
        'RunGroup'
    ]
    
    # Generate test data with Kiro's selected fields
    generate_all_test_scenarios(
        output_dir='Projects/StateOfNewHampshire/TestScripts/test_data',
        interface_id='INT_FIN_013',
        field_names=selected_fields
    )
"""

import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import random

try:
    from fsm_field_discovery import discover_fsm_fields
    FSM_DISCOVERY_AVAILABLE = True
except ImportError:
    FSM_DISCOVERY_AVAILABLE = False
    print("⚠️  FSM field discovery not available. Using default field names.")


def generate_gl_transaction_data(scenario: str, output_file: str, num_records: int = 10, 
                                field_names: Optional[List[str]] = None) -> str:
    """
    Generate GL Transaction test data file.
    
    Args:
        scenario: Type of data to generate
            - 'valid': Clean, valid data
            - 'invalid_format': Bad date/number formats
            - 'duplicate': Duplicate sequence numbers
            - 'empty': Empty file with headers only
            - 'business_rule_error': Closed period dates, invalid accounts
        output_file: Path to save CSV file
        num_records: Number of records to generate
        field_names: List of field names to include (provided by Kiro)
    
    Returns:
        Path to generated file
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Use provided field names or fallback to defaults
    if field_names:
        headers = field_names
    else:
        # Fallback to default headers
        headers = [
            'FinanceEnterpriseGroup',
            'AccountingEntity',
            'PostingDate',
            'Account',
            'SubAccount',
            'Amount',
            'DebitCredit',
            'Description',
            'Reference',
            'RunGroup'
        ]
    
    if scenario == 'empty':
        # Just headers, no data
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
        return str(output_path)
    
    # Generate records based on scenario
    records = []
    
    for i in range(1, num_records + 1):
        if scenario == 'valid':
            record = _generate_valid_record(i, headers)
        elif scenario == 'invalid_format':
            record = _generate_invalid_format_record(i, headers)
        elif scenario == 'duplicate':
            # Create duplicates every 3rd record
            seq = i if i % 3 != 0 else i - 1
            record = _generate_valid_record(seq, headers)
        elif scenario == 'business_rule_error':
            record = _generate_business_rule_error_record(i, headers)
        else:
            record = _generate_valid_record(i, headers)
        
        records.append(record)
    
    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"✅ Generated {scenario} test data: {output_path} ({len(records)} records)")
    return str(output_path)


def _generate_valid_record(sequence: int, headers: List[str]) -> Dict[str, str]:
    """Generate a valid GL transaction record with correct FSM field names"""
    base_date = datetime.now() - timedelta(days=random.randint(1, 30))
    
    accounts = ['1010', '2010', '3010', '4010', '5010']
    debit_credit = random.choice(['D', 'C'])
    amount = round(random.uniform(100, 10000), 2)
    
    # Build record with only fields that exist in headers
    record = {}
    
    # Map field names to values
    field_values = {
        'FinanceEnterpriseGroup': 'SONH',
        'AccountingEntity': 'SONH',
        'PostingDate': base_date.strftime('%Y%m%d'),
        'TransactionDate': base_date.strftime('%Y%m%d'),
        'Account': random.choice(accounts),
        'AccountCode': random.choice(accounts),  # Correct FSM field name
        'SubAccount': '000',
        'Amount': f"{amount:.2f}",
        'TransactionAmount': f"{amount:.2f}",  # Correct FSM field name
        'DebitCredit': debit_credit,
        'DebitCreditFlag': debit_credit,  # Correct FSM field name
        'Description': f'Test Transaction {sequence}',
        'Reference': f'REF{sequence:04d}',
        'RunGroup': f'TEST_{datetime.now().strftime("%Y%m%d")}',
        'GLTransactionInterface': f'TEST_{datetime.now().strftime("%Y%m%d")}',  # Correct FSM field name for RunGroup
        'TransactionNumber': str(sequence),
        'Sequence': str(sequence),
        'JournalType': 'GL'
    }
    
    # Only include fields that are in headers
    for header in headers:
        if header in field_values:
            record[header] = field_values[header]
        else:
            record[header] = ''  # Empty for unknown fields
    
    return record


def _generate_invalid_format_record(sequence: int, headers: List[str]) -> Dict[str, str]:
    """Generate record with format errors"""
    errors = [
        # Bad date format
        lambda: {
            'PostingDate': '1082025',  # Invalid format
            'TransactionDate': '1082025',
            'Amount': '1000.00',
            'TransactionAmount': '1000.00',
            'DebitCredit': 'D',
            'DebitCreditFlag': 'D',
            'Description': 'Invalid date format'
        },
        # Bad number format (comma in amount)
        lambda: {
            'PostingDate': datetime.now().strftime('%Y%m%d'),
            'TransactionDate': datetime.now().strftime('%Y%m%d'),
            'Amount': '2,105.19',  # Comma not allowed
            'TransactionAmount': '2,105.19',  # Comma not allowed
            'DebitCredit': 'D',
            'DebitCreditFlag': 'D',
            'Description': 'Invalid amount format'
        },
        # Missing required field
        lambda: {
            'PostingDate': datetime.now().strftime('%Y%m%d'),
            'TransactionDate': datetime.now().strftime('%Y%m%d'),
            'Account': '',  # Missing account
            'AccountCode': '',  # Missing account
            'Amount': '1000.00',
            'TransactionAmount': '1000.00',
            'DebitCredit': 'D',
            'DebitCreditFlag': 'D',
            'Description': 'Missing account'
        }
    ]
    
    error_data = random.choice(errors)()
    
    # Build complete record with defaults
    record = _generate_valid_record(sequence, headers)
    
    # Override with error data
    for key, value in error_data.items():
        if key in record:
            record[key] = value
    
    return record


def _generate_business_rule_error_record(sequence: int, headers: List[str]) -> Dict[str, str]:
    """Generate record that will fail business rules"""
    errors = [
        # Closed period date
        lambda: {
            'PostingDate': '20230101',  # Old closed period
            'TransactionDate': '20230101',
            'Description': 'Closed period transaction'
        },
        # Invalid account code
        lambda: {
            'Account': '9999',  # Non-existent account
            'AccountCode': '9999',  # Non-existent account
            'Description': 'Invalid account code'
        }
    ]
    
    error_data = random.choice(errors)()
    
    # Build complete record with defaults
    record = _generate_valid_record(sequence, headers)
    
    # Override with error data
    for key, value in error_data.items():
        if key in record:
            record[key] = value
    
    return record


def generate_all_test_scenarios(output_dir: str, interface_id: str = 'INT_FIN_013',
                               field_names: Optional[List[str]] = None):
    """
    Generate all test scenario files for an interface.
    
    Args:
        output_dir: Directory to save test files
        interface_id: Interface identifier
        field_names: List of field names to include (provided by Kiro)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🎲 Generating test data files for {interface_id}")
    print(f"📁 Output directory: {output_path}\n")
    
    if field_names:
        print(f"📋 Using {len(field_names)} fields provided by Kiro")
        print(f"   Fields: {', '.join(field_names[:10])}")
        if len(field_names) > 10:
            print(f"   ... and {len(field_names) - 10} more\n")
    
    scenarios = [
        ('valid', 'GLTRANSREL_valid.csv', 10),
        ('invalid_format', 'GLTRANSREL_invalid_format.csv', 5),
        ('duplicate', 'GLTRANSREL_duplicate.csv', 9),
        ('empty', 'GLTRANSREL_empty.csv', 0),
        ('business_rule_error', 'GLTRANSREL_business_error.csv', 5)
    ]
    
    generated_files = []
    
    for scenario, filename, num_records in scenarios:
        file_path = output_path / filename
        generate_gl_transaction_data(
            scenario, 
            str(file_path), 
            num_records,
            field_names=field_names
        )
        generated_files.append(str(file_path))
    
    print(f"\n✅ Generated {len(generated_files)} test data files")
    print("\nFiles created:")
    for file in generated_files:
        print(f"  - {file}")
    
    # Show sample data from valid file
    if generated_files:
        print(f"\n📋 Sample data from {scenarios[0][1]}:")
        with open(generated_files[0], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            print(f"   Headers: {', '.join(headers)}")
            first_row = next(reader, None)
            if first_row:
                print(f"   First record:")
                for key, value in list(first_row.items())[:5]:  # Show first 5 fields
                    print(f"     {key}: {value}")
    
    return generated_files


if __name__ == "__main__":
    # Example: Generate test data for State of New Hampshire
    # In practice, Kiro will call fsm_field_discovery first, then pass selected fields
    print("=" * 60)
    print("FSM Test Data Generator")
    print("=" * 60)
    print("\nNote: This example uses default fields.")
    print("In practice, Kiro will discover fields via API and select which to use.\n")
    
    generate_all_test_scenarios(
        output_dir='Projects/StateOfNewHampshire/TestScripts/test_data',
        interface_id='INT_FIN_013'
    )
    
    print("\n" + "=" * 60)
    print("✅ Test data generation complete!")
    print("=" * 60)
