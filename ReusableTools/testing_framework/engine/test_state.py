"""Runtime state management for test execution"""

import re
from datetime import datetime
from typing import Any, Dict, List, Union
from ..utils.exceptions import StateError


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
        self._state: Dict[str, Any] = {}
        self._history: List[Dict[str, Any]] = []
    
    def initialize_run_group(self) -> str:
        """
        Initialize unique run group identifier for test execution.
        
        Generates format: AUTOTEST_YYYYMMDDHHMMSS_RANDOM
        
        Returns:
            Generated run group identifier
        """
        import random
        import string
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        run_group = f"AUTOTEST_{timestamp}_{random_suffix}"
        
        self.set('run_group', run_group)
        return run_group
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a state variable.
        
        Args:
            key: Variable name
            value: Variable value (should be JSON-serializable)
        """
        old_value = self._state.get(key)
        self._state[key] = value
        
        # Track history
        self._history.append({
            'timestamp': datetime.now(),
            'key': key,
            'old_value': old_value,
            'new_value': value
        })
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a state variable.
        
        Args:
            key: Variable name
            default: Default value if key not found
        
        Returns:
            Variable value or default
        """
        return self._state.get(key, default)
    
    def has(self, key: str) -> bool:
        """
        Check if state variable exists.
        
        Args:
            key: Variable name
        
        Returns:
            True if variable exists
        """
        return key in self._state
    
    def interpolate(self, config: Union[dict, str, list]) -> Union[dict, str, list]:
        """
        Interpolate state variables in configuration.
        
        Supports {{state.variable_name}} syntax.
        
        Args:
            config: Dictionary, string, or list with {{state.key}} placeholders
        
        Returns:
            Configuration with interpolated values
        
        Raises:
            StateError: If referenced variable not found
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
        """
        Interpolate state variables in string.
        
        Args:
            text: String with {{state.variable_name}} or {{VARIABLE_NAME}} placeholders
        
        Returns:
            String with interpolated values
        
        Raises:
            StateError: If referenced variable not found
        """
        def replace_state_var(match):
            var_name = match.group(1)
            if not self.has(var_name):
                raise StateError(f"State variable not found: {var_name}")
            return str(self.get(var_name))
        
        def replace_direct_var(match):
            var_name = match.group(1)
            # Map common placeholders to state variables
            mapping = {
                'FSM_PORTAL_URL': 'fsm_url',
                'FSM_USERNAME': 'fsm_username',
                'FSM_PASSWORD': 'password',
                'TODAY_YYYYMMDD': 'today_yyyymmdd',
                'TODAY_PLUS_7_YYYYMMDD': 'today_plus_7_yyyymmdd'
            }
            
            state_var = mapping.get(var_name, var_name.lower())
            if not self.has(state_var):
                raise StateError(f"Variable not found: {var_name} (mapped to state.{state_var})")
            return str(self.get(state_var))
        
        # Match {{state.variable_name}}
        pattern1 = r'\{\{state\.([a-zA-Z_][a-zA-Z0-9_]*)\}\}'
        text = re.sub(pattern1, replace_state_var, text)
        
        # Match {{VARIABLE_NAME}} (direct placeholders)
        pattern2 = r'\{\{([A-Z_][A-Z0-9_]*)\}\}'
        text = re.sub(pattern2, replace_direct_var, text)
        
        return text
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all state variables.
        
        Returns:
            Copy of all state variables
        """
        return self._state.copy()
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get state change history for debugging.
        
        Returns:
            List of state changes
        """
        return self._history.copy()
    
    def clear(self) -> None:
        """Clear all state variables and history"""
        self._state.clear()
        self._history.clear()
    
    def __repr__(self) -> str:
        return f"TestState({len(self._state)} variables)"
