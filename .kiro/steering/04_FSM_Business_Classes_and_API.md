---
inclusion: auto
name: fsm-business-classes
description: FSM business classes, Landmark operations, REST API integration, GL/AP/AR processes, RICE methodology, LPL configuration, WebRun activities, GLTransactionInterface, GeneralLedgerTransaction, UBC. Use when working with FSM business classes or Landmark API operations.
---

# FSM Business Classes and API Guide

## Table of Contents

- [Quick Reference](#quick-reference)
  - [Quick Decision Guide](#quick-decision-guide)
- [RICE Methodology](#rice-methodology)
  - [RICE Types](#rice-types)
  - [RICE Tracking](#rice-tracking)
- [IPA vs LPL Decision Tree](#ipa-vs-lpl-decision-tree)
  - [Decision Matrix](#decision-matrix)
- [FSM Business Classes](#fsm-business-classes)
  - [GL Business Classes (Core)](#gl-business-classes-core)
  - [Data Flow](#data-flow)
  - [Common Business Classes by Module](#common-business-classes-by-module)
  - [User Business Classes (UBCs)](#user-business-classes-ubcs)
- [API Integration Patterns](#api-integration-patterns)
  - [Documentation Reference](#documentation-reference)
  - [Required Context Fields](#required-context-fields)
  - [Landmark Web Services](#landmark-web-services)
  - [IPA Integration](#ipa-integration)
  - [InterfaceTransactions Action](#interfacetransactions-action)
  - [Authentication](#authentication)
- [Common Patterns](#common-patterns)
  - [Financial Dimensions](#financial-dimensions)
  - [Multi-Currency Support](#multi-currency-support)
  - [Status Value Patterns](#status-value-patterns)
- [Best Practices](#best-practices)
  - [Performance](#performance)
  - [Data Validation](#data-validation)
  - [Error Handling](#error-handling)
  - [Security](#security)
  - [IPA Development](#ipa-development)
- [Troubleshooting](#troubleshooting)
  - [Common API Errors](#common-api-errors)
  - [Debugging Strategies](#debugging-strategies)
  - [Accessing WorkUnit Data](#accessing-workunit-data)

## Quick Reference

**FSM (Financials & Supply Management)**: Infor's ERP suite built on Landmark platform with 450-550 business classes exposed as REST APIs.

**Key Concepts**:

- **Business Class**: Metadata-driven entity representing data/logic (e.g., `GLTransactionInterface`, `Vendor`, `PurchaseOrder`)
- **Landmark Activity**: IPA node for FSM API calls using transaction string syntax
- **WebRun Activity**: IPA node for REST API calls with JSON payloads
- **UBC**: User Business Class - custom business objects

**Environment Context**:

- Typical deployment: 450-550 business classes (excludes GHR unless deployed)
- Modules: GL, AP, AR, PO, IC, AM, CB, TR, Budgeting, Contracts, Projects
- Authentication: Bearer token from ION API or Mingle SSO

**AI Assistant Guidelines**:

- When user mentions "Landmark activity" or "LM node", use transaction string syntax (ampersand-separated)
- When user mentions "WebRun" or "REST API", use JSON payload format
- Always validate required context fields before generating API calls
- Check business class module to determine correct `_module` parameter (gl, ap, ar, po, etc.)

### Quick Decision Guide

**Choose Landmark Activity when**:

- User explicitly requests "Landmark activity" or "LM node"
- Simple CRUD operations on single business class
- Transaction string syntax preferred
- Legacy IPA processes use this pattern

**Choose WebRun Activity when**:

- User explicitly requests "WebRun" or "REST API"
- Complex JSON payloads required
- Multiple records in single API call
- Need to parse detailed JSON responses
- OAuth2 authentication required

**Module Mapping** (for `_module` parameter):

- GL transactions → `_module="gl"`
- AP invoices/vendors → `_module="ap"`
- AR invoices/customers → `_module="ar"`
- Purchase orders → `_module="po"`
- Inventory → `_module="ic"`
- Assets → `_module="am"`
- Cash/Treasury → `_module="cb"` or `_module="tr"`

---

## RICE Methodology

**RICE** = Reports, Interfaces, Conversions, Enhancements

### RICE Types

| Type | Description | Typical Solution |
| --- | --- | --- |
| **R**eport | Data outputs for decision-making | IPA + File generation |
| **I**nterface | Data exchange with external systems | IPA + REST/SOAP APIs |
| **C**onversion | Legacy data migration | IPA + Batch processing |
| **E**nhancement | Custom functionality | IPA + LPL configuration |

### RICE Tracking

- Unique ID: e.g., "RICE-040", "FPI-ANA-050-MATCH-REPORT"
- Documents: ANA-050 (requirements), DES-020 (technical design)
- Specification documents can be analyzed using document analysis tools in ReusableTools/

## IPA vs LPL Decision Tree

**Critical Rule**: Not all RICE items need IPA. Use this decision tree:

```text
Does requirement involve...
├─ Data exchange with external system? → IPA Required ✅
├─ Scheduled/automated processing? → IPA Required ✅
├─ File processing (inbound/outbound)? → IPA Required ✅
├─ Multi-step workflow with approvals? → IPA Required ✅
├─ API calls (Compass, REST, SOAP)? → IPA Required ✅
└─ UI changes only (forms, fields, menus)? → LPL Only ❌ No IPA
```

**IPA Creates Workunits**: When IPA executes, a workunit is created in Process Server Administrator.

**LPL-Only (No Workunit)**:

- Form/list modifications
- New fields on business classes
- Field protection, defaults, visibility
- Menu items and navigation
- Security class configuration

### Decision Matrix

| Requirement | IPA | LPL | Workunit |
| --- | --- | --- | --- |
| External system integration | ✅ | ❌ | ✅ |
| Scheduled data extract | ✅ | ❌ | ✅ |
| Approval workflow | ✅ | Maybe | ✅ |
| UI form modification | ❌ | ✅ | ❌ |
| New business class field | ❌ | ✅ | ❌ |
| Menu/navigation change | ❌ | ✅ | ❌ |
| File-triggered process | ✅ | ❌ | ✅ |
| LPL action → IPA trigger | ✅ | ✅ | ✅ |

---

## FSM Business Classes

### GL Business Classes (Core)

#### 1. GLTransactionInterface (Staging)

**Purpose**: Temporary staging for GL transactions during validation

**Key Fields**:

- `RunGroup` + `SequenceNumber`: Batch identifier
- `Status`: 0=Unreleased, 1=Released, 2=Posted, 3=Error
- `AccountingEntity`, `AccountCode`, `PostingDate`

**Common Operations**:

- `Create`: Add staging records
- `PurgeUnreleased`: Clean up unreleased data
- `UpdateErrorBudgetEdit`: Update budget validation errors
- `InterfaceTransactions`: Validate and post to GL

**API Pattern**:

```javascript
// Landmark Activity (Transaction String Syntax)
_dataArea="FSM" & _module="gl" & 
_objectName="GLTransactionInterface" &
_actionName="Create" & _actionType="CreateUpdateDelete" &
FinanceEnterpriseGroup="FEG01" & 
GLTransactionInterface.RunGroup="BATCH001" &
AccountingEntity="1000" & AccountCode="1010-000" &
PostingDate="20260116" & TransactionAmount="1000.00"
```

**Implementation Notes**:

- Use `RunGroup` to batch related transactions for atomic processing
- Always include `FinanceEnterpriseGroup` and `AccountingEntity` (required context)
- Date format MUST be `YYYYMMDD` (no dashes, slashes, or other separators)
- After creating staging records, call `InterfaceTransactions` action to validate and post

#### 2. GeneralLedgerTransaction (Posted GL)

**Purpose**: Actual posted GL transactions with journal control

**Key Fields**:

- `GeneralLedgerJournalControl`: Journal header reference
- `Status`: 0=Unreleased, 1=Released, 6=Posted, 7=Approved, 8=Rejected, 9=Suspended

**Common Operations**:

- `UpdateUnreleased/UpdateReleased`: Modify transactions
- `ReleaseUnreleased`: Release for posting
- `ManualApprove/ManualReject`: Approval workflow
- `CreateAmortization`: Create amortization entries

**Implementation Notes**:

- Status 6 (Posted) means transaction is in GL and cannot be modified
- Use `UpdateUnreleased` for Status=0, `UpdateReleased` for Status=1
- Approval workflow: Unreleased → Released → Approved (7) → Posted (6)

#### 3. GLTransactionDetail (Detail Records)

**Purpose**: Comprehensive transaction details with project/labor data

**Key Fields**:

- `Status`: 0=Unreleased, 1=Released, 8=NotToBePosted, 9=OnHold
- `Billed`: 0=NotBilled, 1=Billed, 3=PartiallyBilled
- `RevenueRecognized`: 0=NotRecognized, 1=Recognized, 2=PartiallyRecognized

**Common Operations**:

- `TransferIndividualTransaction/TransferMultipleTransactions`
- `PutOnHold/RemoveFromHold`: Billing, Revenue, Capitalization holds
- `UpdateBilledStatus/UpdateRecognizedStatus`

**Implementation Notes**:

- Use this class for project accounting and labor distribution
- Hold types: Billing (prevent invoicing), Revenue (defer recognition), Capitalization (asset tracking)
- Status 8 (NotToBePosted) excludes from GL posting but retains for reporting

### Data Flow

```text
Source Systems
    ↓
GLTransactionInterface (Staging - Validation)
    ↓
GeneralLedgerTransaction (Posted GL)
    ↓
GLTransactionDetail (Operational Details)
    ↓
GeneralLedgerJournalControl (Journal Headers)
    ↓
GeneralLedgerTotal (Aggregated Totals)
```

### Common Business Classes by Module

| Module | Business Classes |
| --- | --- |
| GL | `Ledger`, `JournalEntry`, `GLTransactionInterface`, `GLAccount` |
| AP | `Vendor`, `APInvoice`, `APDistribution`, `APPayment` |
| AR | `Customer`, `ARInvoice`, `ARReceipt`, `ARDistribution` |
| PO | `Requisition`, `PurchaseOrder`, `POReceipt`, `POLine` |
| IC | `StockLocation`, `ItemLocation`, `InventoryCount`, `Item` |
| AM | `Asset`, `AssetBook`, `AssetType`, `AssetDepreciation` |
| CB/TR | `CashCode`, `BankTransaction`, `CashAccount`, `BankReconciliation` |
| Projects | `Project`, `ProjectLine`, `ProjectResource`, `ProjectBilling` |
| System | `Actor`, `WorkUnit`, `SecurityClass`, `DataArea` |

**Important Note on WorkUnit API**:

- `WorkUnit` business class exists under the **pfi module** (Process Flow Integrator)
- **pfi module APIs are NOT exposed** in the FSM API catalog
- Verified via [FSM API Catalog](https://developer.infor.com/hub/apicatalog?&tag=FSM) - search returns 0 results
- WorkUnit data must be accessed through alternative methods (see Troubleshooting section)

### User Business Classes (UBCs)

**Purpose**: Custom business objects for client-specific requirements

**When to Create**:

- Model business-specific logic not in standard FSM
- Add custom fields and relationships
- Integrate with FSM workflows and IPA
- Automatically exposed as REST endpoints

**Creation Steps**:

1. Landmark Rich Client → Configuration Console → Business Class → Create UBC
2. Define: Fields, Keys, Indexes, Relationships, Validation
3. Deploy and verify via Swagger
4. Secure via role-based security

**Naming Convention**: Prefix with `Z` or company code (e.g., `ZCustomerProfile`)

**AI Assistant Guidelines**:

- UBCs follow same API patterns as standard business classes
- Check Swagger documentation for available fields and actions
- UBCs appear in `{url}/soap/classes` endpoint alongside standard classes
- Security must be configured explicitly (not inherited from standard classes)

---

## API Integration Patterns

### Documentation Reference

**Official FSM API Catalog**: [https://developer.infor.com/hub/apicatalog?&tag=FSM](https://developer.infor.com/hub/apicatalog?&tag=FSM)

- 643+ exposed FSM business class APIs
- Searchable catalog with API specifications
- Official source for available FSM APIs
- Use this to verify if a business class API is exposed

**Landmark Web Services Reference Guide**: `D:\Kiro\WorkUnit_Analyzer_ReferenceDocuments\Infor_Landmark_Technology_Web_Services_Reference_Guide.pdf`

**What it covers**:

- REST/JSON and SOAP/WSDL APIs for FSM business classes
- ION API Gateway integration
- Configuration Console for creating defined web services
- Form-based and list-based operations
- OpenAPI documentation configuration
- Page size limits for inbound web services
- Every field of every FSM screen accessible via API

**Key insight**: Every field of every screen in FSM is accessible through the ION API Gateway, including user-defined fields and user-defined business classes.

**AI Assistant Guidelines**:

- Check FSM API Catalog first to verify if a business class API is exposed
- Reference PDF when user asks about specific business class fields or actions
- Use Swagger endpoint (`/IDORequestService/ido/dynamic/api-docs-collection`) for runtime discovery
- Form-based operations use `_FormOperation` suffix in action names
- List-based operations use `_generic` or `_ListOperation` patterns

### Required Context Fields

**GLTransactionInterface**:

```json
{
  "FinanceEnterpriseGroup": "FEG01",
  "GLTransactionInterface": {
    "RunGroup": "BATCH001",
    "SequenceNumber": "1"
  },
  "AccountingEntity": "1000",
  "AccountCode": "1010-000",
  "PostingDate": "20260116"
}
```

**GeneralLedgerTransaction**:

```json
{
  "FinanceEnterpriseGroup": "FEG01",
  "AccountingEntity": "1000",
  "GeneralLedgerClosePeriod": {
    "GeneralLedgerCalendarPeriod": "202601"
  },
  "GeneralLedgerJournalControl": "JC001",
  "GeneralLedgerTransaction": "GT001"
}
```

### Landmark Web Services

#### V2 REST (Recommended)

**URL Pattern**:

```text
{LandmarkURL}/{dataarea}/soap/ldrest/{businessclass}/{operation}?field=value
```

**Example**:

```text
https://server:8080/FSM/fsm/soap/ldrest/GLTransactionInterface/Create?
  FinanceEnterpriseGroup=FEG01&
  GLTransactionInterface.RunGroup=BATCH001&
  AccountingEntity=1000
```

#### Common API Patterns

| Purpose | URL Pattern |
| --- | --- |
| List all classes | `{url}/soap/classes?_links=true` |
| Search classes | `{url}/soap/classes/Item?_links=true` |
| List query | `{url}/soap/classes/Item/lists/_generic?_setName=SymbolicKey&_fields=_all&_limit=20` |
| Find action | `{url}/soap/classes/Item/actions/Find?Item=13&Description=Tape` |

#### Incremental Replication

**Parameters**:

- `_fts` (FromTimeStamp): Extract records changed after (UTC: `YYYYMMDDHHMMSSFF`)
- `_tts` (ToTimeStamp): Extract records changed up to
- `_recordCountOnly=true`: Return count only

### IPA Integration

#### Landmark Activity Node

```xml
<activity activityType="LM" caption="Create GL Transaction">
    <prop name="transactionString">
        _dataArea="FSM" & _module="gl" & 
        _objectName="GLTransactionInterface" &
        _actionName="Create" & _actionType="CreateUpdateDelete" &
        FinanceEnterpriseGroup="<!FEG>" & 
        GLTransactionInterface.RunGroup="<!RunGroup>" &
        AccountingEntity="<!AccountingEntity>" &
        AccountCode="<!AccountCode>" &
        PostingDate="<!PostingDate>" &
        TransactionAmount="<!Amount>"
    </prop>
</activity>
```

**Implementation Notes**:

- Use `<!VariableName>` syntax for IPA variable substitution
- Transaction string uses `&` as field separator (not JSON)
- `_actionType` values: `CreateUpdateDelete`, `Read`, `List`, `Action`
- Always include `_dataArea`, `_module`, `_objectName`, `_actionName`

#### WebRun Activity Node

```javascript
// API endpoint
var apiUrl = Webroot + "/FSM/fsm/soap/classes/GLTransactionInterface";

// JSON payload
var payload = {
    "_records": [{
        "message": "BatchImport",
        "_fields": {
            "FinanceEnterpriseGroup": FEG,
            "GLTransactionInterface.RunGroup": RunGroup,
            "AccountingEntity": AccountingEntity,
            "AccountCode": AccountCode,
            "PostingDate": PostingDate,
            "TransactionAmount": Amount
        }
    }]
};

// Execute API call
var response = webrun(apiUrl, "POST", payload, headers);
```

**Implementation Notes**:

- WebRun uses ES5 JavaScript (no `let`, `const`, arrow functions, template literals)
- `Webroot` is IPA built-in variable containing base Landmark URL
- `message` field: `BatchImport` (create), `BatchUpdate` (update), `BatchDelete` (delete)
- Always parse `response` to check for errors before proceeding
- Headers must include: `Authorization`, `Content-Type: application/json`, `Accept: application/json`

### InterfaceTransactions Action

**REST Endpoint**:

```text
POST /{tenant}/FSM/fsm/soap/ldrest/GLTransactionInterface/
     InterfaceTransactions_InterfaceTransactionsForm_FormOperation
```

**Key Parameters**:

- `PrmRunGroup`: Batch identifier
- `PrmEnterpriseGroup`: Finance enterprise group
- `PrmAccountingEntity`: Entity scope
- `PrmPartialUpdate`: Error handling (true=continue on error, false=stop)
- `PrmJournalizeByEntity`: Entity-based journalization
- `PrmEditOnly`: Validation-only mode (no posting)

**Implementation Notes**:

- This action validates and posts GLTransactionInterface records to GeneralLedgerTransaction
- Use `PrmEditOnly=true` for validation without posting (dry run)
- `PrmPartialUpdate=true` allows batch to continue if some records fail
- Always check response for validation errors before assuming success
- Successful posting changes Status from 0 (Unreleased) to 2 (Posted)

### Authentication

**FSM APIs use OAuth 2.0 Password Grant** for authentication. This is different from external APIs (see `12_External_API_OAuth2_Integration_Guide.md` for Authorization Code Grant).

**CRITICAL SECURITY RULES**:

- **NEVER commit credential files to git** (.gitignore already configured)
- **NEVER log credentials** in work unit logs or console output
- **NEVER hardcode credentials** in IPA processes
- **ALWAYS read from Credentials/ folder** at runtime

**Credential Files Location**: `Credentials/` folder

- `Credentials/.env.fsm` - FSM environment URLs and usernames
- `Credentials/.env.passwords` - User passwords (NEVER commit)
- `Credentials/*.ionapi` - ION API credentials for OAuth2

#### OAuth2 Token Request (Password Grant)

**Endpoint:**

```text
POST https://mingle-sso.inforcloudsuite.com:443/{TENANT}/as/token.oauth2
```

**Parameters:**

```text
grant_type=password
username={TENANT}#{encoded_username}
password={encoded_password}
client_id={TENANT}~{client_id}
client_secret={client_secret}
```

**Credentials Source**: Read from `Credentials/{TENANT}.ionapi` file at runtime

**Example (Postman):**

```text
POST https://mingle-sso.inforcloudsuite.com:443/TAMICS10_AX1/as/token.oauth2
  ?username=TAMICS10_AX1%23VwUpxBIgQak8M3c_YKkg83oO9vxq0yTiHSqXa8rRfFBSFFm0TPsM8NmTQ1ZQPg_YrEqC_cmIgFLAQBZNBnGnjA
  &password=Ya3SGFOD_y8-dsjhKfHlJnU069dpOyun0A40Ry5hJCchxP-SsaNW0qNkQFb9aXO4NZTBnN7ZqJhsZYgIqcnQrA
  &client_id=TAMICS10_AX1~m4wXOfZon75z-FH_7fBcW5yLZg4SHBDwfPCDfTrGuSM
  &client_secret=nruF76-J91cIrriOzg8GI3bsrzqIpWwRMX-H63TpTUmP2eRC8FtjEZF3LeD5ADeseuPQ9628aKHFRJxJ9JyIXA
  &grant_type=password
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "def50200eaa89f99c6b70e6df1fdc37e..."
}
```

**Key Points:**

- Token expires in 3600 seconds (1 hour)
- Username format: `{TENANT}#{encoded_username}`
- Client ID format: `{TENANT}~{client_id}`
- Store credentials securely in FSM config variables (encrypted)

#### Using Bearer Token in API Calls

**Headers:**

```http
Authorization: Bearer {access_token}
Accept: application/json
Content-Type: application/json
```

**Example GET Request:**

```text
GET https://mingle-ionapi.inforcloudsuite.com/TAMICS10_AX1/FSM/fsm/soap/classes/Vendor/lists/_generic
  ?_fields=VendorGroup,VendorClass,Vendor,VendorName,CurrentAddressRel.PostalAddress.Municipality
  &_limit=10
  &_out=JSON
  &_flatten=false

Headers:
  Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
  Accept: application/json
```

**Example POST Request (Batch Create):**

```text
POST https://mingle-ionapi.inforcloudsuite.com/TAMICS10_AX1/FSM/fsm/soap/classes/VendorImport/actions/CreateVendorImport/batch

Headers:
  Authorization: Bearer {access_token}
  Content-Type: application/json

Body:
{
  "_records": [
    {
      "message": "string",
      "_fields": {
        "RunGroup": "TestVendorImport",
        "VendorGroup": "1",
        "VendorClass": "GEN",
        "VendorImport.OldVendor": "TestOldVendor001",
        "VendorName": "TestVendorName001",
        "PostalAddress.Country": "US",
        "PostalAddress.DeliveryAddress.AddressLine1": "AddressLine1 TEST",
        "PostalAddress.Municipality": "Manila",
        "PostalAddress.StateProvince": "NY",
        "PostalAddress.PostalCode": "1234"
      }
    }
  ]
}
```

**Example PUT Request (Update):**

```text
PUT https://mingle-ionapi.inforcloudsuite.com/BAYCAREHS_TRN/FSM/fsm/soap/ldrest/PayablesInvoiceImport/FastUpdate_InvoiceInterface_FormOperation
  ?PayablesInvoiceImport=30558358-6180-cee6-0000-05ed63dde3c0
  &RunGroup=ERROR_EBAPCINV_20230207

Headers:
  Authorization: Bearer {access_token}
  Content-Type: application/json
```

**Example DELETE Request:**

```text
DELETE https://mingle-ionapi.inforcloudsuite.com/HUZ62LQRFQKQDSHJ_PRD/DATAFABRIC/datalake/v2/dataobjects/filter
  ?filter=(dl_document_name eq 'GEO_FSM_GLCOMMIT2') and dl_document_date range [2023-06-26T00:00:00.000Z, 2026-07-18T07:50:06.821Z]
  &includeArchived=true

Headers:
  Authorization: Bearer {access_token}
```

#### Token Management in IPA

**CRITICAL SECURITY RULES**:

- **NEVER commit .ionapi files to git** (.gitignore already configured)
- **NEVER log credentials** in work unit logs
- **NEVER hardcode credentials** in IPA processes
- **ALWAYS read from Credentials/ folder** at runtime

**Credential Files Location**: `Credentials/` folder

- `Credentials/{TENANT}.ionapi` - ION API credentials for OAuth2
- Example: `Credentials/TAMICS10_AX1.ionapi`

**FSM Configuration Variables:**

```javascript
// Runtime variables (in process, not config)
var v_FSM_AccessToken = "";
var v_FSM_TokenExpiry = "";  // Timestamp when token expires
var v_FSM_RefreshToken = "";

// OAuth credentials read from .ionapi file at runtime
var v_IONApi_TenantId = "";
var v_IONApi_ClientId = "";
var v_IONApi_ClientSecret = "";
var v_IONApi_ServiceAccountAccessKey = "";
var v_IONApi_ServiceAccountSecretKey = "";
var v_IONApi_TokenURL = "";
var v_IONApi_BaseURL = "";
```

**ACCFIL Node: Read .ionapi File**

```javascript
// Read .ionapi file from Credentials/ folder
var ionApiFilePath = "Credentials/TAMICS10_AX1.ionapi";
var ionApiContent = readFile(ionApiFilePath);  // IPA file read function

// Parse JSON
var ionApiConfig = JSON.parse(ionApiContent);

// Extract credentials (NEVER log these values)
v_IONApi_TenantId = ionApiConfig.ti;
v_IONApi_ClientId = ionApiConfig.ci;
v_IONApi_ClientSecret = ionApiConfig.cs;
v_IONApi_ServiceAccountAccessKey = ionApiConfig.saak;
v_IONApi_ServiceAccountSecretKey = ionApiConfig.sask;
v_IONApi_TokenURL = ionApiConfig.pu + ionApiConfig.ot;
v_IONApi_BaseURL = ionApiConfig.iu;
```

**WEBRN Node: Get Access Token**

```javascript
// Build token request URL (credentials already loaded from .ionapi file)
var tokenUrl = v_IONApi_TokenURL + 
  "?grant_type=password" +
  "&username=" + encodeURIComponent(v_IONApi_TenantId + "#" + v_IONApi_ServiceAccountAccessKey) +
  "&password=" + encodeURIComponent(v_IONApi_ServiceAccountSecretKey) +
  "&client_id=" + encodeURIComponent(v_IONApi_ClientId) +
  "&client_secret=" + encodeURIComponent(v_IONApi_ClientSecret);

// Execute token request (POST)
var tokenResponse = webrun(tokenUrl, "POST", "", {});

// Parse response
var tokenData = JSON.parse(tokenResponse);
v_FSM_AccessToken = tokenData.access_token;
v_FSM_TokenExpiry = new Date().getTime() + (tokenData.expires_in * 1000);

// Store refresh token if provided
if (tokenData.refresh_token) {
  v_FSM_RefreshToken = tokenData.refresh_token;
}

// NEVER log credentials or tokens
// ❌ console.log("Token: " + v_FSM_AccessToken);  // NEVER DO THIS
// ✅ console.log("Token acquired successfully");   // OK
```

**WEBRN Node: Call FSM API with Token**

```javascript
// Build API URL (base URL already loaded from .ionapi file)
var apiUrl = v_IONApi_BaseURL + "/FSM/fsm/soap/classes/Vendor/lists/_generic?_fields=VendorGroup,Vendor,VendorName&_limit=10&_out=JSON";

// Set headers
var headers = {
  "Authorization": "Bearer " + v_FSM_AccessToken,
  "Accept": "application/json",
  "Content-Type": "application/json"
};

// Execute API call
var apiResponse = webrun(apiUrl, "GET", "", headers);

// Parse response
var data = JSON.parse(apiResponse);

// NEVER log sensitive data
// ❌ console.log("Response: " + apiResponse);  // May contain sensitive data
// ✅ console.log("API call successful, records: " + data.length);  // OK
```

**Token Refresh Pattern:**

```javascript
// Check if token expires in less than 5 minutes
var expiryBuffer = 5 * 60 * 1000;  // 5 minutes in milliseconds
var needsRefresh = (v_FSM_TokenExpiry - new Date().getTime()) < expiryBuffer;

if (needsRefresh || v_FSM_AccessToken == "") {
  // Get new token (use WEBRN node from above)
}
```

#### Swagger Documentation

**Swagger Endpoint:**

```text
GET https://mingle-ionapi.inforcloudsuite.com/{TENANT}/IDORequestService/ido/dynamic/api-docs-collection

Headers:
  Authorization: Bearer {access_token}
```

**AI Assistant Guidelines:**

- Use Swagger for runtime discovery of available business classes and actions
- Token must be refreshed before expiration (typically 1 hour)
- Always implement token expiry checking (refresh 5 minutes before expiry)
- **NEVER log or display tokens** in work unit logs
- **Read credentials from Credentials/ folder** at runtime (never hardcode)
- For external API OAuth2 (Authorization Code Grant), see `12_External_API_OAuth2_Integration_Guide.md`

**Security Best Practices:**

- Store .ionapi files in `Credentials/` folder (excluded from git)
- Add `Credentials/` to `.gitignore` if not already present
- Use service accounts (not user accounts) for API access
- Rotate credentials regularly per security policy
- Monitor token usage for security audits
- Never commit credential files to version control

---

## Common Patterns

### Financial Dimensions

- `FinanceDimension1-10`: Chart of accounts structure
- `Project`: Project code
- `AccountingUnit`: Organizational unit
- `OrganizationCode`: Organization identifier

### Multi-Currency Support

**ReportCurrencyAmount** structure:

- `FunctionalAmount`: Base currency
- `AlternateAmount` (1-3): Alternative currencies
- `ProjectAmount`: Project-specific currency
- `ReportAmount` (1-5): Reporting currencies

### Status Value Patterns

**Staging (GLTransactionInterface)**:

- 0=Unreleased (staged)
- 1=Released (validated)
- 2=Posted (to GL)
- 3=Error (validation failed)

**Posted GL (GeneralLedgerTransaction)**:

- 0=Unreleased
- 1=Released
- 6=Posted
- 7=Approved
- 8=Rejected
- 9=Suspended

**Detail Records (GLTransactionDetail)**:

- Status: 0=Unreleased, 1=Released, 8=NotToBePosted, 9=OnHold
- Billed: 0=NotBilled, 1=Billed, 3=PartiallyBilled, 4=Overbilled
- RevenueRecognized: 0=NotRecognized, 1=Recognized, 2=PartiallyRecognized

---

## Best Practices

### Performance

- **Batch Processing**: Group transactions using `RunGroup` + `SequenceNumber`
- **Page Size**: 30-50 records per API call
- **Purge Staging**: Regularly clean up processed `GLTransactionInterface` records
- **Memory Management**: Monitor during large operations

**AI Assistant Guidelines**:

- For bulk operations, generate code that processes in batches of 30-50 records
- Use `PurgeUnreleased` action to clean up staging tables after successful posting
- Recommend incremental replication (`_fts`/`_tts`) for large data extracts
- Avoid loading entire datasets into memory; process in chunks

### Data Validation

- **Date Format**: Always use `YYYYMMDD` (e.g., `20260116`)
- **Required Fields**: Validate before API calls to avoid errors
- **Enumeration Values**: Match API specifications exactly
- **Currency Precision**: Verify decimal places and formatting

**AI Assistant Guidelines**:

- When generating date values, ALWAYS format as `YYYYMMDD` (no dashes, slashes, or separators)
- Before generating API calls, verify all required context fields are available
- For status fields, use numeric values (0, 1, 2, etc.) not text descriptions
- Currency amounts should match FSM precision (typically 2 decimal places)
- Validate account codes exist before creating transactions

### Error Handling

- **Retry Logic**: Implement for transient failures
- **Detailed Logging**: Capture error messages, timestamps, context
- **Confirmation Messages**: Parse for validation violations
- **Reprocessing**: Maintain error records for retry

**AI Assistant Guidelines**:

- Generate code that parses API response for `_errors` array or confirmation messages
- Implement retry logic with exponential backoff for 500/503 errors
- Log full context (RunGroup, SequenceNumber, AccountCode) for failed transactions
- For GLTransactionInterface, query Status=3 records to identify validation failures
- Never silently ignore API errors; always log and handle appropriately

### Security

- **Token Management**: Refresh Bearer tokens before expiration
- **Input Validation**: Prevent injection attacks
- **Access Controls**: Use role-based security
- **Audit Logs**: Maintain for compliance

### IPA Development

- **ES5 JavaScript**: IPA uses Mozilla Rhino 1.7R4 (no arrow functions, template literals)
- **Error Handling**: Always wrap API calls in try-catch
- **Variable Naming**: Use descriptive names for maintainability
- **Comments**: Document complex logic and API parameters
- **Testing**: Test with small batches before production runs

**AI Assistant Guidelines**:

- When generating IPA JavaScript, NEVER use ES6+ features (`let`, `const`, `=>`, template literals, `class`)
- Always use `var` for variable declarations
- Use string concatenation with `+` instead of template literals
- Declare all functions at the top of the script (function hoisting)
- Use `try-catch` blocks around all API calls and parse response for errors
- For IPA coding standards, see `02_Work_Unit_Analysis.md` steering file

## Troubleshooting

### Common API Errors

**401 Unauthorized**:

- Token expired or invalid
- Solution: Refresh Bearer token from ION API

**400 Bad Request**:

- Missing required context fields (FinanceEnterpriseGroup, AccountingEntity)
- Invalid date format (must be YYYYMMDD)
- Invalid enumeration values
- Solution: Validate all required fields and formats before API call

**404 Not Found**:

- Business class or action name incorrect
- Module parameter wrong (e.g., "GL" instead of "gl")
- Solution: Verify business class exists in Swagger documentation

**500 Internal Server Error**:

- Business logic validation failed
- Database constraint violation
- Solution: Check confirmation message in response for specific error details

### Debugging Strategies

**Landmark Activity Issues**:

1. Check workunit log for exact transaction string sent
2. Verify all required context fields present
3. Test transaction string in Landmark Rich Client first
4. Check field names match exactly (case-sensitive)

**WebRun Activity Issues**:

1. Log full request payload and response
2. Verify JSON structure matches `_records` array format
3. Check `message` field value (BatchImport, BatchUpdate, BatchDelete)
4. Validate headers include Authorization and Content-Type
5. Parse response for `_errors` array

**InterfaceTransactions Failures**:

1. Query GLTransactionInterface for Status=3 (Error) records
2. Check ErrorMessage field for validation details
3. Use `PrmEditOnly=true` to validate without posting
4. Verify all required GL fields populated (AccountCode, PostingDate, Amount)

**AI Assistant Guidelines**:

- When user reports API error, ask for workunit log or error message
- Guide user through systematic debugging based on error type
- Suggest using `PrmEditOnly=true` for validation testing
- Recommend small batch testing before full production runs

### Accessing WorkUnit Data

**Problem**: WorkUnit business class (pfi module) is NOT exposed via FSM API.

**Alternative Methods**:

1. **Process Server Administrator UI**:
   - Manual access through FSM web interface
   - Navigate to Process Server Administrator → Work Units
   - View workunit details, logs, and variables

2. **Direct Database Queries**:
   - If database access is available
   - Query workunit tables directly (requires DBA permissions)
   - Not recommended for production environments

3. **Log File Parsing**:
   - Use `wu_master_template.py` script in workspace root
   - Parses workunit log files from `WU_Logs/` directory
   - Extracts runtime metrics, errors, variables, and performance data
   - Generates Excel reports with analysis

4. **Inbasket Customization**:
   - Display workunit variables in Inbasket lists
   - Configure process key fields for reporting
   - Limited to UI display, not programmatic access

**AI Assistant Guidelines**:

- When user asks about WorkUnit API, inform them it's NOT exposed
- Direct them to log file parsing using `wu_master_template.py`
- For workunit analysis, see `02_Work_Unit_Analysis.md` and `04_WU_Report_Generation.md` steering files
- Never generate code attempting to call WorkUnit via Landmark/WebRun activities
