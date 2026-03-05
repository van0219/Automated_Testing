"""Snapshot parser for Playwright MCP accessibility snapshots"""

from typing import Dict, Any, Optional, List


def find_element_ref(
    snapshot: Dict[str, Any],
    label: str,
    role: Optional[str] = None,
    exact_match: bool = False
) -> Optional[str]:
    """
    Find element reference in Playwright MCP snapshot by label and role.
    
    Args:
        snapshot: Snapshot data from mcp_playwright_browser_snapshot()
        label: Element label text to search for
        role: Optional element role to filter by (button, textbox, combobox, etc.)
        exact_match: If True, label must match exactly; if False, partial match
    
    Returns:
        Element reference string (ref attribute) or None if not found
    
    Example:
        snapshot = playwright.snapshot()
        ref = find_element_ref(snapshot, "Create Invoice", role="button")
        if ref:
            playwright.click(ref, "Create Invoice")
    """
    # Snapshot structure from Playwright MCP is typically a string (YAML/text format)
    # or a dict with content. We need to parse it to find elements.
    
    if isinstance(snapshot, str):
        # Parse string snapshot
        return _parse_string_snapshot(snapshot, label, role, exact_match)
    elif isinstance(snapshot, dict):
        # Check if snapshot has content field
        if 'content' in snapshot:
            return _parse_string_snapshot(snapshot['content'], label, role, exact_match)
        # Otherwise traverse dict structure
        return _traverse_dict_snapshot(snapshot, label, role, exact_match)
    
    return None


def _parse_string_snapshot(
    snapshot_text: str,
    label: str,
    role: Optional[str] = None,
    exact_match: bool = False
) -> Optional[str]:
    """
    Parse string-based snapshot (YAML format from Playwright MCP).
    
    Playwright MCP snapshots are typically in this format:
    - button "Create Invoice" [ref=abc123]
    - textbox "Company" [ref=def456]
    
    Args:
        snapshot_text: Snapshot text content
        label: Element label to search for
        role: Optional role filter
        exact_match: Whether to require exact label match
    
    Returns:
        Element ref or None
    """
    lines = snapshot_text.split('\n')
    
    for line in lines:
        # Look for pattern: role "label" [ref=...]
        # Example: button "Create Invoice" [ref=abc123]
        
        # Check if line contains the label
        if exact_match:
            label_match = f'"{label}"' in line
        else:
            label_match = label.lower() in line.lower()
        
        if not label_match:
            continue
        
        # Check role if specified
        if role:
            # Role is typically at the start of the line
            if not line.strip().startswith(role.lower()):
                continue
        
        # Extract ref attribute
        ref = _extract_ref_from_line(line)
        if ref:
            return ref
    
    return None


def _extract_ref_from_line(line: str) -> Optional[str]:
    """
    Extract ref attribute from snapshot line.
    
    Args:
        line: Snapshot line (e.g., 'button "Create Invoice" [ref=abc123]')
    
    Returns:
        Ref value or None
    """
    # Look for [ref=...] pattern
    if '[ref=' not in line:
        return None
    
    # Extract ref value
    start = line.find('[ref=') + 5
    end = line.find(']', start)
    
    if end == -1:
        return None
    
    return line[start:end]


def _traverse_dict_snapshot(
    snapshot: Dict[str, Any],
    label: str,
    role: Optional[str] = None,
    exact_match: bool = False
) -> Optional[str]:
    """
    Traverse dictionary-based snapshot structure.
    
    Args:
        snapshot: Snapshot dictionary
        label: Element label to search for
        role: Optional role filter
        exact_match: Whether to require exact label match
    
    Returns:
        Element ref or None
    """
    # Check if current node matches
    if _node_matches(snapshot, label, role, exact_match):
        return snapshot.get('ref')
    
    # Recursively search children
    if 'children' in snapshot:
        for child in snapshot['children']:
            ref = _traverse_dict_snapshot(child, label, role, exact_match)
            if ref:
                return ref
    
    # Search other dict values
    for key, value in snapshot.items():
        if key in ['ref', 'children']:
            continue
        
        if isinstance(value, dict):
            ref = _traverse_dict_snapshot(value, label, role, exact_match)
            if ref:
                return ref
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    ref = _traverse_dict_snapshot(item, label, role, exact_match)
                    if ref:
                        return ref
    
    return None


def _node_matches(
    node: Dict[str, Any],
    label: str,
    role: Optional[str] = None,
    exact_match: bool = False
) -> bool:
    """
    Check if node matches search criteria.
    
    Args:
        node: Snapshot node
        label: Element label to search for
        role: Optional role filter
        exact_match: Whether to require exact label match
    
    Returns:
        True if node matches
    """
    # Check role if specified
    if role:
        node_role = node.get('role', '').lower()
        if node_role != role.lower():
            return False
    
    # Check label
    node_label = node.get('label', '') or node.get('name', '') or node.get('text', '')
    
    if exact_match:
        return node_label == label
    else:
        return label.lower() in node_label.lower()


def find_all_elements(
    snapshot: Dict[str, Any],
    role: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Find all elements matching role in snapshot.
    
    Args:
        snapshot: Snapshot data from mcp_playwright_browser_snapshot()
        role: Optional element role to filter by
    
    Returns:
        List of element dictionaries with ref, label, and role
    
    Example:
        snapshot = playwright.snapshot()
        buttons = find_all_elements(snapshot, role="button")
        for button in buttons:
            print(f"Button: {button['label']} [ref={button['ref']}]")
    """
    elements = []
    
    if isinstance(snapshot, str):
        # Parse string snapshot
        lines = snapshot.split('\n')
        for line in lines:
            if role and not line.strip().startswith(role.lower()):
                continue
            
            ref = _extract_ref_from_line(line)
            if ref:
                # Extract label from line
                label = _extract_label_from_line(line)
                element_role = _extract_role_from_line(line)
                
                elements.append({
                    'ref': ref,
                    'label': label,
                    'role': element_role
                })
    
    elif isinstance(snapshot, dict):
        if 'content' in snapshot:
            return find_all_elements(snapshot['content'], role)
        else:
            _collect_elements(snapshot, role, elements)
    
    return elements


def _extract_label_from_line(line: str) -> str:
    """Extract label from snapshot line."""
    # Look for text in quotes
    start = line.find('"')
    if start == -1:
        return ""
    
    end = line.find('"', start + 1)
    if end == -1:
        return ""
    
    return line[start + 1:end]


def _extract_role_from_line(line: str) -> str:
    """Extract role from snapshot line."""
    # Role is typically the first word
    parts = line.strip().split()
    if parts:
        return parts[0]
    return ""


def _collect_elements(
    node: Dict[str, Any],
    role: Optional[str],
    elements: List[Dict[str, Any]]
) -> None:
    """Recursively collect elements from dict snapshot."""
    # Check if current node has ref
    if 'ref' in node:
        node_role = node.get('role', '')
        if not role or node_role.lower() == role.lower():
            elements.append({
                'ref': node['ref'],
                'label': node.get('label', '') or node.get('name', '') or node.get('text', ''),
                'role': node_role
            })
    
    # Recursively search children
    if 'children' in node:
        for child in node['children']:
            _collect_elements(child, role, elements)
    
    # Search other dict values
    for key, value in node.items():
        if key in ['ref', 'children', 'label', 'name', 'text', 'role']:
            continue
        
        if isinstance(value, dict):
            _collect_elements(value, role, elements)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _collect_elements(item, role, elements)
