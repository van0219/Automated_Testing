#!/usr/bin/env python3
"""Generate EXT_FIN_004 test scenarios from TES-070 analysis"""
import json
import re

def parse_scenario_id(title):
    """Extract scenario ID like '3.1' from title"""
    match = re.match(r'^(\d+\.\d+)', title)
    return match.group(1) if match else None

def clean_title(title):
    """Remove scenario ID and 'Scenario:' prefix"""
    title = re.sub(r'^\d+\.\d+\s*', '', title)
    title = re.sub(r'^Scenario:\s*', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s+\d+$', '', title)
    return title.strip()

def infer_vendor_class(title):
    """Infer vendor class from title"""
    title_lower = title.lower()
    if 'garnishment' in title_lower or 'ghr' in title_lower:
        return 'GHR'
    elif 'employee' in title_lower or 'emp' in title_lower:
        return 'EMP'
    else:
        return 'OTHER'

def infer_authority_code(title):
    """Infer authority code from title"""
    if 'authority code = pr1' in title.lower() or 'authority code = "pr1"' in title.lower():
        return 'PR1'
    elif 'authority code = ap1' in title.lower() or 'authority code = "ap1"' in title.lower():
        return 'AP1'
    return None

def infer_amount(title):
    """Infer amount from title"""
    title_lower = title.lower()
    if 'less than $1,000' in title_lower or '< $1,000' in title_lower:
        return '500.00'
    elif 'at least $1,000' in title_lower or '>= $1,000' in title_lower or '$1,000' in title_lower:
        return '1500.00'
    return '100.00'

def infer_expected_route(title):
    """Infer expected approval route from title"""
    title_lower = title.lower()
    if 'auto approved' in title_lower:
        return 'AUTO'
    elif 'routed to payroll' in title_lower or 'payroll manager' in title_lower:
        return 'PayrollMgr'
    elif 'routed to agency' in title_lower and 'then to boa' in title_lower:
        return 'Agency-BOA'
    elif 'routed to agency' in title_lower:
        return 'Agency'
    elif 'routed to boa' in title_lower:
        return 'BOA'
    return 'Unknown'

def infer_expected_status(title):
    """Infer expected final status from title"""
    title_lower = title.lower()
    if 'approved' in title_lower and 'rejected' not in title_lower and 'returned' not in title_lower:
        return 'Released'
    elif 'rejected' in title_lower or 'auto rejected' in title_lower:
        return 'Rejected'
    elif 'returned' in title_lower:
        return 'Returned'
    return 'Released'

# Read the analysis JSON
with open('Projects/SONH/TES-070/Approval_TES070s_For_Regression_Testing/SoNH_TES-070 - EXT_FIN_004 Expense Invoice Approval Test Results Document_analysis.json', 'r', encoding='utf-8') as f:
    analysis = json.load(f)

# Extract all scenarios with scenario IDs 3.1 through 3.21
all_scenarios = analysis['scenarios']
toc_scenarios = []

# Get all scenarios with IDs 3.1 through 3.21
for s in all_scenarios:
    title = s.get('title', '')
    scenario_id = parse_scenario_id(title)
    if scenario_id and scenario_id.startswith('3.'):
        toc_scenarios.append(s)

# Sort by scenario ID and take first 21
toc_scenarios.sort(key=lambda x: float(parse_scenario_id(x['title']) or '0'))
toc_scenarios = toc_scenarios[:21]

# Generate scenarios
scenarios = []

for toc in toc_scenarios:
    scenario_id = parse_scenario_id(toc['title'])
    if not scenario_id:
        continue
    
    clean_title_text = clean_title(toc['title'])
    vendor_class = infer_vendor_class(clean_title_text)
    authority_code = infer_authority_code(clean_title_text)
    amount = infer_amount(clean_title_text)
    expected_route = infer_expected_route(clean_title_text)
    expected_status = infer_expected_status(clean_title_text)
    
    # Build invoice_data
    invoice_data = {
        "company": "10",
        "vendor": vendor_class,
        "invoice_number": f"AUTO-{{{{state.run_group}}}}-{scenario_id.replace('.', '_')}",
        "invoice_date": "{{TODAY_YYYYMMDD}}",
        "due_date": "{{TODAY_PLUS_7_YYYYMMDD}}",
        "invoice_amount": amount,
        "description": f"{clean_title_text} - Automated test"
    }
    
    # Add authority_code only if not None
    if authority_code:
        invoice_data["authority_code"] = authority_code
    
    # Generate standard 7 steps
    steps = [
        {
            "number": 1,
            "description": "Login to FSM",
            "action": {
                "type": "fsm_login",
                "url": "{{FSM_PORTAL_URL}}",
                "username": "{{FSM_USERNAME}}",
                "password": "{{state.password}}",
                "auth_method": "Cloud Identities"
            },
            "expected_result": "Successfully logged into FSM",
            "result": "PENDING"
        },
        {
            "number": 2,
            "description": "Navigate to Payables",
            "action": {
                "type": "fsm_payables",
                "operation": "navigate_to_payables"
            },
            "expected_result": "Payables application loaded",
            "result": "PENDING"
        },
        {
            "number": 3,
            "description": f"Create expense invoice - {clean_title_text}",
            "action": {
                "type": "fsm_payables",
                "operation": "create_invoice",
                "invoice_data": invoice_data
            },
            "expected_result": "Invoice created successfully",
            "result": "PENDING",
            "screenshot": "01_invoice_created"
        },
        {
            "number": 4,
            "description": "Submit invoice for approval",
            "action": {
                "type": "fsm_payables",
                "operation": "submit_for_approval"
            },
            "expected_result": "Invoice submitted for approval workflow",
            "result": "PENDING",
            "screenshot": "02_approval_submitted"
        },
        {
            "number": 5,
            "description": "Navigate to Work Units",
            "action": {
                "type": "fsm_workunits",
                "operation": "navigate"
            },
            "expected_result": "Work Units page loaded",
            "result": "PENDING",
            "screenshot": "03_work_units_page"
        },
        {
            "number": 6,
            "description": "Wait for approval workflow completion",
            "action": {
                "type": "fsm_workunits",
                "operation": "wait_for_completion",
                "process_name": "Expense Invoice Approval",
                "timeout": 300
            },
            "expected_result": "Approval workflow completed",
            "result": "PENDING"
        },
        {
            "number": 7,
            "description": f"Verify workflow completed - Expected route: {expected_route}, Expected status: {expected_status}",
            "action": {
                "type": "fsm_workunits",
                "operation": "verify_status",
                "expected_status": "Completed"
            },
            "expected_result": f"Work unit status is Completed, Invoice status is {expected_status}",
            "result": "PENDING",
            "screenshot": "04_workflow_completed"
        }
    ]
    
    scenario = {
        "scenario_id": scenario_id,
        "title": clean_title_text,
        "description": f"Test scenario {scenario_id}: {clean_title_text}",
        "steps": steps
    }
    
    scenarios.append(scenario)

# Build complete JSON
output = {
    "extension_id": "EXT_FIN_004",
    "interface_type": "approval",
    "description": "Expense Invoice Approval - Regression Test",
    "scenarios": scenarios
}

# Write to file
output_path = 'Projects/SONH/TestScripts/approval/EXT_FIN_004_auto_approval_test.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f"✅ Generated {len(scenarios)} test scenarios")
print(f"📄 Output: {output_path}")
print(f"\nScenarios generated:")
for s in scenarios:
    print(f"  {s['scenario_id']}: {s['title'][:60]}...")
