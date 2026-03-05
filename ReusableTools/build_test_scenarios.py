"""
Interactive Test Scenario Builder

This tool helps functional consultants create test scenario JSON files
through a simple question-and-answer interface.

Usage:
    python ReusableTools/build_test_scenarios.py
"""

import json
from pathlib import Path
from datetime import datetime


def get_input(prompt, default=""):
    """Get user input with optional default value"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()


def get_multiline_input(prompt):
    """Get multiline input (end with empty line)"""
    print(f"{prompt}")
    print("(Press Enter twice when done)")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            lines.pop()  # Remove last empty line
            break
        lines.append(line)
    return "\n".join(lines)


def build_interface_metadata():
    """Collect interface metadata"""
    print("\n" + "="*60)
    print("INTERFACE INFORMATION")
    print("="*60)
    
    metadata = {
        "interface_id": get_input("Interface ID (e.g., INT_FIN_013)"),
        "interface_name": get_input("Interface Name (e.g., GL Transaction Interface)"),
        "interface_type": get_input("Interface Type (inbound/outbound/approval)", "inbound"),
        "client_name": get_input("Client Name", "State of New Hampshire"),
        "author": get_input("Your Name"),
        "environment": get_input("Test Environment", "ACUITY_TST"),
    }
    
    return metadata


def build_prerequisites():
    """Collect prerequisites"""
    print("\n" + "="*60)
    print("PREREQUISITES")
    print("="*60)
    
    # User roles
    print("\nUser Roles (one per line, empty line when done):")
    roles = []
    while True:
        role = input("  Role: ").strip()
        if not role:
            break
        roles.append(role)
    
    test_data = get_multiline_input("\nTest Data Requirements:")
    config = get_multiline_input("\nConfiguration Prerequisites:")
    
    return {
        "user_roles": roles,
        "test_data_requirements": test_data,
        "configuration_prerequisites": config
    }


def build_test_step():
    """Build a single test step"""
    print("\n  --- Test Step ---")
    step_num = get_input("  Step Number")
    description = get_multiline_input("  Step Description:")
    result = get_input("  Result (PASS/FAIL/In Progress)", "PASS")
    screenshot = get_input("  Screenshot name (optional, e.g., 01_step_name)", "")
    
    step = {
        "number": step_num,
        "description": description,
        "result": result
    }
    
    if screenshot:
        step["screenshot"] = screenshot
    
    return step


def build_scenario():
    """Build a complete test scenario"""
    print("\n" + "-"*60)
    print("NEW SCENARIO")
    print("-"*60)
    
    title = get_input("Scenario Title (e.g., Scenario: Successful Import)")
    description = get_multiline_input("Scenario Description:")
    
    # Test steps
    print("\nTest Steps:")
    steps = []
    while True:
        add_step = get_input(f"Add step {len(steps) + 1}? (y/n)", "y").lower()
        if add_step != 'y':
            break
        steps.append(build_test_step())
    
    # Expected results
    print("\nExpected Results (one per line, empty line when done):")
    results = []
    while True:
        result = input("  Result: ").strip()
        if not result:
            break
        results.append(result)
    
    return {
        "title": title,
        "description": description,
        "test_steps": steps,
        "results": results
    }


def main():
    print("\n" + "="*60)
    print("TEST SCENARIO BUILDER")
    print("="*60)
    print("\nThis tool will help you create a test scenario JSON file.")
    print("You can then generate a TES-070 document from it.")
    
    # Collect metadata
    metadata = build_interface_metadata()
    prereqs = build_prerequisites()
    
    # Collect scenarios
    scenarios = []
    while True:
        print(f"\n\nCurrent scenarios: {len(scenarios)}")
        add_scenario = get_input("Add a scenario? (y/n)", "y").lower()
        if add_scenario != 'y':
            break
        scenarios.append(build_scenario())
    
    # Combine all data
    test_data = {
        **metadata,
        **prereqs,
        "scenarios": scenarios
    }
    
    # Save to file
    print("\n" + "="*60)
    print("SAVE FILE")
    print("="*60)
    
    interface_type = metadata['interface_type']
    interface_id = metadata['interface_id']
    
    default_filename = f"TestScripts/{interface_type}/{interface_id}_test_scenarios.json"
    filename = get_input(f"Save as", default_filename)
    
    # Create directory if needed
    filepath = Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # Save JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Test scenarios saved to: {filepath}")
    
    # Generate TES-070?
    generate = get_input("\nGenerate TES-070 document now? (y/n)", "y").lower()
    if generate == 'y':
        print("\nTo generate TES-070 document, run:")
        print(f"  python ReusableTools/generate_tes070_from_json.py {filepath}")
    
    print("\n" + "="*60)
    print("DONE!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
