"""Structured logging for the testing framework"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class StructuredLogger:
    """
    Structured logger for test execution.
    
    Provides consistent logging format with levels, timestamps, and context.
    """
    
    def __init__(self, name: str, log_file: Optional[Path] = None, level: int = logging.INFO):
        """
        Initialize logger.
        
        Args:
            name: Logger name (typically test or module name)
            log_file: Optional log file path
            level: Logging level (default: INFO)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (if specified)
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)  # File gets all levels
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_step(self, step_number: str, description: str, result: str):
        """Log test step execution"""
        self.info(f"Step {step_number}: {description} - {result}")
    
    def log_scenario_start(self, title: str):
        """Log scenario start"""
        self.info(f"{'='*60}")
        self.info(f"Starting scenario: {title}")
        self.info(f"{'='*60}")
    
    def log_scenario_end(self, title: str, passed: bool):
        """Log scenario end"""
        status = "PASS" if passed else "FAIL"
        self.info(f"{'='*60}")
        self.info(f"Scenario completed: {title} - {status}")
        self.info(f"{'='*60}")


# Alias for backward compatibility
Logger = StructuredLogger
