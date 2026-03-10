#!/usr/bin/env python3
"""
Create test instructions JSON from TES-070 analysis for subagent execution.

This script reads the TES-070 analysis JSON and creates a simplified instruction
file that the subagent can use to execute tests via MCP Playwright.
"""

import json
import sys
from pathlib import Path

def create_test_instructions(analysis_path, output_path):
    """
    Convert TES-070 analysis to test instructions for subagent.
    
    Args:
        analysis_path: Path to *_analysis.json file
        output_path: Path to save test instructions JSON
    """
    print(f"📖 Reading TES-070 analysis: {analysis_path}")
    
    with open(analysis_path, 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    # Extract document info
    doc_info = analysis.get('document_info', {})
    test_summary = analysis.get('test_summary', {})
    scenarios = analysis.get('scenarios', [])
    
    # Filter scenarios that have actual test steps (not TOC entries)
    executable_scenarios = []
    for scenario in scenarios:
        test_steps = scenario.get('test_steps', [])
        if test_steps and len(test_steps) > 0:
            # Only include if test_steps have actual content
            if any(step.get('description', '').strip() for step in test_steps):
                executable_scenarios.append({
                    'scenario_id': scenario.get('title', '').split('\t')[0] if '\t' in scenario.get('title', '') else scenario.get('title', ''),
                    'title': scenario.get('title', ''),
                    'description': scenario.get('description', ''),
                    'test_steps': test_steps,
                    'expected_results': scenario.get('results', [])
                })
    
    print(f"✅ Found {len(executable_scenarios)} executable scenarios")
    
    # Create test instructions
    instructions = {
        'extension_id': 'EXT_FIN_004',  # Extract from filename if needed
        'extension_name': 'Expense Invoice Approval',
        'client': 'SONH',  # Extract from path if needed
        'test_date': test_summary.get('actual_scenario_count', ''),
        'total_scenarios': len(executable_scenarios),
        'scenarios': executable_scenarios,
        'prerequisites': []  # Can extract from analysis if needed
    }
    
    # Save instructions
    print(f"💾 Saving test instructions: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(instructions, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Test instructions created successfully!")
    print(f"📄 Output: {output_path}")
    print(f"📊 Scenarios: {len(executable_scenarios)}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python create_test_instructions.py <analysis_json_path> <output_json_path>")
        sys.exit(1)
    
    analysis_path = sys.argv[1]
    output_path = sys.argv[2]
    
    create_test_instructions(analysis_path, output_path)
