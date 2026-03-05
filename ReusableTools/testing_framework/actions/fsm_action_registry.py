"""FSM action registry for StepEngine integration"""

from typing import Optional
from .fsm.fsm_login import FSMLoginAction
from .fsm.fsm_payables import FSMPayablesAction
from .fsm.fsm_workunits import FSMWorkUnitsAction
from ..engine.step_engine import StepEngine
from ..integration.playwright_client import PlaywrightMCPClient
from ..integration.ui_map_loader import UIMapLoader
from ..evidence.screenshot_manager import ScreenshotManager
from ..utils.logger import Logger


def register_fsm_actions(
    step_engine: StepEngine,
    playwright_client: PlaywrightMCPClient,
    ui_map_loader: UIMapLoader,
    screenshot_manager: ScreenshotManager,
    logger: Optional[Logger] = None
) -> None:
    """
    Register FSM automation actions with StepEngine.
    
    This function creates instances of FSM action handlers and registers
    them with the StepEngine so they can be invoked from JSON test scenarios.
    
    Args:
        step_engine: StepEngine instance to register actions with
        playwright_client: PlaywrightMCPClient instance for browser automation
        ui_map_loader: UIMapLoader instance for UI element discovery
        screenshot_manager: ScreenshotManager instance for evidence capture
        logger: Optional logger instance
    
    Example JSON scenario actions that will be supported:
        {
            "action": {
                "type": "fsm_login",
                "url": "{{state.fsm_url}}",
                "username": "{{state.fsm_username}}",
                "password": "{{state.fsm_password}}"
            }
        }
        
        {
            "action": {
                "type": "fsm_payables",
                "operation": "create_invoice",
                "invoice_data": {
                    "company": "10",
                    "vendor": "176258",
                    "invoice_number": "{{state.run_group}}_TEST_001",
                    "invoice_date": "2026-03-05",
                    "due_date": "2026-03-12",
                    "invoice_amount": "500.00"
                }
            }
        }
        
        {
            "action": {
                "type": "fsm_workunits",
                "operation": "verify_status",
                "work_unit_id": "{{state.work_unit_id}}",
                "expected_status": "Completed"
            }
        }
    """
    if logger:
        logger.info("Registering FSM automation actions")
    
    # Create FSM action instances
    fsm_login = FSMLoginAction(
        playwright_client=playwright_client,
        logger=logger
    )
    
    fsm_payables = FSMPayablesAction(
        playwright_client=playwright_client,
        ui_map_loader=ui_map_loader,
        screenshot_manager=screenshot_manager,
        logger=logger
    )
    
    fsm_workunits = FSMWorkUnitsAction(
        playwright_client=playwright_client,
        ui_map_loader=ui_map_loader,
        screenshot_manager=screenshot_manager,
        logger=logger
    )
    
    # Register actions with StepEngine
    step_engine.register_action('fsm_login', fsm_login)
    step_engine.register_action('fsm_payables', fsm_payables)
    step_engine.register_action('fsm_workunits', fsm_workunits)
    
    if logger:
        logger.info("FSM automation actions registered successfully")
        logger.debug("Available FSM actions: fsm_login, fsm_payables, fsm_workunits")


def create_fsm_action_handlers(
    playwright_client: PlaywrightMCPClient,
    ui_map_loader: UIMapLoader,
    screenshot_manager: ScreenshotManager,
    logger: Optional[Logger] = None
) -> dict:
    """
    Create FSM action handler instances without registering them.
    
    Useful for manual action execution or testing.
    
    Args:
        playwright_client: PlaywrightMCPClient instance
        ui_map_loader: UIMapLoader instance
        screenshot_manager: ScreenshotManager instance
        logger: Optional logger instance
    
    Returns:
        Dictionary mapping action names to handler instances
    """
    return {
        'fsm_login': FSMLoginAction(
            playwright_client=playwright_client,
            logger=logger
        ),
        'fsm_payables': FSMPayablesAction(
            playwright_client=playwright_client,
            ui_map_loader=ui_map_loader,
            screenshot_manager=screenshot_manager,
            logger=logger
        ),
        'fsm_workunits': FSMWorkUnitsAction(
            playwright_client=playwright_client,
            ui_map_loader=ui_map_loader,
            screenshot_manager=screenshot_manager,
            logger=logger
        )
    }
