---
inclusion: auto
name: data-fabric-guide
description: Infor OS Data Fabric architecture, Compass API, Data Lake, Metagraph, Orchestrator, Data Catalog, Data Warehouse, Ingestion, SQL queries, BOD, ION, OAuth2. Use when working with Data Fabric APIs or Infor OS integration.
---

# Infor OS and Data Fabric Guide

**Reference Documentation**: `D:\Kiro\WorkUnit_Analyzer_ReferenceDocuments\DataFabric_API\`

**Purpose**: Guide AI assistant in recommending and implementing Data Fabric API integrations for IPA processes and data extraction workflows.

## Table of Contents

- [Quick Decision Tree](#quick-decision-tree)
- [Data Fabric Architecture Overview](#data-fabric-architecture-overview)
- [Complete API Reference](#complete-api-reference)
- [Compass API - SQL Query Engine](#compass-api---sql-query-engine)
- [Data Lake API - Object Management](#data-lake-api---object-management)
- [Data Catalog API - Metadata Registry](#data-catalog-api---metadata-registry)
- [Ingestion API - Data Upload](#ingestion-api---data-upload)
- [Metagraph API - Virtual Joins](#metagraph-api---virtual-joins)
- [Data Orchestrator API - Workflows](#data-orchestrator-api---workflows)
- [Data Warehouse API - Models and Views](#data-warehouse-api---models-and-views)
- [ION OneView API - BOD Retrieval](#ion-oneview-api---bod-retrieval)
- [BI FSM API - Business Intelligence](#bi-fsm-api---business-intelligence)
- [OAuth2 Authentication](#oauth2-authentication)
- [IPA Integration Patterns](#ipa-integration-patterns)
- [Common Pitfalls and Solutions](#common-pitfalls-and-solutions)
- [Best Practices](#best-practices)

---

## Quick Decision Tree

**AI Assistant Action**: Use this decision tree FIRST when user requests data extraction, querying, or integration.

### Query Data

| Scenario | Recommended API | Why |
|----------|----------------|-----|
| >1M records | Data Orchestrator or Data Warehouse | No IPA memory limits, built-in pagination |
| 10K-1M records | Compass API via IPA | Requires memory management, paginate carefully |
| <10K records | Data Lake API | Simpler filter syntax, faster for small datasets |
| Joins across objects | Metagraph API or Data Warehouse | Virtual joins without data duplication |
| Raw BOD payload | ION OneView API or Data Lake API | Source verification, troubleshooting |

### Load Data

| Scenario | Recommended API | Why |
|----------|----------------|-----|
| Custom data upload | Ingestion API | ZLIB compressed, 200 calls/min |
| BI cube data | BI FSM API | IDL loading for analytics |
| Automated ETL | Orchestrator API | Scheduled workflows, no memory limits |

### Metadata Discovery

| Scenario | Recommended API | Why |
|----------|----------------|-----|
| Schema discovery | Data Catalog API | Get column names, types before querying |
| Object listing | Data Catalog API or Data Lake API | Discover available objects |
| BOD noun info | Data Catalog API | BOD metadata and structure |

### Troubleshooting

| Scenario | Recommended API | Why |
|----------|----------------|-----|
| Data quality issues | ION OneView API | Compare raw BODs vs processed data |

---

## Large-Scale Data Extraction (1M+ Records)

**AI Assistant Critical Rule**: When user requests extraction of >100K records, ALWAYS recommend Data Orchestrator or Data Warehouse FIRST. Only suggest IPA WebRun + Compass if user explicitly requires user-triggered extraction.

### IPA Memory Constraint

**CRITICAL**: IPA work units have a **100,000 MiB (100GB) total memory limit** across ALL nodes in the entire process execution.

### Memory Accumulation Problem

When extracting large datasets via WebRun + Compass pagination, memory accumulates across loop iterations:

| Iteration | WebRun Memory | Assign Memory | Cumulative Total |
|-----------|---------------|---------------|------------------|
| Page 1 | 500MB | 200MB | 700MB |
| Page 2 | 500MB | 200MB | 1,400MB |
| Page 10 | 500MB | 200MB | 7,000MB |
| Page 100 | 500MB | 200MB | 70,000MB (70GB) |
| Page 143+ | 500MB | 200MB | 100,000MB+ (FAILS) |

**Why memory accumulates:**

- Each WebRun node loads data into memory
- JavaScript processing in Assign nodes consumes memory
- Variables persist across loop iterations
- File write operations add overhead
- Garbage collection doesn't clear between iterations

### Recommended Solutions by Use Case

| Records | Frequency | Best Solution | Implementation Approach |
|---------|-----------|---------------|------------------------|
| <10K | Any | Data Lake API | Simple filter query, single API call |
| 10K-100K | Ad-hoc | Compass via IPA | Manageable memory, standard pagination |
| 100K-1M | Ad-hoc | Compass via IPA + memory mgmt | Requires careful design, small pages, clear variables |
| 100K-1M | Scheduled | Data Orchestrator | No memory constraints, built-in pagination |
| 1M+ | Any | Data Orchestrator or Data Warehouse | IPA not suitable |
| Any | Recurring | Data Warehouse view | Query pre-processed data, no repeated extracts |

### Solution 1: Data Orchestrator API (Best for Scheduled ETL)

**AI Assistant Recommendation**: Use this for scheduled extracts or when records >1M.

**Advantages:**

- ✅ No IPA memory constraints
- ✅ Built for large-scale ETL
- ✅ Handles pagination automatically
- ✅ Better error recovery with automatic retry
- ✅ Scheduled execution (cron)
- ✅ Can write directly to external systems (SFTP, S3)
- ✅ Parallel task execution

**Use case**: Daily GL balance extract → SFTP → external system

**Implementation**: See "Data Orchestrator API" section for flow creation examples.

### Solution 2: Data Warehouse API (Best for Reusable Views)

**AI Assistant Recommendation**: Use this when same data is queried repeatedly.

**Advantages:**

- ✅ Create materialized views once
- ✅ Query pre-processed data (faster)
- ✅ Incremental loading (high water mark)
- ✅ Published to Compass for easy access
- ✅ No repeated large extracts

**Use case**: Create "InvoiceApprovalHistory" view → query anytime without re-extracting

### Solution 3: Metagraph API (Best for Virtual Joins)

**AI Assistant Recommendation**: Use this when joining multiple BOD types without ETL.

**Advantages:**

- ✅ Virtual joins (no data duplication)
- ✅ Query via Compass like a normal table
- ✅ No ETL required
- ✅ Real-time data access

**Use case**: Join GLJournalEntry + GLAccount + GLCompany without moving data

### Solution 4: IPA WebRun + Compass (Use Only When Required)

**AI Assistant Recommendation**: Only suggest this if user explicitly requires user-triggered extraction AND records <1M.

**Only use if:**

- User-initiated extracts (not scheduled)
- Must be triggered from IPA workflow
- Records <1M
- Willing to implement memory management

**Required memory management pattern:**

```text
1. Paginate with small page sizes (10K-50K rows, NOT 100K)
2. Write to file after EACH page
3. Clear variables after each write (set to null)
4. Monitor cumulative memory usage
5. Implement error recovery for memory failures
```

**Example IPA pattern:**

```text
Loop (offset=0; offset<total; offset+=50000):
  1. WebRun: Compass query (limit=50000, offset=offset)
  2. Assign: Process data
  3. File Access: Append to output file
  4. Assign: Clear data variables (set response = null, set data = null)
  5. Check memory usage (if approaching 80GB, reduce page size)
```

---

## Data Fabric Architecture Overview

**AI Assistant Context**: Data Fabric is Infor's comprehensive data integration and management platform within Infor OS. All APIs require OAuth2 authentication.

### Ecosystem Components

```text
┌─────────────────────────────────────────────────────────────┐
│                     DATA FABRIC ECOSYSTEM                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Data Catalog │◄───┤  Data Lake   │◄───┤  Ingestion   │  │
│  │     API      │    │     API      │    │     API      │  │
│  │  (Metadata)  │    │  (Objects)   │    │  (Upload)    │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                    │          │
│         │                    │                    │          │
│         ▼                    ▼                    ▼          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              DATA LAKE STORAGE                        │  │
│  │  (Raw BODs, JSON, CSV, Data Objects)                 │  │
│  └──────────────────────────────────────────────────────┘  │
│         │                    │                    │          │
│         ▼                    ▼                    ▼          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Compass    │    │  Metagraph   │    │Data Warehouse│  │
│  │     API      │    │     API      │    │     API      │  │
│  │  (SQL Query) │    │(Virtual Join)│    │(Models/Views)│  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                    │          │
│         └────────────────────┴────────────────────┘          │
│                              │                                │
│                              ▼                                │
│                    ┌──────────────────┐                      │
│                    │  Orchestrator    │                      │
│                    │       API        │                      │
│                    │ (Workflows/ETL)  │                      │
│                    └──────────────────┘                      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Patterns

**Pattern 1: Query Existing Data**

```text
Data Catalog (schema) → Compass (query) → IPA (process) → Output
```

**Pattern 2: Upload Custom Data**

```text
Source → Ingestion (upload) → Data Lake (store) → Compass (query)
```

**Pattern 3: Virtual Join**

```text
Data Catalog (schema) → Metagraph (define join) → Compass (query joined view)
```

**Pattern 4: Scheduled ETL**

```text
Orchestrator (schedule) → Compass (extract) → Transform → SFTP/S3 (load)
```

---

## Complete API Reference

**AI Assistant Action**: Reference this table when recommending APIs. Always consider record count, frequency, and use case.

### API Summary

| API | Base Path | Primary Use | Record Limit | Rate Limit |
|-----|-----------|-------------|--------------|------------|
| **Compass API** | `/DATAFABRIC/compass/v2` | SQL queries on Data Lake | 100K/page, unlimited total | 100 submit/min |
| **Data Lake API** | `/DATAFABRIC/datalake/v1` | Object metadata & payloads | 10K max | Standard |
| **Data Catalog API** | `/DATAFABRIC/datacatalog/v1` | Metadata registry | N/A | Standard |
| **Ingestion API** | `/DATAFABRIC/ingestion/v1` | Direct data upload | N/A | 200/min |
| **Metagraph API** | `/DATAFABRIC/metagraph/v1` | Virtual joins | N/A | Standard |
| **Orchestrator API** | `/DATAFABRIC/orchestrator/v1` | Workflow automation | Unlimited | Standard |
| **Data Warehouse API** | `/DATAFABRIC/warehouse/v1` | Models, tables, views | N/A | Standard |
| **ION OneView API** | `/IONSERVICES/oneviewapi` | Raw BOD retrieval | 10K max | Standard |
| **BI FSM API** | `/BI/ApplicationEngine/BI/api/rest` | IDL data loading | N/A | Standard |

### API Selection Guide

**For Querying Data:**

| Scenario | API | Reason |
|----------|-----|--------|
| Large datasets (>10K records) | Compass API | 100K rows/page, unlimited total, SQL syntax |
| Small datasets (<10K records) | Data Lake API | Simpler filter syntax, faster for small queries |
| Complex joins | Metagraph API or Data Warehouse API | Virtual joins or materialized views |
| Raw BOD payloads | ION OneView API or Data Lake API | Source verification, troubleshooting |

**For Loading Data:**

| Scenario | API | Reason |
|----------|-----|--------|
| Custom data upload | Ingestion API | ZLIB compressed, 200 calls/min |
| BI cube data | BI FSM API | IDL loading for analytics |
| ETL workflows | Orchestrator API | Scheduled, automated, no memory limits |

**For Metadata:**

| Scenario | API | Reason |
|----------|-----|--------|
| Schema discovery | Data Catalog API | Get column names, types before querying |
| Object listing | Data Catalog API or Data Lake API | Discover available objects |
| BOD noun metadata | Data Catalog API | BOD structure and properties |

---

## Compass API - SQL Query Engine

**Base URL**: `/DATAFABRIC/compass/v2`

**AI Assistant Recommendation**: Use Compass API for datasets >10K records. Always implement pagination for large result sets.

### Compass API Use Cases

- Query large datasets (>10K records) with SQL syntax
- Reporting and analytics
- Data extraction for external systems
- Complex queries with joins, aggregations, CTEs

### Key Endpoints

| Endpoint | Method | Purpose | AI Implementation Notes |
|----------|--------|---------|------------------------|
| `/ping` | GET | Check service availability | Call before submitting queries to verify service |
| `/jobs/` | POST | Submit Compass SQL query | Returns queryId for status polling |
| `/jobs/{queryId}/status/` | GET | Check query execution status | Use long-polling (timeout=25) to reduce API calls |
| `/jobs/{queryId}/result/` | GET | Retrieve query results (paginated) | Implement pagination loop for large datasets |
| `/jobs/{queryId}/cancel/` | PUT | Cancel a running query | Use for timeout handling |

### Critical Limits and Constraints

**Pagination Limits:**

- **Per page**: Maximum 100,000 rows OR 10MB (whichever is hit first)
- **Total query**: No limit - paginate through all results using offset/limit
- **Example**: 1 million records = 10 API calls with limit=100000

**Rate Limits (per tenant):**

- Submit query: 100 calls/minute
- Check status: 1,000 calls/minute
- Retrieve results: 10,000 calls/minute

**Timeouts:**

- Query execution: 60 minutes max
- Status polling: 0-25 seconds (long-polling supported)

**AI Assistant Action**: When implementing Compass queries, always add 100-500ms delays between API calls to avoid rate limits.

### Query Parameters

**Submit Query (`/jobs/`):**

- `records` (optional): Maximum records to return (0 = all, default)

**Retrieve Results (`/jobs/{queryId}/result/`):**

- `offset` (integer): Row offset, 0-based (default: 0)
- `limit` (integer): Max 100,000 rows per page (default: 0 = all)

**Response Formats:**

- `application/json` - JSON format (default)
- `application/x-ndjson` - Newline Delimited JSON (better for streaming)
- `text/csv` - CSV format (best for file output)

**Accept-Encoding:**

- `gzip`, `deflate`, `identity` (use gzip for large responses)

### Query Status Values

| Status | HTTP Code | Meaning | AI Action |
|--------|-----------|---------|-----------|
| `RUNNING` | 202 | Query is executing | Continue polling status |
| `FINISHED` | 201 | Query completed | Retrieve results with pagination |
| `FAILED` | 201 | Query failed | Retrieve error details, log for troubleshooting |
| `CANCELED` | 201 | Query was canceled | Handle as error condition |

### Compass SQL Capabilities

**Supported Clauses:**

- SELECT / SELECT DISTINCT
- FROM, WHERE, GROUP BY, HAVING, ORDER BY
- LIMIT / OFFSET / TOP
- UNION / UNION ALL
- WITH (CTE - Common Table Expressions)
- Subqueries (in SELECT, FROM, WHERE contexts)

**Supported Joins:**

- INNER JOIN, LEFT OUTER JOIN, RIGHT JOIN, CROSS JOIN

**Data Types:**

- CAST to: varchar, date, datetime, datetime2, decimal, integer, bigint

**Aggregations:**

- COUNT, SUM, AVG, MIN, MAX

**AI Assistant Note**: For detailed SQL syntax, examples, and limitations, refer to `05_Compass_SQL_CheatSheet.md`.

### IPA Implementation Pattern

**AI Assistant Action**: When generating IPA processes for Compass queries, follow this pattern:

```text
1. OAuth2 Token Acquisition (WEBRN)
   - POST to token endpoint
   - Store access_token in variable

2. Submit Query (WEBRN)
   - POST /DATAFABRIC/compass/v2/jobs/
   - Body: {"query": "SELECT ...", "records": 0}
   - Store queryId from response

3. Poll Status (WEBRN + Loop)
   - GET /jobs/{queryId}/status/?timeout=25
   - Loop until status = FINISHED or FAILED
   - Add 1-second delay between polls

4. Retrieve Results (WEBRN + Pagination Loop)
   - Initialize: offset=0, limit=100000
   - Loop:
     - GET /jobs/{queryId}/result/?offset={offset}&limit={limit}
     - Process page data
     - Write to file (append mode)
     - Clear variables (set response = null)
     - offset += limit
     - Continue until no more data

5. Process Data (ASSGN)
   - Parse JSON/CSV
   - Transform as needed

6. Output (ACCFIL/FTP)
   - Write final file or send to destination
```

### Example Compass Query

```sql
SELECT 
  journal_entry_id,
  accounting_entity,
  posting_date,
  journal_source,
  SUM(CAST(debit_amount AS decimal)) AS total_debit,
  SUM(CAST(credit_amount AS decimal)) AS total_credit
FROM GLJournalEntry
WHERE posting_date >= '2024-01-01'
  AND accounting_entity = 'US01'
GROUP BY journal_entry_id, accounting_entity, posting_date, journal_source
ORDER BY posting_date DESC
LIMIT 100000 OFFSET 0
```

**AI Assistant Note**: Always use CAST for numeric operations to avoid type errors.

---

## Data Lake API - Object Management

**Base URL**: `/DATAFABRIC/datalake/v1`

**AI Assistant Recommendation**: Use Data Lake API for small datasets (<10K records) and BOD payload retrieval. For larger datasets, use Compass API.

### Data Lake API Use Cases

- Query small datasets (<10K records)
- Retrieve BOD payloads by ID
- Object metadata queries
- Simple filter-based queries

### Data Lake API Endpoints

| Endpoint | Method | Purpose | AI Implementation Notes |
|----------|--------|---------|------------------------|
| `/dataobjects` | GET | List objects with filter | Max 10K results, use splitquery for more |
| `/dataobjects/{id}` | GET | Get payload by dl_id | Single object retrieval |
| `/dataobjects/byfilter` | GET | Stream multiple objects (multipart) | For batch retrieval |
| `/dataobjects/splitquery` | GET | Split large queries into chunks | Use when expecting >10K results |
| `/dataobjects/ids` | DELETE | Delete by IDs (max 1000) | Batch deletion |
| `/dataobjects/filter` | DELETE | Delete by filter (max 1000) | Filter-based deletion |

### Critical Limits

- **Maximum results**: 10,000 records per query
- **AI Assistant Action**: If user needs >10K records, recommend Compass API instead

### Filter Syntax

**Format**: `(field_name operator 'value')` with `and`/`or` logical operators

**Operators**: `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `like`, `in`

**Examples:**

```text
(dl_document_name eq 'GLJournalEntry')
(dl_document_date ge '2024-01-01' and dl_document_date le '2024-12-31')
(dl_header_accounting_entity in ('US01', 'US02'))
(dl_from_logical_id like 'lid://infor.ln%')
```

**AI Assistant Note**: Filter syntax is identical to ION OneView API.

### Queryable Properties

Common properties available for filtering:

- `dl_id` - Unique object identifier
- `dl_document_name` - Object/BOD name (e.g., 'GLJournalEntry')
- `dl_from_logical_id` - Source logical ID
- `dl_document_date` - Document date
- `dl_instance_count` - Number of instances in object
- `dl_size` - Object size in bytes
- `dl_header_accounting_entity` - Accounting entity
- `dl_batch_id` - Batch identifier

**AI Assistant Action**: Use Data Catalog API to discover all available properties for specific objects before querying.

### Data Lake IPA Pattern

**Pattern 1: Retrieve BOD by Name**

```text
1. OAuth2 Token Acquisition (WEBRN)
2. Query metadata (WEBRN):
   GET /dataobjects?filter=(dl_document_name eq 'GLJournalEntry' and dl_document_date ge '2024-01-01')
3. Extract dl_id from response (ASSGN)
4. Download payload (WEBRN):
   GET /dataobjects/{dl_id}
5. Process NDJSON/JSON data (ASSGN)
```

**Pattern 2: Batch Retrieval**

```text
1. OAuth2 Token Acquisition (WEBRN)
2. Query with byfilter (WEBRN):
   GET /dataobjects/byfilter?filter=(dl_document_name eq 'PayablesInvoice')
3. Process multipart response (ASSGN)
4. Parse each object (ASSGN + Loop)
```

---

## Data Catalog API - Metadata Registry

**Base URL**: `/DATAFABRIC/datacatalog/v1`

**AI Assistant Recommendation**: ALWAYS call Data Catalog API FIRST before writing Compass queries or Data Lake queries. This discovers schema, column names, and data types.

### Data Catalog Use Cases

- Schema discovery before querying
- Object listing and discovery
- BOD noun metadata
- Understanding data structure

### Data Catalog Endpoints

| Endpoint | Method | Purpose | AI Implementation Notes |
|----------|--------|---------|------------------------|
| `/object/list` | GET | List all objects | Filter by type: ANY, BOD, DSV, JSON, VIEW |
| `/object/{name}` | GET | Get object metadata | Returns schema, properties, audit info |
| `/object/{name}/schema` | GET | Get schema only | Faster than full metadata |
| `/object/events` | GET | Get create/delete events | Last 90 days only |
| `/bod/nouns` | GET | List BOD nouns | Discover available BOD types |
| `/bod/noun/{name}` | GET | Get BOD noun details | BOD structure and properties |

### Workflow Pattern

**AI Assistant Action**: Always follow this pattern when user requests data extraction:

```text
1. Call Data Catalog API to get schema
2. Identify column names and data types
3. Write Compass/Data Lake query using correct column names
4. Execute query
```

### Example: Schema Discovery

**Request:**

```http
GET /DATAFABRIC/datacatalog/v1/object/GLJournalEntry/schema
Authorization: Bearer {oauth2_token}
```

**Response:**

```json
{
  "objectName": "GLJournalEntry",
  "columns": [
    {"name": "journal_entry_id", "type": "varchar"},
    {"name": "accounting_entity", "type": "varchar"},
    {"name": "posting_date", "type": "date"},
    {"name": "debit_amount", "type": "decimal"},
    {"name": "credit_amount", "type": "decimal"}
  ]
}
```

**AI Assistant Action**: Use this schema to write accurate Compass queries with correct column names and CAST operations.

### Data Catalog IPA Pattern

```text
1. OAuth2 Token Acquisition (WEBRN)
2. Get Schema (WEBRN):
   GET /datacatalog/v1/object/GLJournalEntry/schema
3. Parse Schema (ASSGN):
   - Extract column names
   - Identify data types
4. Build Compass Query (ASSGN):
   - Use correct column names
   - Add CAST for numeric columns
5. Execute Compass Query (WEBRN)
```

---

## Ingestion API - Data Upload

**Base URL**: `/DATAFABRIC/ingestion/v1`

**AI Assistant Recommendation**: Use Ingestion API when user needs to upload custom data to Data Lake (not BODs from ION).

### Ingestion API Use Cases

- Upload custom data to Data Lake
- Load external data files (CSV, JSON)
- Batch data loading
- Custom data integration

### Ingestion Key Endpoint

**`/dataobjects` (POST)** - Upload compressed data object

### Requirements

- **Compression**: ZLIB compression (deflate method) - REQUIRED
- **Content-Type**: multipart/form-data
- **Required fields**:
  - `dl_document_name` - Object name
  - `dl_from_logical_id` - Source logical ID
- **Rate limit**: 200 calls/minute

### Optional Properties

- `dl_instance_count` - Number of records in object
- `decompressed_size` - Uncompressed size in bytes
- `dl_source_publication_date` - Source publication date
- `dl_header_accounting_entity` - Accounting entity
- `dl_batch_id` - Batch identifier for grouping

### IPA Implementation Pattern

**AI Assistant Note**: Ingestion requires ZLIB compression, which is not natively supported in IPA JavaScript. Recommend Python script or external tool for compression.

```text
1. OAuth2 Token Acquisition (WEBRN)
2. Prepare Data (ASSGN):
   - Format as JSON/CSV
   - Compress with ZLIB (external script)
3. Upload Data (WEBRN):
   POST /ingestion/v1/dataobjects
   - multipart/form-data
   - Include compressed file
   - Set dl_document_name, dl_from_logical_id
4. Verify Upload (WEBRN):
   GET /datalake/v1/dataobjects?filter=(dl_document_name eq 'CustomObject')
```

### Example Upload Request

```http
POST /DATAFABRIC/ingestion/v1/dataobjects
Authorization: Bearer {oauth2_token}
Content-Type: multipart/form-data

--boundary
Content-Disposition: form-data; name="dl_document_name"

CustomSalesData
--boundary
Content-Disposition: form-data; name="dl_from_logical_id"

lid://infor.custom.sales
--boundary
Content-Disposition: form-data; name="file"; filename="data.json.zlib"
Content-Type: application/octet-stream

[ZLIB compressed data]
--boundary--
```

---

## Metagraph API - Virtual Joins

**Base URL**: `/DATAFABRIC/metagraph/v1`

**AI Assistant Recommendation**: Use Metagraph API when user needs to join multiple BOD types or data objects without ETL or data duplication.

### Primary Use Cases

- Join multiple BOD types (e.g., GLJournalEntry + GLAccount + GLCompany)
- Create virtual views without moving data
- Real-time data access across objects
- Reduce data duplication

### Key Concepts

- **Nodes**: DATA_OBJECT, COMPASS_VIEW, METAGRAPH
- **Edges**: Join relationships (INNER, LEFT, RIGHT, FULL)
- **Driver Node**: Starting point (driver: true)

### Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/metagraphs` | GET | List all metagraphs |
| `/metagraphs` | POST | Create new metagraph |
| `/metagraphs/{name}` | GET | Get metagraph definition |
| `/metagraphs/{name}` | PUT | Update metagraph |
| `/metagraphs/{name}` | DELETE | Delete metagraph |

### Example: Join GLJournalEntry with GLAccount

**Create Metagraph:**

```json
{
  "name": "GLJournalEntryWithAccount",
  "description": "Join journal entries with account details",
  "nodes": [
    {
      "name": "JournalEntry",
      "type": "DATA_OBJECT",
      "objectName": "GLJournalEntry",
      "driver": true
    },
    {
      "name": "Account",
      "type": "DATA_OBJECT",
      "objectName": "GLAccount"
    }
  ],
  "edges": [
    {
      "from": "JournalEntry",
      "to": "Account",
      "joinType": "LEFT",
      "condition": "JournalEntry.account_id = Account.account_id"
    }
  ]
}
```

**Query Metagraph via Compass:**

```sql
SELECT 
  je.journal_entry_id,
  je.posting_date,
  je.debit_amount,
  a.account_name,
  a.account_type
FROM GLJournalEntryWithAccount je
WHERE je.posting_date >= '2024-01-01'
```

**AI Assistant Action**: After creating metagraph, it's queryable via Compass API like a normal table.

### IPA Implementation Pattern

```text
1. OAuth2 Token Acquisition (WEBRN)
2. Create Metagraph (WEBRN):
   POST /metagraph/v1/metagraphs
   - Define nodes and edges
3. Query via Compass (WEBRN):
   POST /compass/v2/jobs/
   - Query metagraph like a table
4. Retrieve Results (WEBRN + Pagination)
```

### Advantages Over Physical Joins

- ✅ No data duplication
- ✅ Real-time data access
- ✅ No ETL required
- ✅ Queryable via Compass
- ✅ Reduced storage costs

---

## Data Orchestrator API - Workflows

**Base URL**: `/DATAFABRIC/orchestrator/v1`

**AI Assistant Critical Rule**: When user requests scheduled ETL or extraction of >1M records, ALWAYS recommend Data Orchestrator as the primary solution.

**CRITICAL**: Data Orchestrator has **NO UI** - all flows must be created via REST API calls.

### Available Interfaces

| Interface | Available? | Purpose |
|-----------|------------|---------|
| **Data Fabric UI** | ❌ No | UI only has: Data Lake, Compass, Data Catalog, Metagraphs, Security, Utilities, Tags |
| **REST API** | ✅ Yes | Create/manage flows via API calls |
| **Postman/API Client** | ✅ Yes | Most common approach for creating flows |
| **Python Script** | ✅ Yes | DevOps/automation approach |
| **IPA WebRun** | ✅ Yes | One-time setup via IPA process |

### Primary Use Cases

- Scheduled data extraction (daily, weekly, monthly)
- Large-scale ETL (1M+ records)
- Automated data pipelines
- Multi-step workflows with dependencies
- Direct integration with external systems (SFTP, S3, REST APIs)

### Why Use Data Orchestrator Over IPA

| Aspect | IPA WebRun | Data Orchestrator |
|--------|------------|-------------------|
| **Memory Limit** | 100GB total | No practical limit |
| **Pagination** | Manual implementation | Built-in automatic |
| **Scheduling** | IPA triggers only | Cron schedules |
| **Error Recovery** | Manual retry logic | Automatic retry with backoff |
| **Monitoring** | Work unit logs | Execution dashboard via API |
| **Best For** | <100K records, user-triggered | 1M+ records, scheduled |
| **External Integration** | Manual SFTP/FTP nodes | Built-in SFTP, S3, HTTP tasks |

### Key Endpoints

| Endpoint | Method | Purpose | AI Implementation Notes |
|----------|--------|---------|------------------------|
| `/flows` | GET | List all flows | Discover existing flows |
| `/flows` | POST | Create new flow | Define tasks, parameters, schedules |
| `/flows/{flowName}` | GET | Get flow definition | Review flow configuration |
| `/flows/{flowName}` | PUT | Update flow | Modify existing flow |
| `/flows/{flowName}` | DELETE | Delete flow | Remove flow |
| `/flows/{flowName}/execute` | POST | Execute flow manually | Trigger on-demand execution |
| `/flows/{flowName}/executions` | GET | List execution history | Monitor past runs |
| `/flows/{flowName}/executions/{executionId}` | GET | Get execution details | Troubleshoot failures |
| `/flows/{flowName}/schedules` | GET | List schedules | View cron schedules |
| `/flows/{flowName}/schedules` | POST | Create schedule | Add cron trigger |
| `/flows/{flowName}/schedules/{scheduleId}` | DELETE | Delete schedule | Remove cron trigger |

### Flow Structure

**AI Assistant Action**: When creating flows, use this structure as a template.

```json
{
  "name": "extract_gl_balances",
  "description": "Extract GL balances for external reporting",
  "parameters": [
    {
      "name": "start_date",
      "type": "Date",
      "required": true,
      "defaultValue": "2024-01-01"
    },
    {
      "name": "accounting_entity",
      "type": "String",
      "required": false
    }
  ],
  "tasks": [
    {
      "name": "query_compass",
      "type": "CompassQuery",
      "config": {
        "query": "SELECT * FROM GLJournalEntry WHERE posting_date >= '${start_date}'",
        "outputFormat": "CSV",
        "pagination": {
          "enabled": true,
          "pageSize": 100000
        }
      }
    },
    {
      "name": "transform_data",
      "type": "Script",
      "dependsOn": ["query_compass"],
      "config": {
        "language": "JavaScript",
        "script": "// Transform logic here"
      }
    },
    {
      "name": "upload_to_sftp",
      "type": "SFTP",
      "dependsOn": ["transform_data"],
      "config": {
        "host": "sftp.example.com",
        "path": "/reports/gl_balances_${start_date}.csv",
        "credentials": "sftp_credentials"
      }
    }
  ],
  "outputParameters": [
    {
      "name": "records_processed",
      "type": "Integer"
    },
    {
      "name": "output_file",
      "type": "String"
    }
  ]
}
```

### Task Types

**AI Assistant Action**: Use these task types when building flows.

| Task Type | Purpose | Key Config Parameters |
|-----------|---------|----------------------|
| **CompassQuery** | Query Data Fabric | query, outputFormat, pagination |
| **DataLakeQuery** | Query Data Lake objects | filter, objectName |
| **Script** | JavaScript/Python transformation | language, script |
| **SFTP** | Upload to SFTP server | host, path, credentials |
| **S3** | Upload to AWS S3 | bucket, key, credentials |
| **HTTP** | Call REST API | url, method, headers, body |
| **Email** | Send email notification | to, subject, body |
| **Parallel** | Execute tasks in parallel | tasks[] |
| **Sequential** | Execute tasks in sequence | tasks[] |

### Creating a Flow - Complete Example

**AI Assistant Action**: Use this complete example when user requests scheduled extraction of large datasets.

**Use Case**: Extract 1M+ invoices daily at 2 AM, upload to SFTP, send notification

**Step 1: Create Flow Definition**

```http
POST /DATAFABRIC/orchestrator/v1/flows
Authorization: Bearer {oauth2_token}
Content-Type: application/json

{
  "name": "daily_invoice_extract",
  "description": "Extract all invoices for external reporting",
  "parameters": [
    {
      "name": "extract_date",
      "type": "Date",
      "required": true
    }
  ],
  "tasks": [
    {
      "name": "extract_invoices",
      "type": "CompassQuery",
      "config": {
        "query": "SELECT invoice_number, vendor_id, amount, status FROM PayablesInvoice WHERE invoice_date = '${extract_date}'",
        "outputFormat": "CSV",
        "pagination": {
          "enabled": true,
          "pageSize": 100000
        },
        "outputPath": "/temp/invoices_${extract_date}.csv"
      }
    },
    {
      "name": "upload_to_sftp",
      "type": "SFTP",
      "dependsOn": ["extract_invoices"],
      "config": {
        "host": "sftp.client.com",
        "port": 22,
        "path": "/reports/invoices_${extract_date}.csv",
        "credentials": "client_sftp",
        "sourceFile": "/temp/invoices_${extract_date}.csv"
      }
    },
    {
      "name": "send_notification",
      "type": "Email",
      "dependsOn": ["upload_to_sftp"],
      "config": {
        "to": "finance@client.com",
        "subject": "Invoice Extract Complete - ${extract_date}",
        "body": "Invoice extract completed. Records: ${extract_invoices.recordCount}"
      }
    }
  ]
}
```

**Step 2: Create Schedule (Daily at 2 AM)**

```http
POST /DATAFABRIC/orchestrator/v1/flows/daily_invoice_extract/schedules
Authorization: Bearer {oauth2_token}
Content-Type: application/json

{
  "name": "daily_2am_schedule",
  "cron": "0 2 * * *",
  "timezone": "America/New_York",
  "enabled": true,
  "parameters": {
    "extract_date": "${today}"
  }
}
```

**Step 3: Monitor Execution**

```http
GET /DATAFABRIC/orchestrator/v1/flows/daily_invoice_extract/executions
Authorization: Bearer {oauth2_token}
```

### IPA Integration Pattern (Hybrid Approach)

**AI Assistant Recommendation**: Use this pattern when user triggers extract from IPA, but Orchestrator handles heavy lifting.

**Use Case**: User clicks "Generate Invoice Report" in IPA, Orchestrator processes 1M+ records

```text
IPA Process:
1. User Action: "Generate Invoice Report"
2. Assign: Prepare parameters (date range, filters)
3. WebRun: POST /orchestrator/v1/flows/invoice_extract/execute
   - Pass parameters
   - Receive executionId
4. Assign: Store executionId in process variable
5. Email: "Report generation started. You'll receive notification when complete."
6. End Process

Orchestrator Flow:
1. Extract 1M+ invoices (handles pagination automatically)
2. Transform data
3. Upload to SFTP
4. Send completion email to user
```

**AI Assistant Note**: This pattern avoids IPA memory limits while maintaining user-triggered workflow.

### Error Handling and Retry Logic

**AI Assistant Action**: Always include error handling in production flows.

**Automatic Retry Configuration:**

```json
{
  "tasks": [
    {
      "name": "query_compass",
      "type": "CompassQuery",
      "config": {
        "query": "SELECT * FROM GLJournalEntry",
        "retry": {
          "maxAttempts": 3,
          "backoffMultiplier": 2,
          "initialDelay": "5s"
        }
      }
    }
  ]
}
```

**Error Notification Task:**

```json
{
  "tasks": [
    {
      "name": "on_error_notify",
      "type": "Email",
      "triggerOn": "ERROR",
      "config": {
        "to": "admin@company.com",
        "subject": "Flow Failed: ${flowName}",
        "body": "Error: ${error.message}\nExecution ID: ${executionId}"
      }
    }
  ]
}
```

### Best Practices

**AI Assistant Action**: Follow these best practices when creating flows.

1. **Use pagination** for queries >100K records
2. **Add error notifications** for production flows
3. **Use parameters** for dynamic values (dates, filters)
4. **Test with small datasets** before scheduling
5. **Monitor execution history** regularly via API
6. **Use parallel tasks** for independent operations
7. **Clean up temp files** in final task
8. **Set appropriate timeouts** for long-running tasks
9. **Use descriptive task names** for troubleshooting
10. **Document flow purpose** in description field

### Documentation Sources

**CRITICAL**: Data Orchestrator has **NO user documentation** beyond the Swagger API specification.

**Searched Documentation:**

- ❌ `Infor_Data_Fabric_User_Guide.pdf` - No Data Orchestrator section
- ❌ `Infor_Data_Fabric_ETL_Client_for_DataLake_Admin_Guide.pdf` - No Data Orchestrator section
- ❌ `Infor_Landmark_Technology_Web_Services_Reference_Guide.pdf` - Covers **Landmark web services** (REST/SOAP APIs for FSM business classes), not Data Orchestrator

**What the Landmark Web Services Guide Covers:**

- REST/JSON and SOAP/WSDL APIs for FSM business classes
- ION API Gateway integration
- Configuration Console for creating defined web services
- Form-based and list-based operations
- OpenAPI documentation configuration
- Page size limits for inbound web services
- Every field of every FSM screen accessible via API

**Available Resources for Data Orchestrator:**

- ✅ Swagger API spec: `D:\Kiro\WorkUnit_Analyzer_ReferenceDocuments\DataFabric_API\DataOrchestrator.json`
- ✅ This guide (compiled from API spec + experimentation)

**AI Assistant Recommendation**: Use Swagger spec as primary reference. Test flows in non-production environment first.

---

## Data Warehouse API - Models and Views

**Base URL**: `/DATAFABRIC/warehouse/v1`

**AI Assistant Recommendation**: Use Data Warehouse API when user needs reusable views or materialized data for recurring queries.

### Primary Use Cases

- Create materialized views for recurring queries
- Build data warehouse models
- Incremental data loading (high water mark)
- Publish views to Compass for easy access
- Reduce repeated large extracts

### Key Concepts

- **Models**: Logical groupings of tables/views/scripts
- **Tables**: Physical storage with columns, primary keys
- **Views**: SQL views over tables or Data Lake objects
- **Scripts**: SQL transformation scripts
- **Load Queries**: ETL queries from external sources

### Key Features

- **Analytical mode** for analytics workloads
- **Published objects** available via Compass
- **Incremental loading** (high water mark pattern)
- **Model import/export** for version control

### Use Case Example

**Problem**: User queries "InvoiceApprovalHistory" daily, extracting 500K records each time

**Solution**: Create Data Warehouse view once, query anytime

```text
1. Create view: InvoiceApprovalHistory
2. Load data incrementally (high water mark)
3. Publish to Compass
4. Query via Compass: SELECT * FROM InvoiceApprovalHistory WHERE approval_date >= '2024-01-01'
```

**AI Assistant Action**: Recommend Data Warehouse views for recurring queries to avoid repeated large extracts.

---

## ION OneView API - BOD Retrieval

**Base URL**: `/IONSERVICES/oneviewapi`

**AI Assistant Recommendation**: Use ION OneView API when troubleshooting data quality issues or comparing raw BODs with processed data.

### Primary Use Cases

- Access raw BOD data from ION message store
- Troubleshoot data quality issues
- Compare source BODs vs processed data in Data Lake
- Audit trail for BOD messages
- Source data verification

### Key Endpoints

| Endpoint | Method | Purpose | AI Implementation Notes |
|----------|--------|---------|------------------------|
| `/data` | GET | Query messages with filters | Max 10K results, use pagination |
| `/data/documentPayload` | GET | Download BOD by MessageID | Single BOD retrieval |
| `/data/streamDocumentPayload` | GET | Stream large BODs | For BODs >10MB |

### Filter Syntax

**Format**: `(field_name operator 'value')` with `and`/`or` logical operators

**Operators**: `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `like`, `in`

**Examples:**

```text
(document_sent_from eq 'lid://infor.ln.us01')
(document_type eq 'Sync.GLJournalEntry')
(message_date ge '2024-01-01' and message_date le '2024-12-31')
(document_size gt 1000000)
```

### Key Fields

- `document_sent_from` - Source logical ID
- `document_type` - BOD type (e.g., 'Sync.GLJournalEntry')
- `message_date` - Message timestamp
- `message_id` - Unique message identifier
- `document_size` - BOD size in bytes

### Troubleshooting Pattern

**AI Assistant Action**: Use this pattern when user reports data quality issues.

```text
1. Query ION OneView for raw BODs:
   GET /data?filter=(document_type eq 'Sync.GLJournalEntry' and message_date ge '2024-01-01')

2. Download specific BOD:
   GET /data/documentPayload?messageId={message_id}

3. Query Data Lake for processed data:
   GET /datalake/v1/dataobjects?filter=(dl_document_name eq 'GLJournalEntry')

4. Compare raw BOD vs processed data:
   - Identify missing fields
   - Identify transformation errors
   - Determine if issue is in source or processing

5. Report findings:
   - If raw BOD is incorrect → Source system issue
   - If processed data is incorrect → IPA/Data Fabric issue
```

**AI Assistant Note**: This pattern proves whether data quality issues originated from source BODs or IPA processing. Raw BOD data can be retrieved using ION OneView API for investigation.

---

## BI FSM API - Business Intelligence

**Base URL**: `/BI/ApplicationEngine/BI/api/rest/ColemanAIService/v1/BIFSM/<ApiName>/v1`

**AI Assistant Recommendation**: Use BI FSM API when user needs to load data into IDL (Infor Data Lake) objects from BI cubes.

### Primary Use Cases

- Load data into IDL objects from BI cubes
- Extract BI cube data for analytics
- Populate Data Lake with BI data

### Common APIs

- `FCE_IDL_GeneralLedgerBalancesByPeriod` - GL balances by period
- `FPI_FCIL_FMFC_IDL_GeneralLedgerBalancesByPeriod` - GL balances (FPI variant)

### Error Handling

**Worker Unavailable (HTTP 500)**:

- **Cause**: BI worker not available
- **Solution**: Retry with 30-second intervals (4 attempts max)
- **AI Assistant Action**: Implement retry logic with exponential backoff

### IPA Implementation Pattern

```text
1. OAuth2 Token Acquisition (WEBRN)
2. Call BI FSM API (WEBRN):
   POST /BI/ApplicationEngine/BI/api/rest/ColemanAIService/v1/BIFSM/FCE_IDL_GeneralLedgerBalancesByPeriod/v1
3. Handle HTTP 500 (ASSGN + Loop):
   - Retry up to 4 times
   - Wait 30 seconds between retries
4. Process Response (ASSGN)
```

---

## OAuth2 Authentication

**AI Assistant Critical Rule**: ALL Data Fabric and ION APIs require OAuth2 bearer tokens. Always include token acquisition as first step in IPA processes.

**CRITICAL SECURITY RULES**:

- **NEVER commit .ionapi files to git** (.gitignore already configured)
- **NEVER log credentials** in work unit logs or console output
- **NEVER hardcode credentials** in IPA processes
- **ALWAYS read from Credentials/ folder** at runtime

**Credential Files Location**: `Credentials/` folder

- `Credentials/{TENANT}.ionapi` - ION API credentials for OAuth2
- Example: `Credentials/TAMICS10_AX1.ionapi`, `Credentials/ACUITY_TST.ionapi`

### .ionapi File Structure

**Location**: `Credentials/` folder or `ReusableTools/<ToolName>/config/`

```json
{
  "ti": "TENANT_ID",
  "ci": "TENANT_ID~ClientIdString",
  "cs": "ClientSecretString",
  "iu": "https://mingle-ionapi.inforcloudsuite.com",
  "pu": "https://mingle-sso.inforcloudsuite.com:443/TENANT_ID/as/",
  "ot": "token.oauth2",
  "saak": "TENANT_ID#ServiceAccountAccessKey",
  "sask": "ServiceAccountSecretKey"
}
```

**NEVER commit these files to git** - add `Credentials/` to `.gitignore`

### Token Request

**Endpoint**: `{pu}{ot}` (e.g., `https://mingle-sso.inforcloudsuite.com:443/TENANT_ID/as/token.oauth2`)

**Method**: POST

**Content-Type**: `application/x-www-form-urlencoded`

**Body**:

```text
username={ti}%23{saak}&password={sask}&client_id={ci}&client_secret={cs}&grant_type=password
```

**CRITICAL**: URL-encode `#` as `%23` in username field

**Response**:

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 7200
}
```

### Token Lifetime and Refresh

- **Lifetime**: 2 hours (7200 seconds)
- **AI Assistant Action**: Implement token refresh logic for long-running processes
- **Pattern**: Check token expiration before each API call, refresh if <5 minutes remaining

### IPA Implementation Pattern

**AI Assistant Action**: Always read credentials from .ionapi file at runtime, never hardcode.

```text
1. Read .ionapi file (ACCFIL)
   - Path: Credentials/{TENANT}.ionapi
   - Read file content

2. Parse JSON (ASSGN)
   - Extract: ti, ci, cs, saak, sask, pu, ot
   - NEVER log these values

3. Build token request (ASSGN):
   - URL: {pu}{ot}
   - Body: username={ti}%23{saak}&password={sask}&client_id={ci}&client_secret={cs}&grant_type=password
   - CRITICAL: URL-encode # as %23 in username

4. Request token (WEBRN):
   - POST to token endpoint
   - Content-Type: application/x-www-form-urlencoded
   - NEVER log request body (contains credentials)

5. Extract access_token (ASSGN)
   - Parse JSON response
   - Store access_token in variable
   - NEVER log token value

6. Use in API calls (WEBRN):
   - Header: Authorization: Bearer {access_token}
   - NEVER log Authorization header
```

### Security Best Practices

- **Never commit .ionapi files to git** (add `Credentials/` to .gitignore)
- **Store in Credentials/ folder** (excluded from version control)
- **Use service accounts** (not user accounts)
- **Rotate credentials regularly** per security policy
- **Monitor token usage** for security audits
- **NEVER log credentials or tokens** in work unit logs or console output
- **Read credentials at runtime** from .ionapi files (never hardcode)
- **Validate .gitignore** includes `Credentials/` folder before committing code

---

## IPA Integration Patterns

**AI Assistant Action**: Use these patterns as templates when implementing Data Fabric integrations in IPA processes.

### Pattern 1: Compass Query with Pagination

**Use Case**: Extract large dataset (>10K records) from Data Lake

```text
1. OAuth2 Token Acquisition (WEBRN)
   - POST to token endpoint
   - Store access_token

2. Submit Query (WEBRN)
   - POST /DATAFABRIC/compass/v2/jobs/
   - Body: {"query": "SELECT ...", "records": 0}
   - Store queryId

3. Poll Status (WEBRN + Loop)
   - GET /jobs/{queryId}/status/?timeout=25
   - Loop until status = FINISHED or FAILED
   - Add 1-second delay between polls

4. Retrieve Results (WEBRN + Pagination Loop)
   - Initialize: offset=0, limit=100000
   - Loop:
     - GET /jobs/{queryId}/result/?offset={offset}&limit={limit}
     - Process page data (ASSGN)
     - Write to file (ACCFIL - append mode)
     - Clear variables (ASSGN: set response = null, set data = null)
     - offset += limit
     - Continue until no more data

5. Output (ACCFIL/FTP)
   - Write final file or send to destination
```

### Pattern 2: Data Lake Object Retrieval

**Use Case**: Retrieve specific BOD payloads (<10K records)

```text
1. OAuth2 Token Acquisition (WEBRN)

2. Query Metadata (WEBRN)
   - GET /datalake/v1/dataobjects?filter=(dl_document_name eq 'GLJournalEntry' and dl_document_date ge '2024-01-01')
   - Store dl_id list

3. Loop Through Objects (Loop + WEBRN)
   - For each dl_id:
     - GET /datalake/v1/dataobjects/{dl_id}
     - Process NDJSON/JSON data (ASSGN)
     - Write to file (ACCFIL)

4. Output (ACCFIL/FTP)
```

### Pattern 3: ION BOD Investigation

**Use Case**: Troubleshoot data quality issues by comparing raw BODs with processed data

```text
1. OAuth2 Token Acquisition (WEBRN)

2. Query ION OneView (WEBRN)
   - GET /IONSERVICES/oneviewapi/data?filter=(document_type eq 'Sync.GLJournalEntry' and message_date ge '2024-01-01')
   - Store message_id list

3. Download Raw BODs (Loop + WEBRN)
   - For each message_id:
     - GET /data/streamDocumentPayload?messageId={message_id}
     - Store raw BOD

4. Query Data Lake (WEBRN)
   - GET /datalake/v1/dataobjects?filter=(dl_document_name eq 'GLJournalEntry')
   - Store processed data

5. Compare Data (ASSGN)
   - Identify missing fields
   - Identify transformation errors
   - Determine if issue is in source or processing

6. Report Findings (Email/File)
   - If raw BOD is incorrect → Source system issue
   - If processed data is incorrect → IPA/Data Fabric issue
```

### Pattern 4: Schema Discovery Before Query

**Use Case**: Discover schema before writing Compass query

```text
1. OAuth2 Token Acquisition (WEBRN)

2. Get Schema (WEBRN)
   - GET /datacatalog/v1/object/GLJournalEntry/schema
   - Store column names and types

3. Build Compass Query (ASSGN)
   - Use correct column names from schema
   - Add CAST for numeric columns
   - Build WHERE clause with correct field names

4. Execute Compass Query (WEBRN)
   - Follow Pattern 1 (Compass Query with Pagination)
```

### Pattern 5: Hybrid IPA + Orchestrator

**Use Case**: User triggers extract from IPA, Orchestrator handles large-scale processing

```text
IPA Process:
1. User Action: "Generate Report"
2. Prepare Parameters (ASSGN)
   - Date range, filters, output path
3. Trigger Orchestrator Flow (WEBRN)
   - POST /orchestrator/v1/flows/{flowName}/execute
   - Pass parameters
   - Store executionId
4. Notify User (Email)
   - "Report generation started. You'll receive notification when complete."
5. End Process

Orchestrator Flow (runs independently):
1. Extract data (handles pagination automatically)
2. Transform data
3. Upload to SFTP/S3
4. Send completion email to user
```

**AI Assistant Note**: This pattern avoids IPA memory limits while maintaining user-triggered workflow.

---

## Common Pitfalls and Solutions

**AI Assistant Action**: Check for these common pitfalls when reviewing or implementing Data Fabric integrations.

### Pitfall 1: Using Data Lake API for Large Datasets

**Problem**: Data Lake API has 10K record limit, user needs 100K+ records

**Symptom**: Query returns only 10K records, missing data

**Solution**: Use Compass API for >10K records with pagination

**AI Assistant Action**: When user requests >10K records, immediately recommend Compass API

### Pitfall 2: Not Implementing Pagination

**Problem**: Only retrieving first 100K rows from Compass, missing remaining data

**Symptom**: Report shows 100K records but user expects 500K

**Solution**: Loop through all pages using offset/limit until no more data

**AI Assistant Action**: Always implement pagination loop in Compass queries

### Pitfall 3: Forgetting Schema Discovery

**Problem**: Writing Compass queries without knowing column names/types

**Symptom**: Query fails with "column not found" or type conversion errors

**Solution**: Always call Data Catalog API first to get schema

**AI Assistant Action**: Include Data Catalog API call before Compass query in implementation pattern

### Pitfall 4: Rate Limit Violations

**Problem**: Hitting rate limits (HTTP 429 Too Many Requests)

**Symptom**: API calls fail intermittently with 429 errors

**Solution**: Add 100-500ms delays between API calls, implement exponential backoff

**AI Assistant Action**: Include delay logic in pagination loops

### Pitfall 5: Token Expiration

**Problem**: OAuth2 token expires after 2 hours during long-running process

**Symptom**: API calls fail with 401 Unauthorized after 2 hours

**Solution**: Implement token refresh logic or re-authenticate

**AI Assistant Action**: For processes >2 hours, add token refresh logic

### Pitfall 6: Incorrect Filter Syntax

**Problem**: Using SQL WHERE syntax in Data Lake/ION OneView filters

**Symptom**: Filter query fails with syntax error

**Solution**: Use `(field_name operator 'value')` syntax, not SQL WHERE clause

**Example**:

```text
❌ Wrong: filter=document_type = 'Sync.GLJournalEntry'
✅ Correct: filter=(document_type eq 'Sync.GLJournalEntry')

❌ Wrong: filter=message_date >= '2024-01-01' AND message_date <= '2024-12-31'
✅ Correct: filter=(message_date ge '2024-01-01' and message_date le '2024-12-31')
```

**AI Assistant Action**: Always use correct filter syntax for Data Lake and ION OneView APIs

### Pitfall 7: Not Clearing Variables in Pagination Loops

**Problem**: Memory accumulates in IPA work unit during pagination

**Symptom**: Work unit fails with memory error after processing many pages

**Solution**: Clear variables after each page (set response = null, set data = null)

**AI Assistant Action**: Include variable clearing in pagination loop pattern

### Pitfall 8: Using IPA for 1M+ Record Extracts

**Problem**: IPA work unit hits 100GB memory limit

**Symptom**: Work unit fails with memory error during large extract

**Solution**: Use Data Orchestrator or Data Warehouse instead

**AI Assistant Action**: Recommend Data Orchestrator for >1M records, even if user asks for IPA solution

### Pitfall 9: Not Handling Query Timeouts

**Problem**: Compass query times out after 60 minutes

**Symptom**: Query status shows FAILED with timeout error

**Solution**: Optimize query (add indexes, reduce date range) or split into smaller queries

**AI Assistant Action**: Recommend query optimization or splitting for long-running queries

### Pitfall 10: Hardcoding Credentials

**Problem**: Hardcoding OAuth2 credentials in IPA process

**Symptom**: Security risk, credentials exposed in process definition

**Solution**: Store credentials in .ionapi file, read at runtime

**AI Assistant Action**: Always use .ionapi file pattern for credential management

## Best Practices

**AI Assistant Action**: Follow these best practices when implementing Data Fabric integrations.

### Query Optimization

1. **Use LIMIT for pagination** - Always paginate large result sets (100K rows/page)
2. **Select specific columns** - Avoid SELECT *, specify only needed columns
3. **Filter early with WHERE clauses** - Reduce data volume before processing
4. **Use long-polling for status checks** - Set timeout=25 to reduce API calls
5. **Add indexes** - For recurring queries, consider Data Warehouse views with indexes

### Rate Limiting

1. **Add delays between API calls** - 100-500ms recommended for pagination loops
2. **Monitor for HTTP 429** - Implement exponential backoff when rate limited
3. **Use batch operations** - Combine multiple operations when possible
4. **Respect rate limits** - Compass: 100 submit/min, Ingestion: 200/min

### Error Handling

1. **Retry on transient failures** - HTTP 500, 502, 503 should trigger retry
2. **Log transaction IDs** - Include in error logs for support cases
3. **Handle query timeouts gracefully** - Implement timeout detection and recovery
4. **Validate responses** - Check for null/empty responses before processing
5. **Implement circuit breakers** - Stop retrying after max attempts

### Data Considerations

1. **Account for replication lag** - Data may not be immediately available
2. **Use CAST for type conversions** - Explicit type conversion prevents errors
3. **Handle NULL values** - Check for nulls before processing
4. **Monitor schema changes** - Re-run Data Catalog queries periodically
5. **Validate data quality** - Compare raw BODs with processed data when issues arise

### Security

1. **Never commit .ionapi files** - Add to .gitignore
2. **Use service accounts** - Not user accounts for API access
3. **Rotate credentials regularly** - Follow security best practices
4. **Monitor token usage** - Track API calls for security audits
5. **Use HTTPS only** - Never use HTTP for API calls

### Performance

1. **Use compression** - Accept gzip encoding for large responses
2. **Parallel processing** - Use Data Orchestrator parallel tasks when possible
3. **Cache schema metadata** - Don't query Data Catalog on every execution
4. **Optimize queries** - Use EXPLAIN to understand query performance
5. **Monitor execution times** - Track and optimize slow queries

### Documentation

1. **Document API endpoints** - Keep track of which APIs are used
2. **Version control flows** - Export Data Orchestrator flows to version control
3. **Document filter syntax** - Keep examples for team reference
4. **Track schema changes** - Document when schemas change
5. **Maintain runbooks** - Document troubleshooting procedures

---

**Reference Documentation**: All API specs available at `D:\Kiro\WorkUnit_Analyzer_ReferenceDocuments\DataFabric_API\`
