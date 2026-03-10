# TES-070 Generation Workflow

## Overview

After executing test scenarios with browser automation, this workflow generates an updated TES-070 Word document with:
- Test execution results (Pass/Fail status)
- Embedded evidence screenshots
- Actual vs Expected comparisons
- Execution metadata (date, tester, environment)
- Work unit references

## Purpose

Regression testing requires updated TES-070 documents to show stakeholders the current state of testing. Even though an original TES-070 exists, it may be outdated. This workflow creates a new TES-070 with fresh test results.

## Input Requirements

### Test Execution Results

**Location**: `Projects/{Client}/Temp/test_results_{extension_id}.json`

**Required Fields**:
```json
{
  "extension_id": "EXT_FIN_004",
  "document_title": "Expense Invoice Approval Workflow",
  "client_name": "SONH",
  "test_date": "2026-03-10",
  "tester_name": "Kiro Agent",
  "environment": "ACUITY_TST",
  "scenarios": [
    {
      "scenario_id": "3.1",
      "scenario_title": "Garnishment Invoice Auto-Approval",
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

### Evidence Screenshots

**Location**: `Projects/{Client}/Temp/evidence/{scenario_id}/`

**Naming Convention**: `scenario_{scenario_id}_step_{step_number}_{action}.png`

**Examples**:
- `scenario_3.1_step_1_login.png`
- `scenario_3.1_step_2_invoice_creation.png`
- `scenario_3.1_step_3_submission.png`
- `scenario_3.1_step_4_work_unit_status.png`

### Original TES-070 Document

**Location**: `Projects/{Client}/TES-070/Approval_TES070s_For_Regression_Testing/{extension_id}*.docx`

**Purpose**: Reference for document structure, scenario descriptions, and formatting

## Output

**Location**: `Projects/{Client}/TES-070/Generated_TES070s/{client}_{extension_id}_Regression_{timestamp}.docx`

**Example**: `SONH_EXT_FIN_004_Regression_2026-03-10.docx`

## Workflow Steps

### Step 1: Prepare Test Results JSON

During test execution (Phase 3), capture all required data:

1. **Initialize Results Structure**
   ```python
   test_results = {
       "extension_id": extension_id,
       "document_title": "Expense Invoice Approval Workflow",
       "client_name": client_name,
       "test_date": datetime.now().strftime("%Y-%m-%d"),
       "tester_name": "Kiro Agent",
       "environment": "ACUITY_TST",
       "scenarios": [],
       "summary": {}
   }
   ```

2. **For Each Scenario**:
   - Record scenario ID, title, description
   - Track each test step with result (PASS/FAIL)
   - Capture screenshot filenames
   - Record expected vs actual results
   - Save work unit IDs
   - Set overall scenario status

3. **Calculate Summary Statistics**:
   - Total scenarios
   - Passed count
   - Failed count
   - Pass rate percentage

4. **Save Results JSON**:
   ```python
   output_path = f"Projects/{client}/Temp/test_results_{extension_id}.json"
   with open(output_path, 'w') as f:
       json.dump(test_results, f, indent=2)
   ```

### Step 2: Generate TES-070 Document

Use the regression TES-070 generator tool with test results:

**Command**:
```bash
python ReusableTools/generate_regression_tes070.py \
  "Projects/{Client}/Temp/test_results_{extension_id}.json"
```

**Tool Behavior**:
1. Load test results JSON
2. Load TES-070 template (regression format)
3. Populate document metadata
4. Generate test summary table
5. Add prerequisites section
6. For each scenario:
   - Add scenario title and description
   - Create test steps table
   - Embed screenshots from evidence folder
   - Add expected vs actual results
   - Show Pass/Fail status
7. Generate table of contents
8. Apply TES-070 formatting standards
9. Save Word document

### Step 3: Validate Generated Document

**Validation Checklist**:
- [ ] Document title includes client, extension ID, "Regression", and date
- [ ] Test summary table shows correct statistics
- [ ] All scenarios included with correct status
- [ ] Screenshots embedded and visible
- [ ] Test steps table formatted correctly
- [ ] Expected vs Actual results documented
- [ ] Work unit IDs referenced
- [ ] Table of contents generated
- [ ] Formatting matches TES-070 standards (Arial font, correct sizes)

### Step 4: Report Generation Results

Display summary to user:

```
## TES-070 Document Generated Successfully!

**Document**: SONH_EXT_FIN_004_Regression_2026-03-10.docx
**Location**: Projects/SONH/TES-070/Generated_TES070s/

**Test Summary**:
- Total Scenarios: 5
- Passed: 4
- Failed: 1
- Pass Rate: 80%

**Scenarios**:
✅ 3.1 - Garnishment Invoice Auto-Approval
✅ 3.2 - Manual Journal Approval
❌ 3.3 - Cash Transaction Approval (Failed: Work unit timeout)
✅ 3.4 - Invoice with Distributions
✅ 3.5 - Multi-Level Approval

**Evidence**: 23 screenshots embedded

**Next Steps**:
1. Review generated document
2. Share with stakeholders
3. Address failed scenarios if needed
```

## TES-070 Document Structure

### Title Page

- Client logo (if available)
- Document title: `{Client}_TES-070 - {Extension ID} {Title} Regression Test Results`
- Version: `Regression_{date}`
- Date: Test execution date
- Author: "Kiro Agent" or tester name

### Document Control Table

| Field | Value |
|-------|-------|
| Document ID | TES-070-{Extension ID}-Regression |
| Version | Regression_{date} |
| Author | Kiro Agent |
| Creation Date | {test_date} |
| Last Updated | {test_date} |
| Status | Completed |
| Environment | {environment} |

### Test Summary Table

| Metric | Value |
|--------|-------|
| Count of Total Tests | {total_scenarios} |
| Count of Completed Tests | {total_scenarios} |
| % of Completed Tests | 100% |
| Count of Passed Tests | {passed} |
| Count of Failed Tests | {failed} |
| % of Passed Tests | {pass_rate}% |

### Prerequisites Section

```
Prerequisites:
- Environment: {environment}
- User Roles: {roles_used}
- Test Data: Live FSM data
- Configuration: {configuration_notes}
- Dependencies: {dependencies}
```

### Test Scenarios

For each scenario:

**Scenario {scenario_id}: {scenario_title}**

**Description**: {scenario_description}

**Test Steps**:

| Step # | Test Step Description | Result |
|--------|----------------------|--------|
| 1 | {step_description} | {PASS/FAIL} |
| 2 | {step_description} | {PASS/FAIL} |

**Expected Result**: {expected_result}

**Actual Result**: {actual_result}

**Work Unit ID**: {work_unit_id}

**Status**: ✅ PASS or ❌ FAIL

**Evidence**:
- Screenshot 1: {description}
  [Embedded image]
- Screenshot 2: {description}
  [Embedded image]

## Formatting Standards

### Font and Typography

- **Primary Font**: Arial (NOT Calibri)
- **Title Page**: 18pt bold
- **Heading 1**: 14pt bold, ALL CAPS
- **Heading 2**: 14pt bold, Title Case
- **Body text**: 11pt
- **Table text**: 10pt
- **Table headers**: 10pt bold

### Colors

- **Infor Blue**: #13A3F7 (for highlights)
- **Black**: #000000 (for text)
- **White**: #FFFFFF (for table headers)
- **Gray**: #F2F2F2 (for alternating table rows)

### Page Layout

- **Page Size**: A4 (8.27" x 11.69")
- **Margins**: 1" all sides
- **Headers**: Document title (left), Version (right)
- **Footers**: Page number (center), Date (right)

### Table Formatting

- **Header row**: Black background, white text, bold
- **Body rows**: Alternating white/light gray
- **Cell padding**: 5pt
- **Borders**: 1pt solid black

## Screenshot Embedding

### Best Practices

1. **Embed, Don't Link**: Screenshots should be embedded in document, not linked
2. **Resize Appropriately**: Scale to fit page width (6.5" max)
3. **Maintain Aspect Ratio**: Don't distort images
4. **Add Captions**: Brief description below each screenshot
5. **Group by Step**: Keep screenshots with their corresponding test steps

### Screenshot Captions

Format: `Figure {number}: {description}`

Examples:
- `Figure 1: FSM Login Screen`
- `Figure 2: Invoice Creation Form`
- `Figure 3: Submission Confirmation`
- `Figure 4: Work Unit Status - Completed`

## Error Handling

### Missing Screenshots

**Issue**: Screenshot file not found in evidence folder

**Solution**:
- Log warning with missing filename
- Add placeholder text: `[Screenshot not available: {filename}]`
- Continue document generation
- Report missing screenshots in summary

### Invalid Test Results JSON

**Issue**: JSON structure doesn't match expected format

**Solution**:
- Validate JSON schema before generation
- Report specific validation errors
- Suggest corrections
- Do not generate document until JSON is valid

### Template Not Found

**Issue**: TES-070 template file missing

**Solution**:
- Check template location: `ReusableTools/templates/tes070_regression_template.docx`
- If missing, create minimal template with required sections
- Log warning about using minimal template

## Integration with Test Execution

### Phase 3 Updates (Test Execution)

Add result tracking to test execution workflow:

```python
# Initialize results at start of Phase 3
test_results = initialize_test_results(extension_id, client_name)

# For each scenario
for scenario in test_instructions["scenarios"]:
    scenario_result = {
        "scenario_id": scenario["id"],
        "scenario_title": scenario["title"],
        "status": "IN_PROGRESS",
        "steps": [],
        "work_unit_id": None
    }
    
    # Execute each step
    for step in scenario["steps"]:
        step_result = execute_step(step)
        scenario_result["steps"].append({
            "step_number": step["number"],
            "description": step["description"],
            "result": "PASS" if step_result.success else "FAIL",
            "screenshot": step_result.screenshot_filename
        })
    
    # Set overall scenario status
    scenario_result["status"] = "PASS" if all_steps_passed else "FAIL"
    test_results["scenarios"].append(scenario_result)

# Calculate summary
test_results["summary"] = calculate_summary(test_results["scenarios"])

# Save results JSON
save_test_results(test_results, client_name, extension_id)
```

### Phase 4 Updates (Report Results)

Add TES-070 generation to reporting:

```python
# After displaying console summary
print("\n## Generating TES-070 Document...")

# Generate TES-070
generate_tes070(
    input_json=f"Projects/{client}/Temp/test_results_{extension_id}.json",
    output_dir=f"Projects/{client}/TES-070/Generated_TES070s/",
    template="regression"
)

print(f"✅ TES-070 document generated: {output_filename}")
print(f"📁 Location: Projects/{client}/TES-070/Generated_TES070s/")
```

## Tool Requirements

### generate_regression_tes070.py

**Location**: `ReusableTools/generate_regression_tes070.py`

**Dependencies**:
- `python-docx` - Word document generation
- `Pillow` - Image processing
- `json` - JSON parsing
- `tes070_generator` - Core TES-070 generation module

**Usage**:
```bash
python ReusableTools/generate_regression_tes070.py Projects/SONH/Temp/test_results_EXT_FIN_004.json
```

**Key Functions**:

1. `load_test_results(json_path)` - Load and validate test results JSON
2. `create_document_from_template(template_path)` - Load TES-070 template
3. `populate_metadata(doc, results)` - Add title page and document control
4. `generate_summary_table(doc, results)` - Create test summary table
5. `add_scenario(doc, scenario, evidence_path)` - Add scenario with screenshots
6. `embed_screenshot(doc, image_path, caption)` - Embed and format screenshot
7. `apply_formatting(doc)` - Apply TES-070 formatting standards
8. `generate_toc(doc)` - Generate table of contents
9. `save_document(doc, output_path)` - Save Word document

### Template File

**Location**: `ReusableTools/templates/tes070_regression_template.docx`

**Contents**:
- Pre-formatted title page
- Document control table
- Test summary table placeholder
- Prerequisites section
- Scenario template with test steps table
- Proper styles and formatting

## Success Criteria

A successful TES-070 generation includes:

1. ✅ Document created with correct filename
2. ✅ All metadata populated (title, date, author, environment)
3. ✅ Test summary table with accurate statistics
4. ✅ All scenarios documented with Pass/Fail status
5. ✅ All screenshots embedded and visible
6. ✅ Test steps tables formatted correctly
7. ✅ Expected vs Actual results documented
8. ✅ Work unit IDs referenced
9. ✅ Table of contents generated
10. ✅ Formatting matches TES-070 standards

## Example Output

**Filename**: `SONH_EXT_FIN_004_Regression_2026-03-10.docx`

**Contents**:
- Title: "SONH_TES-070 - EXT_FIN_004 Expense Invoice Approval Workflow Regression Test Results"
- Version: Regression_2026-03-10
- 5 test scenarios with Pass/Fail status
- 23 embedded screenshots
- Test summary: 80% pass rate (4 passed, 1 failed)
- Work unit IDs for each scenario
- Expected vs Actual results comparison

## Next Steps

After generating TES-070:

1. **Review Document**: Open and verify all content is correct
2. **Share with Stakeholders**: Distribute to project team
3. **Address Failures**: Investigate and fix failed scenarios
4. **Archive**: Store in project documentation
5. **Update Tracking**: Mark regression testing as complete

## Related Documentation

- `tes-070-standards` steering file - TES-070 formatting standards
- `evidence-collection.md` - Screenshot capture guidelines
- `test-execution.md` - Test execution workflow
- `ReusableTools/generate_regression_tes070.py` - Regression TES-070 generator tool
- `ReusableTools/REGRESSION_TES070_README.md` - Tool usage guide

## Summary

Phase 5 (TES-070 Generation) completes the regression testing workflow by creating an updated TES-070 document with fresh test results. This provides stakeholders with current evidence that approval workflows are functioning correctly.

**Key Benefits**:
- Automated document generation (no manual Word editing)
- Consistent formatting (matches TES-070 standards)
- Complete evidence (all screenshots embedded)
- Accurate results (Pass/Fail status from actual execution)
- Audit trail (work unit IDs, timestamps, environment)
