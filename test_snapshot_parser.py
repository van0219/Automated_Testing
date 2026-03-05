import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from ReusableTools.testing_framework.utils.snapshot_parser import find_element_ref

# Real snapshot data from TEST 1
snapshot = """- generic "Cloud Identities" [ref=e9] [cursor=pointer]:
  - img "Cloud Identities" [ref=e11]
  - link "Cloud Identities" [ref=e12]:
    - /url: "#"
    - generic [ref=e13]: Cloud Identities
  - radio "Cloud Identities"
- generic "Azure for AX4" [ref=e14] [cursor=pointer]:
  - img "Azure for AX4" [ref=e16]
  - link "Azure for AX4" [ref=e17]:
    - /url: "#"
    - generic [ref=e18]: Azure for AX4
  - radio "Azure for AX4"
"""

print('Testing Snapshot Parser with Real Data')
print('='*60)

# Test 1: Find Cloud Identities
print('\nTest 1: Find "Cloud Identities" (no role filter)')
ref = find_element_ref(snapshot, 'Cloud Identities')
print(f'  Result: {ref}')
print(f'  Status: {"PASS" if ref == "e9" else "FAIL"}')

# Test 2: Find with role=generic
print('\nTest 2: Find "Cloud Identities" with role="generic"')
ref = find_element_ref(snapshot, 'Cloud Identities', role='generic')
print(f'  Result: {ref}')
print(f'  Status: {"PASS" if ref == "e9" else "FAIL"}')

# Test 3: Find link
print('\nTest 3: Find "Cloud Identities" with role="link"')
ref = find_element_ref(snapshot, 'Cloud Identities', role='link')
print(f'  Result: {ref}')
print(f'  Status: {"PASS" if ref == "e12" else "FAIL"}')

# Test 4: Find Azure
print('\nTest 4: Find "Azure for AX4"')
ref = find_element_ref(snapshot, 'Azure for AX4')
print(f'  Result: {ref}')
print(f'  Status: {"PASS" if ref == "e14" else "FAIL"}')

print('\n' + '='*60)
print('Snapshot Parser Validation: COMPLETE')
