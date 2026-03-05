---
inclusion: auto
name: work-unit-analysis
description: Work unit log analysis, error patterns, IPA process execution, activity logs, approval workflows. Use when analyzing work unit logs, troubleshooting IPA process failures, or conducting peer reviews.
---

# Work Unit Analysis Guide

## Purpose

This guide provides systematic approaches for analyzing IPA work unit logs, identifying error patterns, and troubleshooting process failures. Use when investigating failed work units, conducting peer reviews, or optimizing IPA performance.

## Table of Contents

- [Critical Rules](#critical-rules)
- [Log Structure & Parsing](#log-structure--parsing)
- [Error Patterns](#error-patterns)
- [JavaScript Engine (ES5)](#javascript-engine-es5)
- [Performance Analysis](#performance-analysis)
- [Analysis Methodology](#analysis-methodology)
- [Data Tracing](#data-tracing)

## Critical Rules

1. **Timestamp Format**: ALL IPA logs use `MM/DD/YYYY HH:MM:SS.mmm AM/PM` format
   - Parse with: `datetime.strptime(timestamp, '%m/%d/%Y %I:%M:%S.%f %p')`
   - Example: `08/26/2025 05:27:56.919 AM`

2. **Memory Limits**: Work units have 100,000 MiB (100GB) maximum
   - Critical: >90,000 MiB
   - Warning: >70,000 MiB
   - For >1M records, recommend Data Orchestrator or Data Warehouse

3. **JavaScript Engine**: Mozilla Rhino 1.7R4 (ES5 only)
   - NO ES6+ features (arrow functions, template literals, spread operator)
   - Use `var` instead of `let`/`const` for clarity
   - Use `function() {}` instead of `() => {}`

4. **Activity Types**: Common types include START, LM (Landmark), ASSGN (Assignment), BRANCH, UA (User Action), WEBRN (Web Run), ACCFIL (File Access), END


## Log Structure & Parsing

### Header Format

```text
Workunit [ID] started @ [DateTime]
    Landmark version: [Version]
    Process name: [ProcessName]
    Auto Restart: [Enabled/Disabled]
```

### Activity Pattern

Activities have start and completion markers with execution details between them:

**Start**: `Activity name:ActivityName type:TYPE id:N started @ [timestamp]`
**End**: `Activity name:ActivityName id:N completed @ [timestamp]`

**Extraction Regex**:
```python
pattern = r'Activity name:([^\s]+)\s+type:(\w+)\s+id:(\d+)\s+started @ ([^\n]+)\n(.*?)(?=Activity name:|\Z)'
```

### Work Unit Types

**FSM (Financials & Supply Management)**:
- Complex approval workflows with multi-level user interactions
- Financial data processing with detailed business logic
- Extensive JavaScript for calculations and transformations
- Longer execution times (minutes to hours including user wait time)
- Examples: `FPI_JournalEntryApproval`, `GLAgriBankInterface`, `MatchReport_Outbound`

**GHR (Global Human Resources)**:
- Simpler execution patterns with minimal logging
- Timeout-driven processes (system-initiated actions)
- Employee data operations with delta change tracking
- OAuth-based API integrations
- Examples: `HRMEmployeeExport`, `ImmediateApprve`
- Common errors: Timeout escalations, security proxy issues, empty OAuth data

### Bulk Data Processing

For work unit logs with millions of records (100MB+ files), use line-by-line pre-filtering:

**Preserve**:
- Activity markers (start/completion)
- Metrics sections
- Error messages
- Performance data

**Remove**:
- XML/JSON data blocks
- Large result sets
- Repetitive records (10+ consecutive)
- Large parameter blocks (>1000 chars)

**Result**: Reduces 100MB files to 5-10MB while preserving analysis-critical data.

## Error Patterns

### Quick Reference Table

| Error Signature | Pattern # | Severity | Root Cause |
|----------------|-----------|----------|------------|
| `No valid users [] or tasks []` | #1 | Critical | Empty actor variables |
| `Row not found: Unable to lock row` | #2 | High | Record deleted/missing |
| `Invalid JSON passed to JSON.parse()` | #3 | Medium | Malformed JSON config |
| `Timeout escalation: Dispatch Action` | #4 | Medium | Process hanging |
| `client is closed` | #5 | Medium | SFTP connectivity |
| `Error evaluating expression` | #6 | Medium-High | JavaScript syntax/type errors |
| `"variableName" is not defined` | #7 | Medium | Missing variable |
| Modern JS syntax | #8 | Medium | ES6+ features used |
| `Source file(s)/folder(s) do not exist` | #11 | High | Path mismatch |
| `Access denied for ... on ...` | #15 | High | Missing permissions |
| `All branch conditions false` | #16 | Medium | Null/undefined values |

### Pattern #1: User Assignment Configuration Error (CRITICAL)

**Signature**: `UserActionConfigException: No valid users [] or tasks [] with valid users were found for assignment`

**Root Cause**: Empty actor variables in UserAction activities - CSV user list resolves to empty values (`,,,`)

**Analysis Steps**:
1. Identify the failing UserAction activity name
2. Check all actor variables:
   - `CurrentApproverActor` (individual)
   - `CurrentApproverActorList` (list)
   - `CurrentTeamActorList` (team)
   - `CurrentPositionActorList` (position)
3. Verify ApprovalProcessor configuration
4. Check approval level and escalation settings

**Resolution**: Configure proper user assignments or team membership in approval workflow.

### Pattern #2: Database Record Not Found

**Signature**: `Row not found: Unable to lock row. Entry with key values [KeyValues] not found`

**Root Cause**: Record deleted or missing between process steps (common in long approval cycles)

**Resolution**:
- Add record existence validation before operations
- Implement graceful handling for missing records
- Review data retention policies
- Consider record locking during approval

### Pattern #3: JSON Parsing Issues

**Signature**: `Invalid JSON passed to JSON.parse()` or `SyntaxError: Empty JSON string`

**Root Cause**: Malformed JSON configuration or empty JSON strings

**Resolution**:
- Validate JSON syntax (trailing commas, quotes)
- Check for empty/null JSON variables before parsing
- Add try-catch around JSON.parse() calls

### Pattern #4: Timeout Escalation (GHR)

**Signature**: `Timeout escalation: Dispatch Action taken by system for [ID]`

**Characteristics**: Minimal log content, system-initiated action

**Resolution**:
- Optimize process performance
- Implement timeout handling
- Add monitoring and alerts

### Pattern #5: SFTP Connection Errors

**Signature**: `FileTransfer: Execution error java.io.IOException: client is closed`

**Root Cause**: Network connectivity issues during file transfer

**Resolution**:
- Implement retry logic with exponential backoff
- Add connection health checks
- Verify network/firewall configuration

### Pattern #6-8: JavaScript Errors

**Signatures**:
- `Error evaluating expression`
- `ReferenceError: "variableName" is not defined`
- `TypeError`, `SyntaxError`
- Modern JS syntax (ES6+) in ES5 environment

**Analysis Required**:
- Exact activity name and expression
- Specific variable names
- Root cause explanation
- Multiple fix options with code examples

**Resolution**:
- Define missing variables with defaults
- Fix syntax errors
- Convert ES6+ to ES5 (see JavaScript Engine section)
- Add null/undefined checks
- Use try-catch for error handling

### Pattern #9-10: Approval Configuration Errors

**Signature**: `UserActionConfigException` with JSON approval data

**Root Cause**: Empty arrays in JSON approval configuration

**Problematic JSON**:
```json
{
  "ActorList": [],
  "TeamActorList": [],
  "Actor": "",
  "ApprovalTeam": ""
}
```

**Resolution**:
1. Review `DerivedRoutingApprovalJSON` structure
2. Populate ActorList arrays with valid user IDs
3. Configure ApprovalTeam and TeamActorList
4. Validate JSON syntax and completeness
5. Test approval routing

### Pattern #11: File Transfer Source Missing

**Signature**: `FileTransfer: Source error - Source file(s)/folder(s) do not exist`

**Root Cause**: File path mismatch between FileAccess and FTP activities

**Common Issues**:
- Mismatched file paths
- Incorrect storage location
- File naming inconsistencies
- Temporary file cleanup before transfer

**Resolution**:
1. Verify FileAccess output path matches FTP source path
2. Check file naming variables for consistency
3. Validate storage location configuration
4. Add file existence validation before transfer
5. Implement retry logic

### Pattern #15: Security Access Denied

**Signature**: `Access denied for [ActionName] on [BusinessClass] for actor [ActorName]`

**Root Cause**: User lacks security permissions for approval action

**Resolution**:
1. Identify required security permissions
2. Grant business class permissions to approval users
3. Configure security roles for workflow participants
4. Test approval actions with assigned users
5. Add error handling for access denied scenarios

### Pattern #16: Branch Logic Null/Undefined Errors

**Signature**: `Branch [BranchName]: All branch conditions false` with undefined operations

**Root Cause**: Branch conditions evaluate undefined/null values from empty query results

**Resolution**:
1. Add null/undefined validation in JavaScript
2. Implement default values for empty results
3. Add branch conditions for empty/null scenarios
4. Use try-catch for variable operations
5. Validate data existence before processing

### Pattern #17: Data Extraction Key Validation Errors

**Signature**: `DoesNotExistException: [BusinessClass] does not exist` with invalid keys

**Root Cause**: Fixed-width data extraction produces invalid key values (spaces, wrong format)

**Resolution**:
1. Add data validation before lookup operations
2. Trim extracted values
3. Validate key format
4. Add error handling for invalid keys
5. Log extraction issues for debugging


## JavaScript Engine (ES5)

**Engine**: Mozilla Rhino 1.7R4 (JavaScript 1.7 with partial ES5)

### Supported Features ✅

```javascript
// Variables
var x = 5;                    // ✅ Recommended
const y = 10;                 // ✅ Works but doesn't enforce immutability

// Functions
function myFunc() { }         // ✅ Required syntax

// Strings
var msg = 'Hello ' + name;    // ✅ Concatenation required

// Arrays
var arr = [1, 2, 3];
arr.push(4);
arr.slice(0, 2);

// Objects
var obj = { key: 'value' };
obj.key = 'newValue';
```

### NOT Supported ❌

```javascript
// Arrow functions
() => {}                      // ❌ Use function() {}

// Template literals
`Hello ${name}`               // ❌ Use 'Hello ' + name

// Spread operator
[...array]                    // ❌ Use Array.prototype.slice.call(array)

// ES6 Classes
class MyClass {}              // ❌ Use function constructors

// Destructuring
const {x, y} = obj;           // ❌ Use obj.x and obj.y

// let keyword
let x = 5;                    // ❌ Use var x = 5;

// for...of loops
for (let x of arr)            // ❌ Use for (var i=0; i<arr.length; i++)
```

### Important: `const` Behavior

Rhino 1.7R4 supports `const` syntax but does NOT enforce immutability:
- ✅ Declaration works: `const x = 5;`
- ❌ Does NOT prevent reassignment
- ❌ Does NOT require initialization
- ❌ Does NOT prevent object/array modification

**Recommendation**: Use `var` for clarity about actual behavior.

### Common ES6 to ES5 Conversions

| ES6 Feature | ES5 Equivalent |
|-------------|----------------|
| `() => {}` | `function() {}` |
| `` `Hello ${name}` `` | `'Hello ' + name` |
| `[...arr]` | `Array.prototype.slice.call(arr)` |
| `let x = 5;` | `var x = 5;` |
| `const x = 5;` | `var x = 5;` |
| `for (let x of arr)` | `for (var i=0; i<arr.length; i++)` |
| `{x, y}` destructuring | `var x = obj.x; var y = obj.y;` |

### Performance Best Practices

- Prefer `for` loops over `for...in` for arrays
- Minimize `JSON.parse()` calls, cache results
- Combine `var` declarations at function top
- Use `===` for strict comparison
- Implement `try-catch` for error handling
- Use `typeof` for undefined checks

## Performance Analysis

### Activity Duration Benchmarks

- Database queries: 200ms - 2s (pagination: 48-85ms)
- User actions: Indefinite (human wait time)
- JavaScript processing: 10-50ms (data transformation: 2-16ms/record)
- File operations: 100-500ms

### Memory Thresholds

**Work Unit Level**:
- Maximum: 100,000 MiB (100GB)
- Critical: >90,000 MiB
- Warning: >70,000 MiB
- Normal: <70,000 MiB

**Node Level**:
- Critical: >1,000 MiB
- Warning: >500 MiB
- Normal: <500 MiB

**Typical Consumption**:
- Landmark activities: 100-800 MiB (highest)
- JavaScript assignments: 5-10 MiB (moderate)

**For >1M records**: Always recommend Data Orchestrator or Data Warehouse instead of IPA to avoid memory limits.

## Analysis Methodology

### Step-by-Step Approach

1. **Initial Assessment**
   - Check work unit status (SUCCESS/FAILED)
   - Identify process type (FSM vs GHR)
   - Review memory usage vs 100,000 MiB limit
   - Note auto-restart configuration

2. **Activity Flow Analysis**
   - Follow chronological sequence
   - Note branch decisions and routing
   - Identify bottlenecks and delays
   - Check user action patterns

3. **Error Pattern Matching**
   - Compare with known error signatures (see Error Patterns section)
   - Identify root cause category
   - Assess impact and severity
   - Check for cascading failures

4. **Performance Analysis**
   - Review metrics section
   - Identify memory-intensive activities (>800 MiB)
   - Analyze database query performance
   - Check JavaScript execution times

5. **JavaScript Code Review**
   - Check ES5 compliance (no ES6+ features)
   - Identify undefined variables
   - Review error handling
   - Assess performance patterns

6. **Root Cause Determination**
   - Correlate errors with activity flow
   - Identify configuration issues
   - Check data quality problems
   - Determine fix priority

7. **Recommendation Generation**
   - Provide specific code fixes with ES5-compliant syntax
   - Suggest configuration changes
   - Recommend process improvements
   - Include testing requirements

## Data Tracing

### Purpose

Use data tracing when investigating data quality issues (zeros, nulls, missing values) in BIFSM API + Compass API data extraction processes.

### Complete Data Flow Pattern

```text
1. GLTOT Cube (d/EPM)     → Source GL balance data
2. BIFSM_LoadApi          → Loads to Infor Data Lake (IDL Object)
3. Compass API InitQuery  → Submits SQL query to Data Lake
4. GetStatus (polling)    → Waits for query completion
5. GetResult              → Retrieves query results
6. Assign (raw)           → Stores API response (quoted CSV)
7. Assign (processed)     → Cleans data (unquoted CSV)
8. WriteFile              → Writes CSV file
9. SFTP                   → Transfers to client
```

### Tracing Steps

1. **Check raw API response** (quoted format: `"FCE","value"`)
   - Count zeros in target column
   - If zeros exist here → **source data issue**

2. **Check processed data** (unquoted format: `FCE,value`)
   - Count zeros in target column
   - Compare with raw zero count

3. **Verify BIFSM_LoadApi success**
   - Look for `"Data Successfully Loaded into IDL Object"`
   - Check HTTP 200 status

4. **Identify affected period**
   - Group zeros by period column
   - Compare with known-good files

5. **Determine root cause location**
   - Raw = Processed zeros → **Source data (cube) issue**
   - Processed > Raw zeros → **IPA processing issue**
   - Client file > Processed → **Client merge issue**

### Python Analysis Pattern

```python
def count_zeros_in_column(lines, column_index, is_quoted=False):
    """Count zero values in specific column."""
    zero_count = 0
    for line in lines:
        if is_quoted:
            parts = parse_quoted_csv(line)
        else:
            parts = line.split(',')
        
        if len(parts) > column_index:
            try:
                value = float(parts[column_index])
                if value == 0.0:
                    zero_count += 1
            except ValueError:
                continue  # Skip non-numeric values
    
    return zero_count
```

---

*This guide provides systematic approaches for work unit log analysis and troubleshooting based on real-world FSM and GHR implementations.*
