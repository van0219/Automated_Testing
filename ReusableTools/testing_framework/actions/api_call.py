"""API call action handler for FSM operations"""

from typing import Dict, Any
from .base import BaseAction
from ..engine.test_state import TestState
from ..engine.results import ActionResult
from ..integration.fsm_api_client import FSMAPIClient
from ..utils.exceptions import ActionError
from ..utils.logger import Logger


class APICallAction(BaseAction):
    """
    Execute FSM API calls.
    
    Supports List, Get, Add, Update, Delete operations on FSM business classes.
    """
    
    def __init__(self, fsm_api_client: FSMAPIClient, logger: Logger = None):
        """
        Initialize API call action.
        
        Args:
            fsm_api_client: FSM API client instance
            logger: Optional logger instance
        """
        super().__init__(logger)
        self.fsm_api_client = fsm_api_client
    
    def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Execute FSM API call.
        
        Config:
        - business_class: Business class name
        - action: "List", "Get", "Add", "Update", "Delete"
        - filters: Query filters (optional)
        - data: Record data for Add/Update (optional)
        - record_id: Record ID for Get/Update/Delete (optional)
        
        Returns:
            ActionResult with state_updates: api_record_count, last_record_id
        
        Raises:
            ActionError: If API call fails
        """
        try:
            # Extract configuration
            business_class = config.get('business_class')
            action = config.get('action', 'List')
            filters = config.get('filters', {})
            data = config.get('data', {})
            record_id = config.get('record_id')
            
            if not business_class:
                raise ActionError("Missing required field: business_class")
            
            if self.logger:
                self.logger.info(f"Executing API call: {action} {business_class}")
            
            # Execute API call based on action
            if action == "List":
                records = self.fsm_api_client.list_records(business_class, filters)
                
                # Extract state updates
                state_updates = {
                    'api_record_count': len(records)
                }
                
                # Extract last record ID if available
                if records and isinstance(records, list) and len(records) > 0:
                    last_record = records[-1]
                    if isinstance(last_record, dict) and 'id' in last_record:
                        state_updates['last_record_id'] = last_record['id']
                
                return ActionResult(
                    success=True,
                    message=f"Retrieved {len(records)} records from {business_class}",
                    data={'records': records},
                    state_updates=state_updates
                )
                
            elif action == "Get":
                if not record_id:
                    raise ActionError("Missing required field: record_id for Get action")
                
                record = self.fsm_api_client.get_record(business_class, record_id)
                
                return ActionResult(
                    success=True,
                    message=f"Retrieved record {record_id} from {business_class}",
                    data={'record': record},
                    state_updates={}
                )
                
            elif action == "Add":
                result = self.fsm_api_client.add_record(business_class, data)
                
                # Extract record ID if available
                state_updates = {}
                if isinstance(result, dict) and 'id' in result:
                    state_updates['last_record_id'] = result['id']
                
                return ActionResult(
                    success=True,
                    message=f"Added record to {business_class}",
                    data={'record': result},
                    state_updates=state_updates
                )
                
            elif action == "Update":
                if not record_id:
                    raise ActionError("Missing required field: record_id for Update action")
                
                result = self.fsm_api_client.update_record(business_class, record_id, data)
                
                return ActionResult(
                    success=True,
                    message=f"Updated record {record_id} in {business_class}",
                    data={'record': result},
                    state_updates={}
                )
                
            elif action == "Delete":
                if not record_id:
                    raise ActionError("Missing required field: record_id for Delete action")
                
                result = self.fsm_api_client.delete_record(business_class, record_id)
                
                return ActionResult(
                    success=True,
                    message=f"Deleted record {record_id} from {business_class}",
                    data={'result': result},
                    state_updates={}
                )
                
            else:
                raise ActionError(f"Unknown API action: {action}")
                
        except ActionError:
            raise
        except Exception as e:
            if self.logger:
                self.logger.error(f"API call failed: {str(e)}")
            raise ActionError(f"API call failed: {str(e)}")
