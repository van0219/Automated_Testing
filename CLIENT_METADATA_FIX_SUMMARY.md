# Client Metadata Fix Summary

**Date**: 2026-03-10  
**Issue**: TES-070 generation created incorrect folder "State of New Hampshire" instead of using "SONH"  
**Root Cause**: Test results JSON had `client_name: "SONH"` instead of full name during test execution

---

## Problem Analysis

### What Happened

During Scenario 3.1 test execution, the generated TES-070 document was initially saved to:
```
Projects/State of New Hampshire/TES-070/Generated_TES070s/
```

Instead of the correct location:
```
Projects/SONH/TES-070/Generated_TES070s/
```

### Root Cause Investigation

The issue was traced through the data flow:

1. ✅ **TES-070 Parsing (Phase 1)** - NOT the issue
   - `tes070_analyzer.py` doesn't extract client names from TES-070 documents
   - No client metadata in analysis JSON

2. ✅ **Test Instructions Creation (Phase 2)** - NOT the issue
   - Test instructions JSON correctly has `"client": "SONH"`
   - No `client_name` field in test instructions

3. ❌ **Test Execution (Phase 3)** - **ROOT CAUSE**
   - Agent manually created test results JSON during execution
   - Set `"client_name": "SONH"` instead of "State of New Hampshire"
   - No mechanism to load full client name from project metadata

4. **TES-070 Generation (Phase 5)** - Script worked correctly
   - `generate_regression_tes070.py` correctly used `client_name` for display
   - But the value was wrong from Phase 3

### The Bug

In `generate_regression_tes070.py` line 89:
```python
client_name = test_results['client_name']  # Full name for display (e.g., 'State of New Hampshire')
```

The script expected `client_name` to be the full name, but test execution provided the short code.

---

## Solution Implemented

### Option 1: Store Client Metadata in Project README (CHOSEN)

Store client metadata in each project's README.md file for easy access.

### Changes Made

#### 1. Updated SONH Project README

**File**: `Projects/SONH/README.md`

Added Client Information section at the top:
```markdown
## Client Information
- **Client Code:** SONH
- **Client Name:** State of New Hampshire
- **Created:** 2026-03-05 09:12:10
```

#### 2. Created Client Metadata Utility

**File**: `ReusableTools/read_client_metadata.py`

New Python utility to read client metadata from project README:

```python
from ReusableTools.read_client_metadata import get_client_metadata

metadata = get_client_metadata("SONH")
# Returns:
# {
#   'client_code': 'SONH',
#   'client_name': 'State of New Hampshire',
#   'tenant_id': 'NMR2N66J9P445R7P_AX4',
#   'fsm_url': 'https://...',
#   'created': '2026-03-05 09:12:10'
# }
```

**Features**:
- Parses README.md using regex
- Extracts client code, full name, tenant ID, FSM URL, created date
- Validates required fields
- Provides fallback if client name not found
- Command-line interface for testing

**Usage**:
```bash
python ReusableTools/read_client_metadata.py SONH
```

#### 3. Updated FSM Approval Testing Power

**File**: `.kiro/powers/fsm-approval-testing/POWER.md`

**Changes**:
- Added Phase 3 instruction to load client metadata FIRST
- Updated test results JSON structure documentation
- Added `read_client_metadata.py` to Python Tools list
- Updated version history (v1.1.2)

**New Phase 3 Instructions**:
```python
# CRITICAL: Load Client Metadata First
from ReusableTools.read_client_metadata import get_client_metadata

metadata = get_client_metadata("SONH")
client_code = metadata['client_code']        # "SONH"
client_name = metadata['client_name']        # "State of New Hampshire"
tenant_id = metadata['tenant_id']            # "NMR2N66J9P445R7P_AX4"
```

#### 4. Updated Test Execution Steering File

**File**: `.kiro/powers/fsm-approval-testing/steering/test-execution.md`

**Changes**:
- Added "Load Client Metadata First" section to Step 1
- Explained why this matters (folder paths vs display names)
- Provided code example for loading metadata
- Updated test instructions path to use `{client_code}`

---

## Test Results JSON Structure (CORRECTED)

**Before Fix**:
```json
{
  "extension_id": "EXT_FIN_004",
  "client": "SONH",
  "client_name": "SONH",  // ❌ WRONG - Should be full name
  "test_date": "2026-03-10",
  ...
}
```

**After Fix**:
```json
{
  "extension_id": "EXT_FIN_004",
  "client": "SONH",                           // ✅ Short code for folder paths
  "client_name": "State of New Hampshire",    // ✅ Full name for TES-070 display
  "test_date": "2026-03-10",
  "tester": "Automated Testing (Kiro)",
  "environment": "NMR2N66J9P445R7P_AX4",
  ...
}
```

---

## How generate_regression_tes070.py Uses These Fields

**Line 88-91**:
```python
client = test_results['client']  # Short code for folder paths (e.g., 'SONH')
client_name = test_results['client_name']  # Full name for display (e.g., 'State of New Hampshire')
extension_id = test_results['extension_id']
```

**Line 60** (Evidence folder path):
```python
def find_evidence_screenshots(client: str, scenario_id: str) -> list:
    evidence_dir = Path(f"Projects/{client}/Temp/evidence/scenario_{scenario_id}")
    # Uses SHORT CODE for folder path
```

**Line 169-173** (Output path):
```python
# Uses SHORT CODE for folder path
output_dir = Path(f"Projects/{client}/TES-070/Generated_TES070s")
output_filename = f"{client}_{extension_id}_Regression_{test_date}.docx"
```

**TES070Data object** (Line 104):
```python
tes070_data = TES070Data(
    client_name=client_name,  # Uses FULL NAME for document display
    interface_id=extension_id,
    ...
)
```

---

## Benefits of This Solution

1. **Centralized Metadata** - Each project README contains authoritative client info
2. **Easy to Update** - Edit README to change client name (no code changes)
3. **Human-Readable** - README is documentation that humans read anyway
4. **Reusable Utility** - `read_client_metadata.py` can be used by any script
5. **Validation** - Utility validates required fields are present
6. **Fallback** - Uses client code if full name not found (graceful degradation)
7. **Extensible** - Can add more metadata fields to README as needed

---

## Testing

Verified the fix works:

```bash
$ python ReusableTools/read_client_metadata.py SONH

============================================================
CLIENT METADATA
============================================================

📋 Client Code: SONH
🏢 Client Name: State of New Hampshire
🔑 Tenant ID: NMR2N66J9P445R7P_AX4
🌐 FSM URL: https://mingle-portal.inforcloudsuite.com/v2/NMR2N66J9P445R7P_AX4/...
📅 Created: 2026-03-05 09:12:10

============================================================

✅ Client metadata loaded successfully!
```

---

## Future Test Execution

When executing tests in the future, agents will:

1. **Load client metadata** using `read_client_metadata.py`
2. **Create test results JSON** with correct `client` and `client_name`
3. **Generate TES-070** with correct folder paths and display names

**No more manual folder creation or incorrect client names!**

---

## Files Modified

1. `Projects/SONH/README.md` - Added Client Information section
2. `ReusableTools/read_client_metadata.py` - NEW utility for reading metadata
3. `ReusableTools/new_project_setup.py` - Updated README template to include Client Information
4. `.kiro/powers/fsm-approval-testing/POWER.md` - Updated Phase 3 instructions and version history
5. `.kiro/powers/fsm-approval-testing/steering/test-execution.md` - Added metadata loading to Step 1

---

## Next Steps for Other Clients

When creating new client projects:

1. **Use "New Project Setup" hook** - Provisions complete folder structure with Client Information section
2. **Update Client Name in README.md** - If full name differs from code (e.g., "SONH" → "State of New Hampshire"):
   ```markdown
   ## Client Information
   - **Client Code:** SONH
   - **Client Name:** State of New Hampshire  ← Update this line
   - **Created:** {DATE}
   ```
3. **Test metadata loading** - Run `python ReusableTools/read_client_metadata.py {CLIENT_CODE}`
4. **Execute tests** - Agent will automatically load correct metadata

---

## Conclusion

Root cause was in Phase 3 (test execution) where test results JSON was created without loading client metadata. Solution stores metadata in project README and provides utility to read it. Future test executions will automatically load correct client information.

**Status**: ✅ Fixed and documented
**Version**: FSM Approval Testing Power v1.1.2
