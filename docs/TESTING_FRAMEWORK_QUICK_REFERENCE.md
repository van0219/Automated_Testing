# FSM Testing Framework - Quick Reference

## Architecture at a Glance

```
JSON Scenarios → TestOrchestrator → Executors → Integration Modules → TES-070
```

## Key Components

| Component | Purpose | Location |
|-----------|---------|----------|
| TestOrchestrator | Main engine | `testing_framework/orchestrator/test_orchestrator.py` |
| InboundExecutor | Inbound tests | `testing_framework/orchestrator/inbound_executor.py` |
| ApprovalExecutor | Approval tests | `testing_framework/orchestrator/approval_executor.py` |
| OutboundExecutor | Outbound tests | `testing_framework/orchestrator/outbound_executor.py` |
| FSMAPIValidator | Real-time validation | `testing_framework/integration/fsm_api_validator.py` |
| PlaywrightAutomation | UI automation | `testing_framework/integration/playwright_automation.py` |
| WorkUnitMonitor | Work unit polling | `testing_framework/integration/work_unit_monitor.py` |
| EvidenceCollector | Evidence aggregation | `testing_framework/evidence/evidence_collector.py` |
| TES070Generator | Document generation | `testing_framework/reporting/tes070_generator.py` |

## Action Types

| Type | Use For | Example |
|------|---------|---------|
| `sftp_upload` | Upload test file | Inbound interface file drop |
| `sftp_download` | Download output file | Outbound interface validation |
| `ui_action` | UI interaction | Navigate, click, type |
| `api_call` | FSM API operation | Trigger interface, query data |
| `wait` | Wait for condition | Work unit creation, file arrival |
| `validate` | Validation check | Data verification, status check |

## Validation Types

| Type | Use For | Example |
|------|---------|---------|
| `file_exists` | File presence | SFTP file uploaded |
| `api_query` | FSM data validation | Record count, status values |
| `ui_check` | UI element validation | Error message, button state |
| `work_unit_status` | Work unit completion | IPA execution success |

## Critical Constraints

1. **No Compass Queries**: Use FSM APIs only (Compass queries Data Lake, not real-time)
2. **No WorkUnit API**: Use UI automation (WorkUnit API not exposed)
3. **OAuth Token Management**: Refresh before expiration (3600s lifetime)
4. **Test Isolation**: Use unique RunGroup identifiers per execution
5. **Browser State**: Keep browser open across scenarios for efficiency

## Quick Start

```bash
# Execute test
python ReusableTools/testing_framework/run_tests.py \
  --scenario Projects/SONH/TestScripts/inbound/INT_FIN_013_test_scenarios.json \
  --environment ACUITY_TST

# Output
# - Logs: Projects/SONH/Temp/{interface_id}_{timestamp}/logs/
# - Screenshots: Projects/SONH/Temp/{interface_id}_{timestamp}/screenshots/
# - TES-070: Projects/SONH/TES-070/Generated_TES070s/
```

## Implementation Phases

1. **Foundation** (Weeks 1-2): Core structure, orchestrator, credentials
2. **Integration** (Weeks 3-4): FSM API, Playwright, work units, SFTP
3. **Executors** (Weeks 5-6): Inbound, approval, outbound executors
4. **Evidence** (Weeks 7-8): Screenshots, logs, TES-070 generation
5. **Testing** (Weeks 9-10): Real scenarios, refinement
6. **Production** (Weeks 11-12): Error handling, documentation, training

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Unified JSON schema | Consistency, maintainability, extensibility |
| Pluggable executors | Easy to add new test types |
| FSM API validation | Real-time, accurate results |
| Intelligent polling | Faster tests, reliable completion |
| Automated evidence | Complete audit trail |
| Structured logging | Debugging, analysis, audit |
| Centralized credentials | Security, maintainability |

## See Also

- Full Architecture: `docs/FSM_TESTING_FRAMEWORK_ARCHITECTURE.md`
- JSON Schema Examples: `.kiro/templates/`
- Current Implementation: `ReusableTools/automation_examples/`
