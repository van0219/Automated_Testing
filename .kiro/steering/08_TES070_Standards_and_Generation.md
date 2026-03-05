---
inclusion: auto
name: tes-070-standards
description: TES-070 test results document standards, formatting, evidence requirements, generation patterns. Use when creating or analyzing TES-070 documents.
---

# TES-070 Standards and Generation Guide

## Table of Contents

- [Overview](#overview)
- [What is TES-070?](#what-is-tes-070)
- [Document Purpose and Audience](#document-purpose-and-audience)
- [Document Structure](#document-structure)
- [Formatting Standards](#formatting-standards)
- [Required Sections](#required-sections)
- [Test Scenario Patterns](#test-scenario-patterns)
- [Evidence Requirements](#evidence-requirements)
- [Screenshot Guidelines](#screenshot-guidelines)
- [Table Formats](#table-formats)
- [Testing Workflows by Interface Type](#testing-workflows-by-interface-type)
- [Quality Checklist](#quality-checklist)
- [Generation Guidelines](#generation-guidelines)
- [Related Tools](#related-tools)

## Overview

TES-070 is the **official test results document** format used to document testing evidence for RICE items (Reports, Interfaces, Conversions, Enhancements). This guide provides standards for creating, formatting, and generating TES-070 documents.

**Key Principle**: TES-070 documents must provide **complete, reproducible evidence** that the solution works as specified in ANA-050/DES-020 documents.

## What is TES-070?

**TES-070** = Test Results Document

**Purpose**:
- Document test execution and results
- Provide evidence of successful testing
- Capture screenshots and validation steps
- Prove requirements are met
- Support User Acceptance Testing (UAT)
- Serve as deployment approval documentation

**Relationship to Other Documents**:
- **ANA-050** (Functional Spec) → Defines WHAT to test
- **DES-020** (Technical Spec) → Defines HOW it's built
- **TES-070** (Test Results) → Proves IT WORKS

## Document Purpose and Audience

**Primary Audience**:
- Business stakeholders (proof of functionality)
- QA team (test validation)
- Project managers (deployment approval)
- Support team (reference for troubleshooting)

**Secondary Audience**:
- Auditors (compliance evidence)
- Future developers (understanding behavior)
- Training team (example workflows)

## Document Structure

### Standard TES-070 Structure

```
1. Title Page
   - Document title with interface ID
   - Client/project name
   - Version and date

2. Document Control
   - Version history
   - Author information
   - Review/approval status

3. Table of Contents
   - Auto-generated with page numbers

4. Test Summary
   - Statistics table (total, passed, failed, pass rate)
   - Overall status

5. Prerequisites
   - Required setup
   - Test data requirements
   - User roles needed
   - Environment information

6. Test Scenarios (Multiple)
   For each scenario:
   - Scenario title and description
   - Test steps table (Step #, Description, Result)
   - Expected results
   - Actual results
   - Screenshots as evidence
   - Pass/Fail status

7. Appendix (Optional)
   - Additional notes
   - Known issues
   - Future enhancements
```

## Formatting Standards

### Font and Typography

**Primary Font**: Arial (NOT Calibri)

**Font Sizes**:
- Title Page: 18pt bold
- Heading 1: 14pt bold, ALL CAPS
- Heading 2: 14pt bold, Title Case
- Heading 3: 12pt bold, ALL CAPS
- Heading 4: 12pt bold, Title Case
- Body text: 11pt
- Table text: 10pt
- Table headers: 10pt bold

**Colors**:
- Infor Blue: #13A3F7 (for highlights and accents)
- Black: #000000 (for text)
- White: #FFFFFF (for table headers background)
- Gray: #F2F2F2 (for alternating table rows)

### Page Layout

**Page Size**: A4 (8.27" x 11.69")
**Margins**: 
- Top: 1"
- Bottom: 1"
- Left: 1"
- Right: 1"

**Headers/Footers**:
- Header: Document title (left), Version (right)
- Footer: Page number (center), Date (right)

### Spacing

**Paragraph Spacing**:
- Before heading: 12pt
- After heading: 6pt
- Between paragraphs: 6pt
- Line spacing: 1.15

**Table Spacing**:
- Before table: 6pt
- After table: 12pt

## Required Sections

### 1. Title Page

**Required Elements**:
- Client logo (if available)
- Document title: `[Client]_TES-070 - [Interface ID] [Interface Name] Test Results Document`
- Version number
- Date
- Author name

**Example**:
```
SoNH_TES-070 - INT_FIN_013 GL Transaction Interface Test Results Document
Version: 1.0
Date: 09/08/2025
Author: Ivy Cafe
```

### 2. Document Control Table

| Field | Description |
|-------|-------------|
| Document ID | TES-070-[Interface ID] |
| Version | 1.0, 1.1, 2.0, etc. |
| Author | Name of tester |
| Creation Date | Initial creation date |
| Last Updated | Most recent update date |
| Status | Draft, In Review, Approved |
| Reviewers | Names of reviewers |
| Approvers | Names of approvers |

### 3. Test Summary Table

**Required Statistics**:

| Metric | Value |
|--------|-------|
| Count of Total Tests | [Number] |
| Count of Completed Tests | [Number] |
| % of Completed Tests | [Percentage] |
| Count of Passed Tests | [Number] |
| Count of Failed Tests | [Number] |
| % of Passed Tests | [Percentage] |

**Calculation Rules**:
- % Completed = (Completed Tests / Total Tests) × 100
- % Passed = (Passed Tests / Completed Tests) × 100
- Target: 100% completed, 100% passed for deployment approval

### 4. Prerequisites Section

**Required Information**:
- Environment (TST, PP1, PRD)
- User roles required
- Test data setup
- Configuration prerequisites
- Dependencies on other interfaces

**Example**:
```
Prerequisites:
- Environment: ACUITY_TST
- User Roles: Process Server Administrator, Financials Processor
- Test Data: Sample GL transaction files in FSM format
- File Channel: SONH_GLTransactionInterface configured and active
- Email Recipients: Configured in IPA for notifications
```

### 5. Test Scenarios

**Each scenario must include**:

1. **Scenario Title**: Clear, descriptive name
2. **Description**: What is being tested and why
3. **Test Steps Table**: Numbered steps with results
4. **Expected Results**: What should happen
5. **Actual Results**: What actually happened
6. **Screenshots**: Evidence at each critical step
7. **Pass/Fail Status**: Overall scenario result

## Test Scenario Patterns

### Pattern 1: Happy Path (Success Scenario)

**Purpose**: Prove the interface works end-to-end with valid data

**Required Steps**:
1. Setup/trigger the interface
2. Verify data processing
3. Validate output/results
4. Confirm notifications (if applicable)
5. Check work unit status

**Evidence Required**:
- Trigger confirmation (file drop, manual trigger, schedule)
- Processing status (work unit, staging data)
- Output validation (FSM records, output files)
- Notifications (email screenshots)
- Final status confirmation

**Example** (from INT_FIN_013):
```
Scenario: Successful import and interface of GL Transactions

Steps:
1. Drop file to SFTP
2. File Channel scans and processes
3. Email notification received
4. Work unit verified as Completed

Evidence: 9 screenshots showing each step
```

### Pattern 2: Data Validation Errors

**Purpose**: Prove the interface catches and reports bad data

**Required Steps**:
1. Submit data with known errors
2. Verify errors are detected
3. Confirm error reporting
4. Show error details
5. Demonstrate correction workflow (optional)

**Evidence Required**:
- Error detection (staging errors, validation failures)
- Error notifications (email with error details)
- Error reports (attached files, error messages)
- Work unit with error status
- Correction workflow (if applicable)

**Common Error Types to Test**:
- Invalid data formats (dates, numbers)
- Missing required fields
- Invalid reference data (account codes, etc.)
- Business rule violations
- Duplicate records

**Example** (from INT_FIN_013):
```
Scenario: Error upon DB Import to GL Transaction Interface (Staging)

Errors tested:
- Invalid date format (1082025 instead of YYYYMMDD)
- Bad number format (2,105.19 with comma)
- Primary key violation (duplicate sequence numbers)

Evidence: 7 screenshots showing error detection and reporting
```

### Pattern 3: Interface/Business Rule Errors

**Purpose**: Prove the interface validates against FSM business rules

**Required Steps**:
1. Submit data that passes format validation but violates business rules
2. Verify data imports to staging
3. Confirm interface errors are caught
4. Show error correction in FSM
5. Demonstrate reprocessing

**Evidence Required**:
- Successful staging import
- Interface error detection
- Error details in FSM UI
- Correction workflow
- Successful reprocessing

**Common Business Rule Errors**:
- Closed accounting periods
- Invalid account combinations
- Missing configuration data
- Insufficient permissions
- Workflow violations

**Example** (from INT_FIN_013):
```
Scenario: Successful import with Interface error

Errors tested:
- Transactions dated in closed periods
- Invalid account codes
- Missing configuration data

Evidence: 12 screenshots showing error correction workflow
```

### Pattern 4: Partial Success/Partial Error

**Purpose**: Prove the interface handles mixed results (some records succeed, some fail)

**Required Steps**:
1. Submit batch with mix of valid and invalid records
2. Verify partial import to staging
3. Confirm partial interface success
4. Show error records separately
5. Demonstrate error correction without reprocessing entire batch

**Evidence Required**:
- Batch submission confirmation
- Staging data showing both successful and failed records
- Interface results showing partial completion
- Error details for failed records
- Correction workflow for errors
- Reprocessing of corrected records only

**Common Scenarios**:
- Some invoices succeed, others fail validation
- Mixed data quality in single file
- Partial business rule compliance

**Example** (from INT_FIN_010):
```
Scenario: Partial Successfully Interfaced AR Invoice and Partial Interfaced Error AR Invoice

Steps:
1. Submit file with mixed valid/invalid invoices
2. Verify partial staging import
3. Check interface results (some complete, some error)
4. Review error details
5. Correct errors and reprocess

Evidence: 14 screenshots showing mixed results handling
```

### Pattern 5: Outbound Interface

**Purpose**: Prove data extraction, file generation, and transfer works

**Required Steps**:
1. Trigger outbound interface (manual or scheduled)
2. Verify data extraction from FSM
3. Confirm file generation
4. Validate file content and format
5. Verify file transfer to SFTP/destination
6. Check email notifications (if applicable)
7. Confirm work unit completion

**Evidence Required**:
- Trigger confirmation (manual action or schedule)
- Data selection criteria
- Generated file in FSM File Storage
- File content validation
- SFTP destination folder with file
- Email notifications (success or with file attachment)
- Work unit status

**Common Scenarios**:
- Scheduled daily/weekly extracts
- On-demand file generation
- Multiple file formats for different recipients
- Email remittance to vendors

**Example** (from INT_FIN_127):
```
Scenario: Successful ACH Payment File creation for Cash Code 0042

Steps:
1. Navigate to Payment Electronic Transfer
2. Select payments for processing
3. Trigger ACH file generation
4. Verify file created in FSM
5. Check file transferred to SFTP
6. Validate file format and content
7. Confirm email remittance sent
8. Verify work unit completed

Evidence: 17 screenshots showing complete outbound flow
```

### Pattern 6: Email Remittance

**Purpose**: Prove vendor-specific email notifications work correctly

**Required Steps**:
1. Trigger interface with email remittance enabled
2. Verify email recipients determined correctly
3. Confirm emails sent to each vendor/location
4. Validate email content (payment details, amounts)
5. Check for multiple emails when needed (different locations)
6. Verify email delivery

**Evidence Required**:
- Email configuration
- Recipient determination logic
- Email screenshots (subject, body, attachments)
- Multiple emails for different locations
- Payment details in email body

**Example** (from INT_FIN_127):
```
Scenario: ACH Payment File Creation with Email Remittance for Same Vendor, Different Locations

Steps:
1-11. Complete payment processing with email remittance

Evidence: 21 screenshots including multiple vendor emails
```

### Pattern 7: File Naming Convention Validation

**Purpose**: Prove automatic file naming works correctly

**Required Steps**:
1. Create new configuration record
2. Trigger file generation
3. Verify file name follows convention
4. Validate timestamp/sequence in filename

**Evidence Required**:
- Configuration settings
- Generated filename
- Filename pattern validation

**Example** (from INT_FIN_127):
```
Scenario: Automatic file naming convention for newly added PaymentElectronicTransferID records

Steps:
1. Verify automatic file naming

Evidence: 3 screenshots showing filename validation
```

## Evidence Requirements

### Screenshot Guidelines

**When to Capture Screenshots**:
- At every critical step in the test
- Before and after state changes
- Error messages and validation failures
- Email notifications
- Work unit status
- Final results/output

**Screenshot Quality Standards**:
- Full screen or relevant section clearly visible
- No sensitive data (passwords, SSNs, etc.)
- Timestamp visible when relevant
- Annotations/highlights for clarity (optional)
- Consistent zoom level (use Ctrl+Minus 3x for browser)

**Screenshot Naming Convention**:
```
[Interface]_[Scenario]_[Step]_[Type].png

Examples:
- INT_FIN_013_Scenario1_Step2_FileChannel.png
- INT_FIN_013_Scenario2_Step4_ErrorEmail.png
- INT_FIN_013_Scenario3_Step5_JournalControl.png
```

### Evidence Types by Category

**1. Trigger Evidence**:
- File drop confirmation (SFTP folder screenshot)
- Manual trigger action (button click, right-click menu)
- Schedule confirmation (scheduled job settings)
- File Channel scan status

**2. Processing Evidence**:
- Work unit ID and status
- Staging data records
- Processing logs (if errors)
- Progress indicators

**3. Validation Evidence**:
- FSM records created/updated
- Output files generated
- Data comparison (before/after)
- Business rule validation

**4. Notification Evidence**:
- Email screenshots (subject, body, attachments)
- User action notifications
- Error alerts
- Success confirmations

**5. Error Evidence**:
- Error messages (full text)
- Error files/reports
- Validation failure details
- Stack traces (if applicable)

**6. Resolution Evidence**:
- Correction steps
- Reprocessing confirmation
- Final success status

## Table Formats

### Test Steps Table

**Required Columns**:
1. Step # (number)
2. Test Step Description (detailed instructions)
3. Result (PASS/FAIL)

**Formatting**:
- Header row: Black background, white text, bold
- Body rows: Alternating white/light gray
- Font: 10pt Arial
- Cell padding: 5pt
- Borders: 1pt solid black

**Example**:

| Step # | Test Step Description | Result |
|--------|----------------------|--------|
| 1 | Log into FTP Program using Infor SFTP credentials. Navigate to `/Infor_FSM/GLTransactionInterface/Inbound`. Drop the GL Transaction inbound file. Wait for file channel to trigger scanning (currently scheduled every 5 mins). | PASS |
| 2 | Log into Infor FSM as Process Server Administrator > Administration > Channels Administrator > File Channels tab > Search for SONH_GLTransactionInterface. Right click and click Scan Now. | PASS |

### Test Summary Table

**Format**: 2 columns (Metric, Value)
- Header row: Black background, white text
- Metrics in left column, values in right column
- Bold metric names
- Percentage values with % symbol

### Document Control Table

**Format**: 2 columns (Field, Value)
- No header row
- Field names in left column (bold)
- Values in right column (normal)

## Testing Workflows by Interface Type

### Inbound File Interface (File Channel Triggered)

**Standard Workflow**:
1. Prepare test file with valid data
2. Drop file to SFTP server
3. Wait for File Channel scan (or trigger manually)
4. Verify file consumed from SFTP
5. Check staging data import
6. Validate FSM records created
7. Verify email notification
8. Check work unit status

**Evidence Checklist**:
- [ ] SFTP folder before (file present)
- [ ] SFTP folder after (file consumed)
- [ ] File Channel scan status
- [ ] Staging data records
- [ ] FSM records created
- [ ] Email notification
- [ ] Work unit completed

### Inbound File Interface (Manual/Scheduled)

**Standard Workflow**:
1. Prepare test file with valid data
2. Upload file to FSM File Storage or designated location
3. Manually trigger interface via Integration Architect or Process Server Administrator
4. Verify file processing
5. Check staging data import
6. Validate FSM records created
7. Verify email notification
8. Check work unit status

**Evidence Checklist**:
- [ ] File upload confirmation
- [ ] Manual trigger action
- [ ] Staging data records
- [ ] FSM records created
- [ ] Email notification
- [ ] Work unit completed

### Outbound File Interface

**Standard Workflow**:
1. Navigate to interface trigger location (FSM UI or Process Server Administrator)
2. Select data/parameters for extraction
3. Trigger file generation (manual or scheduled)
4. Verify data extracted from FSM
5. Check file created in FSM File Storage
6. Validate file content and format
7. Verify file transferred to SFTP (if applicable)
8. Check email notifications (if applicable)
9. Verify work unit status

**Evidence Checklist**:
- [ ] Trigger action (manual or schedule confirmation)
- [ ] Data selection criteria
- [ ] File generated in FSM File Storage
- [ ] File content validation (open and review)
- [ ] SFTP destination folder (file present)
- [ ] Email notifications (if applicable)
- [ ] Work unit completed

**Common Variations**:
- **Cash code-specific processing**: Different logic for different payment types
- **Email remittance**: Vendor-specific emails with payment details
- **Multiple file formats**: Different formats for different recipients
- **File naming conventions**: Automatic naming with timestamps/sequences

## Quality Checklist

### Before Generating TES-070

- [ ] All test scenarios identified from ANA-050
- [ ] Test data prepared and validated
- [ ] Environment configured correctly
- [ ] User roles and permissions verified
- [ ] Dependencies resolved

### During Testing

- [ ] Screenshots captured at each step
- [ ] Error scenarios tested thoroughly
- [ ] Work unit IDs recorded
- [ ] Email notifications verified
- [ ] Data validation performed

### After Testing

- [ ] All scenarios documented
- [ ] All screenshots embedded
- [ ] Pass/fail status recorded
- [ ] Summary statistics calculated
- [ ] Document reviewed for completeness

### Document Quality

- [ ] Formatting matches standards (Arial font, correct sizes)
- [ ] All required sections present
- [ ] Table of contents generated
- [ ] Page numbers correct
- [ ] Headers/footers consistent
- [ ] No spelling/grammar errors
- [ ] Screenshots clear and relevant
- [ ] Version and date correct

## Generation Guidelines

### Automated TES-070 Generation

**Input Requirements**:
- Interface metadata (ID, name, type)
- Test scenarios (title, description, steps)
- Test results (pass/fail status)
- Screenshots (organized by scenario/step)
- Work unit IDs
- Email notifications
- Timestamps

**Generation Process**:
1. Create document from template
2. Populate metadata (title, author, date)
3. Generate test summary table
4. Add prerequisites section
5. For each scenario:
   - Add scenario title and description
   - Create test steps table
   - Embed screenshots in order
   - Add results and status
6. Generate table of contents
7. Apply formatting standards
8. Save to `TES-070/Generated_TES070s/`

**Output Location**:
```
TES-070/Generated_TES070s/[Client]_TES-070_[InterfaceID]_[InterfaceName]_Test_Results_Document.docx
```

### Manual TES-070 Creation

**When to Create Manually**:
- Complex scenarios requiring narrative
- First-time testing of new interface type
- Exploratory testing
- When automated testing is not feasible

**Process**:
1. Copy template from `TES-070/Sample_Documents/`
2. Update metadata
3. Document scenarios as you test
4. Capture screenshots in real-time
5. Organize evidence by scenario
6. Calculate summary statistics
7. Review and finalize

## Related Tools

### TES-070 Analyzer (`tes070_analyzer.py`)

**Purpose**: Analyze existing TES-070 documents to extract structure and patterns

**Usage**:
```bash
python ReusableTools/tes070_analyzer.py "path/to/tes070.docx"
```

**Output**: JSON file with document structure, scenarios, images, and OCR text

### TES-070 Generator (`tes070_generator.py`)

**Purpose**: Generate new TES-070 documents from test execution data

**Usage**: [To be documented after tool creation]

**Features**:
- Template-based generation
- Automatic formatting
- Screenshot embedding
- Summary calculation
- Table of contents generation

## Best Practices

### Testing Best Practices

1. **Test in Order**: Happy path first, then error scenarios
2. **Document as You Go**: Capture screenshots during testing, not after
3. **Use Real Data**: Test with realistic data volumes and scenarios
4. **Verify End-to-End**: Don't just check staging, verify final output
5. **Test Error Handling**: Prove errors are caught and reported correctly

### Documentation Best Practices

1. **Be Specific**: Include exact navigation paths, field names, values
2. **Show, Don't Tell**: Screenshots are evidence, not decoration
3. **Explain Errors**: Don't just show error messages, explain what caused them
4. **Include Context**: Work unit IDs, timestamps, file names
5. **Think Reproducibility**: Could someone else follow your steps and get the same results?

### Screenshot Best Practices

1. **Capture at the Right Time**: Before and after critical actions
2. **Show Relevant Information**: Zoom to show important details
3. **Annotate When Helpful**: Highlight key fields or messages
4. **Organize by Scenario**: Keep screenshots grouped with their test steps
5. **Name Descriptively**: Use clear, consistent naming conventions

## Summary

TES-070 documents are the **official proof** that RICE items work as specified. They must be:

- **Complete**: All scenarios tested and documented
- **Clear**: Easy to understand and follow
- **Consistent**: Follow formatting and structure standards
- **Credible**: Provide real evidence (screenshots, work unit IDs)
- **Compliant**: Meet project and audit requirements

**Key Principles**:
1. Evidence over narrative (show, don't just tell)
2. Reproducibility (someone else could repeat your test)
3. Completeness (happy path AND error scenarios)
4. Clarity (clear steps, clear results, clear status)

**Next Steps**:
1. Analyze remaining sample TES-070s to identify additional patterns
2. Build TES-070 generator tool based on these standards
3. Test generator by recreating sample documents
4. Use in automated testing to generate new TES-070s

---

**Document Status**: Complete - All patterns documented from 3 sample TES-070 analyses:
- INT_FIN_013: GL Transaction Interface (Inbound, File-triggered)
- INT_FIN_010: Receivables Invoice Import (Inbound, File-triggered, Partial success pattern)
- INT_FIN_127: ACH Files Outbound (Outbound, Manual/scheduled, Email remittance)
