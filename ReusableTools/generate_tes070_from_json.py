"""
Generate TES-070 documents from JSON test scenario files

This tool allows functional consultants to define test scenarios in simple JSON files
and automatically generate properly formatted TES-070 documents.

Usage:
    python ReusableTools/generate_tes070_from_json.py TestScripts/inbound/INT_FIN_013_test_scenarios.json

The tool will:
1. Read the JSON test scenario file
2. Look for screenshots in Temp/{interface_id}_{timestamp}/ folder
3. Generate a complete TES-070 document in TES-070/Generated_TES070s/
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from tes070_generator import TES070Data, TestScenario, TestStep, generate_tes070


def load_test_scenarios(json_path: str) -> TES070Data:
    """Load test scenarios from JSON file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert JSON scenarios to TestScenario objects
    scenarios = []
    for scenario_data in data.get('scenarios', []):
        test_steps = []
        screenshots = []
        
        for step_data in scenario_data.get('test_steps', []):
            test_steps.append(TestStep(
                number=step_data.get('number', ''),
                description=step_data.get('description', ''),
                result=step_data.get('result', '')
            ))
            
            # Collect screenshot paths if specified
            if 'screenshot' in step_data:
                screenshot_name = step_data['screenshot']
                # Look for screenshot in Temp folder
                # Pattern: Temp/{interface_id}_{timestamp}/{step_number}_{screenshot_name}.png
                screenshots.append(screenshot_name)
        
        scenarios.append(TestScenario(
            title=scenario_data.get('title', ''),
            description=scenario_data.get('description', ''),
            test_steps=test_steps,
            results=scenario_data.get('results', []),
            screenshots=[]  # Will be populated when screenshots are captured
        ))
    
    # Create TES070Data object
    tes070_data = TES070Data(
        client_name=data.get('client_name', ''),
        interface_id=data.get('interface_id', ''),
        interface_name=data.get('interface_name', ''),
        author=data.get('author', 'Functional Consultant'),
        version=data.get('version', '1.0'),
        environment=data.get('environment', ''),
        user_roles=data.get('user_roles', []),
        test_data_requirements=data.get('test_data_requirements', ''),
        configuration_prerequisites=data.get('configuration_prerequisites', ''),
        scenarios=scenarios
    )
    
    return tes070_data


def find_screenshots(interface_id: str, screenshot_names: list) -> list:
    """Find screenshot files in Temp folder"""
    temp_dir = Path("Temp")
    screenshots = []
    
    # Look for most recent folder matching pattern
    matching_folders = sorted(temp_dir.glob(f"{interface_id}_*"), reverse=True)
    
    if matching_folders:
        screenshot_dir = matching_folders[0]
        print(f"📁 Looking for screenshots in: {screenshot_dir}")
        
        for name in screenshot_names:
            # Try different patterns
            patterns = [
                f"*{name}.png",
                f"{name}.png",
                f"*_{name}.png"
            ]
            
            for pattern in patterns:
                matches = list(screenshot_dir.glob(pattern))
                if matches:
                    screenshots.append(str(matches[0]))
                    break
    
    return screenshots


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_tes070_from_json.py <json_file>")
        print("\nExample:")
        print("  python ReusableTools/generate_tes070_from_json.py TestScripts/inbound/INT_FIN_013_test_scenarios.json")
        sys.exit(1)
    
    json_path = sys.argv[1]
    
    if not Path(json_path).exists():
        print(f"❌ Error: File not found: {json_path}")
        sys.exit(1)
    
    print(f"📖 Reading test scenarios from: {json_path}")
    tes070_data = load_test_scenarios(json_path)
    
    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{tes070_data.interface_id}_{tes070_data.interface_name.replace(' ', '_')}_{timestamp}.docx"
    output_path = Path("TES-070/Generated_TES070s") / output_filename
    
    # Generate TES-070 document
    print(f"\n📝 Generating TES-070 document...")
    result_path = generate_tes070(tes070_data, str(output_path))
    
    print(f"\n✅ TES-070 Document Generated!")
    print(f"📄 Location: {result_path}")
    print(f"\n📊 Summary:")
    print(f"   Scenarios: {len(tes070_data.scenarios)}")
    print(f"   Total Tests: {tes070_data.total_tests}")
    print(f"   Passed: {tes070_data.passed_tests}")
    print(f"   Failed: {tes070_data.failed_tests}")
    print(f"   Pass Rate: {tes070_data.percent_passed}")
    
    print(f"\n💡 Next Steps:")
    print(f"   1. Open the document in Word")
    print(f"   2. Click in the Table of Contents area")
    print(f"   3. Press F9 to update the TOC")
    print(f"   4. Review and add any missing screenshots")


if __name__ == "__main__":
    main()
