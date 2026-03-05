# Quick Start Guide - FSM Automated Testing

## For Functional Consultants 👨‍💼👩‍💼

This guide shows you how to create TES-070 test documents using the 3-step workflow.

## Available Clients

You can test with any of these 4 clients:

1. **StateOfNewHampshire** - Production environment (NMR2N66J9P445R7P_AX4)
2. **TAMICS10** - Sandbox/POC environment (TAMICS10_AX1)
3. **BayCare** - Training environment (BAYCAREHS_TRN)
4. **ACUITY** - Test environment (ACUITY_TST)

## The 3-Step Workflow

### Interface Step 1: Define Test Scenarios 📋

**What it does**: Launches a modern GUI tool to create test scenario JSON files

**How to use**:
1. Click the "Interface Step 1: Define Test Scenarios" hook in Kiro
2. Modern GUI launches automatically
3. Select interface type from welcome screen (Inbound/Outbound/Approval)
4. All 3 predefined scenarios auto-load
5. Fill in interface details in left sidebar:
   - Client name (e.g., StateOfNewHampshire)
   - Interface ID (e.g., INT_FIN_013)
   - Interface name (e.g., GL Transaction Interface)
   - Author name
   - Environment
   - Prerequisites (roles, test data, config)
6. Edit the pre-loaded scenarios as needed
7. Click "Save JSON" button

**Output**: JSON file saved to `Projects/{ClientName}/TestScripts/{type}/{interface_id}_test_scenarios.json`

**GUI Features**:
- 🎨 Modern 2026 design
- 🚀 Smart auto-loading of scenarios
- ✏️ Everything is editable
- 👁️ JSON preview before saving

**Example**:
```
Projects/StateOfNewHampshire/TestScripts/inbound/INT_FIN_013_test_scenarios.json
```

---

### Interface Step 2: Execute Tests in FSM 🧪

**What it does**: Runs your tests in FSM and captures screenshots

**How to use**:
1. Click the "Interface Step 2: Execute Tests in FSM" hook in Kiro
2. Specify which client you're testing
3. Select the JSON file created in Step 1
4. Kiro will:
   - Open FSM in a browser
   - Execute each test step
   - Capture screenshots automatically
   - Validate results

**Output**: Screenshots saved to `Projects/{ClientName}/Temp/{interface_id}_{timestamp}/`

**Example**:
```
Projects/StateOfNewHampshire/Temp/INT_FIN_013_20260213_120000/
├── 01_sftp_file_drop.png
├── 02_file_channel_scan.png
├── 03_work_unit_status.png
└── ...
```

---

### Interface Step 3: Generate TES-070 📄

**What it does**: Creates the final TES-070 Word document

**How to use**:
1. Click the "Interface Step 3: Generate TES-070" hook in Kiro
2. Specify which client you tested
3. Select the JSON file
4. Kiro will generate the TES-070 document
5. Open the document in Word
6. Press F9 to update the Table of Contents
7. Review and save

**Output**: TES-070 document saved to `Projects/{ClientName}/TES-070/Generated_TES070s/`

**Example**:
```
Projects/StateOfNewHampshire/TES-070/Generated_TES070s/INT_FIN_013_GL_Transaction_Interface_20260213_120000.docx
```

---

## Complete Example: Testing INT_FIN_013 for State of New Hampshire

### Interface Step 1: Define Test Scenarios
```
1. Click "Interface Step 1: Define Test Scenarios"
2. Modern GUI launches automatically
3. Select "Inbound Interface" card from welcome screen
4. Fill in left sidebar:
   - Client: StateOfNewHampshire
   - Interface ID: INT_FIN_013
   - Interface Name: GL Transaction Interface
   - Author: [Your Name]
   - Environment: ACUITY_TST
   - Prerequisites: (fill in roles, test data, config)
5. Edit the 3 pre-loaded scenarios:
   - Scenario 1: Successful Import (happy path)
   - Scenario 2: Database Import Errors
   - Scenario 3: Interface Errors
6. Click "Save JSON"
7. JSON created at: Projects/StateOfNewHampshire/TestScripts/inbound/INT_FIN_013_test_scenarios.json
```

### Interface Step 2: Execute Tests
```
1. Click "Interface Step 2: Execute Tests in FSM"
2. Select: StateOfNewHampshire
3. Select: INT_FIN_013_test_scenarios.json
4. Kiro opens FSM and runs tests
5. Screenshots saved to: Projects/StateOfNewHampshire/Temp/INT_FIN_013_20260213_120000/
```

### Interface Step 3: Generate Document
```
1. Click "Interface Step 3: Generate TES-070"
2. Select: StateOfNewHampshire
3. Select: INT_FIN_013_test_scenarios.json
4. Document created at: Projects/StateOfNewHampshire/TES-070/Generated_TES070s/INT_FIN_013_GL_Transaction_Interface_20260213_120000.docx
5. Open in Word, press F9, review, save
```

---

## Tips & Best Practices

### Test Scenario Design
- **Happy Path First**: Always start with a successful scenario
- **Error Scenarios**: Test common errors (validation, data issues)
- **Edge Cases**: Test boundary conditions
- **Recovery**: Test error correction and reprocessing

### Screenshot Naming
- Use descriptive names: `01_sftp_file_drop.png`, `02_file_channel_scan.png`
- Number them in order: 01, 02, 03, etc.
- Keep names short but clear

### Test Steps
- Be specific: "Navigate to Process Server Administrator > Scheduling > By Process Definition"
- Include expected results: "Work unit status should be 'Completed'"
- Note any wait times: "Wait 2 minutes for file channel to scan"

### Multiple Clients
- Each client is completely isolated
- You can work on multiple clients simultaneously
- Just specify the client name in each step

---

## Folder Structure Reference

```
Projects/
├── StateOfNewHampshire/
│   ├── Credentials/              # FSM login credentials
│   ├── TestScripts/              # Test scenario JSON files
│   │   ├── inbound/
│   │   ├── outbound/
│   │   └── approval/
│   ├── TES-070/                  # Generated TES-070 documents
│   │   └── Generated_TES070s/
│   └── Temp/                     # Screenshots
├── TAMICS10/
│   └── (same structure)
├── BayCare/
│   └── (same structure)
└── ACUITY/
    └── (same structure)
```

---

## Troubleshooting

### "Credentials not found"
- Check that `Projects/{ClientName}/Credentials/` folder exists
- Verify `.env.fsm` and `.env.passwords` files are present
- Ask your admin for credentials if missing

### "Screenshots not captured"
- Ensure FSM is accessible
- Check browser automation didn't fail
- You can add screenshots manually in Word later

### "JSON file not found"
- Make sure you completed Step 1 first
- Check the correct client folder
- Use listDirectory to find the file

### "TES-070 generation failed"
- Verify the JSON file is valid
- Check that Python is installed
- Run the command manually if needed

---

## Getting Help

- **Kiro AI**: Ask Kiro any questions about the workflow
- **Documentation**: Check `Projects/README.md` and `WORKSPACE_STRUCTURE.md`
- **Steering Files**: Kiro has detailed guides in `.kiro/steering/`
- **Examples**: See `TES-070/Sample_Documents/` for reference

---

## Next Steps

1. Choose a client from the 4 available
2. Click "Interface Step 1: Define Test Scenarios" to start
3. Follow the 3-step workflow
4. Submit your TES-070 for review

**Ready to start? Click "Interface Step 1: Define Test Scenarios" now!** 🚀

