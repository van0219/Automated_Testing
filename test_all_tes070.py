import sys
from pathlib import Path

files = [
    "TES-070/Sample_Documents/SoNH_TES-070_INT_FIN_013 GL Transaction Interface Test Results Document.docx",
    "TES-070/Sample_Documents/SoNH_TES-070 - INT_FIN_010 Receivables Invoice Import Test Results Document.docx"
]

sys.path.insert(0, 'ReusableTools')
from tes070_analyzer import analyze_tes070

print("\n=== COMPREHENSIVE TEST OF ALL 3 TES-070 DOCUMENTS ===\n")

for i, file_path in enumerate(files, 1):
    if Path(file_path).exists():
        print(f"\n{i}. {Path(file_path).stem}")
        print("-" * 60)
        try:
            result = analyze_tes070(file_path, save_json=False)
            print(f" Scenarios: {len(result['scenarios'])}")
            for j, scenario in enumerate(result['scenarios'], 1):
                print(f"  {j}. {scenario['title'][:60]}...")
                print(f"     Steps: {len(scenario['test_steps'])}, Images: {len(scenario['images'])}")
        except Exception as e:
            print(f" Error: {e}")
    else:
        print(f"\n{i}. File not found: {file_path}")

# Test INT_FIN_127 separately due to special character
import glob
ach_files = glob.glob("TES-070/Sample_Documents/*127*.docx")
if ach_files:
    print(f"\n3. {Path(ach_files[0]).stem}")
    print("-" * 60)
    try:
        result = analyze_tes070(ach_files[0], save_json=False)
        print(f" Scenarios: {len(result['scenarios'])}")
        for j, scenario in enumerate(result['scenarios'], 1):
            print(f"  {j}. {scenario['title'][:60]}...")
            print(f"     Steps: {len(scenario['test_steps'])}, Images: {len(scenario['images'])}")
    except Exception as e:
        print(f" Error: {e}")
