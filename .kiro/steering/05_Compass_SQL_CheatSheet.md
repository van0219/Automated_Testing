---
inclusion: auto
name: compass-sql
description: Compass SQL dialect, Data Fabric queries, Data Lake operations, SQL syntax, JDBC connections. Use when writing Compass SQL queries, querying Data Fabric, or working with Infor OS data.
---

# Compass SQL CheatSheet

## Table of Contents

- [Critical Rules for AI](#critical-rules-for-ai)
- [Quick Reference](#quick-reference)
- [Object Naming Rules](#object-naming-rules)
- [Supported SQL Features](#supported-sql-features)
- [CAST and Type Conversion](#cast-and-type-conversion)
- [Common Query Patterns](#common-query-patterns)
  - [Pattern 1: Paginated Results](#pattern-1-paginated-results)
  - [Pattern 2: Cross-Format Join (JSON + DSV)](#pattern-2-cross-format-join-json--dsv)
  - [Pattern 3: Aggregation with Filtering](#pattern-3-aggregation-with-filtering)
  - [Pattern 4: Common Table Expression (CTE)](#pattern-4-common-table-expression-cte)
  - [Pattern 5: UNION for Combining Results](#pattern-5-union-for-combining-results)
- [Limitations](#limitations)
- [Connectivity](#connectivity)
- [AI Assistant Guidelines](#ai-assistant-guidelines)
- [SQL Query Visualization](#sql-query-visualization)

## Critical Rules for AI

**MUST KNOW UPFRONT:**

- **READ-ONLY**: No `INSERT`, `UPDATE`, `DELETE`, or `CREATE` statements
- **Case Rules**: Object/property names are case-insensitive, data values are case-sensitive
- **CAST Failures**: Return `NULL` instead of errors (always check for NULL after CAST)
- **Timeout**: 60-minute query timeout limit
- **Quote Names**: Use double quotes for names with spaces, hyphens, starting with numbers, or reserved words

**DO:**

- Use `CAST(column AS type)` for type conversions
- Use double quotes for problematic object/property names: `"Order Date"`
- Check for NULL after CAST operations
- Use `LIMIT` and `OFFSET` for pagination
- Join JSON and DSV objects freely

**DON'T:**

- Generate `INSERT`, `UPDATE`, `DELETE`, or DDL statements
- Assume CAST will error on failure (it returns NULL)
- Use single quotes for object names (use double quotes)
- Create duplicate property names differing only by case
- Expect window functions (limited/unclear support)

## Quick Reference

**Most Common Operations:**

```sql
-- Basic SELECT with filtering
SELECT column1, column2
FROM ObjectName
WHERE column1 = 'value'
ORDER BY column2 DESC
LIMIT 100;

-- Type conversion (returns NULL on failure)
SELECT CAST(dateColumn AS date) AS converted_date
FROM ObjectName
WHERE CAST(amountColumn AS decimal) > 100.00;

-- JOIN across object types
SELECT o1.property1, o2.property2
FROM JsonObject o1
INNER JOIN DsvObject o2 ON o1.key = o2.key;

-- Aggregation
SELECT category, COUNT(*) AS count, SUM(amount) AS total
FROM Sales
GROUP BY category
HAVING COUNT(*) > 10
ORDER BY total DESC;

-- Pagination
SELECT * FROM LargeObject
ORDER BY id
LIMIT 1000 OFFSET 0;  -- First page
```

## Object Naming Rules

**Valid Characters:**

| Object Names | Property Names |
| --- | --- |
| A-Z, a-z, 0-9, underscore `_` | A-Z, a-z, 0-9, underscore `_`, period `.`, space |

**When to Use Double Quotes:**

```sql
-- Names with spaces
SELECT "Order Date", "Customer Name" FROM Orders;

-- Names starting with numbers
SELECT "2024_Sales" FROM "2024_Data";

-- Reserved words
SELECT "SELECT", "FROM" FROM ReservedWordTable;

-- Names with hyphens
SELECT "order-id" FROM "customer-orders";
```

**Case Sensitivity:**

- Object names: `Orders`, `ORDERS`, `orders` are all the same
- Property names: `OrderDate`, `ORDERDATE`, `orderdate` are all the same
- Data values: `'Smith'` and `'SMITH'` are different

## Supported SQL Features

**Clauses:**

- `SELECT` / `SELECT DISTINCT`
- `FROM`
- `WHERE`
- `GROUP BY`
- `HAVING`
- `ORDER BY`
- `LIMIT` / `OFFSET` / `TOP`
- `UNION` / `UNION ALL`
- `EXCEPT`
- `INTERSECT`
- `WITH` (Common Table Expressions)

**Joins:**

- `INNER JOIN`
- `LEFT OUTER JOIN`
- `RIGHT JOIN`
- `CROSS JOIN`

**Functions:**

- **Aggregation**: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- **Math**: `+`, `-`, `*`, `/`, `ROUND`, `ABS`
- **Comparison**: `=`, `<>`, `<`, `<=`, `>`, `>=`
- **Logical**: `AND`, `OR`, `NOT`, `IN`, `LIKE`
- **Date/Time**: Current date/time, date arithmetic, date difference

**Subqueries:**

```sql
-- Subquery in WHERE
SELECT * FROM Orders
WHERE customerId IN (
  SELECT customerId FROM Customers WHERE region = 'West'
);

-- Subquery in FROM
SELECT sub.category, AVG(sub.total) AS avg_total
FROM (
  SELECT category, SUM(amount) AS total
  FROM Sales
  GROUP BY category
) sub
GROUP BY sub.category;
```

## CAST and Type Conversion

**Supported Types:**

- `varchar`
- `date`
- `datetime`
- `datetime2`
- `decimal`
- `integer`
- `bigint`

**CRITICAL**: CAST returns `NULL` on failure, not an error.

**Examples:**

```sql
-- Safe conversion with NULL check
SELECT 
  orderId,
  CAST(orderDate AS date) AS order_date,
  CAST(orderTotal AS decimal) AS total_decimal
FROM Orders
WHERE CAST(orderDate AS date) IS NOT NULL  -- Filter out failed conversions
  AND CAST(orderTotal AS decimal) > 100.00;

-- Convert datetime to string (CONVERT)
SELECT CONVERT(varchar, orderDateTime) AS date_string
FROM Orders;

-- Convert string to datetime
SELECT CAST('2024-01-15' AS date) AS parsed_date;
```

**Pattern for Safe Conversion:**

```sql
-- Always check for NULL after CAST in WHERE clause
WHERE CAST(column AS type) IS NOT NULL

-- Or use COALESCE for default values
SELECT COALESCE(CAST(amount AS decimal), 0.00) AS safe_amount
FROM Transactions;
```

## Common Query Patterns

### Pattern 1: Paginated Results

```sql
-- Page 1 (rows 1-1000)
SELECT * FROM LargeTable
ORDER BY id
LIMIT 1000 OFFSET 0;

-- Page 2 (rows 1001-2000)
SELECT * FROM LargeTable
ORDER BY id
LIMIT 1000 OFFSET 1000;
```

### Pattern 2: Cross-Format Join (JSON + DSV)

```sql
-- Join JSON object with DSV object
SELECT 
  json_obj.customerId,
  json_obj.customerName,
  dsv_obj.orderTotal
FROM CustomerJson json_obj
INNER JOIN OrdersDsv dsv_obj
  ON json_obj.customerId = dsv_obj.customerId
WHERE dsv_obj.orderDate >= '2024-01-01';
```

### Pattern 3: Aggregation with Filtering

```sql
-- Aggregate with HAVING clause
SELECT 
  productCategory,
  COUNT(*) AS order_count,
  SUM(CAST(orderTotal AS decimal)) AS total_sales
FROM Orders
WHERE CAST(orderDate AS date) >= '2024-01-01'
GROUP BY productCategory
HAVING COUNT(*) > 100
ORDER BY total_sales DESC
LIMIT 10;
```

### Pattern 4: Common Table Expression (CTE)

```sql
-- Use WITH for complex queries
WITH RecentOrders AS (
  SELECT 
    customerId,
    COUNT(*) AS order_count,
    SUM(CAST(total AS decimal)) AS total_spent
  FROM Orders
  WHERE CAST(orderDate AS date) >= '2024-01-01'
  GROUP BY customerId
)
SELECT 
  c.customerName,
  ro.order_count,
  ro.total_spent
FROM Customers c
INNER JOIN RecentOrders ro ON c.customerId = ro.customerId
WHERE ro.order_count > 5
ORDER BY ro.total_spent DESC;
```

### Pattern 5: UNION for Combining Results

```sql
-- Combine results from multiple sources
SELECT customerId, 'Active' AS status FROM ActiveCustomers
UNION ALL
SELECT customerId, 'Inactive' AS status FROM InactiveCustomers
ORDER BY customerId;
```

## Limitations

**Not Supported:**

- ❌ `INSERT`, `UPDATE`, `DELETE` statements
- ❌ DDL statements (`CREATE TABLE`, `ALTER TABLE`, etc.)
- ❌ Window functions (limited/unclear support)
- ❌ Stored procedures or user-defined functions
- ❌ Transactions or locking

**Constraints:**

- **Query Timeout**: 60 minutes maximum
- **API Pagination**: Max rows per page (varies by deployment)
- **Duplicate Names**: Cannot have property names differing only by case
- **CAST Behavior**: Returns NULL on failure (no error thrown)

**Comparison with Standard SQL:**

| Feature | Compass SQL | Standard SQL (Postgres/MySQL) |
| --- | --- | --- |
| DML (INSERT/UPDATE) | ❌ Not supported | ✅ Supported |
| Window Functions | ⚠️ Limited | ✅ Full support |
| Subqueries | ✅ Supported | ✅ Supported |
| CTEs (WITH) | ✅ Supported | ✅ Supported |
| Joins | ✅ INNER, LEFT, RIGHT, CROSS | ✅ Full support |
| CAST/CONVERT | ✅ Limited types | ✅ Extensive types |
| Case Sensitivity | Names: insensitive, Values: sensitive | Configurable |

## Connectivity

**JDBC Driver:**

```java
// Driver class
com.infor.idl.jdbc.Driver

// Connection string pattern
jdbc:infordatalake://<tenant-host>

// Example
jdbc:infordatalake://mytenant.inforcloudsuite.com
```

**Compass API (REST):**

- Endpoint: `https://<tenant>/IONAPI/compass/v2/queries`
- Authentication: OAuth2 bearer token
- Pagination: Use `LIMIT` and `OFFSET` in query
- Response: JSON with data array and metadata

**Query Editor:**

- Access via Infor OS Portal > Data Fabric > Compass
- Interactive query building and execution
- Export results to CSV/Excel

## AI Assistant Guidelines

**When generating Compass SQL queries:**

1. **Start with object metadata check**: Verify object exists in Data Catalog
2. **Use CAST defensively**: Always check for NULL after type conversion
3. **Quote problematic names**: Use double quotes for spaces, hyphens, numbers
4. **Add pagination**: Include `LIMIT` for large result sets
5. **Explain limitations**: Tell user if requested feature isn't supported (e.g., window functions)
6. **Provide NULL handling**: Show how to handle CAST failures

**Example AI Response Pattern:**

```text
I'll generate a Compass SQL query to [task]. Note that:
- Compass SQL is read-only (no INSERT/UPDATE)
- CAST returns NULL on failure, so I'll add NULL checks
- I'll use LIMIT for pagination

[Query here]

This query:
1. Casts dateColumn to date type (returns NULL if invalid)
2. Filters out NULL conversions in WHERE clause
3. Limits results to 1000 rows for performance
```

## SQL Query Visualization

When working with Compass SQL queries, you can visualize table relationships using the SQL to ERD Generator.

**Use Cases:**

- Document Data Fabric object relationships
- Visualize JOIN patterns in complex queries
- Show data flow for IPA processes
- Create reference diagrams for RICE specifications

**See Also:**

- `.kiro/steering/05_Compass_SQL_CheatSheet.md` - Compass SQL syntax and examples
- `.kiro/steering/07_Infor_OS_Data_Fabric_Guide.md` - Data Fabric architecture and APIs
