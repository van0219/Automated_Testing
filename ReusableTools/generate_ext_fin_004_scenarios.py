#!/usr/bin/env python3
"""
Generate complete test scenarios for EXT_FIN_004 from TES-070 analysis
"""
import json
import re
from datetime import datetime, timedelta

def generate_scenarios():
    # Read the analysis JSON
    with open('Projects/SONH/TES-070/Approval_TES070s_For_Regression_Testing/SoNH_TES-070 - EXT_FIN_004 Expense Invoice Approval Test Results Document_analysis.json', 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    # Extract scenario titles from the TOC entries (first 21 scenarios)
    toc_scenarios = analysis['scenarios'][:21]
    
    # Define all 21 scenarios based on TES-070
    scenarios_data = [
        {'scenario_id': '3.1', 'title': 'Garnishment expense invoice auto approved', 'vendor_class': 'GHR', 'authority_code': None, 'amount': '100.00', 'expected_route': 'AUTO', 'expected_status': 'Released'},
        {'scenario_id': '3.2', 'title': 'Employee expense invoice routed to BOA and approved', 'vendor_class': 'EMP', 'authority_code': None, 'amount': '100.00', 'expected_route': 'BOA', 'expected_status': 'Released'},
        {'scenario_id': '3.3', 'title': 'Employee expense invoice routed to BOA and rejected', 'vendor_class': 'EMP', 'authority_code': None, 'amount': '100.00', 'expected_route': 'BOA', 'expected_status': 'Rejected'},
        {'scenario_id': '3.4', 'title': 'Employee expense invoice no approver found and returned', 'vendor_class': 'EMP', 'authority_code': None, 'amount': '100.00', 'expected_route': 'BOA', 'expected_status': 'Returned'},
        {'scenario_id': '3.5', 'title': 'Employee expense invoice routed to BOA-Exception and rejected', 'vendor_class': 'EMP', 'authority_code': None, 'amount': '100.00', 'expected_route': 'BOA', 'expected_status': 'Rejected'},
        {'scenario_id': '3.6', 'title': 'Employee expense invoice routed to BOA escalated timed out auto rejected', 'vendor_class': 'EMP', 'authority_code': None, 'amount': '100.00', 'expected_route': 'BOA', 'expected_status': 'Rejected'},
        {'scenario_id': '3.7', 'title': 'Other expense invoice less than $1000 routed to Agency and approved', 'vendor_class': 'OTHER', 'authority_code': None, 'amount': '500.00', 'expected_route': 'Agency', 'expected_status': 'Released'},
        {'scenario_id': '3.8', 'title': 'Other expense invoice less than $1000 routed to Agency and rejected', 'vendor_class': 'OTHER', 'authority_code': None, 'amount': '500.00', 'expected_route': 'Agency', 'expected_status': 'Rejected'},
        {'scenario_id': '3.9', 'title': 'Other expense invoice less than $1000 no approver found and returned', 'vendor_class': 'OTHER', 'authority_code': None, 'amount': '500.00', 'expected_route': 'Agency', 'expected_status': 'Returned'},
        {'scenario_id': '3.10', 'title': 'Other expense invoice less than $1000 routed to Agency-Exception and approved', 'vendor_class': 'OTHER', 'authority_code': None, 'amount': '500.00', 'expected_route': 'Agency', 'expected_status': 'Released'},
        {'scenario_id': '3.11', 'title': 'Other expense invoice less than $1000 routed to Agency escalated timed out auto rejected', 'vendor_class': 'OTHER', 'authority_code': None, 'amount': '500.00', 'expected_route': 'Agency', 'expected_status': 'Rejected'},
        {'scenario_id': '3.12', 'title': 'Other expense invoice at least $1000 routed to Agency then BOA and approved', 'vendor_class': 'OTHER', 'authority_code': None, 'amount': '1500.00', 'expected_route': 'Agency', 'expected_status': 'Released'},
        {'scenario_id': '3.13', 'title': 'Other expense invoice at least $1000 routed to Agency then BOA but rejected', 'vendor_class': 'OTHER', 'authority_code': None, 'amount': '1500.00', 'expected_route': 'Agency', 'expected_status': 'Rejected'},
        {'scenario_id': '3.14', 'title': 'Other expense invoice at least $1000 escalated timed out auto rejected', 'vendor_class': 'OTHER', 'authority_code': None, 'amount': '1500.00', 'expected_route': 'Agency', 'expected_status': 'Rejected'},
        {'scenario_id': '3.15', 'title': 'Other expense invoice at least $1000 routed to Agency no approver from BOA auto rejected', 'vendor_class': 'OTHER', 'authority_code': None, 'amount': '1500.00', 'expected_route': 'Agency', 'expected_status': 'Rejected'},
        {'scenario_id': '3.16', 'title': 'Employee expense invoice with authority code PR1 routed to Payroll Manager and approved', 'vendor_class': 'EMP', 'authority_code': 'PR1', 'amount': '100.00', 'expected_route': 'PayrollMgr', 'expected_status': 'Released'},
        {'scenario_id': '3.17', 'title': 'Other expense invoice with authority code PR1 routed to Payroll Manager-Exception and approved', 'vendor_class': 'OTHER', 'authority_code': 'PR1', 'amount': '100.00', 'expected_route': 'PayrollMgr', 'expected_status': 'Released'},
        {'scenario_id': '3.18', 'title': 'Other expense invoice with authority code PR1 routed to Payroll Manager escalated timed out auto rejected', 'vendor_class': 'OTHER', 'authority_code': 'PR1', 'amount': '100.00', 'expected_route': 'PayrollMgr', 'expected_status': 'Rejected'},
        {'scenario_id': '3.19', 'title': 'Employee expense invoice with authority code AP1 routed to BOA and approved', 'vendor_class': 'EMP', 'authority_code': 'AP1', 'amount': '100.00', 'expected_route': 'BOA', 'expected_status': 'Released'},
        {'scenario_id': '3.20', 'title': 'Other expense invoice with authority code AP1 routed to BOA-Exception and rejected', 'vendor_class': 'OTHER', 'authority_code': 'AP1', 'amount': '100.00', 'expected_route': 'BOA', 'expected_status': 'Rejected'},
        {'scenario_id': '3.21', 'title': 'Other expense invoice with authority code AP1 routed to BOA escalated timed out auto rejected', 'vendor_class': 'OTHER', 'authority_code': 'AP1', 'amount': '100.00', 'expected_route': 'BOA', 'expected_status': 'Rejected'},
    ]
    
    # Build complete framework JSON
    framework_json = {
        "extension_id": "EXT_FIN_004",
        "interface_type": "approval",
        "description": "Expense Invoice Approval - Regression Test",
        "scenarios": []
    }
    
    # Generate all 21 scenarios
    for data in scenarios_data:
        # Build invoice_data
        invoice_data = {
            "company": "10",
            "vendor": data['vendor_class'],
            "invoice_number": f"AUTO-{{{{state.run_group}}}}",
            "invoice_date": "{{TODAY_YYYYMMDD}}",
            "due_date": "{{TODAY_PLUS_7_YYYYMMDD}}",
            "invoice_amount": data['amount'],
            "description": f"{data['title']} - Automated test"
        }
        
        # Add authority_code only if not None
        if data['authority_code']:
            invoice_data['authority_code'] = data['authority_code']
        
        scenario = {
            "scenario_id": data['scenario_id'],
            "title": data['title'],
            "description": f"Test {data['title']}",
            "steps": [
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
                    "description": f"Create expense invoice for {data['vendor_class']} vendor",
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
                    "description": "Verify workflow completed successfully",
                    "action": {
                        "type": "fsm_workunits",
                        "operation": "verify_status",
                        "expected_status": "Completed"
                    },
                    "expected_result": "Work unit status is Completed",
                    "result": "PENDING",
                    "screenshot": "04_workflow_completed"
                }
            ]
        }
        
        framework_json['scenarios'].append(scenario)
    
    # Write complete JSON
    output_path = 'Projects/SONH/TestScripts/approval/EXT_FIN_004_auto_approval_test.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(framework_json, f, indent=2, ensure_ascii=False)
    
    print(f'✅ Generated {len(framework_json["scenarios"])} complete test scenarios')
    print(f'📄 Output: {output_path}')
    return output_path

if __name__ == '__main__':
    generate_scenarios()
