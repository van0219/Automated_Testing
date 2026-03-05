---
inclusion: auto
name: fsm-navigation
description: FSM UI navigation, Playwright browser automation, Process Server administration, IPA Designer, Service Definitions, triggers, scheduling. Use when navigating FSM interface or automating browser interactions.
---

# FSM Navigation & Browser Automation Guide

This guide provides actionable patterns for FSM UI navigation, Playwright automation, and IPA process management.

## Table of Contents

- [Critical Rules - Execute in Order](#critical-rules---execute-in-order)
- [Environment & Authentication](#environment--authentication)
- [Browser Automation with Playwright](#browser-automation-with-playwright)
- [FSM Navigation Patterns](#fsm-navigation-patterns)
- [Common Mistakes to Avoid](#common-mistakes-to-avoid)
- [Environment-Specific Data Quality](#environment-specific-data-quality)
- [Process Server Administrator](#process-server-administrator)
- [Work Units Management](#work-units-management)
- [Invoice Approval Workflow Example](#invoice-approval-workflow-example)

## Critical Rules - Execute in Order

### Rule 1: Snapshot Before Every Action

**ALWAYS use `mcp_playwright_browser_snapshot` before any interaction.**

Why:

- Shows exact page state with element refs for clicking
- Reveals sidebar state (expanded/collapsed)
- Displays actual menu structure and available options
- Eliminates guessing and trial-and-error

Correct pattern:

```javascript
// 1. Take snapshot
await mcp_playwright_browser_snapshot();

// 2. Find element in snapshot output
// Example: button "Toggle Navigation" [ref=f3e35]

// 3. Click using ref
await mcp_playwright_browser_click({ ref: "f3e35" });
```

**NEVER use `mcp_playwright_browser_run_code` for navigation or clicking.**

### Rule 2: Expand Sidebar First

**Before ANY navigation, expand the sidebar by clicking the hamburger icon (☰).**

```javascript
// 1. Take snapshot
await mcp_playwright_browser_snapshot();

// 2. Find "Toggle Navigation" button ref in snapshot
// 3. Click it
await mcp_playwright_browser_click({ ref: "found_ref" });

// 4. Wait for animation
await page.waitForTimeout(500);
```

Why critical:

- FSM starts with collapsed sidebar
- Most menu items are hidden when collapsed
- Navigation will fail without expanded sidebar

### Rule 3: Use Browser Zoom (Not CSS)

**Use keyboard commands for zoom, never CSS.**

Correct:

```javascript
// Apply 70% zoom (recommended)
await page.keyboard.press('Control+Minus');
await page.keyboard.press('Control+Minus');
await page.keyboard.press('Control+Minus');
```

Wrong:

```javascript
// DON'T DO THIS - causes layout issues
document.body.style.zoom = "0.7";
```

### Rule 4: Authentication by Environment

| Environment      | Auth Method                      | Credentials Location                        |
|------------------|----------------------------------|---------------------------------------------|
| TAMICS10_AX1     | Cloud Identities OR Windows      | `Credentials/.env.fsm` + `.env.passwords`   |
| ACUITY_TST       | Cloud Identities ONLY            | `Credentials/.env.fsm` + `.env.passwords`   |
| ACUITY_PRD       | Cloud Identities ONLY            | `Credentials/.env.fsm` + `.env.passwords`   |

**Security rules:**

- NEVER commit credential files to git
- NEVER log credentials in console or work unit logs
- ALWAYS read from `Credentials/` folder at runtime

### Rule 5: Double-Click for Record Details

- **Single-click**: Selects record (highlights row)
- **Double-click**: Opens record detail view (REQUIRED for PO, invoices, work units)

```javascript
// Wrong - only selects
await page.click('a[href*="PurchaseOrder"]');

// Correct - opens detail
await page.locator('a[href*="PurchaseOrder"]').dblclick();
```

### Rule 6: Use Search for Comprehensive Lists

**Avoid homepage widgets** - they show filtered subsets only.

**Use Search bar** for comprehensive lists:

```javascript
await page.click('input[placeholder="Search"]');
await page.type('input[placeholder="Search"]', 'PurchaseOrder');
await page.click('text=PurchaseOrder.PurchaseOrderList');
```

## Environment & Authentication

### Environment Selection

| Environment      | Purpose           | Data Quality                                      | Auth Method              |
|------------------|-------------------|---------------------------------------------------|--------------------------|
| **ACUITY_TST**   | Testing, UAT      | Excellent - real vendors, employees, emails       | Cloud Identities only    |
| **ACUITY_TRN**   | Training          | Training data for end users                       | Cloud Identities only    |
| **ACUITY_PRD**   | Production        | Live business data                                | Cloud Identities only    |
| **TAMICS10_AX1** | Sandbox, POC      | Limited/placeholder data                          | Cloud Identities OR Windows |

**Recommendation**: Use ACUITY_TST for realistic testing.

### Credential Management

**File structure:**

```text
Credentials/
├── .env.fsm              # FSM URLs and usernames
├── .env.passwords        # Passwords (NEVER commit)
├── TAMICS10_AX1.ionapi   # ION API credentials
├── ACUITY_TST.ionapi     # ION API credentials
```

**Security rules:**

- NEVER commit credential files to git (.gitignore configured)
- NEVER log credentials in console or work unit logs
- ALWAYS read from `Credentials/` folder at runtime

**Example .env.fsm:**

```bash
DEFAULT_ENVIRONMENT=TAMICS10_AX1

TAMICS10_AX1_URL=https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1/
TAMICS10_AX1_USERNAME=user@example.com
TAMICS10_AX1_PASSWORD=${TAMICS10_AX1_PASSWORD}
```

**Example .env.passwords:**

```bash
TAMICS10_AX1_PASSWORD=actual_password_here
ACUITY_TST_PASSWORD=actual_password_here
```

**Playwright authentication pattern:**

```javascript
// 1. Read credentials
const fs = require('fs');
const envContent = fs.readFileSync('Credentials/.env.passwords', 'utf8');
const envFsmContent = fs.readFileSync('Credentials/.env.fsm', 'utf8');

// 2. Parse
const password = envContent.match(/TAMICS10_AX1_PASSWORD=(.+)/)[1];
const url = envFsmContent.match(/TAMICS10_AX1_URL=(.+)/)[1];
const username = envFsmContent.match(/TAMICS10_AX1_USERNAME=(.+)/)[1];

// 3. Login
await page.goto(url);
await page.fill('input[name="username"]', username);
await page.fill('input[name="password"]', password);
await page.click('button[type="submit"]');

// 4. NEVER log credentials
console.log('Login successful'); // OK
// console.log(`Password: ${password}`); // NEVER DO THIS
```

## Browser Automation with Playwright

### MCP Configuration

**File**: `.kiro/settings/mcp.json`

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--isolated"],
      "disabled": false
    }
  }
}
```

### Essential Tools

- `mcp_playwright_browser_navigate` - Navigate to URLs
- `mcp_playwright_browser_snapshot` - Capture page state (use before actions)
- `mcp_playwright_browser_click` - Click elements using refs
- `mcp_playwright_browser_type` - Type text
- `mcp_playwright_browser_fill_form` - Fill multiple fields
- `mcp_playwright_browser_take_screenshot` - Capture screenshots for evidence

### Standard Automation Sequence

```javascript
// 1. Navigate and authenticate
await page.goto(url);
await page.fill('input[name="username"]', username);
await page.fill('input[name="password"]', password);
await page.click('button[type="submit"]');

// 2. Take snapshot to see page state
await mcp_playwright_browser_snapshot();

// 3. Expand sidebar (CRITICAL)
// Find "Toggle Navigation" ref in snapshot, then:
await mcp_playwright_browser_click({ ref: "found_ref" });
await page.waitForTimeout(500);

// 4. Apply browser zoom (70% recommended)
await page.keyboard.press('Control+Minus');
await page.keyboard.press('Control+Minus');
await page.keyboard.press('Control+Minus');

// 5. Navigate to target using snapshot + click pattern
await mcp_playwright_browser_snapshot();
// Find element ref, then click
await mcp_playwright_browser_click({ ref: "element_ref" });
```

### Click Strategies

**Standard click** (try first):

```javascript
await mcp_playwright_browser_click({ ref: "element_ref" });
```

**Double-click** (for record details):

```javascript
await page.locator('selector').dblclick();
```

**JavaScript evaluation** (fallback for intercepted clicks):

```javascript
await page.evaluate(() => {
    document.querySelector('selector').click();
});
```

## FSM Navigation Patterns

### Accessing FSM Application

**CRITICAL**: FSM (Financials & Supply Management) is the main application. Roles are accessed WITHIN FSM.

**Navigation sequence:**

1. Login to Infor OS Portal
2. Take snapshot
3. Expand sidebar (☰) if collapsed
4. Navigate to Applications section
5. Click "See more"
6. Click "Financials & Supply Management"
7. Wait for "My Available Applications" page
8. Select desired role (Integration Architect, Process Server Administrator, Payables, etc.)

### Search-Based Navigation (Recommended)

**Why**: Homepage widgets show filtered subsets. Search provides comprehensive lists.

**Pattern:**

```javascript
// 1. Take snapshot
await mcp_playwright_browser_snapshot();

// 2. Find search input ref, click it
await mcp_playwright_browser_click({ ref: "search_ref" });

// 3. Type business class name
await page.type('input[placeholder="Search"]', 'PurchaseOrder');

// 4. Take snapshot to find list option
await mcp_playwright_browser_snapshot();

// 5. Click .List option
await mcp_playwright_browser_click({ ref: "list_ref" });
```

**Business class examples:**

- `PurchaseOrder.PurchaseOrderList` - All POs
- `PayablesInvoice.PayablesInvoiceList` - All invoices
- `Vendor.VendorList` - All vendors

### Record Access

- **Single-click**: Selects record (highlights row)
- **Double-click**: Opens record detail view (REQUIRED)

```javascript
// Wrong - only selects
await page.click('a[href*="PurchaseOrder"]');

// Correct - opens detail
await page.locator('a[href*="PurchaseOrder"]').dblclick();
```

### Menu Navigation

**Expanding submenus:**

- Click caret/arrow (▶) to expand without navigating
- Click menu text to navigate to default page

```javascript
// Expand Setup menu without navigating
await page.click('button[aria-label="Expand Setup"]');

// Then click submenu
await page.click('text=Invoice Routing Rules');
```

## Common Mistakes to Avoid

### 1. Using run_code Instead of Snapshot + Click

**Problem**: Using `mcp_playwright_browser_run_code` to navigate or click elements

**Impact**: Timeout errors, element not found, wasted debugging time

**Solution**: ALWAYS use snapshot first, then click with refs

Wrong:

```javascript
await page.run_code(`
  await frame.locator('a:has-text("Work Units")').click();
`);
```

Correct:

```javascript
// 1. Take snapshot
await mcp_playwright_browser_snapshot();
// 2. Find: link "Work Units" [ref=f3e257]
// 3. Click using ref
await mcp_playwright_browser_click({ ref: "f3e257" });
```

### 2. Confusing PSA Homepage with Work Units Page

**Problem**: Thinking you're on Work Units page when on Process Server Administrator homepage

**Impact**: Filtering wrong grid, no work units showing

**Solution**: Check page title in snapshot - should say "Work Units", not "Process Server Administrator"

Verification:

- Take snapshot
- Look for heading "Work Units" [level=1]
- If you see "Process Server Administrator", navigate to Administration > Work Units

### 3. Forgetting to Expand Sidebar

**Problem**: Attempting navigation without clicking hamburger icon (☰)

**Impact**: Navigation fails, menu items hidden

**Solution**: ALWAYS expand sidebar first

### 4. Using CSS Zoom Instead of Browser Zoom

**Problem**: `document.body.style.zoom = "0.7"`

**Impact**: Layout breaks, blank spaces

**Solution**: Use `page.keyboard.press('Control+Minus')` 3x

### 5. Wrong Authentication Method

**Problem**: Attempting Windows auth on ACUITY_TST/PRD

**Impact**: Login loops, authentication failures

**Solution**: Use Cloud Identities only for ACUITY environments

### 6. Single-Click Instead of Double-Click

**Problem**: Single-clicking records expecting detail view

**Impact**: Only selects record, doesn't open details

**Solution**: Use `.dblclick()` for record details

### 7. Using Homepage Widgets for Comprehensive Data

**Problem**: Relying on filtered widgets (Unreleased POs, etc.)

**Impact**: Missing data, incomplete analysis

**Solution**: Use Search → BusinessClass.List for comprehensive views

## Environment-Specific Data Quality

### TAMICS10_AX1 (Sandbox)

- **Data**: Limited, placeholder ([Sample Name], [sample@email.com])
- **Use For**: POC, basic functionality testing
- **Avoid For**: Realistic testing, UAT

### ACUITY_TST (Test)

- **Data**: Excellent - real vendors (CDW DIRECT), employees (Angela Erdmann), emails (<example@acuity.com>)
- **Use For**: UAT, comprehensive testing, template validation
- **Best Choice**: Most realistic non-production environment

### ACUITY_PRD (Production)

- **Data**: Live business data
- **Use For**: Production operations only
- **Restrictions**: Change control, limited testing access

## Process Server Administrator

### Role Overview

Process Server Administrator role provides access to IPA process management: process definitions, version control, scheduling, and work unit monitoring.

### Accessing Process Server Administrator

1. Login to FSM environment
2. Switch to "Process Server Administrator" role
3. Access via hamburger menu (☰) → Configuration or Scheduling sections

**Key areas:**

- **Configuration > Process Definitions**: View and manage deployed IPAs
- **Scheduling > By Process Definition**: Create and manage process triggers
- **Administration > Channels Administrator > File Channels**: Configure file-based triggers
- **Administration > Work Units**: Monitor IPA executions

### Process Definitions

#### Process Types

| Type                 | Description                  | Use Case                      |
|----------------------|------------------------------|-------------------------------|
| User Defined         | Custom IPAs uploaded from IPD | Client-specific workflows     |
| System Defined       | Out-of-box Infor IPAs        | Standard Infor automation     |
| Application Defined  | App-specific IPAs            | FSM, GHR automation           |

**Navigation**: Configuration > Process Definitions > [Type]

#### Process Detail Page

**Access**: Double-click any process in list

**Key tabs:**

- **General**: Process name, description, category
- **Properties**: Work Unit Logging, Auto Restart, Timeout
- **Process Versions**: Version history with upload dates
- **Triggers**: Associated scheduled triggers

#### Version Management

**Version History tab shows:**

- Version number
- Upload date and uploader
- Comments

**Right-click actions:**

- **Make Current Version**: Activate specific version (rollback)
- **View Details**: See version metadata
- **Compare Versions**: Identify changes
- **Download**: Download LPD file

**Rollback procedure:**

1. Navigate to Process Versions tab
2. Right-click desired version
3. Select "Make Current Version"
4. Confirm
5. New work units use selected version

### Process Scheduling and Triggers

#### Scheduling Views

| View                     | Purpose                          | Navigation                           |
|--------------------------|----------------------------------|--------------------------------------|
| By Service Definition    | Schedule service-based triggers  | Scheduling > By Service Definition   |
| By Process Definition    | Schedule process-based triggers  | Scheduling > By Process Definition   |

**Recommended**: Use "By Process Definition" for IPA scheduling

#### Process Triggers List Page

**Purpose**: Create, configure, schedule, and manually trigger IPAs

**Grid columns:**

- Process Name (e.g., "GetWorkUnits")
- Work Title (e.g., "**IPD**_GetWorkUnits")
- Status

**Right-click context menu** (use this, not toolbar):

- **Open**: View/edit trigger configuration
- **Schedule**: Configure trigger timing
- **Start**: Manually run trigger immediately
- **Update**: Modify trigger properties
- **Delete**: Remove trigger

#### Process Trigger Detail Page

**Access**: Double-click trigger row

**Configuration fields:**

- **Process Name**: Required - Select IPA to trigger
- **Work Title**: Required - Display title for work units
- **Filter Key/Value**: Optional - Filter criteria
- **Apps Key/Value**: Optional - Application-specific values

**Tabs:**

1. **Variables**: Define input variables passed to IPA at runtime
2. **Related Links**: Link to documentation or resources

**More Actions menu:**

- **Start**: Manually run trigger
- **Export To PDF**: Export configuration
- **Audit**: View configuration change history

#### Creating and Scheduling Triggers

**Workflow:**

```text
1. Create Trigger (unscheduled)
   ↓
2. Configure Properties
   ↓
3. Schedule Trigger (set timing)
   ↓
4. Activate
```

**Creating:**

1. Navigate to Scheduling > By Process Definition
2. Click "Create"
3. Select process definition
4. Configure properties
5. Save (trigger created but NOT scheduled)

**Scheduling:**

1. Right-click trigger
2. Select "Schedule"
3. Configure:
   - Frequency (Daily, Weekly, Monthly, Hourly)
   - Start Time
   - Recurrence
   - End Date (optional)
4. Save

**Manual execution:**

1. Right-click trigger
2. Select "Start"
3. Confirm
4. Monitor work unit

#### Trigger Best Practices

**Naming conventions:**

- Use descriptive names: `APIA_InvoiceApproval_Nightly`
- Include frequency: `_Daily`, `_Hourly`, `_Weekly`
- Add environment prefix: `PRD_`, `TST_`, `TRN_`

**Scheduling considerations:**

- Schedule resource-intensive IPAs during off-peak hours
- Consider upstream/downstream process timing
- Verify server timezone

**Monitoring:**

- Enable Work Unit Logging for all scheduled IPAs
- Review execution history regularly
- Monitor execution duration trends

### Common Process Management Tasks

**Deploy new IPA version:**

1. Upload LPD from IPD to FSM
2. Navigate to Configuration > Process Definitions > User Defined
3. Find process (use filter)
4. Double-click to open detail
5. Verify new version in Process Versions tab
6. Right-click new version → "Make Current Version"
7. Test with manual trigger

**Rollback to previous version:**

1. Navigate to process detail page
2. Open Process Versions tab
3. Identify stable version
4. Right-click version → "Make Current Version"
5. Confirm
6. Test with manual trigger

**Schedule new IPA:**

1. Navigate to Scheduling > By Process Definition
2. Click "Create"
3. Select process definition
4. Configure trigger properties
5. Save (unscheduled)
6. Right-click trigger → "Schedule"
7. Configure schedule
8. Save
9. Verify trigger shows as scheduled

**Disable scheduled IPA:**

1. Navigate to Scheduling > By Process Definition
2. Find trigger
3. Right-click → "Disable"
4. Confirm

**Review execution history:**

1. Navigate to Scheduling > By Process Definition
2. Find trigger
3. Right-click → "View History"
4. Review dates, statuses, work unit IDs
5. Click work unit ID for detailed log

## Work Units Management

### Work Units Overview

Work Units are execution instances of IPA processes. Each IPA execution creates a work unit to track execution, store logs, variables, and results.

### Accessing Work Units

**CRITICAL**: Process Server Administrator homepage is NOT the Work Units page.

**Correct navigation:**

1. Take snapshot to verify current page
2. Expand sidebar (☰) if collapsed
3. Click "Administration" menu
4. Click "Work Units" submenu
5. Take snapshot to confirm page title is "Work Units"

**Common mistake**: Staying on PSA homepage expecting to see work units. The bottom grid shows "Process Server Run Time Status", NOT work units.

### Work Units List Page

**Grid columns:**

- Work Unit (ID, e.g., "637305")
- Work Title (e.g., "Birthdays")
- Process (IPA name, e.g., "RequestNewInvoicePayment")
- Status (Completed, Failed, Running, Waiting)
- Start Date
- Close Date
- Elapsed Time
- Service (if triggered by service definition)

**Toolbar actions:**

- Create, Open, Delete, Search, Refresh, More Actions

**Filter capabilities:**

- Filter by Work Unit ID (exact match)
- Filter by Process (contains)
- Filter by Status (dropdown)
- Filter by Start/Close Date

### Work Unit Detail Page

**Access**: Double-click work unit row

**Key tabs for troubleshooting:**

1. **Error Messages**: First place to check when work unit fails
2. **Log**: Detailed execution log
3. **Activity Nodes**: See which activities executed
4. **Variables**: Check variable values during execution
5. **Resource Metric**: Identify performance issues

**Status values:**

- Completed: Finished successfully
- Failed: Execution failed with errors
- Running: Currently executing
- Waiting: Waiting for condition or user action
- Canceled: Canceled by user

### Work Unit Best Practices

1. **Use filters**: Filter by Process name to find specific IPA executions
2. **Check status**: Monitor "Failed" status for errors
3. **Review errors**: Always check Error Messages tab first
4. **Track elapsed time**: Identify slow-running processes
5. **Monitor resources**: Check Resource Metric tab for performance issues
6. **Link to definitions**: Cross-reference with Process Definitions for version info

## Invoice Approval Workflow Example

Real-world example: BayCare APIA (Invoice Approval Process Automation)

### Workflow

```text
User Action (Release Invoice)
   ↓
Business Class Action (PayablesInvoice)
   ↓
Service Definition (InvoiceApproval)
   ↓
IPA Execution (InvoiceApproval_APIA_NONPOROUTING)
   ↓
Work Unit Created (1:1 ratio)
```

### Key Components

**Service Definition** (InvoiceApproval):

- Triggered by PayablesInvoice.Release action
- NO filtering - all releases trigger service
- Passes to IPA for routing logic

**IPA Process** (InvoiceApproval_APIA_NONPOROUTING.lpd):

- Queries invoice details including RoutingCategory field
- Evaluates routing rules based on RoutingCategory
- Routes to appropriate approval path
- Creates User Actions for approvers
- Sends email notifications

**Routing Logic**:

- RoutingCategory = "F": Full approval workflow (L1 Coder → L2 Person Responsible → L3+ Management)
- RoutingCategory ≠ "F": Alternative path

**Cross-Application Data** (FSM ↔ GHR):

- FSM IPAs query GHR business classes for employee data
- Dynamic dataArea mapping: BAYCAREHS_TRN_FSM → BAYCAREHS_TRN_HCM
- GHR classes: HROrganizationUnit, Employee, WorkAssignment, Supervisor
- Purpose: Retrieve Person Responsible, supervisor chain, emails

### Automated Workflows

**Nightly Release IPA**:

- Scheduled trigger runs nightly
- Queries unreleased invoices
- Programmatically calls Release action
- Each release triggers main approval IPA

**Auto-Reject IPA**:

- Standalone monitoring process (runs daily)
- Queries work units pending > 30 business days
- Auto-rejects stale invoices
- NOT part of main approval workflow

### Key Principles

1. No service-level filtering - service passes ALL releases to IPA
2. One-to-one work units - one invoice = one work unit (audit trail)
3. IPA internal routing - all routing logic inside IPA
4. Nightly trigger optional - just automation convenience
5. Reject IPA standalone - separate monitoring process

### Navigation

**Access Invoice Management**:

1. Switch to Payables Manager role
2. Expand sidebar (☰)
3. Click "Manage Invoices"

**Access Routing Rules**:

1. Expand sidebar (☰)
2. Click Setup caret (▶)
3. Click "Invoice Approval Setup" caret
4. Click "Invoice Routing Rules"

**Access Service Definitions**:

1. Switch to Process Server Administrator role
2. Configuration > Service Definitions
3. Search "InvoiceApproval"

---

*This guide provides actionable patterns for FSM navigation and browser automation based on real-world implementations.*
