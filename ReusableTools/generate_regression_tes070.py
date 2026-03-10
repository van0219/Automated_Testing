"""
Generate Regression TES-070 Documents from Test Execution Results

This tool generates updated TES-070 documents for approval workflow regression testing.
It takes test execution results (JSON) from Phase 3 and creates a professional Word document
with embedded screenshots, Pass/Fail status, and proper TES-070 formatting.

Usage:
    python ReusableTools/generate_regression_tes070.py Projects/SONH/Temp/test_results_EXT_FIN_004.json

The tool will:
1. Load test execution results JSON
2. Find evidence screenshots in Projects/{Client}/Temp/evidence/
3. Generate TES-070 document with:
   - Updated test summary (Pass/Fail statistics)
   - All test scenarios with current results
   - Embedded evidence screenshots
   - Expected vs Actual comparisons
   - Work unit references
   - Execution metadata
4. Save to Projects/{Client}/TES-070/Generated_TES070s/

Output: {Client}_{ExtensionID}_Regression_{timestamp}.docx
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from tes070_generator import TES070Data, TestScenario, TestStep, generate_tes070


def load_test_results(json_path: str) -> dict:
    """Load test execution results from JSON file"""
    print(f"📖 Loading test results from: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Validate required fields
    required_fields = ['extension_id', 'client', 'test_date', 'scenarios', 'summary']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise ValueError(f"Missing required fields in JSON: {', '.join(missing_fields)}")
    
    # Use 'client' for folder paths, 'client_name' for display (fallback to 'client' if not provided)
    if 'client_name' not in data:
        data['client_name'] = data['client']
    
    print(f"✅ Loaded results for {data['extension_id']} - {data.get('document_title', 'Unknown')}")
    print(f"   Client: {data['client_name']}")
    print(f"   Test Date: {data['test_date']}")
    print(f"   Scenarios: {data['summary']['total_scenarios']}")
    print(f"   Pass Rate: {data['summary']['pass_rate']}%")
    
    return data


def find_evidence_screenshots(client: str, scenario_id: str) -> list:
    """Find all screenshots for a scenario in evidence folder
    
    Args:
        client: Short client code (e.g., 'SONH') used for folder paths
        scenario_id: Scenario identifier (e.g., '3.1')
    """
    evidence_dir = Path(f"Projects/{client}/Temp/evidence/scenario_{scenario_id}")
    
    if not evidence_dir.exists():
        print(f"⚠️  Warning: Evidence folder not found: {evidence_dir}")
        return []
    
    # Find all PNG files in the scenario folder
    screenshots = sorted(evidence_dir.glob("*.png"))
    
    if screenshots:
        print(f"   📸 Found {len(screenshots)} screenshots for scenario {scenario_id}")
    else:
        print(f"   ⚠️  No screenshots found for scenario {scenario_id}")
    
    return [str(s) for s in screenshots]


def convert_to_tes070_data(test_results: dict) -> TES070Data:
    """Convert test execution results to TES070Data format"""
    print(f"\n📝 Converting test results to TES-070 format...")
    
    client = test_results['client']  # Short code for folder paths (e.g., 'SONH')
    client_name = test_results['client_name']  # Full name for display (e.g., 'State of New Hampshire')
    extension_id = test_results['extension_id']
    
    # Convert scenarios
    scenarios = []
    for scenario_data in test_results['scenarios']:
        scenario_id = scenario_data['scenario_id']
        
        # Convert test steps
        test_steps = []
        for step_data in scenario_data.get('steps', []):
            test_steps.append(TestStep(
                number=str(step_data['step_number']),
                description=step_data['description'],
                result=step_data['result']
            ))
        
        # Find screenshots for this scenario (use short client code for folder path)
        screenshots = find_evidence_screenshots(client, scenario_id)
        
        # Build results list (Expected vs Actual)
        results = [
            f"Expected Result: {scenario_data.get('expected_result', 'N/A')}",
            f"Actual Result: {scenario_data.get('actual_result', 'N/A')}"
        ]
        
        # Add work unit ID if available
        if scenario_data.get('work_unit_id'):
            results.append(f"Work Unit ID: {scenario_data['work_unit_id']}")
        
        # Add overall status
        status_emoji = "✅" if scenario_data['status'] == 'PASS' else "❌"
        results.append(f"Status: {status_emoji} {scenario_data['status']}")
        
        scenarios.append(TestScenario(
            title=f"Scenario {scenario_id}: {scenario_data['scenario_title']}",
            description=scenario_data.get('description', ''),
            test_steps=test_steps,
            results=results,
            screenshots=screenshots
        ))
    
    # Create TES070Data object
    tes070_data = TES070Data(
        client_name=client_name,
        interface_id=extension_id,
        interface_name=f"{test_results.get('document_title', 'Approval Workflow')} - Regression Test Results",
        author=test_results.get('tester_name', 'Kiro Agent'),
        version=f"Regression_{test_results['test_date']}",
        date=test_results['test_date'],
        
        # Test summary from results
        total_tests=test_results['summary']['total_scenarios'],
        completed_tests=test_results['summary']['total_scenarios'],
        passed_tests=test_results['summary']['passed'],
        failed_tests=test_results['summary']['failed'],
        
        # Prerequisites
        environment=test_results.get('environment', 'ACUITY_TST'),
        user_roles=test_results.get('user_roles', ['Payables', 'Process Server Administrator']),
        test_data_requirements="Live FSM data used for regression testing",
        configuration_prerequisites=test_results.get('configuration_notes', 'Standard approval workflow configuration'),
        
        # Scenarios
        scenarios=scenarios
    )
    
    print(f"✅ Converted {len(scenarios)} scenarios")
    
    return tes070_data


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_regression_tes070.py <test_results_json>")
        print("\nExample:")
        print("  python ReusableTools/generate_regression_tes070.py Projects/SONH/Temp/test_results_EXT_FIN_004.json")
        print("\nInput JSON Structure:")
        print("  {")
        print('    "extension_id": "EXT_FIN_004",')
        print('    "document_title": "Expense Invoice Approval Workflow",')
        print('    "client_name": "SONH",')
        print('    "test_date": "2026-03-10",')
        print('    "tester_name": "Kiro Agent",')
        print('    "environment": "ACUITY_TST",')
        print('    "scenarios": [...],')
        print('    "summary": {')
        print('      "total_scenarios": 5,')
        print('      "passed": 4,')
        print('      "failed": 1,')
        print('      "pass_rate": 80.0')
        print('    }')
        print('  }')
        sys.exit(1)
    
    json_path = sys.argv[1]
    
    if not Path(json_path).exists():
        print(f"❌ Error: File not found: {json_path}")
        sys.exit(1)
    
    try:
        # Load test results
        test_results = load_test_results(json_path)
        
        # Convert to TES070Data format
        tes070_data = convert_to_tes070_data(test_results)
        
        # Generate output filename (use short client code for filename and folder path)
        client = test_results['client']  # Short code (e.g., 'SONH')
        extension_id = test_results['extension_id']
        test_date = test_results['test_date'].replace('-', '')
        output_filename = f"{client}_{extension_id}_Regression_{test_date}.docx"
        
        # Ensure output directory exists (use short client code for folder path)
        output_dir = Path(f"Projects/{client}/TES-070/Generated_TES070s")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / output_filename
        
        # Generate TES-070 document
        print(f"\n📝 Generating TES-070 document...")
        result_path = generate_tes070(tes070_data, str(output_path))
        
        print(f"\n✅ TES-070 Document Generated Successfully!")
        print(f"📄 Location: {result_path}")
        print(f"\n📊 Summary:")
        print(f"   Document: {output_filename}")
        print(f"   Total Scenarios: {tes070_data.total_tests}")
        print(f"   Passed: {tes070_data.passed_tests}")
        print(f"   Failed: {tes070_data.failed_tests}")
        print(f"   Pass Rate: {tes070_data.percent_passed}")
        print(f"   Screenshots: {sum(len(s.screenshots) for s in tes070_data.scenarios)}")
        
        print(f"\n💡 Next Steps:")
        print(f"   1. Open the document in Word")
        print(f"   2. Click in the Table of Contents area")
        print(f"   3. Press F9 to update the TOC")
        print(f"   4. Review scenarios and screenshots")
        print(f"   5. Share with stakeholders")
        
        # Show scenario breakdown
        print(f"\n📋 Scenario Breakdown:")
        for i, scenario in enumerate(tes070_data.scenarios, 1):
            status = "✅ PASS" if all(step.result == 'PASS' for step in scenario.test_steps if step.result) else "❌ FAIL"
            print(f"   {i}. {scenario.title} - {status}")
        
    except Exception as e:
        print(f"\n❌ Error generating TES-070 document:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
