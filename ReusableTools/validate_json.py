#!/usr/bin/env python3
"""
Simple JSON validation utility
Usage: python validate_json.py <json_file_path>
"""
import json
import sys

def validate_json(file_path):
    """Validate JSON file and print summary"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Valid JSON file: {file_path}")
        
        # Print summary if it's a test scenario file
        if 'interface_id' in data:
            print(f"\nInterface ID: {data['interface_id']}")
            print(f"Interface Type: {data.get('interface_type', 'N/A')}")
            print(f"Total Scenarios: {len(data.get('scenarios', []))}")
            
            if data.get('scenarios'):
                print("\nScenarios:")
                for scenario in data['scenarios']:
                    scenario_id = scenario.get('scenario_id', 'N/A')
                    title = scenario.get('title', 'N/A')
                    steps = len(scenario.get('steps', []))
                    print(f"  - {scenario_id}: {title} ({steps} steps)")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_json.py <json_file_path>")
        sys.exit(1)
    
    success = validate_json(sys.argv[1])
    sys.exit(0 if success else 1)
