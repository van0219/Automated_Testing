# Kiro Automated Testing Workspace – Architecture & Workflow

## Purpose

This document defines the architecture and workflow for the Kiro Automated Testing Workspace.

The goal is to improve performance, reliability, and scalability of automated testing for Infor FSM implementations while maintaining compatibility with existing TES-070 regression documentation.

The framework adopts a **hybrid automation architecture** where APIs are used for fast data creation while UI automation is reserved only for validation scenarios where APIs are unavailable.

---

# Key Architecture Principles

1. **UI automation must not be used for transaction creation.**
   UI form population is slow and fragile. Transaction creation will use FSM APIs whenever possible.

2. **Playwright will only be used for UI validation and monitoring.**
   UI automation will be used for:
   - Approval workflow validation
   - FSM UI verification
   - Process Server Admin monitoring
   - File channel verification
   - IPA workunit verification

3. **Kiro acts as the test orchestration engine.**
   Kiro coordinates parsing, validation, execution, monitoring, and reporting.

---

# Hybrid Automation Architecture

```
Kiro AI Orchestrator
│
├── Input Layer
│   ├── TES-070 Documents
│   └── Test Scripts
│
├── Processing Layer
│   ├── TES-070 Parser
│   └── Script Generator
│
├── Review Gate
│   └── Tester Approval Step
│
├── Validation Engine
│   ├── Global Validation Rules
│   └── Client Validation Rules
│
├── Execution Engine
│   ├── FSM API Data Creation
│   ├── Playwright FSM UI Validation
│   └── Playwright Process Server Monitoring
│
└── Reporting Engine
    └── TES-070 Output Generator
```

---

# Two Test Entry Paths

The framework supports two ways to initiate testing.

## Path 1 – Regression Testing (Using TES-070)

Regression testing uses existing TES-070 documentation as the starting point.

Workflow:

```
TES-070 Document
  ↓
TES-070 Parser
  ↓
Generated Test Script
  ↓
⏸ REVIEW GATE – Tester Review Required
  ↓
Approved Test Script
  ↓
Automation Execution
  ↓
Test Results
  ↓
TES-070 Output Report
```

The generated script must be reviewed and approved by a tester before execution.

This ensures that ambiguous or inconsistent instructions from TES-070 are corrected before automation runs.

---

## Path 2 – Net New Testing

For new test scenarios, scripts are created directly without TES-070 parsing.

Workflow:

```
Test Script Creation
  ↓
⏸ REVIEW GATE – Tester Review Required
  ↓
Approved Test Script
  ↓
Automation Execution
  ↓
Test Results
  ↓
TES-070 Output Report
```

TES-070 parsing is skipped in this path.

---

# Review Gate (Mandatory Approval Step)

All test scripts must pass through a **review gate** before execution.

Script lifecycle:

```
Generated
  ↓
Pending Review
  ↓
Approved
  ↓
Executed
  ↓
Completed
```

Automation must **not execute scripts that are not approved**.

This prevents incorrect or incomplete scripts from running.

Example metadata inside scripts:

```json
{
  "test_name": "EXT_FIN_004 Expense Invoice Approval",
  "source": "TES-070",
  "status": "pending_review"
}
```

Execution can only proceed when the status is:

```
approved
```

---

# Data Creation Strategy

All transactions should be created using **FSM APIs whenever possible**.

Examples:
- Expense Invoice
- Journal Entry
- Vendor records
- Requisitions
- AP invoices

Typical process:

1. Kiro parses the test scenario.
2. Kiro prepares the test data payload.
3. Kiro calls the FSM API.
4. FSM creates the transaction.
5. The transaction ID is returned and used for validation.

This approach eliminates slow UI form automation.

---

# Workflow Validation

After the transaction is created, workflow behavior must be validated.

Playwright UI automation will perform actions such as:

1. Login as the appropriate approver role
2. Navigate to the approval queue
3. Locate the generated transaction
4. Perform approval or rejection
5. Verify status changes

This ensures approval logic behaves correctly.

---

# Process Server Admin Validation

Some functionality does not expose APIs and must be verified through the UI.

Examples include:
- File Channel monitoring
- IPA Workunit execution
- Process Server Admin monitoring
- Integration execution logs

Playwright automation will verify:
- Files received in channels
- Workunit creation
- IPA execution status
- Error logs

---

# Validation Rules Framework

Validation rules ensure that test data is valid before execution.

Two rule layers exist.

## Global Validation Rules

Location:

```
Projects/_Global/ValidationRules/global_validation_rules.xlsx
```

Contains universal FSM rules such as:
- Date formats
- Positive amounts
- Required fields
- Standard account structure

---

## Client-Specific Validation Rules

Location:

```
Projects/{ClientName}/ValidationRules/{client}_validation_rules.xlsx
```

Contains:
- Client-specific accounts
- Event codes
- Approval thresholds
- Local overrides

Rule precedence:

```
Client rules override global rules when conflicts exist.
```

---

# Validation Types

**Static Validation**

Checks performed using rule definitions only.

Examples:
- Required fields
- Format validation
- Business rule checks

**Dynamic Validation**

Checks performed by querying FSM.

Examples:
- Valid accounts
- Vendors
- Cost centers
- Event codes

**Hybrid Validation**

Combination of static rule checks and FSM queries.

---

# Script Storage Structure

Test scripts should be organized to reflect their lifecycle state.

Example structure:

```
Projects/ClientName/TestScripts/
    PendingReview/
    Approved/
    Executed/
```

Scripts move between folders as they progress through the lifecycle.

---

# Expected Benefits

**Performance**

API-based transaction creation significantly reduces execution time.

**Reliability**

Reduced UI dependency minimizes automation failures caused by UI changes.

**Scalability**

The framework supports multiple clients and modules with consistent rules.

**Traceability**

TES-070 remains the documentation artifact while scripts power the automation.

**Controlled Automation**

The review gate ensures testers maintain oversight of generated scripts.

---

End of document.
