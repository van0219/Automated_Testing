"""Custom exceptions for the testing framework"""


class TestFrameworkError(Exception):
    """Base exception for all framework errors"""
    pass


class ConfigurationError(TestFrameworkError):
    """Configuration or setup error"""
    pass


class ActionExecutionError(TestFrameworkError):
    """Error during action execution"""
    pass


class ValidationError(TestFrameworkError):
    """Error during validation"""
    pass


class StateError(TestFrameworkError):
    """Error related to test state management"""
    pass


class IntegrationError(TestFrameworkError):
    """Error in integration layer (SFTP, API, etc.)"""
    pass


class TimeoutError(TestFrameworkError):
    """Operation timeout"""
    pass


class AuthenticationError(IntegrationError):
    """Authentication failure"""
    pass


class APIError(IntegrationError):
    """FSM API error"""
    pass


class SFTPError(IntegrationError):
    """SFTP operation error"""
    pass


class PlaywrightError(IntegrationError):
    """Playwright MCP error"""
    pass


class ConnectionError(IntegrationError):
    """Connection error"""
    pass


class ActionError(ActionExecutionError):
    """Action execution error"""
    pass


class WorkUnitError(IntegrationError):
    """Work unit operation error"""
    pass
