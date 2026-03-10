# TES-070 Parsing Workflow

Guide for parsing TES-070 documents and extracting test scenarios.

## Overview

TES-070 documents contain test results for FSM approval workflows. This workflow extracts structured data from Word documents for automated test execution.

## Prerequisites

- TES-070 document in Word format (.docx)
- Python tool: `ReusableTools/tes070_analyzer.py`
- Document located in: `Projects/{ClientName}/TES-070/Approval_TES070s_For_Regression_Testing/`

**IMPORTANT**: This workflow works with ANY approval TES-070 document, not just specific samples. The power dynamically discovers all available projects and TES-070 documents.

## Workflow Steps

### Step 0: Automatic Workspace Discovery (CRITICAL - Do This FIRST)

**Before presenting options to user, ALWAYS scan workspace:**

1. **List all client projects:**
   ```bash
   List directories in Projects/
   ```
   
2. **For each project, check:**
   - TES-070 documents in `Projects/{Client}/TES-070/Approval_TES070s_For_Regression_Testing/`
   - Credentials in `Projects/{Client}/Credentials/` (.env.fsm and .env.passwords)
   - Count available documents

3. **Present contextual summary:**
   ```
   ## Available Projects and TES-070 Documents
   
   **SONH** (3 documents, credentials ✅)
   - EXT_FIN_001 - Manual Journal Entry Approval
   - EXT_FIN_004 - Expense Invoice Approval ✅ Previously tested
   - EXT_FIN_016 - Cash Ledger Transaction Approval
   
   **ClientB** (1 document, credentials ❌)
   - EXT_FIN_025 - Purchase Order Approval
   
   **To add new project:**
   1. Trigger "New Project Setup" hook
   2. Add credentials to Projects/{NewClient}/Credentials/
   3. Add TES-070 documents to Projects/{NewClient}/TES-070/Approval_TES070s_For_Regression_Testing/
   
   Which project would you like to test?
   ```

4. **If no projects found:**
   - Explain no client projects exist
   - Guide user to trigger "New Project Setup" hook
   - Explain folder structure requirements

### Step 1: User Selects Project and Document

1. User selects client from discovered projects
2. List TES-070 documents for selected client
3. User selects TES-070 document

**Example Paths:**
```
Projects/SONH/TES-070/Approval_TES070s_For_Regression_Testing/
  SoNH_TES-070 - EXT_FIN_004 Expense Invoice Approval Test Results Document.docx
  
Projects/ClientB/TES-070/Approval_TES070s_For_Regression_Testing/
  ClientB_TES-070 - EXT_FIN_025 Purchase Order Approval.docx
```

**Supported Document Types:**
- Any approval workflow TES-070 (not limited to samples)
- ExpenseInvoice, ManualJournal, CashLedgerTransaction
- Can be extended to PurchaseOrder, Requisition, etc.
- Any naming convention (as long as .docx format)

### Step 2: Run TES-070 Analyzer

Execute Python tool to parse document:

```bash
python ReusableTools/tes070_analyzer.py "<full_path_to_tes070_document>"
```

**What It Does:**
- Reads Word document structure
- Extracts document metadata (title, author, version)
- Parses test summary table (total tests, passed, failed)
- Extracts test scenarios with:
  - Scenario title
  - Description
  - Test steps
  - Expected results
  - Actual results
- Identifies transaction type (ExpenseInvoice, ManualJournal, etc.)

**Output File:**
```
{TES070_filename}_analysis.json
```

Saved in same directory as source document.

### Step 3: Review Analysis JSON

Read generated JSON file to verify:

1. **Document Info:**
   - Title extracted correctly
   - Version number present
   - Author identified

2. **Test Summary:**
   - Total test count matches document
   - Pass/fail counts accurate
   - Percentage calculations correct

3. **Scenarios:**
   - All scenarios extracted
   - Test steps present
   - Expected results captured
   - No TOC entries included (should be filtered)

4. **Transaction Type:**
   - Correctly identified (ExpenseInvoice, ManualJournal, CashLedgerTransaction)
   - Based on document title and scenario descriptions

### Step 4: Validate JSON Structure

Run validation tool:

```bash
python ReusableTools/validate_json.py "<path_to_analysis_json>"
```

**Checks:**
- Valid JSON syntax
- Required fields present
- Data types correct
- No parsing errors

**Expected Output:**
```
✅ Valid JSON file: {filename}
```

## Analysis JSON Structure

```json
{
  "document_info": {
    "title": "Document title",
    "file_path": "Full path to source document",
    "author": "Author name",
    "date": "Document date",
    "version": "Version number"
  },
  "test_summary": {
    "total_tests": "21",
    "completed_tests": "21",
    "percent_completed": "100%",
    "passed_tests": "21",
    "failed_tests": "0",
    "percent_passed": "100%",
    "actual_scenario_count": "21"
  },
  "scenarios": [
    {
      "title": "Scenario title",
      "description": "Scenario description",
      "test_steps": [
        {
          "number": "1",
          "description": "Step description",
          "result": "Expected result"
        }
      ],
      "results": ["Actual result 1", "Actual result 2"],
      "content_flow": [...]
    }
  ],
  "transaction_type": "ExpenseInvoice"
}
```

## Transaction Type Detection

The analyzer detects transaction type by examining:

1. **Document Title:**
   - "Expense Invoice" → ExpenseInvoice
   - "Manual Journal" → ManualJournal
   - "Cash Ledger" → CashLedgerTransaction
   - "Purchase Order" → PurchaseOrder (extensible)
   - "Requisition" → Requisition (extensible)

2. **Scenario Descriptions:**
   - Keywords: "expense invoice", "journal entry", "cash transaction", "purchase order"
   - FSM module references: "Payables", "General Ledger", "Cash Management", "Purchasing"

3. **Business Class Names:**
   - ExpenseInvoice, ManualJournal, CashLedgerTransaction, PurchaseOrder, Requisition

**Default:** If unclear, defaults to ExpenseInvoice

**Extensibility:** The analyzer can be extended to support new transaction types by:
- Adding keywords to detection logic
- Updating transaction type mapping
- Adding FSM navigation patterns for new modules

## Filtering TOC Entries

The analyzer filters out Table of Contents entries:

**TOC Entry Characteristics:**
- No test steps
- No results
- Only contains title with page number
- Style: "toc 2" or similar

**Executable Scenario Characteristics:**
- Has test steps array (may be empty but present)
- Has results array
- Contains actual test content

**Example TOC Entry (Filtered):**
```json
{
  "title": "3.1\tScenario: Test scenario name\t10",
  "description": "",
  "test_steps": [],
  "results": [],
  "content_flow": [{"type": "text", "content": "...", "style": "toc 2"}]
}
```

**Example Executable Scenario (Kept):**
```json
{
  "title": "Scenario: Test scenario name",
  "description": "Detailed description",
  "test_steps": [
    {"number": "1", "description": "Step 1", "result": "Expected"}
  ],
  "results": ["Actual result"],
  "content_flow": [...]
}
```

## Common Issues

### Issue: No scenarios extracted

**Cause:** Document structure doesn't match expected format

**Solution:**
- Verify document is TES-070 format
- Check for test scenario tables
- Review document structure manually

### Issue: Transaction type incorrect

**Cause:** Document title or scenarios don't contain clear keywords

**Solution:**
- Manually specify transaction type
- Update analyzer keyword matching
- Check document title and scenario descriptions

### Issue: TOC entries included in scenarios

**Cause:** TOC entries have unexpected structure

**Solution:**
- Review content_flow for TOC entries
- Update filtering logic in analyzer
- Manually remove TOC entries from JSON

### Issue: Test steps missing

**Cause:** Document doesn't have structured test steps

**Solution:**
- Check if document uses different format
- Extract steps from description or results
- Manually add test steps to JSON

## Next Steps

After successful parsing:

1. **Create Test Instructions** - Use `create_test_instructions.py`
2. **Execute Tests** - Follow test-execution.md workflow
3. **Collect Evidence** - Follow evidence-collection.md workflow

## Related Files

- `ReusableTools/tes070_analyzer.py` - Parser implementation
- `ReusableTools/create_test_instructions.py` - Next step in workflow
- `ReusableTools/validate_json.py` - JSON validation tool
- `test-execution.md` - Test execution workflow
