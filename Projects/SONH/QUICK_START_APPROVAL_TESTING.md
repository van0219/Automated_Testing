# Quick Start: Testing Approval Flows

## What You Need to Know

Approval flow testing is different from inbound/outbound interface testing:

- **No file uploads** - You create transactions directly in FSM UI
- **User interactions** - You submit for approval, then approve/reject as different users
- **Email tracking** - Monitor email notifications at each stage
- **Work unit monitoring** - Track IPA execution in Process Server Administrator

## The 5-Step Process

### 1. Create Transaction in FSM
- Navigate to FSM (e.g., Payables > Create Invoice)
- Fill in details matching your test scenario
- Save transaction
- **Screenshot**: Transaction form

### 2. Submit for Approval
- Click "Submit for Approval" button
- Status changes to "Pending Approval"
- **Screenshot**: Pending status

### 3. Monitor Work Unit
- Go to Process Server Administrator > Work Units
- Find your transaction's work unit
- Note work unit ID
- Wait for status = "Completed"
- **Screenshot**: Work unit details

### 4. Check Emails
- Requester gets "submitted" email
- Approver gets "action required" email
- **Screenshot**: Email notifications

### 5. Approve/Reject
- Log in as approver
- Navigate to inbasket or click email link
- Approve or Reject
- Verify final status (Released/Rejected)
- **Screenshot**: Final status

## Example: Testing EXT_FIN_004

Based on the TES-070 document you provided, here are the key scenarios:

### Scenario 1: Auto-Approved (GHR Vendor)
1. Create invoice with vendor class = "GHR"
2. Submit for approval
3. Verify auto-approved (no approver needed)
4. Check email: "Invoice has been Auto Approved"
5. Verify status = "Released"

### Scenario 2: BOA Approval (EMP Vendor)
1. Create invoice with vendor class = "EMP"
2. Submit for approval
3. Verify routed to BOA approver
4. Log in as BOA approver
5. Approve invoice
6. Verify status = "Released"

### Scenario 3: BOA Rejection (EMP Vendor)
1. Create invoice with vendor class = "EMP"
2. Submit for approval
3. Verify routed to BOA approver
4. Log in as BOA approver
5. Reject invoice
6. Verify status = "Rejected"

### Scenario 4: Two-Level Approval (Other Vendor, ≥$1,000)
1. Create invoice with vendor class ≠ GHR/EMP, amount ≥ $1,000
2. Submit for approval
3. Verify routed to Agency approver
4. Log in as Agency approver, approve
5. Verify routed to BOA approver
6. Log in as BOA approver, approve
7. Verify status = "Released"

## Using the 5-Step Workflow

### Interface Step 0: Generate Test Data (Optional)
If you need test invoices with specific attributes, you can:
- Use existing test vendors in FSM
- Create new test vendors with specific vendor classes
- Use unique invoice numbers (e.g., SONH_TEST_001, SONH_TEST_002)

### Approval Step 1: Define Test Scenarios
1. Click "Approval Step 1: Define Test Scenarios" hook
2. Select "Approval" interface type
3. Template loads with 3 predefined scenarios
4. Customize scenarios based on EXT_FIN_004 requirements
5. Save JSON to `Projects/SONH/TestScripts/approval/EXT_FIN_004_test_scenarios.json`

### Approval Step 2: Execute Tests in FSM
1. Click "Approval Step 2: Execute Tests in FSM" hook
2. AI will use Playwright to automate FSM interactions
3. Screenshots captured at each step
4. Results validated and documented

### Approval Step 3: Generate TES-070
1. Click "Approval Step 3: Generate TES-070" hook
2. AI generates TES-070 document from JSON and screenshots
3. Review document in `Projects/SONH/TES-070/Generated_TES070s/`

## Key Configuration to Check

Before testing, verify:

### 1. Approval Matrix
- **Location**: Application Administrator > Financials > Shared Processes > Approval Matrix > Expense Invoice
- **Check**: Routing rules match your test scenarios
- **Example**: GHR vendor class → auto-approved, EMP vendor class → BOA

### 2. User Tasks
- **Location**: Process Server Administrator > Configuration > User Configuration > Tasks
- **Check**: Approvers are assigned to tasks
- **Example**: SONH-FIN-AP-BOA-APExpInvoice has BOA approvers assigned

### 3. Test Users
- **Requester**: Must have "Payables Invoice Processor" role with Agent
- **Approvers**: Must have appropriate roles and email addresses

## Common Questions

**Q: How do I know which approver to use?**
A: Check the User Tasks configuration in Process Server Administrator. Each task shows assigned approvers.

**Q: What if the work unit shows "Error"?**
A: Open the work unit, check the Variables tab for error details. Document the UI error message (don't analyze logs).

**Q: How long should I wait for approval routing?**
A: Work units typically complete within seconds. If status is "Running" for >1 minute, something may be wrong.

**Q: Can I test escalation and timeout?**
A: Yes, but it requires waiting 5 days for escalation. For testing, you may need to adjust escalation timers in the IPA configuration (requires IPA development access).

**Q: Do I need to test all 21 scenarios from the TES-070?**
A: Start with the core scenarios (auto-approved, single-level approval, two-level approval, rejection). Add edge cases (escalation, exception routing) as needed.

## Next Steps

1. **Read the full guide**: `Projects/SONH/APPROVAL_FLOW_TESTING_GUIDE.md`
2. **Review the TES-070 sample**: `Temp/SoNH_TES-070 - EXT_FIN_004 Expense Invoice Approval Test Results Document.docx`
3. **Verify FSM configuration**: Check Approval Matrix and User Tasks
4. **Start with Scenario 1**: Test auto-approval (GHR vendor) first
5. **Use the 5-step workflow**: Define scenarios → Execute tests → Generate TES-070

## Tips

- **Keep browser open** across all scenarios (saves login time)
- **Use unique invoice numbers** for each test (e.g., SONH_TEST_001, SONH_TEST_002)
- **Document work unit IDs** for reference
- **Capture screenshots** at every step
- **Check email notifications** to verify routing
- **Test one scenario at a time** for clear evidence

## Need Help?

Ask me to:
- "Show me how to create a test invoice for scenario X"
- "Help me verify the Approval Matrix configuration"
- "Explain the difference between Exception and Escalation routing"
- "Generate test scenarios JSON for EXT_FIN_004"
- "Walk me through testing scenario 1 step-by-step"
