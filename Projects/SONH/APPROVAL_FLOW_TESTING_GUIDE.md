# Approval Flow Testing Guide for SONH

## Overview

This guide explains how to test approval workflows in FSM based on the EXT_FIN_004 Expense Invoice Approval process. Use this as a template for testing any approval flow.

## What is an Approval Flow?

An approval flow is an IPA-based process that:
1. Routes transactions (invoices, requisitions, etc.) to designated approvers
2. Creates User Actions in approvers' inbaskets
3. Sends email notifications to approvers
4. Handles approvals, rejections, escalations, and timeouts
5. Updates transaction status based on approval decisions

## Key Components

### 1. Approval Matrix
- **Location**: Application Administrator > Financials > Shared Processes > Approval Matrix
- **Purpose**: Defines routing rules based on transaction attributes
- **Configuration**: Transaction type, authority codes, vendor class, amount ranges, etc.

### 2. User Tasks (Approver Tasks)
- **Location**: Process Server Administrator > Configuration > User Configuration > Tasks
- **Purpose**: Assigns specific users to approval roles
- **Features**: Filter values (e.g., agency-specific approvers), escalation settings

### 3. Work Units
- **Location**: Process Server Administrator > Administration > Work Units
- **Purpose**: Track IPA execution for each approval flow instance
- **Status**: Running, Completed, Error

### 4. Email Notifications
- Sent to requesters and approvers at each stage
- Contain transaction details and approval links
- Track approval history

## Testing Workflow

### Step 1: Understand the Approval Logic

Before testing, document the approval routing rules:

**Example from EXT_FIN_004:**
- **GHR vendor class** → Auto-approved (no approver needed)
- **EMP vendor class** → Routes to BOA
- **Authority Code = AP1** → Routes to BOA (regardless of vendor class/amount)
- **Authority Code = PR1** → Routes to Payroll Manager
- **Other invoices < $1,000** → Routes to Agency only
- **Other invoices ≥ $1,000** → Routes to Agency, then BOA
- **Exception routing** → If requester is also an approver, routes to Exception task
- **Escalation** → After 5 days of no response, escalates to Escalation task
- **Timeout** → After escalation reminders, auto-rejects if no action

### Step 2: Verify Prerequisites

Check that the following are configured:

1. **Approval Matrix** is set up with correct routing rules
2. **User Tasks** have approvers assigned
3. **Requester** has appropriate role (e.g., Payables Invoice Processor with Agent)
4. **Approvers** have appropriate roles and email addresses
5. **Security roles** are assigned (if testing matrix administration)

### Step 3: Define Test Scenarios

Create scenarios that cover:

**Happy Path:**
- Standard approval (routed to correct approver, approved)
- Auto-approval (if applicable)

**Alternative Paths:**
- Rejection by approver
- No approver found (returned to requester)
- Exception routing (requester is also approver)

**Error Paths:**
- Escalation (no response after 5 days)
- Timeout and auto-rejection

**Example Scenarios from EXT_FIN_004:**
1. Garnishment invoice (GHR) → Auto-approved
2. Employee invoice (EMP) → BOA approves
3. Employee invoice (EMP) → BOA rejects
4. Employee invoice (EMP) → No approver found, returned
5. Employee invoice (EMP) → Exception routing, rejected
6. Employee invoice (EMP) → Escalated, timed out, auto-rejected
7. Other invoice < $1,000 → Agency approves
8. Other invoice < $1,000 → Agency rejects
9. Other invoice ≥ $1,000 → Agency approves, BOA approves
10. Other invoice ≥ $1,000 → Agency approves, BOA rejects
11. Invoice with Authority Code = AP1 → BOA approves
12. Invoice with Authority Code = PR1 → Payroll Manager approves

### Step 4: Execute Tests

For each scenario:

#### 4.1 Create Transaction
- Navigate to FSM UI (e.g., Payables > Create Invoice)
- Fill in transaction details matching scenario criteria
- **Screenshot**: Transaction creation form

#### 4.2 Submit for Approval
- Click "Submit for Approval"
- Verify status changes to "Pending Approval"
- **Screenshot**: Pending approval status

#### 4.3 Monitor Work Unit
- Navigate to Process Server Administrator > Work Units
- Find work unit for this transaction (search by invoice number or recent timestamp)
- Note work unit ID
- Verify status (Running → Completed)
- **Screenshot**: Work unit details

#### 4.4 Check Email Notifications
- Verify requester receives "submitted for approval" email
- Verify approver receives "action required" email
- **Screenshot**: Email notifications

#### 4.5 Perform Approval Action
- Log in as approver (or use approver's inbasket)
- Navigate to inbasket or click email link
- Approve or Reject transaction
- **Screenshot**: Approval action

#### 4.6 Verify Final Status
- Check transaction status in FSM (e.g., Released, Rejected, Returned)
- Verify requester receives final notification email
- **Screenshot**: Final transaction status

#### 4.7 Validate Data
- For approved transactions: Verify data is correct (amounts, distributions, etc.)
- For rejected transactions: Verify status and reason code
- **Screenshot**: Transaction details

### Step 5: Document Results

For each test step, capture:
- **Step number and description**
- **Expected result**
- **Actual result**
- **Screenshot** (FSM UI, email, work unit)
- **Pass/Fail status**

## Test Data Requirements

### For Approval Flow Testing:

1. **Vendors** with different vendor classes (GHR, EMP, etc.)
2. **Test users** assigned to approval tasks
3. **Test invoices** with varying:
   - Vendor classes
   - Authority codes
   - Amounts (to test threshold routing)
   - Accounting entities/agencies

### Creating Test Data:

**Option 1: Use existing test vendors/users**
- Query FSM to find test vendors: Payables > Vendors > Search
- Check User Tasks to see assigned approvers

**Option 2: Create new test data**
- Create test vendors with specific vendor classes
- Assign test users to approval tasks
- Use unique invoice numbers (e.g., RMBFIN004-001, RMBFIN004-002)

## Common Pitfalls

1. **Forgetting to expand FSM sidebar** before navigation
2. **Not waiting for work unit to complete** before checking status
3. **Missing email notifications** (check spam folder, verify email addresses)
4. **Incorrect approval matrix configuration** (verify routing rules match requirements)
5. **Approver not assigned to task** (check User Tasks configuration)
6. **Using production data** instead of test data (always use test vendors/invoices)

## Automation Considerations

### Manual Testing (Recommended for Initial Testing):
- Use Playwright to automate FSM UI interactions
- Capture screenshots at each step
- Manually check email notifications
- Manually verify work unit status

### Automated Testing (For Regression):
- Use testing framework with JSON scenarios
- Automate transaction creation via FSM API (if available)
- Monitor work units via Process Server Administrator UI
- Parse email notifications (if email API available)

## Example Test Scenario JSON Structure

```json
{
  "interface_id": "EXT_FIN_004",
  "interface_type": "approval",
  "scenarios": [
    {
      "scenario_id": "S001",
      "title": "Garnishment invoice auto-approved",
      "description": "Requester submits expense invoice with vendor class = GHR, which is auto-approved",
      "steps": [
        {
          "number": 1,
          "description": "Create expense invoice with vendor class = GHR",
          "action": {
            "type": "ui_interaction",
            "details": "Navigate to Payables > Create Invoice, fill form, save"
          },
          "screenshot": "S001_step1_create_invoice"
        },
        {
          "number": 2,
          "description": "Submit invoice for approval",
          "action": {
            "type": "ui_interaction",
            "details": "Click 'Submit for Approval' button"
          },
          "screenshot": "S001_step2_submit_approval"
        },
        {
          "number": 3,
          "description": "Verify work unit created and completed",
          "validation": {
            "type": "workunit",
            "expected_status": "Completed"
          },
          "screenshot": "S001_step3_work_unit"
        },
        {
          "number": 4,
          "description": "Verify email notification received",
          "validation": {
            "type": "email",
            "expected_subject": "Invoice .* has been Auto Approved"
          },
          "screenshot": "S001_step4_email_notification"
        },
        {
          "number": 5,
          "description": "Verify invoice status is Released",
          "validation": {
            "type": "ui_check",
            "expected_status": "Released"
          },
          "screenshot": "S001_step5_final_status"
        }
      ]
    }
  ]
}
```

## Next Steps

### To start testing the SONH approval flow:

1. **Review the TES-070 document** to understand all 21 scenarios
2. **Verify FSM configuration**:
   - Check Approval Matrix (Application Administrator role)
   - Check User Tasks (Process Server Administrator role)
   - Verify test users have correct roles
3. **Create test data** (if needed):
   - Test vendors with different vendor classes
   - Test invoices with unique numbers
4. **Run Approval Step 1: Define Test Scenarios**:
   - Use Test Scenario Builder GUI
   - Load approval workflow template
   - Customize scenarios based on EXT_FIN_004 requirements
5. **Run Approval Step 2: Execute Tests in FSM**:
   - Use Playwright automation
   - Capture screenshots at each step
   - Document results
6. **Run Approval Step 3: Generate TES-070**:
   - Generate final TES-070 document
   - Review and finalize

## Key Differences: Approval vs Inbound/Outbound

| Aspect | Inbound/Outbound | Approval Flow |
|--------|------------------|---------------|
| **Trigger** | File upload or schedule | User action (Submit for Approval) |
| **Data Source** | External file or FSM query | FSM transaction (invoice, requisition) |
| **Validation** | File format, data integrity | Approval routing, user permissions |
| **Evidence** | File contents, FSM data | Email notifications, work units, transaction status |
| **User Interaction** | Minimal (upload file) | High (create transaction, approve/reject) |
| **Test Data** | CSV/JSON files | FSM transactions (invoices, requisitions) |

## Resources

- **TES-070 Sample**: `Temp/SoNH_TES-070 - EXT_FIN_004 Expense Invoice Approval Test Results Document.docx`
- **Approval Template**: `.kiro/templates/approval_workflow_template.json`
- **FSM Navigation Guide**: Load steering file 01_FSM_Navigation_Guide.md
- **IPA Guide**: Load steering file 03_IPA_and_IPD_Complete_Guide.md

## Questions?

If you're unsure about:
- **Approval Matrix configuration** → Check with Application Administrator
- **User Task assignments** → Check with Process Server Administrator
- **Routing logic** → Review ANA-050/DES-020 specification document
- **Test data** → Use existing test vendors or create new ones
- **Automation** → Start with manual testing, then automate repetitive scenarios
