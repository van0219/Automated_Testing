#!/usr/bin/env python3
"""Count scenarios in TES-070 analysis JSON"""
import json
import sys

if len(sys.argv) < 2:
    print("Usage: python count_scenarios.py <analysis_json_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

scenarios = data.get('scenarios', [])
print(f"Total scenarios: {len(scenarios)}")

# Find detailed scenarios (those with test_steps)
detailed = [s for s in scenarios if len(s.get('test_steps', [])) > 0]
print(f"Detailed scenarios (with test_steps): {len(detailed)}")

# Find TOC entries (those without test_steps)
toc = [s for s in scenarios if len(s.get('test_steps', [])) == 0]
print(f"TOC entries (without test_steps): {len(toc)}")

print("\nDetailed scenario titles:")
for i, s in enumerate(detailed, 1):
    title = s.get('title', 'Unknown')
    steps = len(s.get('test_steps', []))
    images = len(s.get('images', []))
    print(f"{i}. {title[:80]}... (steps:{steps}, images:{images})")
