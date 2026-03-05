---
title: FSM Testing Framework MVP - Design Specification
version: 1.0
date: 2026-03-05
status: Draft
---

# FSM Testing Framework MVP - Design Specification

## 1. Architecture Overview

### 1.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI Entry Point                         │
│                    (run_tests.py)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   TestOrchestrator                          │
│  - Load JSON scenarios                                      │
│  - Select executor                                          │
│  - Aggregate results                                        │
│  - Generate TES-070                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   InboundExecutor                           │
│  - Generate unique IDs                                      │
│  - Execute steps sequentially                               │
│  - Collect results                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     StepEngine                              │
│  - Interpolate state variables                              │
│  - Route to action handlers                                 │
│  - Execute validations                                      │
│  - Capture screenshots                                      │
└─────┬───────────────────┬───────────────────┬───────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
┌──────────┐      ┌──────────────┐    ┌─────────────┐
│ Actions  │      │ Validators   │    │ Evidence    │
└──────────┘      └──────────────┘    └─────────────┘
```

### 1.2 Module Organization

```
ReusableTools/testing_framework/
├── __init__.py
├── engine/
│   ├── __init__.py
│   ├── test_state.py          # TestState
│   ├── step_engine.py         # StepEngine
│   ├── validator_engine.py    # ValidatorEngine
│   └── results.py             # Result classes
├── orchestration/
│   ├── __init__.py
│   ├── test_orchestrator.py   # TestOrchestrator
│   └── inbound_executor.py    # InboundExecutor
├── actions/
│   ├── __init__.py
│   ├── base.py                # BaseAction
│   ├── sftp_upload.py         # SFTPUploadAction
│   ├── wait.py                # WaitAction
│   └── api_call.py            # APICallAction
├── validators/
│   ├── __init__.py
│   ├── base.py                # BaseValidator
│   ├── file_validator.py      # FileValidator
│   ├── workunit_validator.py  # WorkUnitValidator
│   └── api_validator.py       # APIValidator
├── integration/
│   ├── __init__.py
│   ├── credential_manager.py  # CredentialManager
│   ├── sftp_client.py         # SFTPClient
│   ├── fsm_api_client.py      # FSMAPIClient
│   ├── playwright_client.py   # PlaywrightMCPClient
│   └── workunit_monitor.py    # WorkUnitMonitor
├── evidence/
│   ├── __init__.py
│   ├── screenshot_manager.py  # ScreenshotManager
│   └── tes070_generator.py    # TES070Generator
└── utils/
    ├── __init__.py
    ├── logger.py              # Logger
    └── exceptions.py          # Custom exceptions
```

## 2. Core Engine Design

### 2.1 TestState

**Purpose**: Manage runtime state with variable interpolation

**Class Definition**:
```python
class TestState:
    """Runtime state management with variable interpolation."""
    
    def __init__(self):
        self._state: Dict[str, Any] = {}
        self._history: List[Dict[str, Any]] = []
    
    def set(self, key: str, value: Any) -> None:
        """Set state variable and track history."""
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get state variable with optional default."""
        
    def has(self, key: str) -> bool:
        """Check if key exists in state."""
        
    def interpolate(self, value: Any) -> Any:
        """Interpolate {{state.variable}} syntax recursively."""
        
    def get_all(self) -> Dict[str, Any]:
        """Return all state variables."""
        
    def get_history(self) -> List[Dict[str, Any]]:
        """Return state change history."""
        
    def clear(self) -> None:
        """Clear all state and history."""
        
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
```

**Interpolation Algorithm**:
```python
def _interpolate_string(self, text: str) -> str:
    """
    Interpolate {{state.variable}} in string.
    
    Algorithm:
    1. Find all {{state.xxx}} patterns using regex
    2. For each match:
       a. Extract variable name
       b. Look up in state
       c. If not found, raise ValueError
       d. Replace with string representation
    3. Return interpolated string
    
    Pattern: r'\{\{state\.([a-zA-Z_][a-zA-Z0-9_]*)\}\}'
    """
    import re
    pattern = r'\{\{state\.([a-zA-Z_][a-zA-Z0-9_]*)\}\}'
    
    def replacer(match):
        var_name = match.group(1)
        if var_name not in self._state:
            raise ValueError(f"State variable not found: {var_name}")
        return str(self._state[var_name])
    
    return re.sub(pattern, replacer, text)

def _interpolate_recursive(self, value: Any) -> Any:
    """
    Recursively interpolate state variables.
    
    - str: Apply string interpolation
    - dict: Recursively interpolate all values
    - list: Recursively interpolate all items
    - other: Return as-is
    """
    if isinstance(value, str):
        return self._interpolate_string(value)
    elif isinstance(value, dict):
        return {k: self._interpolate_recursive(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [self._interpolate_recursive(item) for item in value]
    else:
        return value
```

**State History Format**:
```python
{
    "timestamp": "2026-03-05T10:30:45.123456",
    "key": "work_unit_id",
    "old_value": None,
    "new_value": "WU-12345"
}
```

### 2.2 StepEngine

**Purpose**: Centralized step execution with pluggable actions

**Class Definition**:
```python
class StepEngine:
    """Orchestrate test step execution."""
    
    def __init__(
        self,
        state: TestState,
        validator_engine: ValidatorEngine,
        screenshot_manager: ScreenshotManager,
        logger: Logger
    ):
        self.state = state
        self.validator_engine = validator_engine
        self.screenshot_manager = screenshot_manager
        self.logger = logger
        self._action_handlers: Dict[str, BaseAction] = {}
        self._register_default_handlers()
    
    def register_action(self, action_type: str, handler: BaseAction) -> None:
        """Register custom action handler."""
        
    def execute_step(self, step_config: Dict[str, Any]) -> StepResult:
        """Execute single test step with action, validation, screenshot."""
        
    def _register_default_handlers(self) -> None:
        """Register built-in action handlers."""
```

**Execution Flow**:
```
1. Interpolate state variables in step_config
2. Extract action configuration
3. Route to action handler based on action_type
4. Execute action → get ActionResult
5. Update state with action result state_updates
6. If screenshot configured → capture screenshot
7. If validation configured → execute validation
8. Build and return StepResult
```

**Step Configuration Schema**:
```json
{
  "number": 1,
  "description": "Upload test file to SFTP",
  "action": {
    "type": "sftp_upload",
    "test_data_file": "POS_INVENTORY_valid.csv",
    "destination_path": "/inbound/{{state.run_group}}_inventory.csv"
  },
  "screenshot": "01_upload_file",
  "validation": {
    "type": "file",
    "path": "/inbound/{{state.run_group}}_inventory.csv"
  }
}
```

### 2.3 ValidatorEngine

**Purpose**: Route validation requests to specialized validators

**Class Definition**:
```python
class ValidatorEngine:
    """Route validation to specialized validators."""
    
    def __init__(self, state: TestState, logger: Logger):
        self.state = state
        self.logger = logger
        self._validators: Dict[str, BaseValidator] = {}
        self._register_default_validators()
    
    def register_validator(self, validator_type: str, validator: BaseValidator) -> None:
        """Register custom validator."""
        
    def validate(self, validation_config: Dict[str, Any]) -> ValidationResult:
        """Execute validation and return result."""
        
    def _register_default_validators(self) -> None:
        """Register built-in validators."""
```

**Validation Configuration Schema**:
```json
{
  "type": "api",
  "business_class": "POSInventoryInterface",
  "filters": {
    "RunGroup": "{{state.run_group}}",
    "Status": "2"
  },
  "expected_count": 10
}
```

## 3. Action Handler Design

### 3.1 BaseAction (Abstract)

**Purpose**: Define action handler interface

**Class Definition**:
```python
from abc import ABC, abstractmethod

class BaseAction(ABC):
    """Base class for action handlers."""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    @abstractmethod
    def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """Execute action and return result."""
        pass
```

### 3.2 SFTPUploadAction

**Purpose**: Upload files to SFTP server

**Class Definition**:
```python
class SFTPUploadAction(BaseAction):
    """Upload test data files to SFTP."""
    
    def __init__(self, sftp_client: SFTPClient, logger: Logger):
        super().__init__(logger)
        self.sftp_client = sftp_client
    
    def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Upload file to SFTP.
        
        Config:
        - test_data_file: Filename in TestScripts/test_data/
        - destination_path: SFTP destination path
        
        Returns ActionResult with state_updates:
        - uploaded_file: Filename
        - sftp_destination: Full SFTP path
        """
```

**Implementation Logic**:
```
1. Extract test_data_file and destination_path from config
2. Construct source path: Projects/{client}/TestScripts/test_data/{test_data_file}
3. Call sftp_client.upload(source_path, destination_path)
4. Return ActionResult with success and state updates
```

### 3.3 WaitAction

**Purpose**: Wait for conditions with adaptive polling

**Class Definition**:
```python
class WaitAction(BaseAction):
    """Wait for work unit creation or completion."""
    
    def __init__(self, workunit_monitor: WorkUnitMonitor, logger: Logger):
        super().__init__(logger)
        self.workunit_monitor = workunit_monitor
    
    def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Wait for condition to be met.
        
        Config:
        - target: "work_unit_creation" or "work_unit_completion"
        - process_name: Process name (for creation)
        - timeout_seconds: Max wait time (default 600)
        
        Returns ActionResult with state_updates:
        - work_unit_id: Work unit ID
        - work_unit_status: Final status
        """
```

**Adaptive Polling Algorithm**:
```python
def _calculate_poll_interval(elapsed_seconds: float) -> int:
    """
    Calculate poll interval based on elapsed time.
    
    0-2 minutes: 10 seconds
    2-5 minutes: 30 seconds
    5+ minutes: 60 seconds
    """
    if elapsed_seconds < 120:  # 0-2 min
        return 10
    elif elapsed_seconds < 300:  # 2-5 min
        return 30
    else:  # 5+ min
        return 60
```

### 3.4 APICallAction

**Purpose**: Execute FSM API calls

**Class Definition**:
```python
class APICallAction(BaseAction):
    """Execute FSM API calls."""
    
    def __init__(self, fsm_api_client: FSMAPIClient, logger: Logger):
        super().__init__(logger)
        self.fsm_api_client = fsm_api_client
    
    def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Execute FSM API call.
        
        Config:
        - business_class: Business class name
        - action: "List", "Get", "Add", "Update", "Delete"
        - filters: Query filters (optional)
        
        Returns ActionResult with state_updates:
        - api_record_count: Number of records returned
        - last_record_id: ID of last record (if available)
        """
```

## 4. Validator Design

### 4.1 BaseValidator (Abstract)

**Purpose**: Define validator interface

**Class Definition**:
```python
from abc import ABC, abstractmethod

class BaseValidator(ABC):
    """Base class for validators."""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    @abstractmethod
    def validate(self, config: Dict[str, Any], state: TestState) -> ValidationResult:
        """Execute validation and return result."""
        pass
```

### 4.2 FileValidator

**Purpose**: Validate file existence on SFTP

**Class Definition**:
```python
class FileValidator(BaseValidator):
    """Validate file existence on SFTP."""
    
    def __init__(self, sftp_client: SFTPClient, logger: Logger):
        super().__init__(logger)
        self.sftp_client = sftp_client
    
    def validate(self, config: Dict[str, Any], state: TestState) -> ValidationResult:
        """
        Check if file exists on SFTP.
        
        Config:
        - path: SFTP file path
        
        Returns ValidationResult with passed=True if file exists.
        """
```

### 4.3 WorkUnitValidator

**Purpose**: Validate work unit status

**Class Definition**:
```python
class WorkUnitValidator(BaseValidator):
    """Validate work unit status."""
    
    def __init__(self, workunit_monitor: WorkUnitMonitor, logger: Logger):
        super().__init__(logger)
        self.workunit_monitor = workunit_monitor
    
    def validate(self, config: Dict[str, Any], state: TestState) -> ValidationResult:
        """
        Validate work unit status.
        
        Config:
        - work_unit_id: Work unit ID (or read from state)
        - expected_status: Expected status value
        
        Returns ValidationResult with passed=True if status matches.
        """
```

### 4.4 APIValidator

**Purpose**: Validate FSM data via API

**Class Definition**:
```python
class APIValidator(BaseValidator):
    """Validate FSM data via API queries."""
    
    def __init__(self, fsm_api_client: FSMAPIClient, logger: Logger):
        super().__init__(logger)
        self.fsm_api_client = fsm_api_client
    
    def validate(self, config: Dict[str, Any], state: TestState) -> ValidationResult:
        """
        Validate data via FSM API.
        
        Config:
        - business_class: Business class name
        - filters: Query filters
        - expected_count: Expected record count (optional)
        - expected_status: Expected status value (optional)
        - field_validations: List of field validations (optional)
        
        Returns ValidationResult with passed=True if all validations pass.
        """
```

**Field Validation Schema**:
```json
{
  "field_validations": [
    {
      "field": "Status",
      "operator": "equals",
      "value": "2"
    },
    {
      "field": "Amount",
      "operator": "greater_than",
      "value": 0
    }
  ]
}
```

## 5. Integration Client Design

### 5.1 CredentialManager

**Purpose**: Load and manage credentials securely

**Class Definition**:
```python
class CredentialManager:
    """Load and manage credentials from secure files."""
    
    def __init__(self, client_name: str):
        self.client_name = client_name
        self.credentials_dir = f"Projects/{client_name}/Credentials"
        self._credentials: Dict[str, Any] = {}
        self._load_credentials()
    
    def get_fsm_credentials(self) -> Dict[str, str]:
        """Return FSM portal URL, username, password."""
        
    def get_sftp_credentials(self, server_name: str) -> Dict[str, str]:
        """Return SFTP host, username, password for server."""
        
    def get_oauth_credentials(self, tenant: str) -> Dict[str, str]:
        """Return OAuth2 credentials from .ionapi file."""
```

**File Formats**:

`.env.fsm`:
```
FSM_PORTAL_URL=https://acuity-tst.inforcloudsuite.com
FSM_USERNAME=user@example.com
TENANT=ACUITY_TST
```

`.env.passwords`:
```
FSM_PASSWORD=SecurePassword123
SFTP_SERVER_NAME=sftp.example.com
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USERNAME=sftpuser
SFTP_PASSWORD=SftpPassword456
SFTP_INBOUND_PATH=/inbound
SFTP_OUTBOUND_PATH=/outbound
```

`.ionapi` (JSON):
```json
{
  "ti": "ACUITY_TST",
  "cn": "ACUITY_TST~client_id",
  "ci": "client_id",
  "cs": "client_secret",
  "iu": "https://mingle-sso.inforcloudsuite.com/ACUITY_TST/as/token.oauth2",
  "pu": "https://mingle-sso.inforcloudsuite.com/ACUITY_TST/as/token.oauth2",
  "oa": "https://mingle-ionapi.inforcloudsuite.com/ACUITY_TST/IONAPI/api/v2",
  "saak": "access_key",
  "sask": "secret_key"
}
```

### 5.2 SFTPClient

**Purpose**: SFTP file operations

**Class Definition**:
```python
import paramiko

class SFTPClient:
    """SFTP file operations with connection management."""
    
    def __init__(self, credential_manager: CredentialManager, server_name: str):
        self.credential_manager = credential_manager
        self.server_name = server_name
        self._connection: Optional[paramiko.SFTPClient] = None
        self._transport: Optional[paramiko.Transport] = None
    
    def connect(self) -> None:
        """Establish SFTP connection."""
        
    def disconnect(self) -> None:
        """Close SFTP connection."""
        
    def upload(self, local_path: str, remote_path: str) -> None:
        """Upload file to SFTP server."""
        
    def download(self, remote_path: str, local_path: str) -> None:
        """Download file from SFTP server."""
        
    def list_files(self, remote_dir: str) -> List[str]:
        """List files in remote directory."""
        
    def file_exists(self, remote_path: str) -> bool:
        """Check if file exists on SFTP server."""
```

### 5.3 FSMAPIClient

**Purpose**: FSM API operations with OAuth2

**Class Definition**:
```python
import requests
from datetime import datetime, timedelta

class FSMAPIClient:
    """FSM API operations with OAuth2 authentication."""
    
    def __init__(self, credential_manager: CredentialManager):
        self.credential_manager = credential_manager
        self._token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
        self._base_url: str = ""
    
    def _get_token(self) -> str:
        """Obtain OAuth2 token from ION."""
        
    def _refresh_token_if_needed(self) -> None:
        """Refresh token if expiring within 10 minutes."""
        
    def list_records(
        self,
        business_class: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """List records from business class."""
        
    def get_record(self, business_class: str, record_id: str) -> Dict[str, Any]:
        """Get single record by ID."""
        
    def add_record(self, business_class: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add new record."""
        
    def update_record(
        self,
        business_class: str,
        record_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update existing record."""
```

**OAuth2 Token Flow**:
```
1. Read .ionapi credentials
2. POST to token endpoint with client credentials
3. Receive access_token with 3600s expiry
4. Store token and expiry time
5. Before each API call:
   - Check if token expires within 10 minutes
   - If yes, refresh token
6. On 401 response:
   - Refresh token
   - Retry request once
```

**API Request Format** (WebRun):
```json
{
  "_actionName": "List",
  "_objectName": "POSInventoryInterface",
  "_module": "pfi",
  "_dataArea": "ACUITY",
  "FinanceEnterpriseGroup": "100",
  "AccountingEntity": "1000",
  "RunGroup": "AUTOTEST_20260305_ABC123",
  "Status": "2"
}
```

### 5.4 PlaywrightMCPClient

**Purpose**: Browser automation via MCP server

**Class Definition**:
```python
class PlaywrightMCPClient:
    """Browser automation via Playwright MCP server."""
    
    def __init__(self, mcp_server_url: str = "http://localhost:3000"):
        self.mcp_server_url = mcp_server_url
        self._session: Optional[requests.Session] = None
    
    def connect(self) -> None:
        """Connect to MCP server."""
        
    def navigate(self, url: str) -> None:
        """Navigate to URL."""
        
    def snapshot(self) -> Dict[str, Any]:
        """Take accessibility snapshot of current page."""
        
    def click(self, element_ref: str) -> None:
        """Click element by reference."""
        
    def type_text(self, element_ref: str, text: str) -> None:
        """Type text into element."""
        
    def wait_for_load(self, timeout: int = 30) -> None:
        """Wait for page load state."""
        
    def screenshot(self, filename: str) -> str:
        """Capture screenshot and return path."""
```

**MCP Protocol Communication**:
```python
# Navigate
POST /mcp/playwright/navigate
{
  "url": "https://acuity-tst.inforcloudsuite.com/portal"
}

# Snapshot
POST /mcp/playwright/snapshot
Response: {
  "snapshot": "...",
  "elements": [...]
}

# Click
POST /mcp/playwright/click
{
  "ref": "element-123",
  "element": "Submit button"
}
```

### 5.5 WorkUnitMonitor

**Purpose**: Monitor work units with adaptive polling

**Class Definition**:
```python
class WorkUnitMonitor:
    """Monitor work unit status via UI automation."""
    
    def __init__(self, playwright_client: PlaywrightMCPClient, logger: Logger):
        self.playwright_client = playwright_client
        self.logger = logger
    
    def wait_for_creation(
        self,
        process_name: str,
        timeout_seconds: int = 600,
        poll_interval_override: Optional[int] = None
    ) -> Dict[str, Any]:
        """Wait for work unit creation by process name."""
        
    def wait_for_completion(
        self,
        work_unit_id: str,
        timeout_seconds: int = 600,
        poll_interval_override: Optional[int] = None
    ) -> Dict[str, Any]:
        """Wait for work unit completion by ID."""
```

**Work Unit Detection Algorithm**:
```python
def wait_for_creation(self, process_name: str, timeout_seconds: int) -> Dict[str, Any]:
    """
    Algorithm:
    1. Record start time
    2. Navigate to Process Server Administrator > Work Units
    3. Loop until timeout:
       a. Take snapshot
       b. Search for process_name in work unit list
       c. Filter by timestamp >= start time
       d. If found, return work_unit_id and status
       e. Calculate poll interval based on elapsed time
       f. Sleep for poll interval
    4. If timeout exceeded, raise TimeoutError
    """
```

**Adaptive Polling**:
```python
def _get_poll_interval(self, elapsed_seconds: float, override: Optional[int]) -> int:
    """
    Return poll interval based on elapsed time.
    
    If override provided, use it.
    Otherwise:
    - 0-2 min: 10 seconds
    - 2-5 min: 30 seconds
    - 5+ min: 60 seconds
    """
    if override:
        return override
    
    if elapsed_seconds < 120:
        return 10
    elif elapsed_seconds < 300:
        return 30
    else:
        return 60
```

## 6. Orchestration Design

### 6.1 TestOrchestrator

**Purpose**: Main entry point for test execution

**Class Definition**:
```python
class TestOrchestrator:
    """Coordinate end-to-end test execution."""
    
    def __init__(
        self,
        client_name: str,
        environment: str,
        logger: Logger
    ):
        self.client_name = client_name
        self.environment = environment
        self.logger = logger
        
        # Initialize dependencies
        self.credential_manager = CredentialManager(client_name)
        self.state = TestState()
        
        # Initialize integration clients
        self.sftp_client = SFTPClient(self.credential_manager, "default")
        self.fsm_api_client = FSMAPIClient(self.credential_manager)
        self.playwright_client = PlaywrightMCPClient()
        self.workunit_monitor = WorkUnitMonitor(self.playwright_client, logger)
        
        # Initialize engines
        self.validator_engine = ValidatorEngine(self.state, logger)
        self.screenshot_manager = ScreenshotManager(self.playwright_client, "")
        self.step_engine = StepEngine(
            self.state,
            self.validator_engine,
            self.screenshot_manager,
            logger
        )
```
    
    def run(self, scenario_file: str) -> TestResult:
        """
        Execute test scenarios from JSON file.
        
        Flow:
        1. Load and validate JSON
        2. Extract interface metadata
        3. Initialize state with unique IDs
        4. Select executor based on interface_type
        5. Execute all scenarios
        6. Generate TES-070 document
        7. Return TestResult
        """
```

**JSON Test Scenario Schema**:
```json
{
  "interface_id": "INT_POS_001",
  "interface_name": "POS Inventory Inbound Interface",
  "interface_type": "inbound",
  "test_date": "2026-03-05",
  "tester_name": "John Doe",
  "environment": "ACUITY_TST",
  "scenarios": [
    {
      "scenario_id": "S001",
      "title": "Successful Import - Valid Data",
      "description": "Verify successful import of valid POS inventory data",
      "steps": [
        {
          "number": 1,
          "description": "Upload test file to SFTP",
          "action": {
            "type": "sftp_upload",
            "test_data_file": "POS_INVENTORY_valid.csv",
            "destination_path": "/inbound/{{state.run_group}}_inventory.csv"
          },
          "screenshot": "01_upload_file",
          "validation": {
            "type": "file",
            "path": "/inbound/{{state.run_group}}_inventory.csv"
          }
        }
      ]
    }
  ]
}
```

### 6.2 InboundExecutor

**Purpose**: Execute inbound interface test scenarios

**Class Definition**:
```python
import random
import string
from datetime import datetime

class InboundExecutor:
    """Execute inbound interface test scenarios."""
    
    def __init__(self, step_engine: StepEngine, state: TestState, logger: Logger):
        self.step_engine = step_engine
        self.state = state
        self.logger = logger
    
    def execute_scenario(self, scenario: Dict[str, Any]) -> ScenarioResult:
        """
        Execute single test scenario.
        
        Flow:
        1. Generate unique run_group
        2. Store in state
        3. Execute steps sequentially
        4. Collect results
        5. Return ScenarioResult
        """
```

**Unique ID Generation**:
```python
def _generate_run_group(self) -> str:
    """
    Generate unique run_group identifier.
    
    Format: AUTOTEST_<timestamp>_<random>
    Example: AUTOTEST_20260305103045_A7B9C2
    
    Components:
    - AUTOTEST: Prefix for filtering
    - Timestamp: YYYYMMDDHHMMSS
    - Random: 6 uppercase alphanumeric characters
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"AUTOTEST_{timestamp}_{random_suffix}"
```

## 7. Evidence & Reporting Design

### 7.1 ScreenshotManager

**Purpose**: Capture and organize screenshots

**Class Definition**:
```python
import os
from pathlib import Path

class ScreenshotManager:
    """Capture and organize screenshots for evidence."""
    
    def __init__(self, playwright_client: PlaywrightMCPClient, output_dir: str):
        self.playwright_client = playwright_client
        self.output_dir = output_dir
    
    def set_output_dir(self, interface_id: str) -> None:
        """Set output directory for current test."""
        
    def capture(self, step_number: int, name: str) -> str:
        """
        Capture screenshot with naming convention.
        
        Format: {step_number:02d}_{name}.png
        Example: 01_upload_file.png
        
        Returns: Full path to screenshot file
        """
```

**Directory Structure**:
```
Projects/{ClientName}/Temp/
└── INT_POS_001_20260305_103045/
    ├── 01_upload_file.png
    ├── 02_wait_for_trigger.png
    ├── 03_work_unit_created.png
    ├── 04_work_unit_completed.png
    ├── 05_validate_data.png
    ├── 06_fsm_records.png
    └── 07_test_complete.png
```

### 7.2 TES070Generator

**Purpose**: Generate TES-070 Word documents

**Class Definition**:
```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

class TES070Generator:
    """Generate TES-070 Word documents from test results."""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def generate(
        self,
        test_result: TestResult,
        screenshot_dir: str,
        output_dir: str
    ) -> str:
        """
        Generate TES-070 document.
        
        Returns: Path to generated .docx file
        """
```

**Document Structure**:
```
1. Title Page
   - Interface ID and Name
   - Test Date
   - Tester Name
   - Environment

2. Table of Contents (auto-generated)

3. Test Summary
   - Total Scenarios
   - Passed/Failed Count
   - Overall Status

4. For Each Scenario:
   - Scenario ID and Title
   - Description
   - Test Steps Table:
     | Step | Description | Expected | Actual | Status | Evidence |
     |------|-------------|----------|--------|--------|----------|
     | 1    | Upload file | File uploaded | File uploaded | PASS | Screenshot |
   - Embedded screenshots below each step

5. Appendix
   - Test Data Files
   - Configuration Details
```

**Styling**:
- Title: Arial 16pt Bold
- Headings: Arial 14pt Bold
- Body: Arial 11pt
- Table: Grid style with borders
- Screenshots: Max width 6 inches

## 8. Foundation Design

### 8.1 Logger

**Purpose**: Structured logging for test execution

**Class Definition**:
```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class Logger:
    """Structured logging with file and console output."""
    
    def __init__(self, name: str, log_dir: str, level: str = "INFO"):
        self.name = name
        self.log_dir = log_dir
        self.level = level
        self._logger = self._setup_logger()
    
    def debug(self, message: str, **context) -> None:
        """Log debug message with context."""
        
    def info(self, message: str, **context) -> None:
        """Log info message with context."""
        
    def warning(self, message: str, **context) -> None:
        """Log warning message with context."""
        
    def error(self, message: str, **context) -> None:
        """Log error message with context."""
```

**Log Format**:
```
2026-03-05 10:30:45.123 | INFO | TestOrchestrator | Executing scenario S001 | scenario_id=S001 interface_id=INT_POS_001
```

**File Rotation**:
- Max size: 10 MB
- Backup count: 5
- Location: Temp/{interface_id}_{timestamp}/test_execution.log

### 8.2 Exceptions

**Purpose**: Custom exception hierarchy

**Class Definition**:
```python
class TestFrameworkError(Exception):
    """Base exception for testing framework."""
    pass

class TestExecutionError(TestFrameworkError):
    """General test execution failure."""
    pass

class ValidationError(TestFrameworkError):
    """Validation failure."""
    pass

class ActionError(TestFrameworkError):
    """Action execution failure."""
    pass

class ConnectionError(TestFrameworkError):
    """Integration connection failure."""
    pass

class TimeoutError(TestFrameworkError):
    """Timeout condition exceeded."""
    pass

class WorkUnitError(TestFrameworkError):
    """Work unit execution failure."""
    pass

class ConfigurationError(TestFrameworkError):
    """Configuration issue."""
    pass
```

### 8.3 Results

**Purpose**: Structured result objects

**Class Definitions**:
```python
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class ActionResult:
    """Result of action execution."""
    status: str  # "success" or "failure"
    message: str
    data: Optional[Dict[str, Any]] = None
    state_updates: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationResult:
    """Result of validation."""
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None

@dataclass
class StepResult:
    """Result of step execution."""
    step_number: int
    description: str
    action_result: ActionResult
    validation_result: Optional[ValidationResult] = None
    screenshot_path: Optional[str] = None
    passed: bool = True

@dataclass
class ScenarioResult:
    """Result of scenario execution."""
    scenario_id: str
    title: str
    step_results: List[StepResult]
    passed: bool

@dataclass
class TestResult:
    """Result of complete test execution."""
    interface_id: str
    scenario_results: List[ScenarioResult]
    tes070_path: Optional[str] = None
    passed: bool = True
```

### 8.4 CLI Entry Point

**Purpose**: Command-line interface for test execution

**Script**: `run_tests.py`

```python
#!/usr/bin/env python3
"""
FSM Testing Framework - CLI Entry Point

Usage:
    python run_tests.py --scenario path/to/scenario.json --client SONH --environment ACUITY_TST
    python run_tests.py --scenario path/to/scenario.json --client SONH --verbose
"""

import argparse
import sys
from pathlib import Path
from ReusableTools.testing_framework.orchestration.test_orchestrator import TestOrchestrator
from ReusableTools.testing_framework.utils.logger import Logger

def main():
    parser = argparse.ArgumentParser(description="FSM Testing Framework")
    parser.add_argument(
        "--scenario",
        required=True,
        help="Path to JSON test scenario file"
    )
    parser.add_argument(
        "--client",
        required=True,
        help="Client name (e.g., SONH)"
    )
    parser.add_argument(
        "--environment",
        default="ACUITY_TST",
        help="FSM environment (default: ACUITY_TST)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Validate scenario file exists
    scenario_path = Path(args.scenario)
    if not scenario_path.exists():
        print(f"Error: Scenario file not found: {args.scenario}")
        sys.exit(1)
    
    # Initialize logger
    log_level = "DEBUG" if args.verbose else "INFO"
    logger = Logger("TestRunner", ".", log_level)
    
    # Execute tests
    try:
        orchestrator = TestOrchestrator(args.client, args.environment, logger)
        result = orchestrator.run(str(scenario_path))
        
        # Print results
        print("\n" + "="*60)
        print("TEST EXECUTION COMPLETE")
        print("="*60)
        print(f"Interface: {result.interface_id}")
        print(f"Scenarios: {len(result.scenario_results)}")
        print(f"Status: {'PASSED' if result.passed else 'FAILED'}")
        if result.tes070_path:
            print(f"TES-070: {result.tes070_path}")
        print("="*60 + "\n")
        
        sys.exit(0 if result.passed else 1)
        
    except Exception as e:
        logger.error(f"Test execution failed: {str(e)}")
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## 9. Data Flow Diagrams

### 9.1 Complete Test Execution Flow

```
User
  │
  ├─> run_tests.py --scenario test.json --client SONH
  │
  ▼
TestOrchestrator
  │
  ├─> Load JSON scenario
  ├─> Initialize TestState with unique IDs
  ├─> Select InboundExecutor
  │
  ▼
InboundExecutor
  │
  ├─> Generate run_group: AUTOTEST_20260305_ABC123
  ├─> Store in TestState
  │
  ├─> For each step:
  │   │
  │   ▼
  │   StepEngine
  │     │
  │     ├─> Interpolate state variables in config
  │     ├─> Route to action handler
  │     │
  │     ▼
  │     SFTPUploadAction / WaitAction / APICallAction
  │       │
  │       ├─> Execute action
  │       ├─> Return ActionResult with state_updates
  │       │
  │     ◄─┘
  │     │
  │     ├─> Update TestState with state_updates
  │     ├─> Capture screenshot (if configured)
  │     ├─> Execute validation (if configured)
  │     │
  │     ▼
  │     ValidatorEngine
  │       │
  │       ├─> Route to validator
  │       │
  │       ▼
  │       FileValidator / WorkUnitValidator / APIValidator
  │         │
  │         ├─> Execute validation
  │         ├─> Return ValidationResult
  │         │
  │       ◄─┘
  │       │
  │     ◄─┘
  │     │
  │     ├─> Build StepResult
  │     │
  │   ◄─┘
  │   │
  ├─> Collect all StepResults
  ├─> Build ScenarioResult
  │
◄─┘
  │
  ├─> Collect all ScenarioResults
  ├─> Generate TES-070 via TES070Generator
  ├─> Build TestResult
  │
◄─┘
  │
  ├─> Print results
  ├─> Exit with status code
```

### 9.2 State Interpolation Flow

```
Step Configuration (JSON)
  {
    "action": {
      "type": "sftp_upload",
      "destination_path": "/inbound/{{state.run_group}}_inventory.csv"
    }
  }
  │
  ▼
StepEngine.execute_step()
  │
  ├─> TestState.interpolate(step_config)
  │     │
  │     ├─> Recursively traverse dictionary
  │     ├─> Find string: "/inbound/{{state.run_group}}_inventory.csv"
  │     ├─> Regex match: {{state.run_group}}
  │     ├─> Look up "run_group" in state
  │     ├─> Found: "AUTOTEST_20260305_ABC123"
  │     ├─> Replace: "/inbound/AUTOTEST_20260305_ABC123_inventory.csv"
  │     │
  │   ◄─┘
  │
  ▼
Interpolated Configuration
  {
    "action": {
      "type": "sftp_upload",
      "destination_path": "/inbound/AUTOTEST_20260305_ABC123_inventory.csv"
    }
  }
```

### 9.3 Work Unit Monitoring Flow

```
WaitAction.execute()
  │
  ├─> WorkUnitMonitor.wait_for_creation("POS_Inventory_Import")
  │     │
  │     ├─> Record start_time
  │     ├─> Navigate to Process Server Administrator > Work Units
  │     │
  │     ├─> Loop:
  │     │   │
  │     │   ├─> Take snapshot
  │     │   ├─> Search for "POS_Inventory_Import" in list
  │     │   ├─> Filter by timestamp >= start_time
  │     │   │
  │     │   ├─> Found?
  │     │   │   ├─> Yes: Extract work_unit_id, return
  │     │   │   └─> No: Continue
  │     │   │
  │     │   ├─> Calculate elapsed time
  │     │   ├─> Check timeout
  │     │   │   ├─> Exceeded: Raise TimeoutError
  │     │   │   └─> Not exceeded: Continue
  │     │   │
  │     │   ├─> Calculate poll interval:
  │     │   │   ├─> 0-2 min: 10 seconds
  │     │   │   ├─> 2-5 min: 30 seconds
  │     │   │   └─> 5+ min: 60 seconds
  │     │   │
  │     │   ├─> Sleep for poll interval
  │     │   │
  │     │   └─> Repeat
  │     │
  │   ◄─┘
  │
  ├─> Return ActionResult with work_unit_id
```

## 10. Sequence Diagrams

### 10.1 MVP Test Case Execution

```
User -> CLI: run_tests.py --scenario pos_inventory.json --client SONH
CLI -> TestOrchestrator: run(scenario_file)
TestOrchestrator -> TestOrchestrator: Load JSON
TestOrchestrator -> TestState: Initialize with unique IDs
TestOrchestrator -> InboundExecutor: execute_scenario(scenario)

InboundExecutor -> InboundExecutor: Generate run_group
InboundExecutor -> TestState: set("run_group", "AUTOTEST_20260305_ABC123")

# Step 1: Upload file
InboundExecutor -> StepEngine: execute_step(step1_config)
StepEngine -> TestState: interpolate(step1_config)
StepEngine -> SFTPUploadAction: execute(config, state)
SFTPUploadAction -> SFTPClient: upload(local_path, remote_path)
SFTPClient --> SFTPUploadAction: Success
SFTPUploadAction --> StepEngine: ActionResult(state_updates={uploaded_file: "..."})
StepEngine -> TestState: set("uploaded_file", "...")
StepEngine -> ScreenshotManager: capture(1, "upload_file")
ScreenshotManager --> StepEngine: screenshot_path
StepEngine -> ValidatorEngine: validate(validation_config)
ValidatorEngine -> FileValidator: validate(config, state)
FileValidator -> SFTPClient: file_exists(remote_path)
SFTPClient --> FileValidator: True
FileValidator --> ValidatorEngine: ValidationResult(passed=True)
ValidatorEngine --> StepEngine: ValidationResult
StepEngine --> InboundExecutor: StepResult(passed=True)

# Step 2: Wait for work unit creation
InboundExecutor -> StepEngine: execute_step(step2_config)
StepEngine -> WaitAction: execute(config, state)
WaitAction -> WorkUnitMonitor: wait_for_creation("POS_Inventory_Import")
WorkUnitMonitor -> PlaywrightMCPClient: navigate(work_units_url)
WorkUnitMonitor -> PlaywrightMCPClient: snapshot()
PlaywrightMCPClient --> WorkUnitMonitor: snapshot_data
WorkUnitMonitor -> WorkUnitMonitor: Search for process, found WU-12345
WorkUnitMonitor --> WaitAction: {work_unit_id: "WU-12345", status: "Running"}
WaitAction --> StepEngine: ActionResult(state_updates={work_unit_id: "WU-12345"})
StepEngine -> TestState: set("work_unit_id", "WU-12345")
StepEngine --> InboundExecutor: StepResult(passed=True)

# Step 3: Wait for completion
InboundExecutor -> StepEngine: execute_step(step3_config)
StepEngine -> WaitAction: execute(config, state)
WaitAction -> WorkUnitMonitor: wait_for_completion("WU-12345")
WorkUnitMonitor -> PlaywrightMCPClient: snapshot()
WorkUnitMonitor -> WorkUnitMonitor: Check status, still Running, sleep 10s
WorkUnitMonitor -> PlaywrightMCPClient: snapshot()
WorkUnitMonitor -> WorkUnitMonitor: Check status, Completed
WorkUnitMonitor --> WaitAction: {work_unit_id: "WU-12345", status: "Completed"}
WaitAction --> StepEngine: ActionResult(state_updates={work_unit_status: "Completed"})
StepEngine --> InboundExecutor: StepResult(passed=True)

# Step 4: Validate data
InboundExecutor -> StepEngine: execute_step(step4_config)
StepEngine -> APICallAction: execute(config, state)
APICallAction -> FSMAPIClient: list_records("POSInventoryInterface", filters)
FSMAPIClient -> FSMAPIClient: Check token, valid
FSMAPIClient -> FSM API: POST /api/v2/POSInventoryInterface/List
FSM API --> FSMAPIClient: {records: [...10 records...]}
FSMAPIClient --> APICallAction: records
APICallAction --> StepEngine: ActionResult(state_updates={api_record_count: 10})
StepEngine -> ValidatorEngine: validate(validation_config)
ValidatorEngine -> APIValidator: validate(config, state)
APIValidator -> FSMAPIClient: list_records(...)
FSMAPIClient --> APIValidator: records
APIValidator -> APIValidator: Check count=10, Status=2 for all
APIValidator --> ValidatorEngine: ValidationResult(passed=True)
ValidatorEngine --> StepEngine: ValidationResult
StepEngine --> InboundExecutor: StepResult(passed=True)

InboundExecutor --> TestOrchestrator: ScenarioResult(passed=True)
TestOrchestrator -> TES070Generator: generate(test_result, screenshot_dir)
TES070Generator --> TestOrchestrator: tes070_path
TestOrchestrator --> CLI: TestResult(passed=True, tes070_path="...")
CLI -> User: Print results, exit 0
```

## 11. Error Handling Patterns

### 11.1 Action Execution Errors

**Pattern**: Try-catch with descriptive errors

```python
def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
    try:
        # Execute action logic
        result = self._perform_action(config)
        return ActionResult(
            status="success",
            message="Action completed successfully",
            state_updates=result
        )
    except ConnectionError as e:
        self.logger.error(f"Connection failed: {str(e)}")
        raise ActionError(f"Failed to connect: {str(e)}")
    except TimeoutError as e:
        self.logger.error(f"Timeout exceeded: {str(e)}")
        raise ActionError(f"Action timed out: {str(e)}")
    except Exception as e:
        self.logger.error(f"Unexpected error: {str(e)}")
        raise ActionError(f"Action failed: {str(e)}")
```

### 11.2 API Call Retry Logic

**Pattern**: Retry once on 401 with token refresh

```python
def _call_api(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Call API with automatic token refresh on 401."""
    self._refresh_token_if_needed()
    
    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Authorization": f"Bearer {self._token}"}
        )
        
        if response.status_code == 401:
            # Token expired, refresh and retry once
            self.logger.warning("Token expired, refreshing...")
            self._get_token()
            response = requests.post(
                endpoint,
                json=payload,
                headers={"Authorization": f"Bearer {self._token}"}
            )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API call failed: {str(e)}")
```

### 11.3 MCP Connection Recovery

**Pattern**: Reconnect on disconnection

```python
def _ensure_connected(self) -> None:
    """Ensure MCP connection is active."""
    if not self._is_connected():
        self.logger.warning("MCP connection lost, reconnecting...")
        try:
            self.connect()
        except Exception as e:
            raise ConnectionError(f"Failed to reconnect to MCP server: {str(e)}")

def navigate(self, url: str) -> None:
    """Navigate with automatic reconnection."""
    self._ensure_connected()
    try:
        # Perform navigation
        pass
    except Exception as e:
        # Try reconnecting once
        self.logger.warning("Navigation failed, attempting reconnection...")
        self.connect()
        # Retry navigation
```

### 11.4 Validation Failure Handling

**Pattern**: Return ValidationResult with failure details

```python
def validate(self, config: Dict[str, Any], state: TestState) -> ValidationResult:
    """Validate with detailed failure information."""
    try:
        # Perform validation
        actual_count = len(records)
        expected_count = config.get("expected_count")
        
        if actual_count != expected_count:
            return ValidationResult(
                passed=False,
                message=f"Record count mismatch",
                details={
                    "expected": expected_count,
                    "actual": actual_count,
                    "difference": actual_count - expected_count
                }
            )
        
        return ValidationResult(
            passed=True,
            message="Validation passed",
            details={"record_count": actual_count}
        )
        
    except Exception as e:
        self.logger.error(f"Validation error: {str(e)}")
        return ValidationResult(
            passed=False,
            message=f"Validation failed: {str(e)}",
            details={"error": str(e)}
        )
```

## 12. Configuration Management

### 12.1 Environment Configuration

**File**: `Projects/{ClientName}/Credentials/.env.fsm`

```ini
# FSM Environment Configuration
FSM_PORTAL_URL=https://acuity-tst.inforcloudsuite.com
FSM_USERNAME=user@example.com
TENANT=ACUITY_TST
FINANCE_ENTERPRISE_GROUP=100
ACCOUNTING_ENTITY=1000
DATA_AREA=ACUITY
```

### 12.2 Test Configuration

**Embedded in JSON scenario**:

```json
{
  "interface_id": "INT_POS_001",
  "config": {
    "timeout_seconds": 600,
    "poll_interval_override": null,
    "screenshot_format": "png",
    "log_level": "INFO"
  }
}
```

### 12.3 Framework Configuration

**File**: `ReusableTools/testing_framework/config.py`

```python
# Default configuration values
DEFAULT_TIMEOUT = 600  # 10 minutes
DEFAULT_POLL_INTERVALS = {
    "0-2min": 10,
    "2-5min": 30,
    "5+min": 60
}
DEFAULT_SCREENSHOT_FORMAT = "png"
DEFAULT_LOG_LEVEL = "INFO"
MCP_SERVER_URL = "http://localhost:3000"
```

## 13. Testing Strategy

### 13.1 Unit Testing

**Approach**: Test individual components in isolation with mocks

**Example**: TestState unit tests

```python
import unittest
from ReusableTools.testing_framework.engine.test_state import TestState

class TestTestState(unittest.TestCase):
    
    def setUp(self):
        self.state = TestState()
    
    def test_set_and_get(self):
        self.state.set("key1", "value1")
        self.assertEqual(self.state.get("key1"), "value1")
    
    def test_interpolate_string(self):
        self.state.set("run_group", "AUTOTEST_123")
        result = self.state.interpolate("File: {{state.run_group}}.csv")
        self.assertEqual(result, "File: AUTOTEST_123.csv")
    
    def test_interpolate_dict(self):
        self.state.set("id", "12345")
        config = {"path": "/data/{{state.id}}.csv"}
        result = self.state.interpolate(config)
        self.assertEqual(result["path"], "/data/12345.csv")
    
    def test_interpolate_missing_variable(self):
        with self.assertRaises(ValueError):
            self.state.interpolate("{{state.missing}}")
```

### 13.2 Integration Testing

**Approach**: Test component interactions with test doubles

**Example**: StepEngine integration test

```python
import unittest
from unittest.mock import Mock, MagicMock
from ReusableTools.testing_framework.engine.step_engine import StepEngine
from ReusableTools.testing_framework.engine.test_state import TestState

class TestStepEngineIntegration(unittest.TestCase):
    
    def setUp(self):
        self.state = TestState()
        self.validator_engine = Mock()
        self.screenshot_manager = Mock()
        self.logger = Mock()
        
        self.engine = StepEngine(
            self.state,
            self.validator_engine,
            self.screenshot_manager,
            self.logger
        )
    
    def test_execute_step_with_action_and_validation(self):
        # Setup
        self.state.set("run_group", "TEST_123")
        step_config = {
            "number": 1,
            "description": "Test step",
            "action": {
                "type": "sftp_upload",
                "destination_path": "/data/{{state.run_group}}.csv"
            },
            "validation": {
                "type": "file",
                "path": "/data/{{state.run_group}}.csv"
            }
        }
        
        # Mock action handler
        mock_action = Mock()
        mock_action.execute.return_value = ActionResult(
            status="success",
            message="Uploaded",
            state_updates={"uploaded_file": "test.csv"}
        )
        self.engine.register_action("sftp_upload", mock_action)
        
        # Mock validator
        self.validator_engine.validate.return_value = ValidationResult(
            passed=True,
            message="File exists"
        )
        
        # Execute
        result = self.engine.execute_step(step_config)
        
        # Assert
        self.assertTrue(result.passed)
        self.assertEqual(self.state.get("uploaded_file"), "test.csv")
        mock_action.execute.assert_called_once()
        self.validator_engine.validate.assert_called_once()
```

### 13.3 End-to-End Testing

**Approach**: Test complete workflow with real integrations (manual)

**Test Case**: MVP POS Inventory Test

```
Prerequisites:
- Playwright MCP server running
- FSM environment accessible
- SFTP server accessible
- Valid credentials in Projects/SONH/Credentials/

Steps:
1. Create test scenario JSON
2. Run: python run_tests.py --scenario pos_inventory.json --client SONH
3. Verify:
   - File uploaded to SFTP
   - Work unit created and completed
   - Data imported to FSM
   - Screenshots captured
   - TES-070 document generated

Expected Result:
- All steps pass
- TES-070 document in TES-070/Generated_TES070s/
- Exit code 0
```

## 14. Implementation Phases

### Phase 1: Foundation (Week 1)
- ✅ TestState (already implemented)
- ✅ Results (already implemented)
- ✅ Logger (already implemented)
- ✅ Exceptions (already implemented)
- ✅ CredentialManager (already implemented)

### Phase 2: Integration Clients (Week 2)
- SFTPClient
- FSMAPIClient
- PlaywrightMCPClient
- WorkUnitMonitor

### Phase 3: Core Engines (Week 3)
- ValidatorEngine
- StepEngine

### Phase 4: Actions & Validators (Week 4)
- SFTPUploadAction
- WaitAction
- APICallAction
- FileValidator
- WorkUnitValidator
- APIValidator

### Phase 5: Orchestration (Week 5)
- InboundExecutor
- TestOrchestrator
- CLI Entry Point

### Phase 6: Evidence & Testing (Week 6)
- ScreenshotManager
- TES070Generator
- End-to-end testing
- Documentation

## 15. Dependencies

### 15.1 Python Packages

```
# requirements.txt
python-docx>=0.8.11      # Word document generation
paramiko>=3.0.0          # SFTP operations
requests>=2.31.0         # HTTP API calls
python-dotenv>=1.0.0     # Credential loading
```

### 15.2 External Services

- Playwright MCP Server (must be running)
- FSM Environment (must be accessible)
- SFTP Server (must be accessible)
- ION OAuth2 Service (for API authentication)

## 16. Security Considerations

### 16.1 Credential Protection

- Never log credential values
- Never commit credential files to git
- Read credentials from secure files only
- Use environment-specific credential files

### 16.2 Token Management

- Store tokens in memory only
- Implement automatic token refresh
- Clear tokens on cleanup
- Use HTTPS for all API calls

### 16.3 File Permissions

- Restrict credential file permissions (600)
- Validate file paths before operations
- Sanitize user inputs in file paths

---

**Document Status**: Complete
**Version**: 1.0
**Date**: 2026-03-05
**Next Step**: Implementation Phase 2 (Integration Clients)
