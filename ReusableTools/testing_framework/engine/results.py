"""Result classes for actions, validations, and test steps"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from pathlib import Path


@dataclass
class ActionResult:
    """Result of an action execution"""
    success: bool
    message: str
    state_updates: Dict[str, Any] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    
    @classmethod
    def success_result(cls, message: str, state_updates: Dict[str, Any] = None, 
                      data: Dict[str, Any] = None) -> 'ActionResult':
        """Create successful action result"""
        return cls(
            success=True,
            message=message,
            state_updates=state_updates or {},
            data=data or {}
        )
    
    @classmethod
    def failed(cls, message: str, error: str = None) -> 'ActionResult':
        """Create failed action result"""
        return cls(
            success=False,
            message=message,
            error=error or message
        )


@dataclass
class ValidationResult:
    """Result of a validation"""
    passed: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def success(cls, message: str, details: Dict[str, Any] = None) -> 'ValidationResult':
        """Create successful validation result"""
        return cls(
            passed=True,
            message=message,
            details=details or {}
        )
    
    @classmethod
    def failed(cls, message: str, details: Dict[str, Any] = None) -> 'ValidationResult':
        """Create failed validation result"""
        return cls(
            passed=False,
            message=message,
            details=details or {}
        )


@dataclass
class StepResult:
    """Result of a test step execution"""
    step_number: str
    description: str
    action_result: Optional[ActionResult] = None
    validation_result: Optional[ValidationResult] = None
    screenshot_path: Optional[Path] = None
    passed: bool = True
    error: Optional[str] = None
    
    @classmethod
    def failed_step(cls, step_number: str, description: str, error: str) -> 'StepResult':
        """Create failed step result"""
        return cls(
            step_number=step_number,
            description=description,
            passed=False,
            error=error
        )


@dataclass
class ScenarioResult:
    """Result of a test scenario execution"""
    scenario_id: str
    title: str
    step_results: list
    passed: bool
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def total_steps(self) -> int:
        """Total number of steps"""
        return len(self.step_results)
    
    @property
    def passed_steps(self) -> int:
        """Number of passed steps"""
        return sum(1 for r in self.step_results if r.passed)
    
    @property
    def failed_steps(self) -> int:
        """Number of failed steps"""
        return sum(1 for r in self.step_results if not r.passed)


@dataclass
class TestResult:
    """Result of complete test execution"""
    interface_id: str
    interface_name: str
    scenario_results: list
    passed: bool
    execution_time: float
    
    @property
    def total_scenarios(self) -> int:
        """Total number of scenarios"""
        return len(self.scenario_results)
    
    @property
    def passed_scenarios(self) -> int:
        """Number of passed scenarios"""
        return sum(1 for r in self.scenario_results if r.passed)
    
    @property
    def failed_scenarios(self) -> int:
        """Number of failed scenarios"""
        return sum(1 for r in self.scenario_results if not r.passed)
