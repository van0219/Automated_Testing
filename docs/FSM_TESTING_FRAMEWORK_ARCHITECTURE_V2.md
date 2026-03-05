# FSM Automated Testing Framework Architecture v2.0

## Executive Summary

This document defines the **refined architecture** for the FSM automated testing framework, incorporating improvements for maintainability, extensibility, and reliability.

**Key Architectural Improvements (v2.0)**:
1. ✅ **StepEngine** - Centralized step execution with pluggable action handlers
2. ✅ **ValidatorEngine** - Separated validation logic with specialized validators
3. ✅ **TestState** - Runtime state management with variable interpolation
4. ✅ **Adaptive Polling** - Intelligent work unit monitoring
5. ✅ **Test Isolation** - Unique identifiers per execution
6. ✅ **Stable Element Detection** - MCP-first Playwright automation
7. ✅ **Minimal Viable Implementation** - Clear first milestone

**Design Principles**:
- **Separation of Concerns**: Actions, validations, and state management are independent
- **Pluggability**: Easy to add new action handlers and validators
- **Testability**: Each component can be tested in isolation
- **Maintainability**: Clear responsibilities, minimal coupling
- **Extensibility**: New test types require minimal changes

---

## Table of Contents

1. [Refined Architecture Overview](#refined-architecture-overview)
2. [Updated Module Structure](#updated-module-structure)
3. [Core Components](#core-components)
4. [Action Handlers](#action-handlers)
5. [Validators](#validators)
6. [Test State Management](#test-state-management)
7. [Execution Flow](#execution-flow)
8. [Minimal Viable Implementation](#minimal-viable-implementation)
9. [Design Weaknesses & Risks](#design-weaknesses--risks)
10. [Implementation Roadmap](#implementation-roadmap)

---

## Refined Architecture Overview

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     TEST DEFINITION LAYER                            │
│                    (JSON Test Scenarios)                             │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    TEST ORCHESTRATION LAYER                          │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │              TestOrchestrator                             │      │
│  │  - Parse scenarios                                        │      │
│  │  - Initialize TestState                                   │      │
│  │  - Route to executor                                      │      │
│  │  - Generate TES-070                                       │      │
│  └──────────────────────────────────────────────────────────┘      │
│         ↓                  ↓                  ↓                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Approval   │  │   Inbound    │  │   Outbound   │             │
│  │   Executor   │  │   Executor   │  │   Executor   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│         ↓                  ↓                  ↓                      │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │                   StepEngine                              │      │
│  │  - Read step configuration                                │      │
│  │  - Interpolate state variables                            │      │
│  │  - Route to action handler                                │      │
│  │  - Call validator engine                                  │      │
│  │  - Update test state                                      │      │
│  │  - Capture evidence                                       │      │
│  └──────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      ACTION HANDLER LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ SFTP Upload  │  │ SFTP Download│  │  UI Action   │             │
│  │   Action     │  │   Action     │  │              │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  API Call    │  │  Wait        │  │  Validation  │             │
│  │   Action     │  │  Action      │  │   Action     │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      VALIDATOR ENGINE LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │     API      │  │      UI      │  │     File     │             │
│  │  Validator   │  │  Validator   │  │  Validator   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐                                                   │
│  │  Work Unit   │                                                   │
│  │  Validator   │                                                   │
│  └──────────────┘                                                   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      INTEGRATION LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ FSM API      │  │ Playwright   │  │ Work Unit    │             │
│  │ Client       │  │ MCP Client   │  │ Monitor      │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ SFTP         │  │ Credential   │  │  TestState   │             │
│  │ Client       │  │ Manager      │  │              │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      EVIDENCE & REPORTING LAYER                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Screenshot   │  │     Log      │  │   TES-070    │             │
│  │  Manager     │  │  Collector   │  │  Generator   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```


### Component Flow

```
TestOrchestrator
    ↓
Initialize TestState (with unique identifiers)
    ↓
Select Executor (Inbound/Approval/Outbound)
    ↓
For each test step:
    ↓
StepEngine.execute_step(step, state)
    ↓
1. Interpolate state variables in step config
    ↓
2. Route to ActionHandler based on action.type
    ↓
3. ActionHandler executes and returns result
    ↓
4. Update TestState with action results
    ↓
5. Call ValidatorEngine with validation config
    ↓
6. ValidatorEngine routes to appropriate Validator
    ↓
7. Validator executes and returns ValidationResult
    ↓
8. Capture screenshot via ScreenshotManager
    ↓
9. Log step result
    ↓
Return StepResult (action + validation + evidence)
```

---

## Updated Module Structure

### Directory Structure

```
ReusableTools/
├── testing_framework/
│   ├── __init__.py
│   │
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   ├── test_orchestrator.py          # Main orchestration engine
│   │   ├── base_executor.py              # Base executor (minimal)
│   │   ├── inbound_executor.py           # Inbound-specific logic
│   │   ├── approval_executor.py          # Approval-specific logic
│   │   └── outbound_executor.py          # Outbound-specific logic
│   │
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── step_engine.py                # Step execution engine
│   │   ├── validator_engine.py           # Validation engine
│   │   └── test_state.py                 # Runtime state management
│   │
│   ├── actions/
│   │   ├── __init__.py
│   │   ├── base_action.py                # Abstract base action
│   │   ├── sftp_upload_action.py         # SFTP upload handler
│   │   ├── sftp_download_action.py       # SFTP download handler
│   │   ├── ui_action.py                  # UI interaction handler
│   │   ├── api_call_action.py            # FSM API call handler
│   │   ├── wait_action.py                # Wait condition handler
│   │   └── validation_action.py          # Explicit validation handler
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── base_validator.py             # Abstract base validator
│   │   ├── api_validator.py              # FSM API validation
│   │   ├── ui_validator.py               # UI state validation
│   │   ├── file_validator.py             # File presence/content validation
│   │   └── work_unit_validator.py        # Work unit completion validation
│   │
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── fsm_api_client.py             # FSM API client with OAuth
│   │   ├── playwright_mcp_client.py      # Playwright MCP wrapper
│   │   ├── work_unit_monitor.py          # Adaptive work unit polling
│   │   ├── sftp_client.py                # SFTP operations
│   │   └── credential_manager.py         # Credential loading
│   │
│   ├── evidence/
│   │   ├── __init__.py
│   │   ├── screenshot_manager.py         # Screenshot capture/organization
│   │   ├── log_collector.py              # Log aggregation
│   │   └── evidence_collector.py         # Evidence coordinator
│   │
│   ├── reporting/
│   │   ├── __init__.py
│   │   ├── tes070_generator.py           # TES-070 document generation
│   │   └── report_formatter.py           # Evidence formatting
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                     # Structured logging
│       ├── config.py                     # Configuration management
│       ├── exceptions.py                 # Custom exceptions
│       └── helpers.py                    # Utility functions
```

### Module Dependency Graph

```
TestOrchestrator
    ├── BaseExecutor
    │   ├── InboundExecutor
    │   ├── ApprovalExecutor
    │   └── OutboundExecutor
    ├── StepEngine
    │   ├── ActionHandlers (all)
    │   ├── ValidatorEngine
    │   │   └── Validators (all)
    │   └── TestState
    ├── ScreenshotManager
    ├── LogCollector
    ├── EvidenceCollector
    └── TES070Generator

ActionHandlers
    ├── FSMAPIClient
    ├── PlaywrightMCPClient
    ├── SFTPClient
    └── TestState

Validators
    ├── FSMAPIClient
    ├── PlaywrightMCPClient
    ├── WorkUnitMonitor
    ├── SFTPClient
    └── TestState

Integration Modules
    └── CredentialManager
```


---

## Core Components

### 1. TestState - Runtime State Management

**Purpose**: Track runtime variables generated during test execution and provide variable interpolation.

**Class Definition**:

```python
class TestState:
    """
    Runtime state management for test execution.
    
    Tracks variables generated during test execution and provides
    variable interpolation for JSON configurations.
    
    Example usage:
        state = TestState()
        state.set("run_group", "AUTOTEST_20260305_1530")
        state.set("work_unit_id", "637305")
        
        # Interpolate in config
        config = {"filters": {"RunGroup": "{{state.run_group}}"}}
        interpolated = state.interpolate(config)
        # Result: {"filters": {"RunGroup": "AUTOTEST_20260305_1530"}}
    """
    
    def __init__(self):
        self._state = {}
        self._history = []  # Track state changes for debugging
    
    def set(self, key: str, value: Any) -> None:
        """Set a state variable"""
        old_value = self._state.get(key)
        self._state[key] = value
        self._history.append({
            'timestamp': datetime.now(),
            'key': key,
            'old_value': old_value,
            'new_value': value
        })
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a state variable"""
        return self._state.get(key, default)
    
    def has(self, key: str) -> bool:
        """Check if state variable exists"""
        return key in self._state
    
    def interpolate(self, config: Union[dict, str]) -> Union[dict, str]:
        """
        Interpolate state variables in configuration.
        
        Supports {{state.variable_name}} syntax.
        
        Args:
            config: Dictionary or string with {{state.key}} placeholders
        
        Returns:
            Configuration with interpolated values
        """
        if isinstance(config, str):
            return self._interpolate_string(config)
        elif isinstance(config, dict):
            return {k: self.interpolate(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self.interpolate(item) for item in config]
        else:
            return config
    
    def _interpolate_string(self, text: str) -> str:
        """Interpolate state variables in string"""
        import re
        
        def replace_var(match):
            var_name = match.group(1)
            if not self.has(var_name):
                raise ValueError(f"State variable not found: {var_name}")
            return str(self.get(var_name))
        
        # Match {{state.variable_name}}
        pattern = r'\{\{state\.([a-zA-Z_][a-zA-Z0-9_]*)\}\}'
        return re.sub(pattern, replace_var, text)
    
    def get_all(self) -> dict:
        """Get all state variables"""
        return self._state.copy()
    
    def get_history(self) -> list:
        """Get state change history for debugging"""
        return self._history.copy()
    
    def clear(self) -> None:
        """Clear all state variables"""
        self._state.clear()
        self._history.clear()
```

**Key Features**:
- Simple key-value storage
- Variable interpolation with `{{state.variable_name}}` syntax
- State change history for debugging
- Type-safe get/set operations


### 2. StepEngine - Step Execution Engine

**Purpose**: Centralized step execution with pluggable action handlers and validation.

**Class Definition**:

```python
class StepEngine:
    """
    Step execution engine.
    
    Responsibilities:
    - Read step configuration from JSON
    - Interpolate state variables
    - Route to appropriate action handler
    - Call validator engine
    - Update test state
    - Capture evidence
    
    Example usage:
        engine = StepEngine(state, validator_engine, screenshot_manager, logger)
        result = engine.execute_step(step_config)
    """
    
    def __init__(self, 
                 state: TestState,
                 validator_engine: ValidatorEngine,
                 screenshot_manager: ScreenshotManager,
                 logger: Logger,
                 action_handlers: dict = None):
        self.state = state
        self.validator_engine = validator_engine
        self.screenshot_manager = screenshot_manager
        self.logger = logger
        
        # Register action handlers
        self.action_handlers = action_handlers or self._default_action_handlers()
    
    def _default_action_handlers(self) -> dict:
        """Register default action handlers"""
        return {
            'sftp_upload': SFTPUploadAction(),
            'sftp_download': SFTPDownloadAction(),
            'ui_action': UIAction(),
            'api_call': APICallAction(),
            'wait': WaitAction(),
            'validate': ValidationAction()
        }
    
    def execute_step(self, step_config: dict) -> StepResult:
        """
        Execute a single test step.
        
        Args:
            step_config: Step configuration from JSON
        
        Returns:
            StepResult with action result, validation result, and evidence
        """
        step_number = step_config['step_number']
        description = step_config['description']
        
        self.logger.info(f"Executing step {step_number}: {description}")
        
        try:
            # 1. Interpolate state variables in step config
            interpolated_config = self.state.interpolate(step_config)
            
            # 2. Execute action
            action_result = self._execute_action(interpolated_config['action'])
            
            # 3. Update state with action results
            self._update_state_from_action(action_result)
            
            # 4. Capture screenshot
            screenshot_path = None
            if 'screenshot' in step_config:
                screenshot_path = self.screenshot_manager.capture(
                    name=step_config['screenshot'],
                    description=description
                )
            
            # 5. Execute validation
            validation_result = None
            if 'validation' in interpolated_config:
                validation_result = self.validator_engine.validate(
                    interpolated_config['validation']
                )
            
            # 6. Log result
            self.logger.info(f"Step {step_number} completed: {validation_result.status if validation_result else 'NO_VALIDATION'}")
            
            return StepResult(
                step_number=step_number,
                description=description,
                action_result=action_result,
                validation_result=validation_result,
                screenshot_path=screenshot_path,
                passed=validation_result.passed if validation_result else True
            )
            
        except Exception as e:
            self.logger.error(f"Step {step_number} failed: {str(e)}")
            return StepResult.failed(step_number, description, str(e))
    
    def _execute_action(self, action_config: dict) -> ActionResult:
        """Route to appropriate action handler"""
        action_type = action_config['type']
        
        handler = self.action_handlers.get(action_type)
        if not handler:
            raise ValueError(f"Unknown action type: {action_type}")
        
        return handler.execute(action_config, self.state)
    
    def _update_state_from_action(self, action_result: ActionResult) -> None:
        """Update test state with action results"""
        if action_result.state_updates:
            for key, value in action_result.state_updates.items():
                self.state.set(key, value)
```

**Key Features**:
- Pluggable action handlers (easy to add new actions)
- Automatic state variable interpolation
- Integrated validation
- Evidence capture
- Comprehensive error handling


### 3. ValidatorEngine - Validation Engine

**Purpose**: Separated validation logic with specialized validators.

**Class Definition**:

```python
class ValidatorEngine:
    """
    Validation engine.
    
    Responsibilities:
    - Route to appropriate validator based on validation type
    - Execute validation logic
    - Return structured validation results
    
    Example usage:
        engine = ValidatorEngine(state, logger)
        result = engine.validate(validation_config)
    """
    
    def __init__(self, 
                 state: TestState,
                 logger: Logger,
                 validators: dict = None):
        self.state = state
        self.logger = logger
        
        # Register validators
        self.validators = validators or self._default_validators()
    
    def _default_validators(self) -> dict:
        """Register default validators"""
        return {
            'api_query': APIValidator(),
            'ui_check': UIValidator(),
            'file_exists': FileValidator(),
            'work_unit_status': WorkUnitValidator()
        }
    
    def validate(self, validation_config: dict) -> ValidationResult:
        """
        Execute validation.
        
        Args:
            validation_config: Validation configuration from JSON
        
        Returns:
            ValidationResult with pass/fail and details
        """
        validation_type = validation_config['type']
        expected_result = validation_config.get('expected_result')
        
        self.logger.debug(f"Executing validation: {validation_type}")
        
        try:
            # Route to appropriate validator
            validator = self.validators.get(validation_type)
            if not validator:
                raise ValueError(f"Unknown validation type: {validation_type}")
            
            # Execute validation
            result = validator.validate(validation_config, self.state)
            
            # Log result
            if result.passed:
                self.logger.info(f"Validation passed: {result.message}")
            else:
                self.logger.warning(f"Validation failed: {result.message}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            return ValidationResult.failed(f"Validation error: {str(e)}")
```

**Key Features**:
- Pluggable validators (easy to add new validation types)
- Consistent validation result structure
- Comprehensive error handling
- Detailed logging

---

## Action Handlers

### Base Action Handler

```python
class BaseAction(ABC):
    """Abstract base class for action handlers"""
    
    @abstractmethod
    def execute(self, action_config: dict, state: TestState) -> ActionResult:
        """
        Execute action.
        
        Args:
            action_config: Action configuration from JSON
            state: Test state for variable access
        
        Returns:
            ActionResult with execution details and state updates
        """
        pass
```

### 1. SFTPUploadAction

```python
class SFTPUploadAction(BaseAction):
    """SFTP file upload action handler"""
    
    def __init__(self, sftp_client: SFTPClient = None):
        self.sftp_client = sftp_client or SFTPClient()
    
    def execute(self, action_config: dict, state: TestState) -> ActionResult:
        """
        Upload file to SFTP server.
        
        Config example:
        {
            "type": "sftp_upload",
            "parameters": {
                "test_data_file": "GLTRANSREL_valid.csv",
                "source_path": "Projects/SONH/TestScripts/test_data/",
                "destination_path": "/Infor_FSM/GLTransactionInterface/Inbound/"
            }
        }
        """
        params = action_config['parameters']
        
        # Build paths
        source_file = Path(params['source_path']) / params['test_data_file']
        destination_path = params['destination_path']
        
        # Upload file
        self.sftp_client.upload(source_file, destination_path)
        
        return ActionResult.success(
            message=f"Uploaded {source_file.name} to {destination_path}",
            state_updates={
                'uploaded_file': source_file.name,
                'sftp_destination': destination_path
            }
        )
```

### 2. APICallAction

```python
class APICallAction(BaseAction):
    """FSM API call action handler"""
    
    def __init__(self, fsm_api_client: FSMAPIClient = None):
        self.fsm_api_client = fsm_api_client or FSMAPIClient()
    
    def execute(self, action_config: dict, state: TestState) -> ActionResult:
        """
        Execute FSM API call.
        
        Config example:
        {
            "type": "api_call",
            "parameters": {
                "business_class": "GLTransactionInterface",
                "action": "List",
                "filters": {
                    "RunGroup": "{{state.run_group}}",
                    "Status": "2"
                }
            }
        }
        """
        params = action_config['parameters']
        
        business_class = params['business_class']
        action = params['action']
        filters = params.get('filters', {})
        
        # Execute API call
        response = self.fsm_api_client.call(
            business_class=business_class,
            action=action,
            filters=filters
        )
        
        # Extract useful data for state
        state_updates = {}
        if response.get('records'):
            state_updates['api_record_count'] = len(response['records'])
            # Store first record ID if available
            if response['records']:
                first_record = response['records'][0]
                if 'id' in first_record:
                    state_updates['last_record_id'] = first_record['id']
        
        return ActionResult.success(
            message=f"API call successful: {business_class}.{action}",
            data=response,
            state_updates=state_updates
        )
```


### 3. WaitAction

```python
class WaitAction(BaseAction):
    """Wait for condition action handler"""
    
    def __init__(self, work_unit_monitor: WorkUnitMonitor = None):
        self.work_unit_monitor = work_unit_monitor or WorkUnitMonitor()
    
    def execute(self, action_config: dict, state: TestState) -> ActionResult:
        """
        Wait for condition to be met.
        
        Config example:
        {
            "type": "wait",
            "target": "work_unit_creation",
            "parameters": {
                "process_name": "SONH_GLTransactionInterface",
                "timeout_seconds": 600,
                "poll_interval_seconds": 30
            }
        }
        """
        target = action_config['target']
        params = action_config['parameters']
        
        if target == 'work_unit_creation':
            result = self.work_unit_monitor.wait_for_creation(
                process_name=params['process_name'],
                timeout_seconds=params.get('timeout_seconds', 600)
            )
            
            return ActionResult.success(
                message=f"Work unit created: {result.work_unit_id}",
                data=result.to_dict(),
                state_updates={
                    'work_unit_id': result.work_unit_id,
                    'work_unit_status': result.status
                }
            )
        
        elif target == 'work_unit_completion':
            work_unit_id = state.get('work_unit_id')
            if not work_unit_id:
                raise ValueError("work_unit_id not found in state")
            
            result = self.work_unit_monitor.wait_for_completion(
                work_unit_id=work_unit_id,
                timeout_seconds=params.get('timeout_seconds', 600)
            )
            
            return ActionResult.success(
                message=f"Work unit completed: {work_unit_id}",
                data=result.to_dict(),
                state_updates={
                    'work_unit_status': result.status,
                    'work_unit_elapsed_time': result.elapsed_time
                }
            )
        
        else:
            raise ValueError(f"Unknown wait target: {target}")
```

### 4. UIAction

```python
class UIAction(BaseAction):
    """UI interaction action handler"""
    
    def __init__(self, playwright_client: PlaywrightMCPClient = None):
        self.playwright_client = playwright_client or PlaywrightMCPClient()
    
    def execute(self, action_config: dict, state: TestState) -> ActionResult:
        """
        Execute UI interaction.
        
        Config example:
        {
            "type": "ui_action",
            "parameters": {
                "action": "click",
                "element_description": "Submit button",
                "element_ref": "submit_btn_ref"
            }
        }
        """
        params = action_config['parameters']
        
        ui_action = params['action']
        element_ref = params.get('element_ref')
        
        if ui_action == 'click':
            self.playwright_client.click(element_ref)
            message = f"Clicked element: {params.get('element_description', element_ref)}"
        
        elif ui_action == 'type':
            text = params['text']
            self.playwright_client.type(element_ref, text)
            message = f"Typed text into element: {params.get('element_description', element_ref)}"
        
        elif ui_action == 'navigate':
            path = params['path']
            self.playwright_client.navigate(path)
            message = f"Navigated to: {path}"
        
        else:
            raise ValueError(f"Unknown UI action: {ui_action}")
        
        return ActionResult.success(message=message)
```

---

## Validators

### Base Validator

```python
class BaseValidator(ABC):
    """Abstract base class for validators"""
    
    @abstractmethod
    def validate(self, validation_config: dict, state: TestState) -> ValidationResult:
        """
        Execute validation.
        
        Args:
            validation_config: Validation configuration from JSON
            state: Test state for variable access
        
        Returns:
            ValidationResult with pass/fail and details
        """
        pass
```

### 1. APIValidator

```python
class APIValidator(BaseValidator):
    """FSM API validation"""
    
    def __init__(self, fsm_api_client: FSMAPIClient = None):
        self.fsm_api_client = fsm_api_client or FSMAPIClient()
    
    def validate(self, validation_config: dict, state: TestState) -> ValidationResult:
        """
        Validate FSM data via API.
        
        Config example:
        {
            "type": "api_query",
            "expected_result": "10 records with Status=2",
            "validation_query": {
                "business_class": "GLTransactionInterface",
                "filters": {
                    "RunGroup": "{{state.run_group}}"
                },
                "expected_count": 10,
                "expected_status": "2"
            }
        }
        """
        query = validation_config['validation_query']
        
        # Execute API query
        response = self.fsm_api_client.call(
            business_class=query['business_class'],
            action='List',
            filters=query['filters']
        )
        
        records = response.get('records', [])
        actual_count = len(records)
        
        # Validate count
        expected_count = query.get('expected_count')
        if expected_count is not None and actual_count != expected_count:
            return ValidationResult.failed(
                f"Expected {expected_count} records, found {actual_count}"
            )
        
        # Validate status
        expected_status = query.get('expected_status')
        if expected_status is not None:
            statuses = [r.get('Status') for r in records]
            if not all(s == expected_status for s in statuses):
                return ValidationResult.failed(
                    f"Not all records have Status={expected_status}"
                )
        
        return ValidationResult.success(
            f"Validated {actual_count} records with Status={expected_status}"
        )
```


### 2. WorkUnitValidator

```python
class WorkUnitValidator(BaseValidator):
    """Work unit completion validation"""
    
    def __init__(self, work_unit_monitor: WorkUnitMonitor = None):
        self.work_unit_monitor = work_unit_monitor or WorkUnitMonitor()
    
    def validate(self, validation_config: dict, state: TestState) -> ValidationResult:
        """
        Validate work unit status.
        
        Config example:
        {
            "type": "work_unit_status",
            "expected_result": "Work unit completed successfully",
            "validation_query": {
                "work_unit_id": "{{state.work_unit_id}}",
                "expected_status": "Completed"
            }
        }
        """
        query = validation_config['validation_query']
        
        work_unit_id = query.get('work_unit_id')
        if not work_unit_id:
            work_unit_id = state.get('work_unit_id')
        
        if not work_unit_id:
            return ValidationResult.failed("work_unit_id not found")
        
        # Get work unit status
        status = self.work_unit_monitor.get_status(work_unit_id)
        
        expected_status = query.get('expected_status', 'Completed')
        
        if status != expected_status:
            return ValidationResult.failed(
                f"Expected status '{expected_status}', found '{status}'"
            )
        
        return ValidationResult.success(
            f"Work unit {work_unit_id} has status '{status}'"
        )
```

### 3. FileValidator

```python
class FileValidator(BaseValidator):
    """File presence/content validation"""
    
    def __init__(self, sftp_client: SFTPClient = None):
        self.sftp_client = sftp_client or SFTPClient()
    
    def validate(self, validation_config: dict, state: TestState) -> ValidationResult:
        """
        Validate file existence or content.
        
        Config example:
        {
            "type": "file_exists",
            "expected_result": "File exists on SFTP",
            "validation_query": {
                "path": "/Infor_FSM/GLTransactionInterface/Inbound/{{state.uploaded_file}}"
            }
        }
        """
        query = validation_config['validation_query']
        file_path = query['path']
        
        # Check file existence
        exists = self.sftp_client.file_exists(file_path)
        
        if not exists:
            return ValidationResult.failed(f"File not found: {file_path}")
        
        return ValidationResult.success(f"File exists: {file_path}")
```

---

## Test State Management

### State Variable Lifecycle

```
Test Execution Start
    ↓
Initialize TestState
    ↓
Generate unique identifiers
    - run_group = AUTOTEST_<timestamp>
    - test_execution_id = <uuid>
    ↓
Store in state
    ↓
For each test step:
    ↓
    Interpolate state variables in config
    ↓
    Execute action
    ↓
    Action returns state_updates
    ↓
    Update TestState with new variables
    ↓
    Next step can reference new variables
    ↓
Test Execution Complete
```

### Example State Evolution

```python
# Initial state
state = TestState()
state.set("run_group", "AUTOTEST_20260305_1530")
state.set("test_execution_id", "a1b2c3d4-e5f6-7890-abcd-ef1234567890")

# After SFTP upload
state.set("uploaded_file", "GLTRANSREL_valid.csv")
state.set("sftp_destination", "/Infor_FSM/GLTransactionInterface/Inbound/")

# After work unit creation
state.set("work_unit_id", "637305")
state.set("work_unit_status", "Running")

# After work unit completion
state.set("work_unit_status", "Completed")
state.set("work_unit_elapsed_time", "00:05:23")

# After API validation
state.set("api_record_count", 10)
state.set("last_record_id", "GL_12345")

# State can be referenced in subsequent steps
# Example: "filters": {"RunGroup": "{{state.run_group}}"}
```


---

## Execution Flow

### Complete Inbound Interface Test Flow

```
1. TestOrchestrator.execute()
    ↓
2. Load JSON scenario
    ↓
3. Initialize TestState
    - Generate run_group: AUTOTEST_20260305_1530
    - Generate test_execution_id
    ↓
4. Select InboundExecutor
    ↓
5. InboundExecutor.execute_scenario(scenario)
    ↓
6. For each test step:
    ↓
    StepEngine.execute_step(step, state)
        ↓
        6.1. Interpolate state variables
            - Replace {{state.run_group}} with actual value
        ↓
        6.2. Execute action (e.g., sftp_upload)
            - SFTPUploadAction.execute()
            - Upload file to SFTP
            - Return ActionResult with state_updates
        ↓
        6.3. Update TestState
            - state.set("uploaded_file", "GLTRANSREL_valid.csv")
        ↓
        6.4. Capture screenshot
            - ScreenshotManager.capture("01_file_upload")
        ↓
        6.5. Execute validation (e.g., file_exists)
            - ValidatorEngine.validate()
            - FileValidator.validate()
            - Return ValidationResult
        ↓
        6.6. Log step result
        ↓
        6.7. Return StepResult
    ↓
7. Collect all StepResults
    ↓
8. Generate TES-070 document
    - TES070Generator.generate()
    - Embed screenshots
    - Format results
    ↓
9. Return TestResult
```

### Example: Inbound Interface Scenario Execution

**JSON Scenario**:
```json
{
  "interface_id": "INT_POS_001",
  "interface_name": "POS Inventory Inbound",
  "interface_type": "inbound",
  "scenarios": [
    {
      "scenario_id": "scenario_1",
      "title": "Successful Import",
      "test_steps": [
        {
          "step_number": "1",
          "description": "Upload valid CSV file to SFTP",
          "action": {
            "type": "sftp_upload",
            "parameters": {
              "test_data_file": "POS_INVENTORY_valid.csv",
              "source_path": "Projects/SONH/TestScripts/test_data/",
              "destination_path": "/Infor_FSM/POSInventory/Inbound/"
            }
          },
          "validation": {
            "type": "file_exists",
            "expected_result": "File uploaded successfully",
            "validation_query": {
              "path": "/Infor_FSM/POSInventory/Inbound/POS_INVENTORY_valid.csv"
            }
          },
          "screenshot": "01_file_upload"
        },
        {
          "step_number": "2",
          "description": "Wait for File Channel to trigger IPA",
          "action": {
            "type": "wait",
            "target": "work_unit_creation",
            "parameters": {
              "process_name": "SONH_POSInventoryInterface",
              "timeout_seconds": 600
            }
          },
          "validation": {
            "type": "work_unit_status",
            "expected_result": "Work unit created",
            "validation_query": {
              "work_unit_id": "{{state.work_unit_id}}",
              "expected_status": "Running"
            }
          },
          "screenshot": "02_work_unit_created"
        },
        {
          "step_number": "3",
          "description": "Wait for work unit completion",
          "action": {
            "type": "wait",
            "target": "work_unit_completion",
            "parameters": {
              "timeout_seconds": 600
            }
          },
          "validation": {
            "type": "work_unit_status",
            "expected_result": "Work unit completed successfully",
            "validation_query": {
              "expected_status": "Completed"
            }
          },
          "screenshot": "03_work_unit_completed"
        },
        {
          "step_number": "4",
          "description": "Verify data in FSM via API",
          "action": {
            "type": "api_call",
            "parameters": {
              "business_class": "POSInventoryInterface",
              "action": "List",
              "filters": {
                "RunGroup": "{{state.run_group}}",
                "Status": "2"
              }
            }
          },
          "validation": {
            "type": "api_query",
            "expected_result": "10 records with Status=2 (Posted)",
            "validation_query": {
              "business_class": "POSInventoryInterface",
              "filters": {
                "RunGroup": "{{state.run_group}}"
              },
              "expected_count": 10,
              "expected_status": "2"
            }
          },
          "screenshot": "04_data_verification"
        }
      ]
    }
  ]
}
```

**Execution Trace**:
```
[2026-03-05 15:30:00] TestOrchestrator: Starting test execution: INT_POS_001
[2026-03-05 15:30:00] TestState: Initialized with run_group=AUTOTEST_20260305_1530
[2026-03-05 15:30:00] InboundExecutor: Executing scenario: Successful Import
[2026-03-05 15:30:01] StepEngine: Executing step 1: Upload valid CSV file to SFTP
[2026-03-05 15:30:01] SFTPUploadAction: Uploading POS_INVENTORY_valid.csv
[2026-03-05 15:30:02] SFTPUploadAction: Upload successful
[2026-03-05 15:30:02] TestState: Set uploaded_file=POS_INVENTORY_valid.csv
[2026-03-05 15:30:02] ScreenshotManager: Captured 01_file_upload.png
[2026-03-05 15:30:02] FileValidator: Validating file existence
[2026-03-05 15:30:03] FileValidator: File exists: /Infor_FSM/POSInventory/Inbound/POS_INVENTORY_valid.csv
[2026-03-05 15:30:03] StepEngine: Step 1 completed: PASS
[2026-03-05 15:30:03] StepEngine: Executing step 2: Wait for File Channel to trigger IPA
[2026-03-05 15:30:03] WaitAction: Waiting for work unit creation (process: SONH_POSInventoryInterface)
[2026-03-05 15:35:15] WorkUnitMonitor: Work unit created: 637305
[2026-03-05 15:35:15] TestState: Set work_unit_id=637305
[2026-03-05 15:35:15] TestState: Set work_unit_status=Running
[2026-03-05 15:35:15] ScreenshotManager: Captured 02_work_unit_created.png
[2026-03-05 15:35:16] WorkUnitValidator: Validating work unit status
[2026-03-05 15:35:16] WorkUnitValidator: Work unit 637305 has status 'Running'
[2026-03-05 15:35:16] StepEngine: Step 2 completed: PASS
[2026-03-05 15:35:16] StepEngine: Executing step 3: Wait for work unit completion
[2026-03-05 15:35:16] WaitAction: Waiting for work unit completion (ID: 637305)
[2026-03-05 15:40:23] WorkUnitMonitor: Work unit 637305 completed
[2026-03-05 15:40:23] TestState: Set work_unit_status=Completed
[2026-03-05 15:40:23] TestState: Set work_unit_elapsed_time=00:05:07
[2026-03-05 15:40:23] ScreenshotManager: Captured 03_work_unit_completed.png
[2026-03-05 15:40:24] WorkUnitValidator: Work unit 637305 has status 'Completed'
[2026-03-05 15:40:24] StepEngine: Step 3 completed: PASS
[2026-03-05 15:40:24] StepEngine: Executing step 4: Verify data in FSM via API
[2026-03-05 15:40:24] APICallAction: Calling POSInventoryInterface.List
[2026-03-05 15:40:25] APICallAction: API call successful, 10 records returned
[2026-03-05 15:40:25] TestState: Set api_record_count=10
[2026-03-05 15:40:25] ScreenshotManager: Captured 04_data_verification.png
[2026-03-05 15:40:25] APIValidator: Validating API query results
[2026-03-05 15:40:26] APIValidator: Validated 10 records with Status=2
[2026-03-05 15:40:26] StepEngine: Step 4 completed: PASS
[2026-03-05 15:40:26] InboundExecutor: Scenario completed: PASS (4/4 steps passed)
[2026-03-05 15:40:26] TES070Generator: Generating TES-070 document
[2026-03-05 15:40:30] TES070Generator: Document generated: INT_POS_001_TES-070.docx
[2026-03-05 15:40:30] TestOrchestrator: Test execution complete: PASS
```


---

## Minimal Viable Implementation

### Phase 1: Core Framework (MVP)

**Goal**: Prove the architecture works with a single inbound interface test

**Modules to Implement**:

1. **TestState** (`engine/test_state.py`)
   - Variable storage (get/set/has)
   - Variable interpolation
   - State history tracking

2. **StepEngine** (`engine/step_engine.py`)
   - Step execution orchestration
   - Action handler routing
   - Validator engine integration
   - Evidence capture

3. **ValidatorEngine** (`engine/validator_engine.py`)
   - Validator routing
   - Result aggregation

4. **TestOrchestrator** (`orchestrator/test_orchestrator.py`)
   - JSON scenario parsing
   - TestState initialization
   - Executor selection
   - TES-070 generation

5. **InboundExecutor** (`orchestrator/inbound_executor.py`)
   - Scenario execution
   - Unique identifier generation
   - StepEngine integration

6. **Action Handlers**:
   - `SFTPUploadAction` (`actions/sftp_upload_action.py`)
   - `WaitAction` (`actions/wait_action.py`)
   - `APICallAction` (`actions/api_call_action.py`)

7. **Validators**:
   - `FileValidator` (`validators/file_validator.py`)
   - `WorkUnitValidator` (`validators/work_unit_validator.py`)
   - `APIValidator` (`validators/api_validator.py`)

8. **Integration Modules**:
   - `SFTPClient` (`integration/sftp_client.py`)
   - `FSMAPIClient` (`integration/fsm_api_client.py`)
   - `WorkUnitMonitor` (`integration/work_unit_monitor.py`) - with adaptive polling
   - `PlaywrightMCPClient` (`integration/playwright_mcp_client.py`)
   - `CredentialManager` (`integration/credential_manager.py`)

9. **Evidence & Reporting**:
   - `ScreenshotManager` (`evidence/screenshot_manager.py`)
   - `LogCollector` (`evidence/log_collector.py`)
   - `TES070Generator` (`reporting/tes070_generator.py`)

10. **Utilities**:
    - `Logger` (`utils/logger.py`)
    - `Exceptions` (`utils/exceptions.py`)

### MVP Test Case: POS Inventory Inbound Interface

**Test Scenario**:
1. Upload POS_INVENTORY_valid.csv to SFTP
2. Wait for File Channel to trigger IPA
3. Detect work unit creation
4. Wait for work unit completion (with adaptive polling)
5. Validate 10 records in POSInventoryInterface via FSM API
6. Capture screenshots at each step
7. Generate TES-070 document

**Success Criteria**:
- ✅ All 7 steps execute successfully
- ✅ State variables interpolated correctly
- ✅ Work unit monitoring uses adaptive polling
- ✅ FSM API validation returns correct results
- ✅ Screenshots captured at each step
- ✅ TES-070 document generated with proper formatting

### MVP Implementation Order

**Week 1: Foundation**
1. TestState class
2. Logger utility
3. Exceptions utility
4. CredentialManager

**Week 2: Integration Layer**
5. SFTPClient
6. FSMAPIClient (with OAuth)
7. PlaywrightMCPClient
8. WorkUnitMonitor (with adaptive polling)

**Week 3: Engines**
9. ValidatorEngine
10. FileValidator
11. WorkUnitValidator
12. APIValidator
13. StepEngine

**Week 4: Orchestration**
14. SFTPUploadAction
15. WaitAction
16. APICallAction
17. InboundExecutor
18. TestOrchestrator

**Week 5: Evidence & Reporting**
19. ScreenshotManager
20. LogCollector
21. TES070Generator

**Week 6: Testing & Refinement**
22. End-to-end test with POS Inventory scenario
23. Bug fixes and refinements
24. Documentation updates


---

## Design Weaknesses & Risks

### 1. State Variable Naming Collisions

**Risk**: Different action handlers may set state variables with the same name, causing overwrites.

**Example**:
```python
# Step 1 sets work_unit_id
state.set("work_unit_id", "637305")

# Step 5 sets work_unit_id again (different process)
state.set("work_unit_id", "637310")  # Overwrites previous value
```

**Mitigation**:
- Use namespaced state variables: `state.set("step_2.work_unit_id", "637305")`
- Implement state variable scoping (per-step, per-scenario, global)
- Add warnings when overwriting existing variables
- Document state variable naming conventions

**Severity**: Medium
**Likelihood**: Medium

---

### 2. Action Handler Dependency Management

**Risk**: Action handlers may have complex dependencies that are hard to manage.

**Example**:
```python
# WaitAction depends on WorkUnitMonitor
# WorkUnitMonitor depends on PlaywrightMCPClient
# PlaywrightMCPClient depends on CredentialManager
```

**Mitigation**:
- Use dependency injection pattern
- Implement factory pattern for action handler creation
- Provide default implementations with option to override
- Document dependencies clearly

**Severity**: Low
**Likelihood**: High

---

### 3. Validator Engine Complexity

**Risk**: Validators may need to perform complex logic that doesn't fit the simple validate() pattern.

**Example**:
- Validating file content requires downloading and parsing
- Validating UI state requires multiple Playwright operations
- Validating data relationships requires multiple API calls

**Mitigation**:
- Allow validators to be stateful if needed
- Provide helper methods in base validator
- Allow validators to call other validators
- Document complex validation patterns

**Severity**: Medium
**Likelihood**: High

---

### 4. Adaptive Polling Overhead

**Risk**: Adaptive polling may still poll too frequently or not frequently enough.

**Current Strategy**:
- 0-2 min: 10s intervals
- 2-5 min: 30s intervals
- 5+ min: 60s intervals

**Issues**:
- Fast processes (<30s) may timeout before first poll
- Slow processes (>10min) may waste time with frequent polls

**Mitigation**:
- Add configurable polling strategies per test step
- Implement exponential backoff as alternative
- Allow override of polling intervals in JSON
- Monitor and log polling efficiency

**Severity**: Low
**Likelihood**: Medium

---

### 5. Screenshot Timing Issues

**Risk**: Screenshots may be captured before UI has fully updated.

**Example**:
```python
# Click button
playwright_client.click(button_ref)

# Immediate screenshot may show old state
screenshot_manager.capture("after_click")  # Too fast!
```

**Mitigation**:
- Add configurable wait after UI actions
- Use Playwright's wait_for_load_state()
- Implement smart waiting (wait for specific element)
- Document screenshot timing best practices

**Severity**: Medium
**Likelihood**: High

---

### 6. Test State Serialization

**Risk**: TestState may contain non-serializable objects (e.g., API response objects).

**Example**:
```python
# Action returns complex object
state.set("api_response", response_object)  # May not be JSON-serializable

# Later, trying to save state fails
json.dumps(state.get_all())  # Error!
```

**Mitigation**:
- Enforce JSON-serializable types in TestState
- Provide helper methods to extract serializable data
- Add validation when setting state variables
- Document state variable type requirements

**Severity**: Medium
**Likelihood**: Medium

---

### 7. Error Recovery Strategy

**Risk**: Framework may not handle partial failures gracefully.

**Example**:
- Step 3 fails, but steps 1-2 succeeded
- Test data left in FSM
- SFTP files not cleaned up
- Work units still running

**Mitigation**:
- Implement teardown phase in executors
- Add cleanup actions (delete test data, cancel work units)
- Provide rollback capability
- Document cleanup procedures

**Severity**: High
**Likelihood**: High

---

### 8. Playwright MCP Connection Stability

**Risk**: MCP Playwright server may disconnect during long tests.

**Mitigation**:
- Implement connection health checks
- Add automatic reconnection logic
- Retry failed operations
- Save browser state periodically
- Document MCP stability requirements

**Severity**: High
**Likelihood**: Medium

---

### 9. FSM API Token Expiration

**Risk**: OAuth tokens expire during long test executions (3600s = 1 hour).

**Mitigation**:
- Implement proactive token refresh (refresh at 50 minutes)
- Add token expiry checking before each API call
- Retry API calls with fresh token on 401 errors
- Document token management strategy

**Severity**: High
**Likelihood**: High

---

### 10. Test Data Isolation Failures

**Risk**: Unique identifiers may not be unique enough, causing test interference.

**Example**:
```python
# Two tests run simultaneously
run_group_1 = "AUTOTEST_20260305_1530"  # Timestamp to second
run_group_2 = "AUTOTEST_20260305_1530"  # Same timestamp!
```

**Mitigation**:
- Use millisecond timestamps: `AUTOTEST_20260305_153045_123`
- Add random suffix: `AUTOTEST_20260305_1530_a1b2c3`
- Use UUIDs: `AUTOTEST_a1b2c3d4-e5f6-7890`
- Implement test execution locking
- Document parallel execution constraints

**Severity**: High
**Likelihood**: Low (if using milliseconds + random)

---

### 11. JSON Schema Validation

**Risk**: Invalid JSON scenarios may cause runtime errors.

**Mitigation**:
- Implement JSON schema validation on load
- Provide clear error messages for invalid schemas
- Create JSON schema definition file
- Add schema validation to test scenario builder GUI
- Document JSON schema requirements

**Severity**: Medium
**Likelihood**: Medium

---

### 12. Performance with Large Test Suites

**Risk**: Framework may be slow with many scenarios or steps.

**Mitigation**:
- Implement parallel scenario execution (where safe)
- Optimize screenshot capture (compress, async)
- Cache API responses where appropriate
- Profile and optimize bottlenecks
- Document performance characteristics

**Severity**: Low
**Likelihood**: Medium


---

## Implementation Roadmap

### Phase 1: MVP Foundation (Weeks 1-6)

**Goal**: Working inbound interface test with POS Inventory scenario

**Deliverables**:
- Core framework modules (TestState, StepEngine, ValidatorEngine)
- Integration modules (SFTP, FSM API, Work Unit Monitor, Playwright)
- Action handlers (SFTP Upload, Wait, API Call)
- Validators (File, Work Unit, API)
- Evidence collection (Screenshots, Logs)
- TES-070 generation
- End-to-end test with POS Inventory

**Success Criteria**:
- ✅ POS Inventory test executes successfully
- ✅ All 7 steps pass
- ✅ TES-070 document generated
- ✅ Adaptive polling works correctly
- ✅ State variables interpolated correctly

---

### Phase 2: Approval Workflow Support (Weeks 7-9)

**Goal**: Add approval workflow testing capability

**Deliverables**:
- ApprovalExecutor
- UIAction handler (enhanced)
- UIValidator
- User Action monitoring
- Approval-specific test templates
- Manual Journal approval test case

**Success Criteria**:
- ✅ Manual Journal approval test executes successfully
- ✅ User Actions detected and validated
- ✅ Approval status transitions validated
- ✅ TES-070 generated for approval workflow

---

### Phase 3: Outbound Interface Support (Weeks 10-12)

**Goal**: Add outbound interface testing capability

**Deliverables**:
- OutboundExecutor
- SFTPDownloadAction handler
- File content validation
- Outbound-specific test templates
- ACH file generation test case

**Success Criteria**:
- ✅ ACH file generation test executes successfully
- ✅ File content validated
- ✅ Email remittance verified
- ✅ TES-070 generated for outbound interface

---

### Phase 4: Robustness & Reliability (Weeks 13-15)

**Goal**: Improve error handling, recovery, and stability

**Deliverables**:
- Comprehensive error handling
- Cleanup/teardown logic
- Retry mechanisms
- Connection health checks
- Token refresh logic
- Test data isolation improvements

**Success Criteria**:
- ✅ Framework handles failures gracefully
- ✅ Test data cleaned up after execution
- ✅ Connections recover from failures
- ✅ Tokens refreshed proactively

---

### Phase 5: Extensibility & Documentation (Weeks 16-18)

**Goal**: Make framework easy to extend and use

**Deliverables**:
- Plugin system for custom actions/validators
- Comprehensive documentation
- Example test scenarios
- Training materials
- JSON schema validation
- Test scenario builder GUI updates

**Success Criteria**:
- ✅ New action handlers can be added easily
- ✅ Documentation is complete and clear
- ✅ Team trained on framework usage
- ✅ JSON schemas validated automatically

---

### Phase 6: Production Readiness (Weeks 19-20)

**Goal**: Prepare for production use

**Deliverables**:
- Performance optimization
- Parallel execution support
- CI/CD integration
- Monitoring and alerting
- Production deployment guide

**Success Criteria**:
- ✅ Framework is stable and performant
- ✅ Integrated with CI/CD pipeline
- ✅ Monitoring in place
- ✅ Ready for production use

---

## Summary of Improvements (v1.0 → v2.0)

| Aspect | v1.0 | v2.0 | Benefit |
|--------|------|------|---------|
| **Step Execution** | Embedded in executors | Centralized StepEngine | Reusability, maintainability |
| **Validation** | Mixed with actions | Separate ValidatorEngine | Separation of concerns |
| **State Management** | Ad-hoc variables | TestState with interpolation | Consistency, traceability |
| **Work Unit Monitoring** | Fixed polling | Adaptive polling | Efficiency, reliability |
| **Test Isolation** | Manual identifiers | Auto-generated unique IDs | Reliability, safety |
| **Playwright Integration** | CSS selectors | MCP snapshot + refs | Stability, maintainability |
| **Action Handlers** | Monolithic | Pluggable handlers | Extensibility |
| **Validators** | Inline | Pluggable validators | Extensibility |
| **Error Handling** | Basic try-catch | Comprehensive strategy | Robustness |
| **Evidence Collection** | Manual | Automated | Completeness |

---

## Conclusion

This refined architecture (v2.0) provides a **solid foundation** for FSM automated testing with:

✅ **Clear separation of concerns** (actions, validations, state)
✅ **Pluggable architecture** (easy to extend)
✅ **Robust state management** (variable interpolation, history)
✅ **Intelligent monitoring** (adaptive polling)
✅ **Strong test isolation** (unique identifiers)
✅ **Stable UI automation** (MCP-first approach)
✅ **Minimal viable implementation** (clear first milestone)

**Key Design Decisions**:
1. StepEngine centralizes step execution logic
2. ValidatorEngine separates validation from actions
3. TestState provides runtime variable management
4. Adaptive polling optimizes work unit monitoring
5. Unique identifiers ensure test isolation
6. MCP snapshot-first approach ensures stable UI automation

**Next Steps**:
1. Review and approve architecture
2. Begin MVP implementation (Phase 1)
3. Test with POS Inventory scenario
4. Iterate based on feedback
5. Expand to approval and outbound workflows

---

**Document Version**: 2.0
**Created**: 2026-03-05
**Author**: Kiro AI Assistant
**Status**: Ready for Implementation
