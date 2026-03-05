#!/usr/bin/env python3
import json
import sys

json_file = sys.argv[1] if len(sys.argv) > 1 else 'Projects/SONH/TestScripts/approval/EXT_FIN_004_auto_approval_test.json'

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Extension ID: {data["extension_id"]}')
print(f'Interface Type: {data["interface_type"]}')
print(f'Description: {data["description"]}')
print(f'Total Scenarios: {len(data["scenarios"])}')
print('\nScenario List:')
for s in data['scenarios']:
    print(f'  {s["scenario_id"]}: {s["title"]}')
