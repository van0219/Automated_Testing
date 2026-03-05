# FSM Testing Framework v2.0 - Quick Reference

## Architecture at a Glance

```
JSON → TestOrchestrator → Executor → StepEngine → ActionHandlers + ValidatorEngine
                                          ↓              ↓              ↓
                                      TestState    Integration    Evidence
```

## Key Components

| Component | Purpose | Key Methods |
|-----------|---------|-------------|
| **TestState** | Runtime variable management | `set()`, `get()`, `interpolate()` |
| **StepEngine** | Step execution orchestration | `execute_step()` |
| **ValidatorEngine** | Validation routing | `validate()` |
| **TestOrchestrator** | Main engine | `execute()` |
| **Executors** | Test type-specific logic | `execute_scenario()` |

## Action Handlers

| Handler | Purpose | State Updates |
|---------|---------|---------------|
| `SFTPUploadAction` | Upload file to SFTP | `uploaded_file`, `sftp_destination` |
| `SFTPDownloadAction` | Download file from SFTP | `downloaded_file`, `local_path` |
| `UIAction` | UI interactions | Varies by action |
| `APICallAction` | FSM API calls | `api_record_count`, `last_record_id` |
| `WaitAction` | Wait for conditions | `work_unit_id`, `work_unit_status` |
| `ValidationAction` | Explicit validation | None |

## Validators

| Validator | Purpose | Validates |
|-----------|---------|-----------|
| `APIValidator` | FSM data validation | Record count, status, field values |
| `UIValidator` | UI state verification | Element presence, text content |
| `FileValidator` | File operations | File existence, content |
| `WorkUnitValidator` | Work unit status | Completion, status values |

## State Variable Interpolation

**Syntax**: `{{state.variable_name}}`

**Example**:
```json
{
  "filters": {
    "RunGroup": "{{state.run_group}}",
    "WorkUnitID": "{{state.work_unit_id}}"
  }
}
```

**Common State Variables**:
- `run_group` - Unique test execution identifier
- `work_unit_id` - IPA work unit ID
- `uploaded_file` - Uploaded filename
- `api_record_count` - Number of records from API
- `work_unit_status` - Current work unit status

## Adaptive Polling Strategy

| Time Elapsed | Poll Interval | Rationale |
|--------------|---------------|-----------|
| 0-2 minutes | 10 seconds | Fast processes |
| 2-5 minutes | 30 seconds | Normal processes |
| 5+ minutes | 60 seconds | Slow processes |

**Configurable per step** via `poll_interval_seconds` parameter.

## Test Isolation

**Unique Identifier Format**: `AUTOTEST_<timestamp>_<random>`

**Example**: `AUTOTEST_20260305_153045_a1b2c3`

**Generated automatically** by executors and stored in TestState.

## MVP Implementation Order

1. **Week 1**: TestState, Logger, Exceptions, CredentialManager
2. **Week 2**: SFTPClient, FSMAPIClient, PlaywrightMCPClient, WorkUnitMonitor
3. **Week 3**: ValidatorEngine, Validators (File, WorkUnit, API), StepEngine
4. **Week 4**: Action Handlers, InboundExecutor, TestOrchestrator
5. **Week 5**: ScreenshotManager, LogCollector, TES070Generator
6. **Week 6**: End-to-end testing with POS Inventory scenario

## MVP Test Case

**POS Inventory Inbound Interface**:
1. Upload file to SFTP
2. Wait for File Channel trigger
3. Detect work unit creation
4. Wait for work unit completion
5. Validate records via FSM API
6. Capture screenshots
7. Generate TES-070

## Key Design Improvements (v1 → v2)

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Step Execution | Embedded | Centralized StepEngine |
| Validation | Mixed | Separate ValidatorEngine |
| State | Ad-hoc | TestState with interpolation |
| Polling | Fixed | Adaptive |
| Isolation | Manual | Auto-generated IDs |
| UI Automation | CSS selectors | MCP snapshot + refs |

## Critical Constraints

1. **No Compass Queries**: Use FSM APIs only (real-time)
2. **No WorkUnit API**: Use UI automation
3. **OAuth Token**: Refresh before expiration (3600s)
4. **Test Isolation**: Unique identifiers per execution
5. **Browser State**: Keep open across scenarios

## Common Patterns

### Execute Test
```bash
python ReusableTools/testing_framework/run_tests.py \
  --scenario Projects/SONH/TestScripts/inbound/INT_POS_001_test_scenarios.json \
  --environment ACUITY_TST
```

### Add Custom Action Handler
```python
class MyCustomAction(BaseAction):
    def execute(self, action_config: dict, state: TestState) -> ActionResult:
        # Implementation
        return ActionResult.success("Done", state_updates={"key": "value"})

# Register in StepEngine
step_engine.action_handlers['my_custom'] = MyCustomAction()
```

### Add Custom Validator
```python
class MyCustomValidator(BaseValidator):
    def validate(self, validation_config: dict, state: TestState) -> ValidationResult:
        # Implementation
        return ValidationResult.success("Validated")

# Register in ValidatorEngine
validator_engine.validators['my_custom'] = MyCustomValidator()
```

## Design Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| State variable collisions | Medium | Namespaced variables |
| Screenshot timing | Medium | Wait after UI actions |
| Token expiration | High | Proactive refresh at 50min |
| MCP disconnection | High | Health checks + reconnection |
| Test data isolation | High | Millisecond timestamps + random |
| Error recovery | High | Cleanup/teardown logic |

## See Also

- Full Architecture: `docs/FSM_TESTING_FRAMEWORK_ARCHITECTURE_V2.md`
- Original Architecture: `docs/FSM_TESTING_FRAMEWORK_ARCHITECTURE.md`
- JSON Schema Examples: `.kiro/templates/`
