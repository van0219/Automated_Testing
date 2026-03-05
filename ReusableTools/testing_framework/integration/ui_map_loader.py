"""UI map loader for FSM automation"""

import json
import os
from typing import Dict, Any, Optional
from ..utils.logger import Logger


class UIMapLoader:
    """
    Load and provide access to UI maps for FSM automation.
    
    UI maps contain element labels, types, and properties discovered
    during UI discovery sessions.
    """
    
    def __init__(self, ui_maps_dir: str = None, logger: Optional[Logger] = None):
        """
        Initialize UI map loader.
        
        Args:
            ui_maps_dir: Directory containing UI map JSON files
            logger: Optional logger instance
        """
        self.logger = logger
        
        # Default to ui_maps directory in testing_framework
        if ui_maps_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            ui_maps_dir = os.path.join(
                os.path.dirname(current_dir),
                'ui_maps'
            )
        
        self.ui_maps_dir = ui_maps_dir
        self._loaded_maps: Dict[str, Dict[str, Any]] = {}
    
    def load_map(self, map_name: str) -> Dict[str, Any]:
        """
        Load UI map from JSON file.
        
        Args:
            map_name: Name of UI map file (with or without .json extension)
        
        Returns:
            Dictionary containing UI map data
        
        Raises:
            FileNotFoundError: If UI map file not found
            json.JSONDecodeError: If UI map file is invalid JSON
        """
        # Add .json extension if not present
        if not map_name.endswith('.json'):
            map_name = f"{map_name}.json"
        
        # Check if already loaded
        if map_name in self._loaded_maps:
            if self.logger:
                self.logger.debug(f"Using cached UI map: {map_name}")
            return self._loaded_maps[map_name]
        
        # Load from file
        map_path = os.path.join(self.ui_maps_dir, map_name)
        
        if not os.path.exists(map_path):
            raise FileNotFoundError(f"UI map not found: {map_path}")
        
        if self.logger:
            self.logger.debug(f"Loading UI map: {map_name}")
        
        with open(map_path, 'r', encoding='utf-8') as f:
            ui_map = json.load(f)
        
        # Cache the loaded map
        self._loaded_maps[map_name] = ui_map
        
        if self.logger:
            self.logger.debug(f"UI map loaded successfully: {map_name}")
        
        return ui_map
    
    def get_element(self, map_name: str, screen: str, element_name: str) -> Dict[str, Any]:
        """
        Get element configuration from UI map.
        
        Args:
            map_name: Name of UI map file
            screen: Screen name (e.g., 'payables_search', 'create_invoice_form')
            element_name: Element name (e.g., 'create_invoice_button', 'company_field')
        
        Returns:
            Dictionary with element configuration (label, type, role, etc.)
        
        Raises:
            KeyError: If screen or element not found in UI map
        """
        ui_map = self.load_map(map_name)
        
        if screen not in ui_map:
            raise KeyError(f"Screen '{screen}' not found in UI map '{map_name}'")
        
        screen_data = ui_map[screen]
        
        # Check in main elements
        if 'elements' in screen_data and element_name in screen_data['elements']:
            return screen_data['elements'][element_name]
        
        # Check in tab-specific elements (e.g., main_tab_elements)
        for key in screen_data:
            if key.endswith('_elements') and element_name in screen_data[key]:
                return screen_data[key][element_name]
        
        # Check in toolbar buttons
        if 'toolbar_buttons' in screen_data and element_name in screen_data['toolbar_buttons']:
            return screen_data['toolbar_buttons'][element_name]
        
        # Check in search filters
        if 'search_filters' in screen_data and element_name in screen_data['search_filters']:
            return screen_data['search_filters'][element_name]
        
        raise KeyError(f"Element '{element_name}' not found in screen '{screen}' of UI map '{map_name}'")
    
    def get_label(self, map_name: str, screen: str, element_name: str) -> str:
        """
        Get element label for automation.
        
        Args:
            map_name: Name of UI map file
            screen: Screen name
            element_name: Element name
        
        Returns:
            Element label string (e.g., 'Create Invoice', 'Company')
        """
        element = self.get_element(map_name, screen, element_name)
        return element.get('label', element_name)
    
    def get_element_type(self, map_name: str, screen: str, element_name: str) -> str:
        """
        Get element type.
        
        Args:
            map_name: Name of UI map file
            screen: Screen name
            element_name: Element name
        
        Returns:
            Element type (e.g., 'button', 'textbox', 'combobox')
        """
        element = self.get_element(map_name, screen, element_name)
        return element.get('type', 'unknown')
    
    def get_element_role(self, map_name: str, screen: str, element_name: str) -> str:
        """
        Get element role for Playwright selector.
        
        Args:
            map_name: Name of UI map file
            screen: Screen name
            element_name: Element name
        
        Returns:
            Element role (e.g., 'button', 'textbox', 'combobox')
        """
        element = self.get_element(map_name, screen, element_name)
        return element.get('role', element.get('type', 'generic'))
    
    def has_lookup(self, map_name: str, screen: str, element_name: str) -> bool:
        """
        Check if element has lookup button.
        
        Args:
            map_name: Name of UI map file
            screen: Screen name
            element_name: Element name
        
        Returns:
            True if element has lookup button
        """
        element = self.get_element(map_name, screen, element_name)
        return element.get('has_lookup', False)
    
    def has_datepicker(self, map_name: str, screen: str, element_name: str) -> bool:
        """
        Check if element has datepicker.
        
        Args:
            map_name: Name of UI map file
            screen: Screen name
            element_name: Element name
        
        Returns:
            True if element has datepicker
        """
        element = self.get_element(map_name, screen, element_name)
        return element.get('has_datepicker', False)
    
    def is_required(self, map_name: str, screen: str, element_name: str) -> bool:
        """
        Check if element is required.
        
        Args:
            map_name: Name of UI map file
            screen: Screen name
            element_name: Element name
        
        Returns:
            True if element is required
        """
        element = self.get_element(map_name, screen, element_name)
        return element.get('required', False)
    
    def get_screen_info(self, map_name: str, screen: str) -> Dict[str, Any]:
        """
        Get complete screen information.
        
        Args:
            map_name: Name of UI map file
            screen: Screen name
        
        Returns:
            Dictionary with screen configuration
        """
        ui_map = self.load_map(map_name)
        
        if screen not in ui_map:
            raise KeyError(f"Screen '{screen}' not found in UI map '{map_name}'")
        
        return ui_map[screen]
