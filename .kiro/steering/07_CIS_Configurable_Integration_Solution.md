---
inclusion: auto
name: CIS Guide
description: CIS (Configurable Integration Solution) for outbound and inbound interfaces, no-code interface builder, Integration Architect, interface testing, trigger workflows. Use when working with CIS interfaces or testing outbound/inbound integrations.
---

# CIS - Configurable Integration Solution Guide

## Table of Contents

- [Overview](#overview)
- [When to Use This Guide](#when-to-use-this-guide)
- [Key Capabilities](#key-capabilities)
- [Critical Rules - Apply Always](#critical-rules---apply-always)
- [CIS vs Custom IPA - Decision Matrix](#cis-vs-custom-ipa---decision-matrix)
- [CIS Interface Types](#cis-interface-types)
- [Navigation Path to CIS](#navigation-path-to-cis)
- [CIS Outbound List Page - Grid Structure](#cis-outbound-list-page---grid-structure)
- [CIS Outbound Detail Page - Structure](#cis-outbound-detail-page---structure)
- [Testing Outbound Interface - Step-by-Step Workflow](#testing-outbound-interface---step-by-step-workflow)
- [Testing Inbound Interface - Step-by-Step Workflow](#testing-inbound-interface---step-by-step-workflow)
- [Playwright Automation - Code Patterns](#playwright-automation---code-patterns)
- [Context Menu Actions - Available Options](#context-menu-actions---available-options)
- [Common Errors and Resolutions](#common-errors-and-resolutions)
- [Error Handling - AI Instructions](#error-handling---ai-instructions)
- [Monitoring Interface Execution](#monitoring-interface-execution)
- [Best Practices](#best-practices)
- [Related Steering Files](#related-steering-files)
- [Summary](#summary)

## Overview

CIS (Configurable Integration Solution) is a custom-built integration accelerator framework that uses pre-built generic IPAs configured through forms. It's deployed as a package (LPL + IPA files) to each client tenant, eliminating the need for custom IPA development for standard integration scenarios.

**Deployment Model:**
- CIS is installed per tenant (not shared across tenants)
- Each client tenant (TRN, TST, PRD, etc.) requires separate CIS installation
- Package includes LPL layer (UI/forms) and IPA layer (execution logic)

**Key Value:**
- Reduces client implementation costs significantly
- Faster delivery (configure vs custom-code)
- Standardized, maintainable integration patterns

## When to Use This Guide

Use this guide when you need to:

- Test CIS outbound/inbound interfaces
- Trigger interfaces via FSM UI
- Monitor interface execution status
- Troubleshoot CIS errors
- Automate CIS testing with Playwright

## Key Capabilities

- No-code interface configuration through forms
- Pre-built generic IPAs (no custom development needed)
- Built-in trigger and monitoring functionality
- File-based and API-based integrations
- Scheduled and on-demand execution

## Critical Rules - Apply Always

1. **Context Menu**: ALWAYS use right-click context menu for triggering interfaces. Column buttons can be hidden via personalization and are unreliable.

2. **Active Status Check**: MUST verify Active=Yes before attempting to trigger. Active=No interfaces cannot be triggered.

3. **Activation Sequence**: If Active=No, you MUST right-click > Activate BEFORE attempting to trigger the interface.

4. **Status Monitoring**: After triggering, poll Last Run Status column until completion:
   - Ready (green checkmark) = Success
   - Error (red X) = Failed

5. **Work Unit Access**: Click Last Work Unit link to view execution logs and error details.

6. **File Channel Timing**: For inbound file interfaces, wait 1-2 minutes after file drop for File Channel to transfer file from SFTP to FSM File Storage.

7. **Error Documentation**: Document UI error messages only. Do NOT download or analyze work unit logs unless explicitly requested by user.

8. **Navigation Prerequisite**: ALWAYS expand sidebar (☰ hamburger icon) before navigating to Integration Architect.

## CIS vs Custom IPA - Decision Matrix

### Use CIS When

- Standard data extraction patterns (GL, AP, AR, Inventory)
- Simple file-based integrations with minimal transformation
- Scheduled data exports on regular intervals
- Manual or scheduled triggering is acceptable (no automatic file-based triggers needed)
- No complex business logic or conditional processing required
- Quick deployment needed (minutes to hours, not days)
- Pre-built templates match your use case
- Cost reduction is a priority

### Use Custom IPA When

- Automatic file-based triggering required (File Channels)
- Complex business logic with conditional branching required
- Multi-step workflows involving approvals or human interaction
- Custom data transformations beyond field mapping
- Integration orchestrating multiple systems in one process
- Advanced error handling and retry logic needed
- CIS templates don't match your requirements

**Note:** File Channels cannot be used with CIS because they trigger IPAs directly at the Process Server level, bypassing the CIS configuration layer (LPL business class/forms).

### Key Distinction

CIS is for the "I" (Interfaces) in RICE methodology only. For Reports, Conversions, or Enhancements, use custom IPA or other tools.

## CIS Interface Types

### Outbound Interfaces (FSM → External Systems)

Extract data from FSM and send to external systems:

- **DBExport**: Direct database query export to file
- **DataLake**: Export data to Infor Data Lake
- **File**: Export to file formats (CSV, TXT, XML, JSON)
- **API**: Export via REST/SOAP API calls

### Inbound Interfaces (External Systems → FSM)

Import data from external systems into FSM:

- **File**: Import from file formats (CSV, TXT, XML, JSON)
- **DataLake**: Import from Infor Data Lake
- **API**: Import via REST/SOAP API calls
- **ION**: Import via ION BOD messages

## Navigation Path to CIS

### Standard Navigation Sequence

**CRITICAL**: Integration Architect is a role within FSM, not a standalone application. Always navigate to FSM first.

1. Login to Infor OS Portal
2. Expand sidebar by clicking ☰ (hamburger icon)
3. Click **Applications** > **See more**
4. Click **Financials & Supply Management** (FSM)
5. Wait for FSM to load (displays "My Available Applications")
6. Click **Integration Architect** role
7. Click **Configurable Integration** in top menu bar
8. Expand sidebar (☰) to see submenu options:
   - **Admin**: System monitoring and configuration
   - **Outbound**: FSM → External systems interfaces
   - **Inbound**: External systems → FSM interfaces

### URL Pattern

`https://{tenant}.inforcloudsuite.com/fsm/IntegrationArchitect/page/CISIntegrationArchitectPage`

Replace `{tenant}` with your environment tenant name (e.g., TAMICS10_AX1, ACUITY_TST).

## CIS Outbound List Page - Grid Structure

### Grid Columns (Standard Display)

Note: Columns can be personalized/hidden by users. Always use right-click context menu for reliable access to actions.

- **Checkbox**: Select one or more interfaces for bulk operations
- **Integration Name**: Unique identifier (e.g., "FSM-07", "FSM-08", "FSM-10")
- **Description**: Brief description of interface purpose
- **File Name**: Output file name (e.g., "ImportIS.txt", "ImportBS.txt")
- **Last Run Status**:
  - Ready (green checkmark ✅) = Successful execution
  - Error (red X ❌) = Failed execution
  - (Empty) = Never executed
- **Last Work Unit**: Clickable link showing work unit ID (e.g., "635833", "636228")
- **Active**: "Yes" or "No" indicating if interface can be triggered
- **Trigger**: Icon button (play/arrow) for manual triggering (may be hidden)

### Real-World Examples (TAMICS10_AX1 Environment)

| Integration Name | Description | File Name | Type |
| --- | --- | --- | --- |
| FSM-07 | INCOME STATEMENT ACTUAL VALUES | ImportIS.txt | DBExport |
| FSM-08 | BALANCE SHEET ACTUAL VALUES | ImportBS.txt | DBExport |
| FSM-09 | INCOME STATEMENT BUDGET VALUES | ImportISBudget.txt | DBExport |
| FSM-10 | JOURNAL ENTRY EXPORT | ImportJE.txt | DataLake |
| FSM-11 | VENDOR MASTER EXPORT | VendorMaster.csv | DBExport |
| FSM-12 | EMPLOYEE MASTER EXPORT | EmployeeMaster.csv | DBExport |
| FSM-13 | INVOICE DETAIL EXPORT | InvoiceDetail.txt | DataLake |

### Grid Interaction Patterns

**Selecting a row**:

- Single-click: Selects row (highlights, sets aria-selected="true")
- Double-click: Opens detail page

**Opening detail page**:

- Double-click the row (recommended)
- OR right-click > Open
- OR click Integration Name link (if configured as hyperlink)

**Playwright selector for selected row**: `[role="row"][aria-selected="true"]`

## CIS Outbound Detail Page - Structure

### Header Section

- **Integration Name**: Text field (e.g., "TEST-001") - Required
- **Description**: Text field (e.g., "Do Not Delete, Used in Automated Testing")
- **Use Default Process**: Checkbox (controls whether to use default CIS generic process or custom IPA process)
  - When checked: Uses default CIS generic process (no Process field shown)
  - When unchecked: Shows "Process" lookup field to select custom IPA process
- **Process**: Lookup field (only visible when "Use Default Process" is unchecked) - Required when visible
  - Allows selection of custom IPA process instead of default CIS generic process
  - Has lookup button (magnifying glass icon) to search for processes
  - Note: "Press down arrow to select"
- **Last Run Status**: Display with icon and work unit link
  - Shows execution status: "Ready" (success with green checkmark) or "Error" (failure with red X icon)
  - Displays work unit ID as clickable link (e.g., "636228")
  - Clicking work unit link opens Work Unit detail page showing:
    - Work unit header (Work Unit ID, Work Title, Status, Process, Originator, dates)
    - Multiple tabs including "Error Messages (X)" tab showing count of errors
    - Error Messages tab displays grid with error details: Error Message text and Error Date
    - Use Error Messages tab to troubleshoot failed integrations
- **Active**: Checkbox (checked = Yes, unchecked = No) - Disabled when viewing

### Action Buttons (Toolbar)

- **Previous**: Navigate to previous integration in list
- **Next**: Navigate to next integration in list
- **Create**: Create new integration (opens dropdown menu)
- **Save**: Save configuration changes (disabled until changes made)
- **Delete**: Delete current integration
- **Refresh**: Reload current integration data
- **More Actions**: Additional actions menu (ellipsis "..." button)
  - Deactivate: Deactivate the integration (prevents triggering)
  - Reset: Reset form to last saved state
  - Schedule Trigger: Manually trigger the interface execution
  - Trigger: Alternative trigger option (same as Schedule Trigger)
  - Export To PDF: Export integration configuration to PDF
  - Audit: View audit history of configuration changes
  - Select Report Fields: Configure report field selection
  - Drill Around®: Navigate to related records

### Breadcrumb Navigation

Shows path: `Configurable Integration Solution - Outbound / Outbound Integration: {IntegrationName}`

### Tab Structure

The detail page has three tabs:

#### Main Tab

**FTP Directory & File Name Section:**
- **Output File Location**: Text field for directory path (e.g., "/VAN/AutomatedTesting/Output") - Required
  - Note: "Do not include '/' at the end of the directory"
- **Delete file from File Storage**: Checkbox
- **File Name**: Text field (e.g., "Accounts.csv") - Required
- **Append Timestamp To File Name**: Checkbox
- **Time Zone**: Dropdown (e.g., "(UTC+00:00) UTC")
  - Note: "Displaying in use time zones."
- **Time Stamp Format (Java)**: Text field (e.g., "%1$ty%1$tm%1$td")
- **Build Time Stamp Format**: Checkbox (opens format builder)
- **Sample File Name**: Display-only field showing preview (e.g., "Accounts_260212.csv")

**Archiving Section:**
- **Archive**: Checkbox to enable archiving
- **Archive File Location**: Text field (e.g., "/VAN/AutomatedTesting/Archive") - Required when Archive checked
- **Archive Filename**: Text field (optional)
  - Note: "Leave Blank To Use The Same Filename"

**Encryption Section:**
- **Encrypt**: Checkbox to enable file encryption
- Additional encryption fields appear when checked

**Selected Report Fields Section:**
- Collapsible panel showing selected fields for the report
- **Collapse**: Button to collapse/expand panel
- **Cancel Report**: Button to cancel report selection
- **Add to Existing Report**: Button (disabled until report selected)
- **Create New Report**: Button (disabled until fields selected)

#### Solution Tab

Contains data source configuration and query/field mapping settings:

**Data Source Selection (Required):**
- Radio button group:
  - **DB Export**: Direct database query export
  - **Data Lake**: Export via Data Lake Compass SQL
- Tip displayed: "Test in ION API before configuring this section."

**Parameters Section:**

1. **Auto-Replicate**: Checkbox
   - Note: "Auto-Replicate is not allowed for standard Replication Sets. This is also not recommended for custom Replication Sets that are used by multiple processes."

2. **Use Date Override**: Checkbox - Override date parameters in query

3. **Lock Query Text**: Checkbox - Prevent query modifications

4. **SQL Query**: Large text area for Compass SQL query
   - Used when Data Lake option is selected
   - Note: "SQL Query Used In Data Lake Compass"
   - Example query structure:
     ```sql
     SELECT FinanceEnterpriseGroup
     ,Account
     ,AccountDescription
     ,'"' + AccountKey + '"'
     ,AccountType
     FROM FSM_Account
     WHERE FinanceEnterpriseGroup = '1'
     ```

5. **Header**: Checkbox - Include column headers in output file

6. **Header Value**: Text field - Custom header row
   - Note: "Custom Header (Leave Blank To Use Standard Field Labels)"
   - If blank, uses field names from SQL query as headers

**Key Differences Between Data Source Types:**

- **DB Export**: Direct database extraction, typically faster for simple queries
- **Data Lake**: Uses Compass SQL API, supports more complex queries and cross-object joins

#### Notification Tab

Contains email notification settings for interface execution results. Supports separate configurations for failure and success notifications.

**Failure Email Section:**

1. **Failure Email**: Checkbox to enable failure notifications
2. **Failure Email To**: Email address(es) for failure notifications - Required when Failure Email checked
3. **Failure Email Cc**: Email address(es) for CC on failure notifications - Optional
4. **Failure Email From**: Sender email address - Required when Failure Email checked
   - Default: no-reply@inforcloudsuite.com
5. **Failure Email Subject**: Subject line for failure emails - Required when Failure Email checked
   - Default template: `<prefix> [Failed] – <integrationName> to <customer> – Process Date: <processDate>`
6. **Failure Email Body**: HTML template for failure email body - Required when Failure Email checked
   - Supports HTML formatting
   - Typically includes error message and troubleshooting information

**Success Email Section:**

1. **Success Email**: Checkbox to enable success notifications
2. **Success Email To**: Email address(es) for success notifications - Required when Success Email checked
3. **Success Email Cc**: Email address(es) for CC on success notifications - Optional
4. **Success Email From**: Sender email address - Required when Success Email checked
   - Default: no-reply@inforcloudsuite.com
5. **Success Email Subject**: Subject line for success emails - Required when Success Email checked
   - Default template: `<prefix> [Success] – <integrationName> to <customer> – Process Date: <processDate>`
6. **Success Email Body**: HTML template for success email body - Required when Success Email checked
   - Supports HTML formatting
   - Typically includes summary table with filename, file date, file location

**Add Footer Section:**

1. **Add Footer**: Checkbox to enable footer in all emails (failure and success)
2. **Footer Email Body**: HTML template for email footer - Required when Add Footer checked
   - Typically includes environment information, process name, work unit reference
   - Appended to both failure and success email bodies

**Template Variables:**

Email subject and body fields support template variables that are replaced at runtime:

- `<prefix>`: Environment prefix (e.g., "ACUITY_TST", "TAMICS10_AX1")
- `<integrationName>`: Integration Name from Main tab
- `<customer>`: Customer identifier
- `<processDate>`: Process execution date (YYYYMMDD format)
- `<filename>`: Output file name
- `<outputDirectory>`: Output file location
- `<appProdline>`: Application product line
- `<ProcessName>`: IPA process name
- `<WorkUnit>`: Work unit ID for execution reference

**Example Configuration (TEST-001):**

- Failure Email: Checked, To: vananthony.silleza@infor.com
- Success Email: Checked, To: vananthony.silleza@infor.com
- Add Footer: Checked
- All emails use no-reply@inforcloudsuite.com as sender

### Opening Integration Detail Page

**Method 1: Double-click row** (Recommended)
```javascript
// Select row first
await row.click();
// Then double-click to open
await row.dblclick();
```

**Method 2: Select row and click Open button**
```javascript
// Select row
await row.click();
// Click Open button in toolbar
await page.click('button[name="Open"]');
```

### Navigation Between Integrations

Use Previous/Next buttons in toolbar to navigate between integrations without returning to list page.

## CIS Inbound List Page - Structure

### Page Layout

The CIS Inbound page has a unique two-grid layout with master-detail relationship:

1. **Top Grid**: Inbound Integrations List
2. **Bottom Grid**: File Catalog (filtered by selected integration)

### Inbound Integrations Grid (Top)

**Grid Columns (Standard Display):**

- **Checkbox**: Select one or more integrations for bulk operations
- **Integration Name**: Unique identifier (e.g., "GL_NoTransform", "InvoiceImport")
- **Description**: Brief description (e.g., "INT001", "INT003")
- **Source File Location**: Directory path where input files are expected (e.g., "CIS/Inbound/GL/Standard")
- **Last Run Status**:
  - Ready (green checkmark ✅) = Successful execution
  - Completed (green checkmark ✅) = Successful execution
  - CompletedWithError (yellow warning ⚠️) = Partial success with errors
  - Error (red X ❌) = Failed execution
  - (Empty) = Never executed
- **Last Work Unit**: Clickable link showing work unit ID (e.g., "637262", "636223")
- **Active**: "Yes" or "No" indicating if interface can be triggered
- **Trigger**: Icon button for manual triggering (may be disabled if Active=No)

**Key Differences from Outbound:**
- Uses "Source File Location" instead of "File Name" (inbound receives files, outbound generates files)
- Additional status: "CompletedWithError" (indicates partial success - some records processed, some failed)
- File Catalog section below shows expected input files for selected integration

### File Catalog Grid (Bottom)

**Purpose**: Defines expected input files for the selected inbound integration

**Grid Columns:**

- **Checkbox**: Select file catalog entries
- **Business Class**: Target FSM business class for data import (e.g., "GLTransactionInterface", "PayablesInvoiceImport")
- **Source Filename**: Expected filename pattern (supports wildcards with * character)
  - Examples: "GLTransactionInterface*.csv", "PayablesInvoiceImport_import.csv"
- **Is Required**: "Yes" or "No" - indicates if file must be present for integration to run
- **Sequence**: Numeric order for processing multiple files (e.g., "1", "2", "3", "4")

**Master-Detail Relationship:**
- Clicking/selecting an integration in the top grid filters the File Catalog to show only files associated with that integration
- Each inbound integration can have multiple file catalog entries (1-to-many relationship)
- Files are processed in sequence order (1, 2, 3, etc.)
- Required files must be present; optional files (Is Required=No) are processed if available

**Example File Catalog (for InvoiceImport integration):**

| Business Class | Source Filename | Is Required | Sequence |
| --- | --- | --- | --- |
| PayablesInvoiceImport | PayablesInvoiceImport_import.csv | Yes | 1 |
| PayablesInvoiceDistributionImport | PayablesInvoiceDistributionImport_import.csv | Yes | 2 |
| PayablesInvoiceImportComment | PayablesInvoiceImportComment_import_*.csv | No | 3 |
| PayablesInvoicePaymentImport | PayablesInvoicePaymentImport_import_*.csv | No | 4 |

**Example File Catalog (for GL_NoTransform integration):**

| Business Class | Source Filename | Is Required | Sequence |
| --- | --- | --- | --- |
| GLTransactionInterface | GLTransactionInterface*.csv | Yes | 1 |

### Grid Interaction Patterns

**Selecting an integration**:
- Single-click: Selects row and updates File Catalog grid below
- Double-click: Opens detail page

**Viewing File Catalog for specific integration**:
- Click the integration row in top grid
- File Catalog grid automatically updates to show associated files

**Playwright selector for selected row**: `[role="row"][aria-selected="true"]`

## CIS Inbound Detail Page - Structure

### Header Section

- **Integration Name**: Text field (e.g., "GL_NoTransform") - Required
- **Description**: Text field (e.g., "INT001")
- **Last Run Status**: Display with icon and work unit link
  - Shows execution status: "Ready", "Completed" (success with green checkmark), "CompletedWithError" (partial success with yellow warning), "Error" (failure with red X)
  - Displays work unit ID as clickable link (e.g., "637262")
  - Clicking work unit link opens Work Unit detail page with Error Messages tab
- **Active**: Display text (not a checkbox like Outbound)

### Action Buttons (Toolbar)

Same as Outbound - includes Previous, Next, Create, Save, Delete, Refresh, and More Actions (ellipsis) button with trigger options.

### Breadcrumb Navigation

Shows path: `Configurable Integration Solution - Inbound / {IntegrationName}`

### Tab Structure

The detail page has four tabs:

#### Main Tab

**FTP Section:**

1. **FTP Configuration Set**: Lookup field - Required
   - Example: "CIS"
   - Note: "Make sure the selected configuration set is added in the IPA flow logic."
2. **Source File Location**: Text field - Required
   - Directory path where input files are expected
   - Example: "CIS/Inbound/GL/Standard"
   - Note: "Do not include '/' at the end of the directory"

**Transaction Section:**

1. **Finance Enterprise Group**: Display-only field
   - Example: "1"
2. **Interface Group**: Lookup field with description
   - Example: "GL1" with description "GL Transactions"
3. **Data Interface Business Class**: Lookup field
   - Target FSM business class for data import
   - Example: "GLTransactionInterface"
4. **Auto Interface**: Checkbox
   - When checked, automatically processes imported data
5. **Parameter Set**: Lookup field
   - Example: "SET1"

**Bottom Option:**

- **Delete import records for the same Run Group**: Checkbox
  - When checked, deletes previous import records with same Run Group before importing new data

#### Option Tab

**Data Transformation Section:**

1. **Input Format**: Dropdown
   - Options: "Infor" (and possibly others)
   - Defines expected input file format

**Archiving Section:**

1. **Archive**: Checkbox to enable archiving
2. **Archive File Location**: Text field
   - Directory path for archived files
   - Example: "CIS/Inbound/GL/Standard/Archive"
3. **Archive File Rename Method**: Dropdown
   - Options: "Append Workunit Number" (and possibly others)
   - Defines how archived files are renamed

**Decryption Section:**

1. **Decrypt**: Checkbox to enable file decryption
   - Additional decryption fields appear when checked

#### File Catalog Tab

Contains an embedded grid showing file catalog entries for this integration.

**Grid Columns:**
- Business Class
- Source Filename (supports wildcards)
- Is Required (Yes/No)
- Sequence (numeric order)

**Toolbar Actions:**
- Create: Add new file catalog entry
- Open: Open selected entry (disabled when none selected)
- Search: Search file catalog entries
- Refresh: Reload grid
- More Actions: Additional options

**Example (GL_NoTransform):**
- GLTransactionInterface | GLTransactionInterface*.csv | Yes | 1

This is the same File Catalog grid shown on the list page, but embedded in the detail page for easier management.

#### Notification Tab

Contains email notification settings for interface execution results. Similar structure to Outbound Notification tab.

**Failure Email Section:**

1. **Failure Email**: Checkbox to enable failure notifications
2. **Do not send error email if no files are found**: Checkbox
   - Suppresses error email when expected files are missing
3. **Failure Email To**: Email address(es) - Required when Failure Email checked
4. **Failure Email Cc**: Email address(es) - Optional
5. **Failure Email From**: Sender email address - Required when Failure Email checked
   - Default: no-reply@infor.com
6. **Failure Email Subject**: Subject line - Required when Failure Email checked
   - Default template: `<prefix> [Failed] – <integrationName> – Process Date: <processDate>`
7. **Failure Email Body**: HTML template - Required when Failure Email checked
   - Supports template variables: `<integrationName>`, `<FileDetails>`, `<ErrorMessage>`, `<InterfaceResults>`

**Success Email Section:**

1. **Success Email**: Checkbox to enable success notifications
2. **Success Email To**: Email address(es) - Required when Success Email checked
3. **Success Email Cc**: Email address(es) - Optional
4. **Success Email From**: Sender email address - Required when Success Email checked
   - Default: no-reply@infor.com
5. **Success Email Subject**: Subject line - Required when Success Email checked
   - Default template: `<prefix> [Success] – <integrationName> – Process Date: <processDate>`
6. **Success Email Body**: HTML template - Required when Success Email checked
   - Supports template variables: `<integrationName>`, `<FileDetails>`, `<InterfaceResults>`

**Footer Section:**

1. **Add Footer**: Checkbox to enable footer in all emails
2. **Use Global Email Footer**: Checkbox to use global footer template

**Template Variables (Inbound-specific):**
- `<prefix>`: Environment prefix
- `<integrationName>`: Integration Name
- `<processDate>`: Process execution date
- `<FileDetails>`: Details about processed files
- `<ErrorMessage>`: Error message text (failure emails only)
- `<InterfaceResults>`: Summary of interface processing results

**Key Differences from Outbound Notification:**
- Additional checkbox: "Do not send error email if no files are found"
- Different template variables: `<FileDetails>`, `<ErrorMessage>`, `<InterfaceResults>` instead of `<filename>`, `<outputDirectory>`
- "Use Global Email Footer" option available

## Testing Outbound Interface - Step-by-Step Workflow

### Step 1: Navigate to CIS Outbound

1. Use Playwright to navigate to FSM environment
2. Expand sidebar by clicking ☰ (hamburger icon)
3. Click Integration Architect in navigation menu
4. Expand Configurable Integration submenu
5. Click Outbound

### Step 2: Locate Target Interface

1. Search for interface by Integration Name (e.g., "FSM-07")
2. Identify the row in the grid
3. Verify interface details match expected configuration

### Step 3: Check and Update Active Status

1. Check Active column value for target interface
2. If Active=No:
   - Right-click the interface row
   - Click Activate from context menu
   - Wait 1 second for activation to complete
3. If Active=Yes: Proceed to next step

### Step 4: Trigger Interface Execution

**Method 1: From List Page (Recommended)**

1. Right-click the interface row
2. Click "Schedule Trigger" or "Trigger" from context menu
3. Wait 2 seconds for trigger to initiate

**Method 2: From Detail Page**

1. Double-click the interface row to open detail page
2. Click "More Actions" button (ellipsis "..." icon) in toolbar
3. Click "Schedule Trigger" or "Trigger" from dropdown menu
4. Wait 2 seconds for trigger to initiate

### Step 5: Monitor Execution Status

1. Poll Last Run Status column every 2 seconds
2. Stop polling when status shows:
   - Ready (✅) = Successful execution
   - Error (❌) = Failed execution
3. Maximum wait time: 60 seconds (30 polling attempts × 2 seconds)
4. If timeout occurs, document timeout and investigate

### Step 6: Capture Execution Results

1. Record Work Unit ID from Last Work Unit column
2. If status is Error:
   - Click Last Work Unit link to open work unit detail page
   - Navigate to "Error Messages (X)" tab (X shows count of errors)
   - Review error messages in the grid:
     - Error Message column: Full error text with stack trace
     - Error Date column: Timestamp when error occurred
   - Document error messages, work unit ID, and timestamp
   - Click browser back button or breadcrumb to return to CIS Outbound list
3. If status is Ready:
   - Proceed to output validation (Step 7)

### Step 7: Validate Output

1. For file-based interfaces:
   - Check SFTP server or FSM File Storage for output file
   - Verify file exists with expected name
   - Verify file contains expected data and format
2. For Data Lake interfaces:
   - Query Data Lake using Compass API to verify data was written
   - Verify record count and data accuracy
3. Document validation results with evidence (file contents, query results, screenshots)

## Testing Inbound Interface - Step-by-Step Workflow

### Step 1: Navigate to CIS Inbound

1. Use Playwright to navigate to FSM environment
2. Expand sidebar by clicking ☰ (hamburger icon)
3. Click Integration Architect in navigation menu
4. Expand Configurable Integration submenu
5. Click Inbound

### Step 2: Prepare Test File

1. Create test file with sample data matching expected format
2. Upload file to SFTP server or FSM File Storage (depending on interface configuration)
3. Note file name and location for validation

### Step 3: Wait for File Channel Transfer (If Applicable)

1. If using SFTP → FSM File Storage:
   - Wait 1-5 minutes for File Channel to scan and transfer file
   - File Channels scan interval is configurable (minimum 1 minute, typically 5 minutes)
   - Verify file appears in FSM File Storage before proceeding

### Step 4: Locate and Activate Interface

1. Search for interface by Integration Name
2. Check Active column value
3. If Active=No:
   - Right-click interface row
   - Click Activate from context menu
   - Wait 1 second for activation

### Step 5: Trigger Interface (If Not Auto-Triggered)

1. Right-click interface row
2. Click "Schedule Trigger" from context menu
3. Wait 2 seconds for trigger to initiate

Note: Some inbound interfaces auto-trigger when File Channel transfers file. Check interface configuration.

### Step 6: Monitor Execution Status

1. Poll Last Run Status column every 2 seconds
2. Stop polling when status shows Ready (✅) or Error (❌)
3. Maximum wait time: 60 seconds (30 polling attempts × 2 seconds)

### Step 7: Capture Execution Results

1. Record Work Unit ID from Last Work Unit column
2. If status is Error:
   - Click Last Work Unit link to open work unit detail page
   - Capture error message from work unit detail page
   - Document error message, work unit ID, and timestamp
3. If status is Ready:
   - Proceed to import validation (Step 8)

### Step 8: Validate Import

1. Query target business class in FSM using Compass SQL or UI navigation
2. Verify records were created or updated as expected
3. Check data accuracy by comparing imported records against test file
4. Verify record count matches expected count
5. Document validation results with evidence (query results, screenshots)

## Playwright Automation - Code Patterns

### Pattern 1: Navigate to CIS Outbound

```javascript
// CRITICAL: FSM loads content in iframe, wait 3-5 seconds between navigation steps

// Step 1: Expand sidebar (☰ hamburger icon)
await page.click('button[aria-label="Toggle navigation"]');
await page.waitForTimeout(3000); // Wait for sidebar animation

// Step 2: Navigate to Integration Architect
await page.click('text=Integration Architect');
await page.waitForTimeout(5000); // Wait for page load in iframe

// Step 3: Expand Configurable Integration submenu
await page.click('text=Configurable Integration');
await page.waitForTimeout(3000); // Wait for submenu expansion

// Step 4: Click Outbound
await page.click('text=Outbound');
await page.waitForTimeout(5000); // Wait for grid to load
```

### Pattern 2: Select and Open Interface Detail Page

```javascript
// CRITICAL: Use double-click to open detail page (single-click only selects row)

// Locate interface row by Integration Name
const integrationName = "FSM-07";
const row = page.locator(`[role="row"]:has-text("${integrationName}")`);

// Single-click to select row first
await row.click();
await page.waitForTimeout(1000); // Wait for selection

// Verify row is selected
const isSelected = await row.getAttribute('aria-selected');
if (isSelected !== 'true') {
  throw new Error(`Row for ${integrationName} not selected`);
}

// Double-click selected row to open detail page
await page.locator('[role="row"][aria-selected="true"]').dblclick();
await page.waitForTimeout(5000); // Wait for detail page to load
```

### Pattern 3: Check Active Status and Activate If Needed

```javascript
// Locate interface row by Integration Name
const integrationName = "FSM-07";
const row = page.locator(`[role="row"]:has-text("${integrationName}")`);

// Get Active column value (adjust selector based on actual column structure)
const activeCellText = await row.locator('td').filter({ hasText: /^(Yes|No)$/ }).textContent();

if (activeCellText.trim() === 'No') {
  console.log(`Interface ${integrationName} is inactive. Activating...`);
  
  // Right-click row to open context menu
  await row.click({ button: 'right' });
  await page.waitForTimeout(1000);

  // Click Activate from context menu
  await page.click('text=Activate');
  await page.waitForTimeout(3000); // Wait for activation to complete
  
  console.log(`Interface ${integrationName} activated successfully`);
} else {
  console.log(`Interface ${integrationName} is already active`);
}
```

### Pattern 4: Trigger Interface (Two Methods)

**Method 1: From List Page via Right-Click Context Menu (Recommended)**

```javascript
// CRITICAL: Always use right-click context menu (column buttons may be hidden)

const integrationName = "FSM-07";
const row = page.locator(`[role="row"]:has-text("${integrationName}")`);

// Right-click to open context menu
await row.click({ button: 'right' });
await page.waitForTimeout(1000);

// Click Schedule Trigger from context menu
await page.click('text=Schedule Trigger');
await page.waitForTimeout(3000); // Wait for trigger to initiate

console.log(`Interface ${integrationName} triggered successfully`);
```

**Method 2: From Detail Page via More Actions Menu**

```javascript
const integrationName = "FSM-07";

// Open detail page by double-clicking row
const row = page.locator(`[role="row"]:has-text("${integrationName}")`);
await row.click();
await page.waitForTimeout(1000);
await row.dblclick();
await page.waitForTimeout(5000); // Wait for detail page to load

// Click More Actions button (ellipsis)
await page.click('button[name="More Actions"]');
await page.waitForTimeout(1000);

// Click Trigger from dropdown menu
await page.click('text=Trigger');
await page.waitForTimeout(3000); // Wait for trigger to initiate

console.log(`Interface ${integrationName} triggered successfully from detail page`);

// Return to list page
await page.goBack();
await page.waitForTimeout(3000);
```

**Monitoring Execution Status (Same for Both Methods)**

```javascript
// Poll Last Run Status until completion (works from list page)
let status = '';
let attempts = 0;
const maxAttempts = 30; // 60 seconds total (30 × 2 seconds)

while (attempts < maxAttempts) {
  // Refresh row reference to get updated status
  const updatedRow = page.locator(`[role="row"]:has-text("${integrationName}")`);

  // Get status text (adjust selector based on actual column structure)
  const statusCell = updatedRow.locator('td').filter({ hasText: /Ready|Error/ });
  const statusCount = await statusCell.count();

  if (statusCount > 0) {
    status = await statusCell.textContent();
    if (status.includes('Ready') || status.includes('Error')) {
      console.log(`Interface ${integrationName} execution completed with status: ${status}`);
      break; // Execution complete
    }
  }

  await page.waitForTimeout(2000); // Wait 2 seconds before next poll
  attempts++;
}

if (attempts >= maxAttempts) {
  throw new Error(`Timeout waiting for interface ${integrationName} execution (60 seconds)`);
}
```

### Pattern 5: Capture Work Unit ID and Access Error Messages

```javascript
const integrationName = "FSM-07";
const row = page.locator(`[role="row"]:has-text("${integrationName}")`);

// Get Last Work Unit link (adjust selector based on actual column structure)
const workUnitLink = row.locator('a').filter({ hasText: /^\d+$/ }); // Matches numeric work unit IDs
const workUnitId = await workUnitLink.textContent();

console.log(`Work Unit ID: ${workUnitId}`);

// Check Last Run Status
const statusCell = row.locator('td').filter({ hasText: /Ready|Error/ });
const status = await statusCell.textContent();

if (status.includes('Error')) {
  console.log(`Interface ${integrationName} failed. Opening work unit to view errors...`);
  
  // Click work unit link to open detail page
  await workUnitLink.click();
  await page.waitForTimeout(5000); // Wait for work unit detail page to load

  // Click Error Messages tab (tab text includes error count, e.g., "Error Messages (5)")
  await page.click('text=/Error Messages \\(\\d+\\)/');
  await page.waitForTimeout(3000); // Wait for error messages grid to load

  // Get error count from tab text
  const errorTab = await page.locator('text=/Error Messages \\(\\d+\\)/').textContent();
  const errorCount = errorTab.match(/\((\d+)\)/)[1];
  console.log(`Found ${errorCount} error messages in work unit ${workUnitId}`);

  // Extract error messages from grid
  const errorRows = page.locator('[role="row"]').filter({ has: page.locator('text=/Activity|Error encountered/') });
  const errorRowCount = await errorRows.count();

  const errors = [];
  for (let i = 0; i < errorRowCount; i++) {
    const errorRow = errorRows.nth(i);
    const errorCells = errorRow.locator('[role="gridcell"]');
    
    // Get error message (second cell) and error date (third cell)
    const errorMessage = await errorCells.nth(1).textContent();
    const errorDate = await errorCells.nth(2).textContent();
    
    errors.push({
      message: errorMessage.trim(),
      date: errorDate.trim()
    });
  }

  console.log(`Extracted ${errors.length} error messages:`);
  errors.forEach((error, index) => {
    console.log(`Error ${index + 1}:`);
    console.log(`  Date: ${error.date}`);
    console.log(`  Message: ${error.message.substring(0, 200)}...`); // Truncate for readability
  });

  // Return to CIS Outbound list
  await page.goBack();
  await page.waitForTimeout(3000);
  
  // Or use breadcrumb navigation
  // await page.click('text=Configurable Integration Solution - Outbound');
  // await page.waitForTimeout(3000);
} else {
  console.log(`Interface ${integrationName} completed successfully`);
}
```

### Pattern 6: Working with FSM Iframe

```javascript
// CRITICAL: FSM content may load in iframe, handle DOM changes carefully

// Option 1: Wait for iframe to be ready and interact within it
const iframe = page.frameLocator('iframe[name="main-content"]'); // Adjust selector as needed

// Interact with elements inside iframe
await iframe.locator('button[aria-label="Toggle navigation"]').click();
await page.waitForTimeout(3000);

// Option 2: If iframe selector is unreliable, use page-level selectors
// FSM often exposes elements at page level even when content is in iframe
await page.click('button[aria-label="Toggle navigation"]');
await page.waitForTimeout(3000);
```

## Context Menu Actions - Available Options

Right-click any interface row to access these actions. Available actions depend on Active status.

### Active Interfaces (Active = Yes)

- **Schedule Trigger**: Manually trigger the interface execution
- **Trigger**: Alternative trigger option (same as Schedule Trigger)
- **Open**: Open interface configuration detail page
- **Deactivate**: Deactivate the interface (prevents triggering)
- **Update**: Modify interface configuration
- **Delete**: Remove interface permanently
- **Copy From Integration**: Duplicate configuration to create new interface

### Inactive Interfaces (Active = No)

- **Schedule Trigger**: DISABLED (grayed out, cannot trigger)
- **Activate**: Activate the interface (REQUIRED before triggering)
- **Open**: Open interface configuration detail page
- **Update**: Modify interface configuration
- **Delete**: Remove interface permanently
- **Copy From Integration**: Duplicate configuration to create new interface

### Key Rule

Schedule Trigger and Trigger actions only work for Active=Yes interfaces. You MUST activate inactive interfaces before attempting to trigger them.

## Common Errors and Resolutions

### Error: "Interface is not active"

- **Cause**: Attempting to trigger interface with Active=No status
- **Resolution**: Right-click interface row > Activate, then retry trigger
- **Prevention**: Always check Active status before triggering

### Error: "File not found"

- **Cause**: Source file missing or incorrect file path configured
- **Resolution**: 
  - Verify file exists in expected location (SFTP server or FSM File Storage)
  - Check file path configuration in interface settings
  - For inbound interfaces, wait 1-2 minutes for File Channel transfer

### Error: "Permission denied"

- **Cause**: User lacks security access to interface or target business class
- **Resolution**: 
  - Grant appropriate security roles/permissions to user
  - Verify user has access to target business class operations
  - Check FSM security configuration for interface

### Error: "Data validation failed"

- **Cause**: Input data doesn't match expected format or violates business rules
- **Resolution**: 
  - Review input file format and structure
  - Check field mappings in interface configuration
  - Verify data types match expected types
  - Validate required fields are populated

### Error: "Business class error"

- **Cause**: Target business class operation failed (e.g., required field missing, validation rule violated)
- **Resolution**: 
  - Review work unit log for specific business class error message
  - Fix data to meet business class requirements
  - Update interface configuration if field mappings are incorrect

### Error: "Connection timeout"

- **Cause**: Network issue connecting to SFTP server, API endpoint, or Data Lake
- **Resolution**: 
  - Verify network connectivity to target system
  - Check credentials are valid and not expired
  - Retry interface execution
  - Contact system administrator if issue persists

## Error Handling - AI Instructions

When encountering CIS errors during testing or automation:

1. **Capture Error Message**: Extract error message from Last Run Status column or work unit detail page

2. **Document Error Context**:
   - Interface name (Integration Name)
   - Work unit ID (from Last Work Unit column)
   - Timestamp of execution
   - Input data or file name (if applicable)
   - Environment (tenant name)

3. **Check Common Causes**: Review "Common Errors and Resolutions" section above for known issues

4. **Do NOT Analyze Work Unit Logs**: Unless explicitly requested by user, do NOT download or analyze work unit logs. Focus on observable UI error messages only.

5. **Report Error to User**: Provide clear error report including:
   - Clear error description from UI
   - Work unit ID for reference
   - Suggested resolution (if known from common errors)
   - Context information (interface name, timestamp, environment)
   - Next steps or recommendations

## Monitoring Interface Execution

### Status Indicators

**Last Run Status Column Values**:

- ✅ **Ready** (green checkmark): Execution completed successfully
- ❌ **Error** (red X): Execution failed with error
- (Empty): Interface has never been executed

### Accessing Work Unit Logs

**To view detailed execution logs**:

1. Click **Last Work Unit** link (displays work unit ID as clickable link)
2. Work unit detail page opens showing:
   - Execution status (Completed, Failed, Running)
   - Start time and end time
   - Error messages (if execution failed)
   - Variable values used during execution
   - Activity log showing step-by-step execution

### Admin Monitoring Pages

Navigate to **Admin > Overview** for system-wide monitoring:

**Checkpoint**:

- Shows running and completed jobs across all interfaces
- Displays job name, status, start/end timestamps
- Useful for tracking long-running interfaces
- Filter by status, date range, or interface name

**Failed Async Action Trigger List**:

- Shows failed scheduled triggers that need attention
- Displays data area, queue, status, class, action
- Useful for troubleshooting scheduled interfaces that fail to trigger
- Retry failed triggers from this page

**File Channel List**:

- Shows all file channel configurations and status
- Displays channel name, active status, receivers, last scan time
- Useful for troubleshooting file-based interfaces
- Verify file channels are active and scanning regularly (scan interval configurable: 1-5 minutes typical)

## Best Practices

### Configuration Best Practices

- **Naming**: Use descriptive Integration Names that clearly identify purpose (e.g., "FSM-07 | INCOME STATEMENT ACTUAL VALUES")
- **Documentation**: Add clear descriptions explaining interface purpose and business context
- **Testing**: Test with sample data in non-production environment before activating for production use
- **Reusability**: Use parameter sets for configurations that can be reused across multiple interfaces
- **Organization**: Group related interfaces using Interface Groups for easier management

### Testing Best Practices

- **Context Menu**: Always use right-click context menu for triggering (more reliable than column buttons which can be hidden)
- **Active Status**: Check Active status first, activate interface before attempting to trigger
- **Status Monitoring**: Monitor Last Run Status after triggering, don't assume success without verification
- **Log Review**: Review work unit logs even for successful runs to check for warnings or unexpected behavior
- **Output Validation**: Validate actual output/data changes, not just execution status
- **Data Volume**: Test with small datasets first before running full production volumes

### Security Best Practices

- **Service Accounts**: Use service accounts (not personal accounts) for automated interface execution
- **Least Privilege**: Limit permissions to necessary security access only
- **Encryption**: Encrypt sensitive data in output files
- **Auditing**: Audit interface configurations regularly for unauthorized changes
- **Credential Rotation**: Rotate SFTP/API credentials regularly per security policy

### Performance Best Practices

- **Scheduling**: Schedule large data extracts during off-peak hours to minimize system impact
- **Pagination**: Use pagination for very large datasets to avoid memory issues
- **Optimization**: Monitor and optimize slow-running interfaces
- **Cleanup**: Clean up old work unit logs regularly to maintain system performance
- **Query Tuning**: Optimize queries for DBExport interfaces to improve extraction speed

## Related Steering Files

For additional context and related topics, refer to these steering files:

- **01_FSM_Navigation_Guide.md**: FSM UI navigation patterns and Playwright automation techniques
- **02_RICE_Methodology_and_Specifications.md**: RICE methodology with focus on Interfaces category
- **03_IPA_and_IPD_Complete_Guide.md**: Custom IPA development as alternative to CIS for complex scenarios
- **04_FSM_Business_Classes_and_API.md**: Business classes used in CIS interface configurations

## File Channels - Automated Inbound Triggers

### Overview

File Channels provide automated triggering for inbound IPA processes when files arrive on SFTP servers or FSM File Storage. File Channels are configured in Process Server Administrator and are used for custom IPA-based inbound interfaces (NOT for CIS inbound interfaces).

### Navigation Path

1. Login to FSM
2. Select **Process Server Administrator** role
3. Navigate to: **Administration > Channels Administrator**
4. Click **File Channels** tab

### File Channels Page Structure

The File Channels page has a master-detail layout with two grids:

**Top Grid - File Channels:**
- **Channel Name**: Unique identifier for the channel
- **Description**: Brief description
- **Active**: Yes/No - indicates if channel is currently active
- **Active Receivers**: Count of active receivers within this channel
- **Receivers**: Total count of receivers (active + inactive)
- **Last File Scan Time**: Timestamp of last scan for files
- **Enabled**: Yes/No - indicates if channel is enabled for scanning

**Bottom Grid - File Receiver List:**
- **Receiver**: Receiver name
- **Description**: Brief description
- **File Name**: File pattern to watch for (supports wildcards like *.csv)
- **Process**: IPA process name to trigger when file matches pattern
- **Last Message Received Time**: Timestamp of last file received
- **Data**: Data type (e.g., "File Name")
- **Status**: Active/Inactive status

### File Channel Architecture

**1-to-Many Relationship:**
- One File Channel can contain multiple File Receivers
- Each File Receiver watches for a specific file pattern
- Each File Receiver triggers a specific IPA process

**Example:**
- **Channel**: TEST_WUDL
  - **Receivers**: 2
  - **Receiver 1**: Watches for "Invoice*.csv" → Triggers "ProcessInvoices" IPA
  - **Receiver 2**: Watches for "PO*.csv" → Triggers "ProcessPurchaseOrders" IPA

### How File Channels Work

1. **File Arrival**: File is uploaded to SFTP server or FSM File Storage
2. **Channel Scan**: File Channel scans directory at regular intervals (typically every 1 minute)
3. **Pattern Match**: File Receiver checks if file name matches its pattern
4. **Auto-Trigger**: If match found, File Receiver automatically triggers associated IPA process
5. **File Transfer**: File is transferred from SFTP to FSM File Storage (if applicable)
6. **Process Execution**: IPA process runs and processes the file

### Key Differences: File Channels vs CIS Inbound

| Feature | File Channels | CIS Inbound |
| --- | --- | --- |
| **Use Case** | Custom IPA-based inbound | Pre-built CIS inbound |
| **Trigger Method** | Automatic (file arrival) | Manual/Scheduled only |
| **Configuration Location** | Process Server Administrator | Integration Architect |
| **File Monitoring** | Yes (scans SFTP/File Storage) | No (manual trigger required) |
| **IPA Process** | Custom IPA process | Generic CIS IPA process |
| **File Pattern Matching** | Yes (per receiver) | Yes (via File Catalog) |

### When to Use File Channels

Use File Channels when:
- Building custom IPA-based inbound interfaces
- Need automatic triggering when files arrive
- Files come from external SFTP servers
- Require custom business logic beyond CIS capabilities
- Need to trigger different processes based on file patterns

Do NOT use File Channels for:
- CIS inbound interfaces (use manual/scheduled triggers instead)
- Outbound interfaces (File Channels are inbound-only)

### Master-Detail Interaction

Selecting a File Channel in the top grid filters the File Receiver List to show only receivers associated with that channel. This is similar to the CIS Inbound File Catalog master-detail relationship.

## File Channel Detail Page - Structure

### Accessing File Channel Detail Page

**Method**: Double-click any File Channel row in the File Channels list page

### Header Section

- **Page Title**: "File Channel"
- **Breadcrumb**: Channels Administrator / File Channel
- **Action Buttons** (Toolbar):
  - **Previous**: Navigate to previous file channel in list
  - **Next**: Navigate to next file channel in list
  - **Create**: Create new file channel
  - **Save**: Save configuration changes (disabled until changes made)
  - **Delete**: Delete current file channel
  - **Refresh**: Reload current file channel data
  - **More Actions**: Additional actions menu (ellipsis "..." button)

### Tab Structure

The detail page has two tabs:

#### Overview Tab

Contains file channel configuration settings:

**Channel Information Section:**
- **Channel Name**: Text field (e.g., "TEST_WUDL") - Required, unique identifier
- **Description**: Text field (e.g., "TEST_WUDL") - Optional
- **Enabled**: Checkbox - Controls whether channel is active for scanning

**File Channel Configuration Section:**
- **File Channel Type**: Dropdown (e.g., "Remote", "Local")
  - Remote: SFTP server connection
  - Local: FSM File Storage only
- **Source File Directory**: Text field (e.g., "/TEST/Input") - Required
  - Directory path where channel scans for files
- **File Match Case Sensitivity**: Dropdown (e.g., "Ignore Case", "Match Case")
  - Controls how file patterns are matched
- **Error File Directory**: Text field (e.g., "/Error") - Optional
  - Directory where error files are moved

**File Processing Section:**
- **In-Progress File Directory**: Text field (e.g., "/InProgress") - Optional
  - Directory where files are moved during processing
- **Accept Empty Directory**: Checkbox
  - Allow channel to scan even if directory is empty

**Scanning Configuration Section:**
- **File Scan Interval Time In Minutes**: Text field (e.g., "5") - Required
  - How often channel scans for new files (in minutes)
- **Last File Scan Time**: Display-only field (e.g., "2/13/2026 5:23:12 AM")
  - Timestamp of last scan execution

**SFTP Connection Section** (for Remote channels only):
- **Host**: Text field (e.g., "sftp.inforcloudsuite.com") - Required
  - SFTP server hostname
- **Protocol**: Dropdown (e.g., "Sftp", "Ftp")
  - Connection protocol
- **Enable Host Key Checking**: Checkbox
  - Verify SFTP server host key
- **Authentication Type**: Dropdown (e.g., "User And Password", "Public Key")
  - Authentication method
- **User**: Text field (e.g., "csp-mt-tamics10_tam_ax1-usr") - Required
  - SFTP username
- **Sftp Password**: Password field (masked with asterisks) - Required
  - SFTP password
- **Time Out (In Seconds)**: Text field (e.g., "60") - Required
  - Connection timeout in seconds

**Notification Section:**
- **Notify By Email**: Dropdown (e.g., "None", "On Error", "Always")
  - Email notification settings
- **Test File (Works Only With Test Connection With Trace Log)**: Checkbox
  - Enable test file mode for connection testing

**Connection Testing Buttons:**
- **Test Connection**: Test SFTP connection without trace log
- **Test Connection With Trace Log**: Test SFTP connection with detailed trace log

#### File Channel Receivers Tab

Contains embedded grid showing file receivers associated with this channel.

**Grid Columns:**
- **Checkbox**: Select one or more receivers
- **Receiver**: Receiver name (e.g., "GLTxnTest", "WUDL")
- **Description**: Brief description (optional, may be empty)
- **File Name**: File pattern to watch for (supports wildcards)
  - Examples: "GLTransactionInterface_20251029_20251030*", "WUReportTrigger*.txt"
  - Asterisk (*) matches any characters
- **Process**: IPA process name to trigger (e.g., "TAMICS_GLInbound_Interface", "GetWorkUnits")
- **Last Message Received Time**: Timestamp of last file received (e.g., "10/30/2025 3:54:38 PM")
  - Empty if no files received yet
- **Data**: Data type (typically "File Name")
- **Status**: Active/Inactive status with icon

**Toolbar Actions:**
- **Create**: Add new file receiver to this channel
- **Open**: Open selected receiver (disabled when none selected)
- **Delete**: Delete selected receiver (disabled when none selected)
- **Search**: Search file receivers
- **Saved Searches**: Access saved search filters
- **More Actions**: Additional options

**Example Receivers (TEST_WUDL channel):**

| Receiver | Description | File Name | Process | Status |
| --- | --- | --- | --- | --- |
| GLTxnTest | (empty) | GLTransactionInterface_20251029_20251030* | TAMICS_GLInbound_Interface | Active |
| WUDL | TEST_WUDL | WUReportTrigger*.txt | GetWorkUnits | Active |

### Key Observations

1. **File Pattern Matching**: Receivers use wildcard patterns (*) to match multiple files
2. **Process Triggering**: Each receiver triggers a specific IPA process when file pattern matches
3. **Scan Interval**: Channel scans at regular intervals (e.g., every 5 minutes)
4. **SFTP Integration**: Remote channels connect to external SFTP servers
5. **Status Tracking**: Last Message Received Time shows when files were last processed
6. **Multiple Receivers**: One channel can have multiple receivers watching for different file patterns

## Summary

CIS (Configurable Integration Solution) provides no-code interface creation for FSM data integrations:

- **Outbound Interfaces**: Extract data from FSM and send to external systems (files, APIs, Data Lake)
- **Inbound Interfaces**: Import data from external systems into FSM (files, APIs, Data Lake, ION)
- **Testing Workflow**: Built-in trigger and monitoring via right-click context menu
- **Monitoring**: Admin section provides system-wide monitoring of interface execution
- **Best Practice**: Always verify Active=Yes before triggering, use right-click context menu for reliability, validate output data not just execution status
