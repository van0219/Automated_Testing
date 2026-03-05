---
inclusion: auto
name: ipa-ipd-guide
description: IPA and IPD concepts, LPD file analysis, activity nodes, S3 to FSM migration, process designer, work units, JavaScript ES5, approval workflows, Landmark integration. Use when analyzing LPD files, designing IPA processes, or migrating S3 to FSM.
---

# IPA and IPD Complete Guide

Comprehensive reference for Infor Process Automation (IPA) and Infor Process Designer (IPD). This guide provides actionable patterns for analyzing LPD files, designing processes, and migrating S3 to FSM.

## Table of Contents

- [Quick Reference](#quick-reference)
- [Platform Overview](#platform-overview)
- [IPD Environment](#ipd-environment)
- [Activity Node Categories](#activity-node-categories)
- [File Operations Architecture](#file-operations-architecture)
- [Data Access Architecture](#data-access-architecture)
- [Variables and JavaScript](#variables-and-javascript)
- [Error Handling](#error-handling)
- [Auto-Restart Design](#auto-restart-design)
- [ION Integration](#ion-integration)
- [Landmark and Web Service Integration](#landmark-and-web-service-integration)
- [Performance Best Practices](#performance-best-practices)
- [FSM Security and Access](#fsm-security-and-access)
- [S3 to FSM Migration](#s3-to-fsm-migration)
- [Activity Class Name Reference](#activity-class-name-reference)
- [LPD File Creation Checklist](#lpd-file-creation-checklist)
- [Best Practices Summary](#best-practices-summary)
- [FSM Navigation](#fsm-navigation)
- [S3 Legacy Activity Types](#s3-legacy-activity-types)

## Quick Reference

### Related Guides

- `00_Kiro_General_Rules.md` - IPA Analyzer tools, analysis workflow
- `02_Work_Unit_Analysis.md` - Error patterns, JavaScript ES5 compliance
- `03_Process_Patterns_Library.md` - 450+ production IPA templates
- `09_FSM_Navigation_Guide.md` - Playwright automation, FSM UI navigation
- `10_IPA_Report_Generation.md` - Peer reviews, client handover reports

### Core Terminology

- **IPA**: Workflow automation engine for business processes
- **IPD**: Eclipse-based IDE (v9.0.1, Java 17) for designing IPA processes
- **LPD Files**: Process definitions (.lpd XML format)
- **Work Units**: Execution instances with logs and variables
- **JavaScript**: Mozilla Rhino 1.7R4 (ES5 compliant, avoid ES6)

## Platform Overview

### IPA vs LPL

| Aspect | IPA | LPL |
|--------|-----|-----|
| Purpose | Process automation, workflows | UI/form modifications |
| Tool | IPD (Infor Process Designer) | Configuration Console |
| File Type | .lpd | .lpl |
| Scope | Cross-system workflows | FSM form-level only |
| Integration | LPL triggers IPA via events | IPA interacts with LPL objects |

### S3 vs FSM IPA

| Aspect | S3 (Legacy) | FSM (Modern) |
|--------|-------------|--------------|
| Platform | On-premises Lawson S3 | Cloud-first Infor FSM |
| File Types | .pfi, .xml, .ipd | .lpd, .ipd, .xml |
| Data Access | AGS/DME calls, direct tables | Business classes, Data Lake, REST APIs |
| Integration | S3 programs, batch jobs | ION, web services, business classes |
| Deployment | ProcessFlow Integrator server | IPA engine integrated with FSM |
| S3-Only Nodes | AGS, DME, QUERY, RMQR, BATCH | Deprecated - use LM, WEBRN instead |

**Migration Strategy**: Replace AGS/DME with Landmark (LM) activities, convert table queries to business class queries, modernize error handling.

## IPD Environment

### Installation Details

- **Version**: 2025.06.02.56
- **Platform**: Eclipse-based IDE (v9.0.1)
- **Runtime**: Java 17 (Amazon Corretto JDK 17.0.11_9)
- **Architecture**: Plugin-based with 100+ JAR dependencies
- **Documentation**: 258 pages of comprehensive IPD capabilities

### Environment Configuration

- **Primary Environment**: TAMICS10_AX1 (sandbox FSM tenant)
- **Connection Type**: Infor CloudSuite HTTPS endpoints
- **Multi-Tenant Support**: PRD, TST, TRN, AX1, PP1 per client
- **Multi-Environment**: 21+ configured environments

### Sample Solutions Library

100+ production templates including:

- Financial workflows (actaddapproval.lpd, jeapproval.lpd, poapprove.lpd)
- Integration patterns (ION-enabled processes)
- S3 query integrations
- Web service calls

## Activity Node Categories

### Deprecated Nodes (2024.10+)

**DO NOT use these nodes in new processes:**

| Deprecated Node | Replacement | Reason |
| --------------- | ----------- | ------ |
| SQL Query | Landmark Transaction | Use business class queries |
| SQL Transaction | Landmark Transaction | Use business class operations |
| JMS | ION Integration | Use ION messaging |
| Custom Activity | Assign with JavaScript | Use JavaScript for custom logic |
| Data Transformation | Assign with JavaScript | Use JavaScript for transformations |
| WebSphere MQ | ION Integration | Use ION messaging |

### Control Activity Nodes

- **Assign (ASSGN)**: Variable assignment, JavaScript execution
- **Branch (BRANCH)**: Conditional logic, flow control
- **SubProcess (SUBPROC)**: Call other processes
- **Return**: Return from subprocess
- **Wait (Timer)**: Time-based delays, scheduling
- **Trigger**: Trigger other processes

### Data Activity Nodes

- **Data Iterator**: Loop through data sets
- **File Access (ACCFIL)**: Read/write/delete files in FSM File Storage
- **For Each**: XML element iteration
- **FTP (FileTransfer)**: File transfer with SFTP servers
- **IDM**: Infor Document Management (see `08_Infor_IDM_Guide.md`)
- **LDAP Query**: LDAP server queries
- **JSON Parser (JSONPARSER)**: JSON parsing

### Communication Activity Nodes

- **Email (EMAIL)**: Send email notifications
- **SMS**: Send SMS messages
- **ION Outbox**: Send ION BODs
- **ION Notification**: ION notifications
- **ION Alert**: ION alerts with escalation

### Integration Activity Nodes

- **Landmark Transaction (LM)**: FSM/GHR business class operations
- **WebRun (WEBRN)**: HTTP REST calls, OAuth2, Compass API
- **Web Service**: SOAP web service calls
- **M3 Transaction**: Infor M3 integration

## File Operations Architecture

### CRITICAL: File Access vs FTP Nodes

**Two Separate Systems - Cannot Interoperate Directly**:

1. **FSM File Storage** (Cloud Storage)
   - Location: Process Server Administrator > Configuration > File Storage
   - AWS-based cloud storage for FSM multi-tenant ERP
   - Accessible ONLY by ACCFIL (File Access) nodes
   - NOT accessible by FTP nodes

2. **SFTP Servers** (External File Servers)
   - External file transfer servers
   - Accessible ONLY by FTP nodes
   - NOT accessible by ACCFIL nodes

### File Access Node (ACCFIL)

**Purpose**: Read/write/delete files in FSM File Storage ONLY

- **Operations**: Read, Write, Append, Delete, List, Check Exists
- **Encoding**: UTF-8, ASCII, custom encodings
- **Wildcard Support**: `*` wildcards (e.g., `Invoice_*.csv`)
  - Source wildcard → destination must be folder
  - Destination folder must exist
- **Error Handling**: File not found, permission errors

### FTP Node (FileTransfer)

**Purpose**: Transfer files with SFTP servers ONLY

- **Operations**: Get (download), Put (upload), Delete, List
- **Protocols**: FTP, FTPS, SFTP
- **Authentication**: Username/password, SSH keys
- **Wildcard Support**: `*` wildcards for pattern matching
- **Transfer Modes**: Auto, ASCII, Binary

### Integration Patterns

#### Pattern 1: File Channel (Automatic)

```text
SFTP → File Channel → FSM File Storage → ACCFIL → FSM File Storage → File Channel → SFTP
```

#### Pattern 2: FTP + ACCFIL (Manual)

```text
SFTP → FTP (Get) → FSM File Storage → ACCFIL → FSM File Storage → FTP (Put) → SFTP
```

#### Pattern 3: ACCFIL Only (Internal)

```text
FSM File Storage → ACCFIL → FSM File Storage
```

### Common Mistakes to Avoid

When working with file operations:

- ❌ "ACCFIL reads from SFTP" → ✅ "ACCFIL reads from FSM File Storage (File Channel transferred from SFTP)"
- ❌ "FTP node reads from File Storage" → ✅ "FTP node reads from SFTP server and transfers to File Storage"

## Data Access Architecture

### Compass API vs Landmark Nodes

| Use Case | Approach | Activity Type | Reason |
| -------- | -------- | ------------- | ------ |
| GL Data Extraction | Compass API | WEBRN | Large datasets, pagination |
| Match Reports | Compass API | WEBRN | Batch processing, external integration |
| Financial Exports | Compass API | WEBRN | Data Lake optimized for reporting |
| Approval Workflows | Landmark Nodes | LM | Real-time data, transactional integrity |
| Single Record Operations | Landmark Nodes | LM | Direct database access |
| Business Class Actions | Landmark Nodes | LM | Native FSM operations |

**Compass API (WEBRN) Pattern**:

- Queries Infor Data Lake (replicated data)
- OAuth2 authentication via ION API
- Asynchronous query with polling
- Built-in pagination for large datasets
- Production sample: `MatchReport_Outbound.lpd`

**Landmark Node (LM) Pattern**:

- Direct FSM database access
- Synchronous execution
- Real-time data
- Native business class structure
- Production sample: `jeapproval.lpd`

## Variables and JavaScript

### Variable Types

- **Process Variables**: Available throughout process
- **Activity Variables**: Node-specific output variables
- **Global Variables**: System-wide configuration
- **Configuration Variables**: Environment-specific settings

### JavaScript Integration

**ES5 Compliance (Mozilla Rhino 1.7R4)**:

- ✅ Use: `var`, traditional functions, `function() {}` syntax
- ❌ Avoid: `let`, `const`, arrow functions `=>`, template literals
- Variable Access: `<!variableName>` syntax in XML
- Built-in Functions: Date, string, numeric functions
- Expression Builder: GUI-based expression creation

### Special Functions

- **Formatting**: `formatNumber()`, `formatDate()`
- **Translation**: Multi-language support
- **Logging**: Custom logging capabilities
- **Lookup**: xref table integration

## Error Handling

### Error Handling Options

- **Stop Process**: Immediate termination
- **Continue Process**: Continue with error logging
- **Go to Error Handler**: Branch to error handling logic

### Error Connector

- **Built-in Error Handling**: Available on most nodes
- **Custom Error Logic**: Branch to specific error handling
- **Notification**: Email alerts on errors
- **Custom Logging**: Additional error information

### Debugging Features

- **Breakpoints**: Normal and "run to" breakpoints
- **Process Controls**: Start, stop, pause, resume, step
- **Variable Examination**: Runtime variable inspection
- **Variable Modification**: Change values during debugging
- **My Workunits**: Track process executions

## Auto-Restart Design

### When to Enable Auto-Restart

- **Enable**: Batch data loads, interface processes, orchestration, report generation
- **Disable**: Approval workflows, financial transactions, audit-sensitive operations, single-execution requirements

### Restartable Flow Design

- **Enable Auto-Restart**: Process Properties → Auto Restart = Enabled
- **Idempotent Operations**: Same input = same output
- **State Persistence**: Use PfiWorkunitVariable for state
- **Checkpoint Logic**: Track completion status

### Activity Node Restart Patterns

| Activity Type | Restart Approach | Implementation |
| ------------- | ---------------- | -------------- |
| File Access (Write) | Undo or bypass | Check for existing files |
| Email/SMS | Bypass | Avoid resending |
| Transaction (LM) | Undo or bypass | Implement rollback logic |
| File Access (Read) | Save content or re-query | Persist data |
| WebRun Query | Bypass or save data | Cache results |

### Design Patterns

- **Query-Create Pattern**: Query first, create only if not exists
- **Query-Update Pattern**: Query first, update only if values differ
- **Checkpoint Pattern**: Use PfiWorkunitVariable before key activities
- **Duplicate Error Handling**: Clean up duplicate errors post-restart

## ION Integration

### ION Outbox

- **BOD Sending**: Send Business Object Documents
- **Message Properties**: Priority, Tenant ID, Document ID
- **Batch Processing**: Batch ID, sequence, size management
- **XML Message**: Typically from XML node output

### ION Inbox Query/Update

- **Query Filters**: Status, BOD Type, Logical ID combinations
- **Status Updates**: Change inbox record status
- **Iterative Processing**: Loop through inbox records

### ION Notifications/Alerts

- **Notification**: Simple user/task notifications
- **Alert**: Notifications with escalation capability
- **Recipients**: Tasks and users (CSV lists supported)
- **Detail Builders**: Tree structure for complex data

## Landmark and Web Service Integration

### Landmark Integration

- **Business Class Operations**: Create, Update, Delete, Query
- **Configuration Names**: "main" configuration standard
- **Transaction Types**: SingleRecordQuery, MultipleRecordQuery, CreateUpdateDelete
- **Field Selection**: Specify fields to retrieve/update
- **Error Handling**: Built-in Landmark error processing

### Web Service Integration

- **SOAP Support**: Full SOAP 1.1/1.2 support
- **Authentication**: Basic, WS-Security, custom headers
- **Error Handling**: SOAP fault processing
- **Response Processing**: XML response parsing

## Performance Best Practices

### Node Optimization

- **Minimize Nodes**: Fewer nodes = better performance
- **Combine Operations**: Use single Assign vs multiple nodes
- **JavaScript Efficiency**: Optimize script code
- **Database Relations**: Use joins vs multiple queries

### Data Processing

- **Avoid Repetitive File Writes**: Use Message Builder in loops
- **Memory Management**: Keep SQL variables private
- **Page Size Optimization**: Optimal query page sizes (≤30)
- **Bulk Operations**: Use native tools for large data extracts
- **Timestamp Filtering**: Incremental data processing
- **Query Performance**: Maintain under 100ms for paginated operations

## FSM Security and Access

### Required Roles for Work Unit Access

- **Work Unit Administrator**: Access to work unit search and download
- **Process Administrator**: View and manage IPA processes
- **System Administrator**: Full system access (if needed)

### Common New Account Issues

- **Element Not Found Error**: Insufficient permissions to access work unit search fields
- **Page Layout Differences**: Limited permission accounts see different FSM interfaces
- **Search Field Unavailable**: Work unit search requires proper security roles

### Troubleshooting

1. Verify FSM roles with administrator
2. Test manual work unit page navigation
3. Request "Work Unit Administrator" role minimum
4. Use manual work unit analysis while waiting for role assignment

## S3 to FSM Migration

### Data Access Migration

| S3 Pattern | FSM Equivalent | Notes |
| ---------- | -------------- | ----- |
| AGS Program Calls | Landmark (LM) Activities | Replace S3 program tokens with business class actions |
| Direct Table Queries | Business Class Queries | Replace FILE/INDEX with _objectName/_actionName |
| Resource Manager | FSM Security Context | Use FSM roles and user context |
| Batch Jobs | Scheduled Processes | Replace with FSM scheduled automation |

### Common S3 Programs and FSM Equivalents

- **AR21** (Cash Receipts) → ArPayment business class
- **AR24** (Payment Headers) → ArPaymentHeader business class
- **AR30** (Payment Processing) → ArPaymentProcess business class
- **AR82** (Remittance) → ArRemittance business class
- **GL** programs → GeneralLedger business classes
- **AP** programs → AccountsPayable business classes

### Migration Checklist

- [ ] Replace AGS activities with LM activities
- [ ] Convert S3 table queries to business class queries
- [ ] Update field names from S3 to FSM conventions
- [ ] Replace S3 program tokens with FSM actions
- [ ] Convert Resource Manager queries to FSM security calls
- [ ] Update error handling from S3 return codes to FSM patterns
- [ ] Migrate S3 user fields to FSM custom fields
- [ ] Preserve multi-form processing logic
- [ ] Maintain approval hierarchy and escalation
- [ ] Use BRANCH edges from UA and BRANCH activities
- [ ] ItEnd nodes are auto-generated (no manual action needed)
- [ ] Include configurationName="main" for LM activities
- [ ] Proper URL encoding for all JavaScript/error logs
- [ ] Verify FSM security roles for work unit access

## Activity Class Name Reference

### Complete Activity Type to Class Name Mapping

| Activity Type | Java Class Name | Description |
| ------------- | --------------- | ----------- |
| START | com.lawson.bpm.processflow.workFlow.flowGraph.FgaStart | Process entry point |
| END | com.lawson.bpm.processflow.workFlow.flowGraph.FgaEnd | Process exit point |
| ASSGN | com.lawson.bpm.processflow.workFlow.flowGraph.FgaAssign | Variable assignment, JavaScript |
| BRANCH | com.lawson.bpm.processflow.workFlow.flowGraph.FgaBranch | Conditional routing |
| WEBRN | com.lawson.bpm.processflow.workFlow.flowGraph.FgaCgiRun | HTTP/REST API calls |
| LM | com.lawson.bpm.processflow.workFlow.flowGraph.FgaLandmark | Landmark business class operations |
| ACCFIL | com.lawson.bpm.processflow.workFlow.flowGraph.FgaFileAccess | File read/write/delete |
| FileTransfer | com.lawson.bpm.processflow.workFlow.flowGraph.FgaFtp | FTP/SFTP transfers |
| Timer | com.lawson.bpm.processflow.workFlow.flowGraph.FgaTimer | Wait/delay operations |
| SUBPROC | com.lawson.bpm.processflow.workFlow.flowGraph.FgaSubProcess | Subprocess invocation |
| UA | com.lawson.bpm.processflow.workFlow.flowGraph.FgaUserAction | User action/approval |
| JSONPARSER | com.lawson.bpm.processflow.workFlow.flowGraph.FgaJSONParser | JSON parsing |
| ItEnd | com.lawson.bpm.processflow.workFlow.flowGraph.FgaIterEnd | Iterator end (auto-generated with LM) |
| EMAIL | com.lawson.bpm.processflow.workFlow.flowGraph.FgaEmail | Email sending |
| MsgBuilder | com.lawson.bpm.processflow.workFlow.flowGraph.FgaMsgBuilder | Message builder |

### Production-Verified WEBRN Patterns

### OAuth2 Token Acquisition Pattern

**Activity Configuration**:

```xml
<activity activityType="WEBRN" caption="GetAccessToken" className="com.lawson.bpm.processflow.workFlow.flowGraph.FgaCgiRun">
    <prop className="java.lang.String" name="callTypeString" propType="SIMPLE">
        <anyData><![CDATA[Standard+HTTP+Call]]></anyData>
    </prop>
    <prop className="java.lang.String" name="headerString" propType="SIMPLE">
        <anyData><![CDATA[Content-Type%3A+application%2Fx-www-form-urlencoded%0D%0Aaccept%3A+application%2Fjson]]></anyData>
    </prop>
    <prop className="java.lang.String" name="method" propType="SIMPLE">
        <anyData><![CDATA[POST]]></anyData>
    </prop>
    <prop className="java.lang.Boolean" name="externalCall" propType="SIMPLE">
        <anyData><![CDATA[true]]></anyData>
    </prop>
</activity>
```

**OAuth Request Body Construction (JavaScript)**:

```javascript
// Parse .ionapi credentials
var ionapi = JSON.parse(ionapiContent);
var ti = ionapi.ti;           // Tenant ID
var ci = ionapi.ci;           // Client ID
var cs = ionapi.cs;           // Client Secret
var saak = ionapi.saak;       // Service Account Access Key
var sask = ionapi.sask;       // Service Account Secret Key

// Build OAuth request (note: # must be URL-encoded as %23)
req = "username=" + ti + "%23" + saak + "&password=" + sask + 
      "&client_id=" + ci + "&client_secret=" + cs + "&grant_type=password";
```

**Key Implementation Notes**:

- Always URL-encode special characters (`#` → `%23`)
- Store credentials in .ionapi files (never hardcode)
- Use externalCall=true for external OAuth endpoints

### Compass API Query Pattern

**Three-Step Asynchronous Pattern**:

1. **Submit Query** (POST)
2. **Poll Status** (GET with polling loop)
3. **Retrieve Results** (GET with pagination)

**Step 1: Submit Query**:

```xml
<activity activityType="WEBRN" caption="InitQuery">
    <prop className="java.lang.String" name="headerString" propType="SIMPLE">
        <anyData><![CDATA[%3C%21auth%3E%0D%0AContent-Type%3A+application%2Fjson]]></anyData>
    </prop>
    <prop className="java.lang.String" name="programName" propType="SIMPLE">
        <anyData><![CDATA[%3C%21Tenant%3E%2FDATAFABRIC%2Fcompass%2Fv2%2Fjobs%2F]]></anyData>
    </prop>
    <prop className="java.lang.String" name="method" propType="SIMPLE">
        <anyData><![CDATA[POST]]></anyData>
    </prop>
</activity>
```

**Step 2: Poll Status**:

```xml
<activity activityType="WEBRN" caption="GetStatus">
    <prop className="java.lang.String" name="programName" propType="SIMPLE">
        <anyData><![CDATA[%3C%21Tenant%3E%2FDATAFABRIC%2Fcompass%2Fv2%2Fjobs%2F%3C%21queryID%3E%2Fstatus]]></anyData>
    </prop>
    <prop className="java.lang.String" name="method" propType="SIMPLE">
        <anyData><![CDATA[GET]]></anyData>
    </prop>
</activity>
```

**Step 3: Get Results (CSV format)**:

```xml
<activity activityType="WEBRN" caption="GetResult">
    <prop className="java.lang.String" name="headerString" propType="SIMPLE">
        <anyData><![CDATA[%3C%21auth%3E%0D%0AAccept%3A+text%2Fcsv]]></anyData>
    </prop>
    <prop className="java.lang.String" name="programName" propType="SIMPLE">
        <anyData><![CDATA[%3C%21Tenant%3E%2FDATAFABRIC%2Fcompass%2Fv2%2Fjobs%2F%3C%21queryID%3E%2Fresult%3Flimit%3D%3C%21limit%3E%26offset%3D%3C%21offset%3E]]></anyData>
    </prop>
</activity>
```

**Key Implementation Notes**:

- Use Timer node between status polls (avoid tight loops)
- Parse queryID from InitQuery response
- Implement pagination with limit/offset parameters
- Accept header determines format (text/csv or application/json)
- Production example: `MatchReport_Outbound.lpd`

### Production-Verified FileTransfer Pattern

**SFTP Upload Configuration**:

```xml
<activity activityType="FileTransfer" caption="UploadToSFTP" className="com.lawson.bpm.processflow.workFlow.flowGraph.FgaFtp">
    <prop className="java.lang.String" name="targetConfigurationName" propType="SIMPLE">
        <anyData><![CDATA[Interface]]></anyData>
    </prop>
    <prop className="java.lang.String" name="SourceFile" propType="SIMPLE">
        <anyData><![CDATA[%3C%21LocalDirectory%3E%2F%3C%21FileName%3E]]></anyData>
    </prop>
    <prop className="java.lang.String" name="TargetFile" propType="SIMPLE">
        <anyData><![CDATA[%3C%21RemoteDirectory%3E%2F%3C%21FileName%3E]]></anyData>
    </prop>
    <prop className="java.lang.Boolean" name="RemoteSource" propType="SIMPLE">
        <anyData><![CDATA[false]]></anyData>
    </prop>
    <prop className="java.lang.Boolean" name="RemoteTarget" propType="SIMPLE">
        <anyData><![CDATA[true]]></anyData>
    </prop>
    <prop className="java.lang.String" name="transfermode" propType="SIMPLE">
        <anyData><![CDATA[Ascii]]></anyData>
    </prop>
</activity>
```

**Key Configuration Notes**:

- `RemoteSource=false, RemoteTarget=true` → Upload (FSM to SFTP)
- `RemoteSource=true, RemoteTarget=false` → Download (SFTP to FSM)
- `targetConfigurationName` references SFTP connection in FSM
- Transfer mode: Ascii (text files) or Binary (all other files)

## LPD File Creation Checklist

When creating or analyzing LPD files, verify:

- [ ] **Correct activity class names** from Activity Class Name Reference table
- [ ] **URL-encoded content** in all JavaScript and text properties
- [ ] **Proper edge types**: NORMAL (default flow), BRANCH (conditional), ERROR (error handling)
- [ ] **LM activities paired with ItEnd** - IPD auto-generates ItEnd nodes for iterators
- [ ] **OnActivityError sections** with proper error logging on all critical nodes
- [ ] **Configuration references** for environment-specific settings (not hardcoded values)
- [ ] **IPD validation** - test in IPD before deployment
- [ ] **Production sample comparison** - verify format matches existing patterns

### Common LPD Issues

- Missing URL encoding in JavaScript (breaks XML parsing)
- Hardcoded values instead of configuration variables
- Missing error handlers on critical nodes
- Incorrect edge types (using NORMAL instead of BRANCH)
- Manual ItEnd creation (let IPD auto-generate)

## Best Practices Summary

### Design Principles

When designing IPA processes:

1. **Minimize Complexity**: Fewer nodes = better performance and maintainability
2. **Maximize Reusability**: Use subprocess patterns and configuration variables
3. **Optimize Performance**: Efficient data processing, minimal I/O operations
4. **Enable Restart**: Design idempotent operations with state management
5. **Comprehensive Error Handling**: Implement graceful failure recovery
6. **Security First**: Use secure configurations and proper access controls
7. **Maintainable Code**: Clear naming conventions and inline documentation
8. **Testing Strategy**: Local IPD debugging before server deployment

### Restart Design Guidelines

For processes with auto-restart enabled:

1. **Data Generation Activities**: Use Undo (delete created records) or Bypass (check if exists) approaches
2. **Data Consumption Activities**: Use Save Data (persist to variables) or Re-run (idempotent queries) approaches
3. **State Management**: Use PfiWorkunitVariable to track completion status
4. **Error Recovery**: Implement duplicate error cleanup logic
5. **Checkpoint Logic**: Track process completion at key milestones
6. **Testing**: Extensively test restart scenarios before production

## FSM Navigation

### Key FSM Areas

| Area | Purpose | Navigation |
| ---- | ------- | ---------- |
| IPA Designer | View deployed IPAs, scheduling, triggers | Application Menu → IPA |
| Business Classes | View Landmark business class definitions | Application Menu → Business Class |
| Work Units | Monitor IPA execution, view logs | Application Menu → Work Units |
| XREF Tables | Cross-reference configurations | Application Menu → XREF |
| Global Configurations | System-wide settings | Application Menu → Configuration |
| Approval Setup | Approval matrix, routing rules | Application Menu → Approval |
| Process Definitions | Manage deployed IPAs, version control | Configuration > Process Definitions |
| Process Scheduling | Configure IPA triggers and schedules | Scheduling > By Process Definition |

### Process Management Workflow

1. Upload IPA from IPD → appears in User Defined Processes
2. Create Process Trigger (unscheduled)
3. Schedule Trigger (set timing)
4. Monitor Work Units for execution results

**Comprehensive Guide**: See `09_FSM_Navigation_Guide.md` for detailed FSM navigation patterns, authentication methods, browser automation best practices, and troubleshooting.

## S3 Legacy Activity Types

### S3-Only Activity Types (Deprecated in FSM)

- **AGS**: Application Gateway Server calls to S3 programs
- **QUERY**: Direct S3 table queries with field-level access
- **RMQR**: Resource Manager queries for user/role information
- **BATCH**: S3 batch job execution and monitoring
- **DME**: Data Movement Engine calls for S3 data operations

### S3 AGS Call Structure Example

**Typical S3 AGS Activity Configuration**:

```xml
<activity activityType="AGS" className="com.lawson.bpm.processflow.workFlow.flowGraph.FgaAgs">
    <prop name="queryString">
        _PDL=<!appProdline>&           <!-- Product Line -->
        _TKN=AR21.3&                  <!-- S3 Program Token -->
        _EVT=CHG&                     <!-- Event Type -->
        _RTN=DATA&                    <!-- Return Type -->
        _LFN=ALL&                     <!-- Lawson Function -->
        _TDS=IGNORE&                  <!-- Transaction Data Set -->
        FC=Release&                   <!-- Function Code -->
        APM-COMPANY=<!Company>&       <!-- S3 Field Parameters -->
        _DELIM=%09&                   <!-- Delimiter -->
        _OUT=XML&                     <!-- Output Format -->
        _EOT=TRUE                     <!-- End of Transaction -->
    </prop>
</activity>
```

**Key Parameters**:

- `_TKN`: S3 program token (e.g., AR21.3 for Cash Receipts)
- `_EVT`: Event type (CHG=Change, ADD=Add, DEL=Delete)
- `_RTN`: Return type (DATA=data response, NONE=no response)
- Field parameters use S3 field names (e.g., APM-COMPANY)

### S3 Table Query Structure Example

**Typical S3 QUERY Activity Configuration**:

```xml
<activity activityType="QUERY" className="com.lawson.bpm.processflow.workFlow.flowGraph.FgaProcessQuery">
    <prop name="queryString">
        PROD=<!appProdline>&          <!-- Product Line -->
        FILE=ARPAYMENT&               <!-- S3 Table Name -->
        INDEX=APMSET1&                <!-- S3 Index -->
        KEY=<!Company>=<!Batch_Nbr>&  <!-- Key Fields -->
        FIELD=TRANS-NBR;TRANS-TYPE&   <!-- Selected Fields -->
        OUT=CSV&                      <!-- Output Format -->
        DELIM=~                       <!-- Field Delimiter -->
    </prop>
</activity>
```

**Key Parameters**:

- `FILE`: S3 table name (e.g., ARPAYMENT, APVENDOR)
- `INDEX`: S3 index for query optimization
- `KEY`: Key field values for filtering (semicolon-separated)
- `FIELD`: Fields to retrieve (semicolon-separated)
- `OUT`: Output format (CSV, XML, or TAB)

### S3 Resource Manager Query Example

**Typical S3 RMQR Activity Configuration**:

```xml
<activity activityType="RMQR" className="com.lawson.bpm.processflow.workFlow.flowGraph.FgaResourceQuery">
    <prop name="rmQueryStr">
        <?xml version="1.0"?>
        <TRANSACTION user="pfuser" method="getRMQuery">
            <OBJECT><![CDATA[People]]></OBJECT>
            <ATTRIBUTES>
                <ATTRIBUTE><![CDATA[Email]]></ATTRIBUTE>
                <ATTRIBUTE><![CDATA[FirstName]]></ATTRIBUTE>
            </ATTRIBUTES>
            <WHERE><![CDATA[({ID}=<!_user>)]]></WHERE>
        </TRANSACTION>
    </prop>
</activity>
```

**Key Parameters**:

- `OBJECT`: Resource type (People, Roles, Groups)
- `ATTRIBUTES`: Fields to retrieve from resource
- `WHERE`: Filter criteria using S3 Resource Manager syntax

**FSM Migration Note**: FSM uses built-in user context instead of RMQR queries. Remove RMQR activities and use FSM security context variables.

### S3 IPA Conversion Example (prd003_ar_approv.lpd)

**Original S3 Features**:

- Multi-Form Support: AR21, AR24, AR82 form-specific processing
- Two-Level Approval: Agency → Treasury approval with escalation
- Cash Code Routing: Bypass logic for codes 9999, 7777, 2320, 2340
- Direct S3 Integration: AGS calls and table queries
- Error Recovery: Release failure detection and notification

**FSM Conversion Strategy**:

1. **Replace AGS Activities**: Convert S3 program calls to FSM business class actions
   - S3 AGS AR21.3 → FSM LM ArPayment.Approve
2. **Convert Table Queries**: Replace QUERY activities with LM business class queries
   - S3 QUERY ARPAYMENT → FSM LM ArPayment.Find
3. **Update User Actions**: Maintain approval structure but use FSM security context
   - Remove RMQR activities (FSM uses built-in user context)
4. **Preserve Business Logic**: Keep cash code routing and form-specific processing
5. **Modernize Error Handling**: Use FSM error patterns instead of S3 return codes

**Proven Conversion Pattern** (prd003_ar_approv_FSM.lpd):

- ✅ Preserved: Multi-form branching, cash code bypass, two-level approval
- ✅ IPD Compatible: Proper edge types (BRANCH from UA activities), LM+ItEnd pairing (auto-generated)
- ✅ Production-Ready: Tested conversion pattern for S3 to FSM migration

---

This comprehensive guide combines IPA concepts with complete IPD implementation knowledge, enabling creation of sophisticated, production-ready IPA processes with full understanding of all available capabilities, best practices, and optimization techniques.
