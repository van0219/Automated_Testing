---
inclusion: auto
keywords: json, test scenarios, validation, generation, blocking requirement, complete generation
description: JSON generation best practices for test scenarios with blocking requirements for complete generation
---

# JSON Generation Best Practices

## Critical Rule: Complete Generation Required

**BLOCKING REQUIREMENT FOR AUTOMATION TESTING:**

When generating JSON test scenario files for real-world automation testing, you MUST:
- Generate the COMPLETE JSON file with ALL scenarios
- NO "simpler versions" or partial implementations
- NO suggestions for manual completion
- The entire purpose of automation is to eliminate manual work

**Why This Matters:**
- These JSON files drive automated test execution
- Incomplete files break the automation framework
- Manual completion defeats the purpose of automation
- Real-world testing requires complete, production-ready files

**If You Cannot Complete:**
- STOP and explain why
- DO NOT proceed with incomplete solutions
- DO NOT suggest "you can add the rest manually"

## Root Cause Analysis

When generating JSON test scenario files, two main issues can occur:

### Issue 1: Improper fsAppend Usage
**Problem**: Using `fsAppend` after closing braces `}]` creates invalid JSON
**Example of WRONG approach**:
```
File content: {...}]
fsAppend: ,{...}  ← This goes AFTER the closing braces!
Result: {...}],{...}  ← Invalid JSON
```

**Solution**: Always use `fsWrite` for complete JSON generation, not `fsAppend`

### Issue 2: PowerShell String Escaping
**Problem**: Complex Python commands with quotes fail in PowerShell
**Example of WRONG approach**:
```powershell
python -c "import json; print(f'Count: {data[\"scenarios\"]}')"
# Fails due to nested quotes and string interpolation
```

**Solution**: Create dedicated Python utility scripts instead

## Best Practices

### 1. Generate Complete JSON Files

**DO THIS**:
```python
# Generate entire JSON structure at once
fsWrite(path, complete_json_content)
```

**NOT THIS**:
```python
# Don't append to JSON files
fsWrite(path, partial_json)
fsAppend(path, more_json)  # ❌ Creates invalid JSON
```

### 2. Use Utility Scripts for Validation

**Created**: `ReusableTools/validate_json.py`

**Usage**:
```bash
python ReusableTools/validate_json.py <json_file_path>
```

**Benefits**:
- No PowerShell escaping issues
- Clear error messages
- Automatic summary generation
- Reusable across all projects

### 3. JSON Generation Workflow

**Correct workflow**:
1. Parse source document (TES-070, requirements, etc.)
2. Build complete Python dict/JSON structure in memory
3. Write entire structure with `fsWrite` in ONE operation
4. Validate with `validate_json.py`
5. Report summary to user

**Example**:
```python
# Build complete structure
scenarios = []
for scenario_data in parsed_scenarios:
    scenarios.append(build_scenario(scenario_data))

complete_json = {
    "interface_id": "EXT_FIN_004",
    "scenarios": scenarios
}

# Write once
fsWrite(path, json.dumps(complete_json, indent=2))

# Validate
executePwsh("python ReusableTools/validate_json.py " + path)
```

### 4. Avoid Complex PowerShell Commands

**DON'T DO THIS**:
```powershell
python -c "import json; f=open('file.json'); data=json.load(f); print(f'Count: {len(data[\"scenarios\"])}')"
```

**DO THIS INSTEAD**:
```bash
# Use dedicated utility script
python ReusableTools/validate_json.py file.json
```

## Prevention Checklist

Before generating JSON files:
- [ ] Plan complete structure first
- [ ] Use `fsWrite` for entire file (not `fsAppend`)
- [ ] Validate with `validate_json.py` utility
- [ ] Avoid complex inline Python in PowerShell
- [ ] Test with small example first if unsure

## Recovery from Errors

If JSON generation fails:
1. Delete the invalid file
2. Regenerate with `fsWrite` (complete structure)
3. Validate with utility script
4. Confirm with user before proceeding

## Related Tools

- `ReusableTools/validate_json.py` - JSON validation utility
- `ReusableTools/tes070_analyzer.py` - TES-070 document parser
- `ReusableTools/build_test_scenarios.py` - Test scenario builder

## Summary

**Key Principle**: Generate JSON files completely in one operation, validate with dedicated utilities, avoid complex PowerShell string manipulation.
