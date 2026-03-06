#!/usr/bin/env python3
"""
Build EXT_FIN_004 test scenarios JSON from TES-070 analysis
"""
import json
import sys
from datetime import datetime

def build_scenarios_from_analysis(analysis_path, output_path):
    """Build complete test scenarios JSON from TES-070 analysis"""
    
    # Load analysis
    with open(analysis_path, 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    # Extract scenarios with actual test steps (not TOC entries)
    scenarios_with_steps = [s for s in analysis['scenarios'] if len(s.get('test_steps', [])) > 0]
    
    print(f"📊 Found {len(scenarios_with_steps)} scenarios with test steps")
    print(f"📄 Total scenarios in analysis: {len(analysis['scenarios'])}")
    
    # Build complete JSON structure
    test_scenarios = {
        "extension_id": "EXT_FIN_004",
        "extension_name": "Expense Invoice Approval",
        "transaction_type": "ExpenseInvoice",
        "client": "SONH",
        "generated_from": "TES-070 Analysis",
        "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scenarios": []
    }
    
    # Process each scenario
    for idx, scenario in enumerate(scenarios_with_steps, 1):
        scenario_data = {
            "scenario_id": f"3.{idx}",
            "title": scenario['title'].replace('Scenario: ', ''),
            "description": scenario.get('description', ''),
            "steps": []
        }
        
        # Add test steps
        for step in scenario.get('test_steps', []):
            scenario_data['steps'].append({
                "step_number": step.get('number', ''),
                "description": step.get('description', ''),
                "expected_result": step.get('result', 'PASS')
            })
        
        # Add expected results
        scenario_data['expected_results'] = scenario.get('results', [])
        
        test_scenarios['scenarios'].append(scenario_data)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(test_scenarios, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Generated {len(test_scenarios['scenarios'])} scenarios")
    print(f"💾 Saved to: {output_path}")
    
    return test_scenarios

if __name__ == "__main__":
    analysis_path = "Projects/SONH/TES-070/Approval_TES070s_For_Regression_Testing/SoNH_TES-070 - EXT_FIN_004 Expense Invoice Approval Test Results Document_analysis.json"
    output_path = "Projects/SONH/TestScripts/approval/EXT_FIN_004_auto_approval_test.json"
    
    build_scenarios_from_analysis(analysis_path, output_path)
