# Executable Approval Test Scenarios - EXT_FIN_004

## Overview

This document describes the executable test scenario file created for automated testing of the Expense Invoice Approval workflow (EXT_FIN_004).

## File Location

**Executable Scenario File**: `Projects/SONH/TestScripts/approval/EXT_FIN_004_executable_approval_test.json`

## Scenarios Included

### Scenario 3.1: GHR Vendor Class - Auto Approval
- **Vendor**: 176258 (GHR vendor class)
- **Amount**: $500.00
- **Expected Behavior**: Invoice auto-approved without routing to approvers
- **Validation**: Work unit completes with status "Completed"

### Scenario 3.2: EMP Vendor Class - Routed to BOA
- **Vendor**: 176259 (EMP vendor class)
- **Amount**: $750.00
- **Expected Behavior**: Invoice routed to BOA approver for manual approval
- **Validation**: Work unit created with status "Processing"

### Scenario 3.3: 1099 Vendor Class - Routed to Agency
- **Vendor**: 176260 (1099 vendor class)
- **Amount**: $850.00 (< $1000)
- **Expected Behavior**: Invoice routed to Agency approver for manual approval
- **Validation**: Work unit created with status "Processing"

## Framework Actions Used

### 1. fsm_login
- Authenticates to FSM portal using Cloud Identities
- Parameters: url, username, password, auth_method

### 2. fsm_payables
- **navigate_to_payables**: Navigate to Payables application
- **create_invoice**: Create expense invoice with specified data
- **submit_for_approval**: Submit invoice for approval workflow

### 3. fsm_workunits
- **navigate**: Navigate to Work Units page
- **search**: Search for work units by process name
- **verify_status**: Verify work unit status matches expected value

### 4. wait
- Pause execution for specified duration
- Used to allow IPA processes to complete

## State Variables

The following state variables are interpolated at runtime:

- `{{FSM_PORTAL_URL}}` - FSM portal URL from credentials
- `{{FSM_USERNAME}}` - FSM username from credentials
- `{{state.password}}` - FSM password from credentials
- `{{state.run_group}}` - Unique test identifier (AUTOTEST_timestamp_random)
- `{{TODAY_YYYYMMDD}}` - Current date in YYYYMMDD format
- `{{TODAY_PLUS_7_YYYYMMDD}}` - Current date + 7 days in YYYYMMDD format

## Execution Instructions

### Option 1: Via Testing Framework (Recommended)

```bash
python ReusableTools/run_approval_tests_v2.py \
  --client SONH \
  --scenario Projects/SONH/TestScripts/approval/EXT_FIN_004_executable_approval_test.json \
  --environment ACUITY_TST \
  --url "https://mingle-portal.inforcloudsuite.com/SONH" \
  --username "your_username" \
  --password "your_password"
```

### Option 2: Via Hook (User-Friendly)

1. Click "Run FSM Approval Regression Tests" hook
2. Select client: SONH
3. Select scenario file: EXT_FIN_004_executable_approval_test.json
4. Enter FSM credentials when prompted
5. Watch real-time progress in console

## Expected Output

### Evidence Screenshots
- Captured at each critical step
- Saved to: `Projects/SONH/Temp/evidence/`
- Naming convention: `{scenario_id}_{step_number}_{description}.png`

### TES-070 Report
- Generated automatically after test execution
- Location: `Projects/SONH/TES-070/Generated_TES070s/`
- Filename: `TES-070_{timestamp}_EXT_FIN_004.docx`

### Console Output
Real-time progress reporting shows:
- Current scenario being executed
- Step-by-step pass/fail status
- Error messages with context
- Final summary with pass/fail counts

## Limitations & Notes

### Current Scope
- ✅ Invoice creation and submission
- ✅ Auto-approval validation (GHR vendor class)
- ✅ Routing validation (EMP and 1099 vendor classes)
- ✅ Work unit monitoring

### Out of Scope (Requires Manual Testing)
- ❌ Manual approval/rejection via FSM Inbasket
- ❌ Invoice status validation (Unreleased → Pending Approval → Released/Rejected)
- ❌ Email notification verification
- ❌ Escalation and timeout scenarios

### Why Manual Approval Required?
The `fsm_inbasket` action for automated approval/rejection is not yet implemented in the testing framework. Scenarios 3.2 and 3.3 validate that invoices are correctly routed to approvers, but the actual approval/rejection must be performed manually via FSM Inbasket.

## Future Enhancements

To achieve full end-to-end automation, the following actions need to be implemented:

1. **fsm_inbasket** action with operations:
   - `navigate_to_inbasket`: Navigate to FSM Inbasket
   - `find_work_item`: Locate invoice in inbasket by invoice number
   - `approve_work_item`: Approve invoice from inbasket
   - `reject_work_item`: Reject invoice from inbasket with reason

2. **validate_invoice_status** action:
   - Validate invoice status matches expected value
   - Capture screenshots before/after validation
   - Support status transitions: Unreleased → Pending Approval → Released/Rejected

3. **Additional scenarios** from TES-070:
   - Scenario 3.4: No approver found (returned)
   - Scenario 3.5: BOA-Exception routing
   - Scenario 3.6: Escalation and timeout
   - Scenarios 3.7-3.21: Various routing and approval combinations

## Vendor Information

The following vendors are used in test scenarios:

| Vendor ID | Vendor Class | Description |
|-----------|--------------|-------------|
| 176258    | GHR          | Garnishment vendor (auto-approval) |
| 176259    | EMP          | Employee vendor (BOA approval) |
| 176260    | 1099         | 1099 vendor (Agency approval) |

**Note**: Verify these vendor IDs exist in ACUITY_TST environment before running tests.

## Troubleshooting

### Common Issues

1. **Vendor not found**
   - Verify vendor IDs exist in FSM
   - Check vendor class assignments
   - Update vendor IDs in scenario file if needed

2. **Work unit not found**
   - Increase wait duration in step parameters
   - Verify process name: "SONH_ExpenseInvoiceApproval"
   - Check Process Server Administrator for work unit status

3. **Login fails**
   - Verify FSM credentials in `Projects/SONH/Credentials/.env.passwords`
   - Check FSM portal URL is correct
   - Ensure user has Payables Invoice Processor role

4. **Navigation fails**
   - Check if Payables is set as preferred application
   - Verify iframe selectors are correct
   - Increase wait times if FSM is slow to load

## Contact

For questions or issues with these test scenarios, contact the QA Automation Team.

---

**Last Updated**: 2026-03-06  
**Version**: 1.0  
**Status**: Ready for execution (with manual approval for scenarios 3.2 and 3.3)
