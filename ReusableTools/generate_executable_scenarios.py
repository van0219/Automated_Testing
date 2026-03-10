#!/usr/bin/env python3
"""
Generate executable test scenarios JSON from TES-070 analysis
Translates TES-070 test steps into MCP Playwright actions
"""
import json
import sys
from pathlib import Path


def translate_step_to_mcp_action(step_description, step_number, scenario_id):
    """
    Translate a TES-070 test step description into MCP Playwright action
    
    Returns dict with action, description, and parameters
    """
    desc_lower = step_description.lower()
    
    # Login steps
    if "login" in desc_lower or "sign in" in desc_lower:
        if "cloud identities" in desc_lower:
            return {
                "step_number": step_number,
                "action": "mcp_playwright_browser_click",
                "description": "Click Cloud Identities link",
                "parameters": {"element": "Cloud Identities link"}
            }
        elif "username" in desc_lower:
            return {
                "step_number": step_number,
                "action": "mcp_playwright_browser_type",
                "description": "Enter FSM username",
                "parameters": {
                    "element": "Username field",
                    "text": "{{FSM_USERNAME}}",
                    "submit": False
                }
            }
        elif "password" in desc_lower:
            return {
                "step_number": step_number,
                "action": "mcp_playwright_browser_type",
                "description": "Enter FSM password",
                "parameters": {
                    "element": "Password field",
                    "text": "{{state.password}}",
                    "submit": True
                }
            }
        else:
            return {
                "step_number": step_number,
                "action": "mcp_playwright_browser_navigate",
                "description": "Navigate to FSM Portal",
                "parameters": {"url": "{{FSM_PORTAL_URL}}"}
            }
    
    # Navigation steps
    elif "navigate" in desc_lower or "go to" in desc_lower:
        if "payables" in desc_lower:
            return {
                "step_number": step_number,
                "action": "mcp_playwright_browser_click",
                "description": "Navigate to Payables",
                "parameters": {"element": "Payables application link"}
            }
        elif "work unit" in desc_lower:
            return {
                "step_number": step_number,
                "action": "mcp_playwright_browser_click",
                "description": "Navigate to Work Units",
                "parameters": {"element": "Work Units menu item"}
            }
        elif "inbasket" in desc_lower:
            return {
                "step_number": step_number,
                "action": "mcp_playwright_browser_click",
                "description": "Navigate to Inbasket",
                "parameters": {"element": "Inbasket menu item"}
            }
    
    # Invoice creation steps
    elif "create" in desc_lower and "invoice" in desc_lower:
        return {
            "step_number": step_number,
            "action": "mcp_playwright_browser_fill_form",
            "description": "Create expense invoice",
            "parameters": {
                "fields": [
                    {"name": "Company", "type": "textbox", "value": "10"},
                    {"name": "Vendor", "type": "textbox", "value": "{{vendor_id}}"},
                    {"name": "Invoice Number", "type": "textbox", "value": "{{state.run_group}}_INV"},
                    {"name": "Invoice Date", "type": "textbox", "value": "{{TODAY_YYYYMMDD}}"},
                    {"name": "Due Date", "type": "textbox", "value": "{{TODAY_PLUS_7_YYYYMMDD}}"},
                    {"name": "Invoice Amount", "type": "textbox", "value": "{{invoice_amount}}"},
                    {"name": "Description", "type": "textbox", "value": "Test Invoice {{state.run_group}}"}
                ]
            }
        }
    
    # Submit for approval
    elif "submit" in desc_lower and "approval" in desc_lower:
        return {
            "step_number": step_number,
            "action": "mcp_playwright_browser_click",
            "description": "Submit invoice for approval",
            "parameters": {"element": "Submit for Approval button"}
        }
    
    # Approval actions
    elif "approve" in desc_lower and "invoice" in desc_lower:
        return {
            "step_number": step_number,
            "action": "mcp_playwright_browser_click",
            "description": "Approve invoice from Inbasket",
            "parameters": {"element": "Approve button"}
        }
    
    elif "reject" in desc_lower and "invoice" in desc_lower:
        return {
            "step_number": step_number,
            "action": "mcp_playwright_browser_click",
            "description": "Reject invoice from Inbasket",
            "parameters": {"element": "Reject button"}
        }
    
    # Wait/verification steps
    elif "wait" in desc_lower or "status" in desc_lower or "verify" in desc_lower:
        return {
            "step_number": step_number,
            "action": "mcp_playwright_browser_wait_for",
            "description": "Wait for process to complete",
            "parameters": {"time": 5}
        }
    
    # Screenshot/snapshot steps
    elif "email" in desc_lower or "notification" in desc_lower:
        return {
            "step_number": step_number,
            "action": "mcp_playwright_browser_take_screenshot",
            "description": f"Capture evidence - {step_description[:50]}",
            "parameters": {"filename": f"{scenario_id}_step{step_number}_evidence.png"}
        }
    
    # Default: take snapshot
    else:
        return {
            "step_number": step_number,
            "action": "mcp_playwright_browser_snapshot",
            "description": step_description[:100],
            "parameters": {"filename": f"{scenario_id}_step{step_number}_snapshot.md"}
        }


def generate_executable_scenarios(analysis_path, output_path):
    """
    Generate executable scenarios JSON from TES-070 analysis
    
    Args:
        analysis_path: Path to TES-070 analysis JSON
        output_path: Path to save executable scenarios JSON
    """
    print(f"📖 Reading TES-070 analysis: {analysis_path}")
    
    with open(analysis_path, 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    # Extract scenarios with actual test steps (skip TOC entries)
    scenarios_with_steps = [s for s in analysis['scenarios'] if len(s.get('test_steps', [])) > 0]
    
    print(f"✅ Found {len(scenarios_with_steps)} scenarios with test steps")
    
    # Build executable scenarios
    executable = {
        "extension_id": analysis.get('document_info', {}).get('file_path', '').split('EXT_FIN_')[1].split(' ')[0] if 'EXT_FIN_' in analysis.get('document_info', {}).get('file_path', '') else "UNKNOWN",
        "extension_name": "Expense Invoice Approval",
        "client": "SONH",
        "environment": "SONH_AX4",
        "transaction_type": "ExpenseInvoice",
        "test_date": "2026-03-06",
        "tester_name": "QA Automation",
        "scenarios": []
    }
    
    # Process each scenario
    for idx, scenario in enumerate(scenarios_with_steps[:3], 1):  # Limit to first 3 scenarios
        scenario_id = f"3.{idx}"
        
        executable_scenario = {
            "scenario_id": scenario_id,
            "title": scenario.get('title', '').replace('Scenario: ', ''),
            "description": scenario.get('description', ''),
            "expected_result": scenario.get('results', [''])[0] if scenario.get('results') else '',
            "steps": []
        }
        
        # Translate each test step
        for step in scenario.get('test_steps', []):
            step_desc = step.get('description', '')
            step_num = step.get('number', '1')
            
            if step_desc:
                mcp_action = translate_step_to_mcp_action(step_desc, step_num, scenario_id)
                executable_scenario['steps'].append(mcp_action)
        
        executable['scenarios'].append(executable_scenario)
    
    # Save executable scenarios
    print(f"💾 Saving executable scenarios: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(executable, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated {len(executable['scenarios'])} executable scenarios")
    print(f"📄 Output: {output_path}")
    
    return executable


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_executable_scenarios.py <analysis_json> <output_json>")
        sys.exit(1)
    
    analysis_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not Path(analysis_path).exists():
        print(f"❌ Error: Analysis file not found: {analysis_path}")
        sys.exit(1)
    
    try:
        generate_executable_scenarios(analysis_path, output_path)
        print("\n✅ Executable scenarios generated successfully!")
    except Exception as e:
        print(f"\n❌ Error generating executable scenarios: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
