# Regression TES-070 Generator

Generate updated TES-070 documents from approval workflow test execution results.

## Purpose

After running automated regression tests on FSM approval workflows (Phase 3), this tool generates a professional TES-070 Word document with:
- Updated test summary (Pass/Fail statistics)
- All test scenarios with current results
- Embedded evidence screenshots
- Expected vs Actual comparisons
- Work unit references
- Execution metadata (date, tester, environment)

## Usage

```bash
python ReusableTools/generate_regression_tes070.py <test_results_json>
```

### Example

```bash
python ReusableTools/generate_regression_tes070.py Projects/SONH/Temp/test_results_EXT_FIN_004.json
```

## Input: Test Results JSON

The tool expects a JSON file with the following structure:

```json
{
  "extension_id": "EXT_FIN_004",
  "document_title": "Expense Invoice Approval Workflow",
  "client_name": "SONH",
  "test_date": "2026-03-10",
  "tester_name": "Kiro Agent",
  "environment": "ACUITY_TST",
  "user_roles": ["Payables", "Process Server Administrator"],
  "configuration_notes": "Standard approval workflow configuration",
  "scenarios": [
    {
      "scenario_id": "3.1",
      "scenario_title": "Garnishment Invoice Auto-Approval",
      "description": "Test auto-approval for garnishment invoices",
      "status": "PASS",
      "steps": [
        {
          "step_number": 1,
          "description": "Login to FSM as Payables role",
          "result": "PASS",
          "screenshot": "scenario_3.1_step_1_login.png"
        }
      ],
      "expected_result": "Invoice auto-approved",
      "actual_result": "Invoice auto-approved successfully",
      "work_unit_id": "12345"
    }
  ],
  "summary": {
    "total_scenarios": 5,
    "passed": 4,
    "failed": 1,
    "pass_rate": 80.0
  }
}
```

### Required Fields

- `extension_id` - Extension ID (e.g., EXT_FIN_004)
- `client_name` - Client name (e.g., SONH)
- `test_date` - Test execution date (YYYY-MM-DD)
- `scenarios` - Array of test scenarios
- `summary` - Test summary statistics

### Optional Fields

- `document_title` - Document title (defaults to "Approval Workflow")
- `tester_name` - Tester name (defaults to "Kiro Agent")
- `environment` - FSM environment (defaults to "ACUITY_TST")
- `user_roles` - User roles used in testing
- `configuration_notes` - Configuration prerequisites

## Evidence Screenshots

The tool automatically finds screenshots in:

```
Projects/{ClientName}/Temp/evidence/scenario_{scenario_id}/
```

Example:
```
Projects/SONH/Temp/evidence/scenario_3.1/
  ├── scenario_3.1_step_1_login.png
  ├── scenario_3.1_step_2_navigation.png
  ├── scenario_3.1_step_3_invoice_creation.png
  └── scenario_3.1_step_4_submission.png
```

Screenshots are embedded in the TES-070 document in the order they appear in the evidence folder.

## Output

The tool generates a Word document in:

```
Projects/{ClientName}/TES-070/Generated_TES070s/{Client}_{ExtensionID}_Regression_{date}.docx
```

Example:
```
Projects/SONH/TES-070/Generated_TES070s/SONH_EXT_FIN_004_Regression_20260310.docx
```

## Document Structure

The generated TES-070 document includes:

### 1. Title Page
- Client name
- Document title with extension ID
- Version: Regression_{date}
- Test date
- Author name

### 2. Document Control Table
- Document ID
- Version
- Author
- Creation date
- Status
- Environment

### 3. Test Summary Table
| Metric | Value |
|--------|-------|
| Count of Total Tests | 5 |
| Count of Completed Tests | 5 |
| % of Completed Tests | 100% |
| Count of Passed Tests | 4 |
| Count of Failed Tests | 1 |
| % of Passed Tests | 80% |

### 4. Prerequisites Section
- Environment
- User roles
- Test data requirements
- Configuration prerequisites

### 5. Test Scenarios
For each scenario:
- Scenario title and description
- Test steps table with Pass/Fail results
- Embedded screenshots
- Expected vs Actual results
- Work unit ID
- Overall status (✅ PASS or ❌ FAIL)

### 6. Table of Contents
Auto-generated with page numbers (update with F9 in Word)

## Formatting Standards

The tool applies TES-070 formatting standards:

- **Font**: Arial (NOT Calibri)
- **Title Page**: 18pt bold
- **Headings**: 14pt bold (H1), 12pt bold (H2)
- **Body Text**: 11pt
- **Table Text**: 10pt
- **Colors**: Infor Blue (#13A3F7), Black, White, Gray
- **Page Size**: A4 with 1" margins
- **Headers/Footers**: Document title, version, page numbers

## Example Output

```
SONH_TES-070 - EXT_FIN_004 Expense Invoice Approval Workflow
Regression Test Results

Version: Regression_2026-03-10
Date: March 10, 2026
Author: Kiro Agent
Environment: ACUITY_TST

═══════════════════════════════════════════════════════

TEST SUMMARY

| Metric                      | Value |
|-----------------------------|-------|
| Count of Total Tests        | 5     |
| Count of Completed Tests    | 5     |
| % of Completed Tests        | 100%  |
| Count of Passed Tests       | 4     |
| Count of Failed Tests       | 1     |
| % of Passed Tests           | 80%   |

═══════════════════════════════════════════════════════

SCENARIO 3.1: GARNISHMENT INVOICE AUTO-APPROVAL

Test Steps:

| Step # | Test Step Description              | Result |
|--------|------------------------------------|--------|
| 1      | Login to FSM as Payables role      | PASS   |
| 2      | Create expense invoice...          | PASS   |
| 3      | Submit for approval                | PASS   |

Expected Result: Invoice auto-approved
Actual Result: Invoice auto-approved successfully
Work Unit ID: 12345
Status: ✅ PASS

[Screenshots embedded here]
```

## Integration with FSM Approval Testing Power

This tool is Phase 5 of the FSM Approval Testing Power workflow:

1. **Phase 1**: Parse TES-070 Document
2. **Phase 2**: Create Test Instructions
3. **Phase 3**: Execute Tests (generates test_results JSON)
4. **Phase 4**: Report Results
5. **Phase 5**: Generate Updated TES-070 (this tool)

## Dependencies

Install required Python packages:

```bash
pip install python-docx Pillow
```

The tool also requires:
- `tes070_generator.py` - Core TES-070 generation module (included in ReusableTools)

## Troubleshooting

### Error: File not found

**Issue**: Test results JSON file not found

**Solution**: Verify the path to the JSON file is correct. Use relative path from workspace root.

### Warning: Evidence folder not found

**Issue**: Screenshots not found for a scenario

**Solution**: 
- Verify screenshots exist in `Projects/{Client}/Temp/evidence/scenario_{id}/`
- Check scenario ID matches folder name
- Tool will continue without screenshots (placeholders added)

### Error: Missing required fields

**Issue**: JSON structure is invalid

**Solution**: Verify JSON contains all required fields:
- `extension_id`
- `client_name`
- `test_date`
- `scenarios`
- `summary`

## Sample Test Results

A sample test results JSON is provided in:
```
ReusableTools/sample_test_results.json
```

Test the tool with:
```bash
python ReusableTools/generate_regression_tes070.py ReusableTools/sample_test_results.json
```

## Related Documentation

- `.kiro/powers/fsm-approval-testing/POWER.md` - Complete power documentation
- `.kiro/powers/fsm-approval-testing/steering/tes070-generation.md` - Phase 5 workflow guide
- `.kiro/steering/tes-070-standards` - TES-070 formatting standards
- `ReusableTools/tes070_generator.py` - Core generation module

## Version History

- **1.0.0** (2026-03-10) - Initial release
  - Test results JSON to TES-070 Word document
  - Screenshot embedding
  - TES-070 formatting standards
  - Pass/Fail status tracking
  - Work unit references
  - Expected vs Actual comparisons

## License

Proprietary - For internal use only
