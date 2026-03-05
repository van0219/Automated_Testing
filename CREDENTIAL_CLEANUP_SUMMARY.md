# Credential Cleanup Summary

## Changes Made

### 1. SONH Project Credentials Cleaned Up

**Files Updated:**
- `Projects/SONH/Credentials/.env.fsm`
- `Projects/SONH/Credentials/.env.passwords`

**Changes:**
- ❌ Removed: `ACUITY_TST_URL`, `ACUITY_TST_USERNAME`, `ACUITY_TST_PASSWORD`
- ✅ Kept: `SONH_URL`, `SONH_USERNAME`, `SONH_PASSWORD`
- Simplified to single client-based naming convention

**Before:**
```
ACUITY_TST_URL=...
ACUITY_TST_USERNAME=...
ACUITY_TST_PASSWORD=...
SONH_URL=...
SONH_USERNAME=...
SONH_PASSWORD=...
```

**After:**
```
SONH_URL=...
SONH_USERNAME=...
SONH_PASSWORD=...
```

### 2. New Project Setup Script Updated

**File:** `ReusableTools/new_project_setup.py`

**Changes:**
- Simplified credential file generation
- Uses only client name as prefix (e.g., `SONH_URL`, `TAMICS10_URL`)
- No longer generates multiple environment prefixes
- Password stored only in `.env.passwords` (not referenced in `.env.fsm`)

**Generated Credential Format:**
```
# .env.fsm
{CLIENT_NAME}_URL=...
{CLIENT_NAME}_USERNAME=...

# .env.passwords
{CLIENT_NAME}_PASSWORD=...
```

### 3. Testing Hooks Updated

**Files Updated:**
- `.kiro/hooks/approval-step2-execute-tests.kiro.hook`
- `.kiro/hooks/interface-step3-execute-tests-fsm.kiro.hook`

**Changes:**
- Changed `environment='ACUITY_TST'` to `environment='{ClientName}'`
- Framework now uses client name to look up credentials
- Consistent naming: SONH project uses SONH credentials

**Before:**
```python
orchestrator = TestOrchestrator(
    client_name='{ClientName}',
    environment='ACUITY_TST',  # hardcoded
    logger=logger
)
```

**After:**
```python
orchestrator = TestOrchestrator(
    client_name='{ClientName}',
    environment='{ClientName}',  # uses client name
    logger=logger
)
```

## Impact

### For Existing Projects (SONH)
- ✅ Credentials simplified and cleaned up
- ✅ No more confusing ACUITY_TST references
- ✅ Framework will now use `SONH` as environment parameter
- ✅ Credentials loaded correctly: `SONH_URL`, `SONH_USERNAME`, `SONH_PASSWORD`

### For New Projects
- ✅ Cleaner credential files generated
- ✅ Single naming convention: `{CLIENT_NAME}_*`
- ✅ No duplicate or legacy formats
- ✅ Consistent with framework expectations

## Testing

To verify the changes work correctly:

1. **Test SONH Project:**
   ```
   Run "Approval Step 2: Execute Approval Tests" hook
   Select SONH client
   Select EXT_FIN_004_auto_approval_test.json
   Framework should load credentials using SONH prefix
   ```

2. **Test New Project Setup:**
   ```
   Run "New Project Setup" hook
   Create a test project (e.g., "TEST_CLIENT")
   Verify generated files use TEST_CLIENT_* naming
   ```

## Credential Naming Convention

**Standard Format:**
- `{CLIENT_NAME}_URL` - FSM portal URL
- `{CLIENT_NAME}_USERNAME` - FSM login username
- `{CLIENT_NAME}_PASSWORD` - FSM login password

**Examples:**
- SONH project: `SONH_URL`, `SONH_USERNAME`, `SONH_PASSWORD`
- TAMICS10 project: `TAMICS10_URL`, `TAMICS10_USERNAME`, `TAMICS10_PASSWORD`
- ACUITY project: `ACUITY_URL`, `ACUITY_USERNAME`, `ACUITY_PASSWORD`

**Multiple Environments (if needed):**
If a client has multiple environments (TST, PRD, etc.), use:
- `{CLIENT_NAME}_TST_URL`, `{CLIENT_NAME}_TST_USERNAME`, `{CLIENT_NAME}_TST_PASSWORD`
- `{CLIENT_NAME}_PRD_URL`, `{CLIENT_NAME}_PRD_USERNAME`, `{CLIENT_NAME}_PRD_PASSWORD`

Then pass `environment='{CLIENT_NAME}_TST'` or `environment='{CLIENT_NAME}_PRD'` to the framework.

## Security Reminder

⚠️ **NEVER commit credential files:**
- `.env.fsm`
- `.env.passwords`
- `*.ionapi`

These are already in `.gitignore` at workspace root.
