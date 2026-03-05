# Test Scenario Templates

This folder contains predefined test scenario templates used by the Test Scenario Builder GUI.

## Template Files

### 1. `inbound_interface_template.json`
**Use For**: Inbound interfaces (data coming INTO FSM)

**Predefined Scenarios**:
- Successful Import
- Invalid Data Error
- Duplicate Record Handling

**Common Test Steps**:
- Upload file to SFTP
- Wait for File Channel trigger
- Check work unit status
- Verify data in FSM

### 2. `outbound_interface_template.json`
**Use For**: Outbound interfaces (data going OUT of FSM)

**Predefined Scenarios**:
- Successful Export
- No Data to Export
- Large Volume Export

**Common Test Steps**:
- Trigger interface
- Check work unit status
- Verify output file exists
- Validate file contents

### 3. `approval_workflow_template.json`
**Use For**: Approval workflows and IPA processes

**Predefined Scenarios**:
- Successful Approval
- Rejection Handling
- Multi-Level Approval

**Common Test Steps**:
- Trigger approval workflow
- Verify User Actions created
- Approve/Reject requests
- Verify status updates

## Template Structure

Templates contain only the `scenarios` array. The GUI adds interface metadata when the user fills out the form:

```json
{
  "scenarios": [
    {
      "title": "Scenario Title",
      "description": "Scenario description",
      "test_steps": [
        {
          "number": "1",
          "description": "Step description",
          "result": "PASS",
          "screenshot": "01_screenshot_name",
          "test_data_file": "",           // Optional - for upload steps
          "sftp_remote_path": ""          // Optional - for SFTP steps
        }
      ],
      "results": [
        "Expected result 1",
        "Expected result 2"
      ]
    }
  ]
}
```

## Interface Metadata (Added by GUI)

When saving, the GUI adds these fields from the sidebar form:

### Required Fields
- `interface_id`: Interface identifier (e.g., "INT_FIN_013")
- `interface_name`: Human-readable name (e.g., "GL Transaction Interface")
- `interface_type`: Type of interface ("inbound", "outbound", or "approval")
- `client_name`: Client name (e.g., "State of New Hampshire")
- `author`: Test author name
- `environment`: FSM environment (e.g., "NMR2N66J9P445R7P_AX4")

### New Fields (Added in 2026)
- `file_channel_name`: FSM File Channel name for manual triggering (e.g., "SoNH-INT-FIN-013-FileChannel")
- `sftp_server`: SFTP server identifier for credentials (e.g., "Tamics10_AX1", "ACUITY_TST")

### Prerequisites
- `user_roles`: Array of FSM roles needed for testing
- `test_data_requirements`: Description of test data needed
- `configuration_prerequisites`: Setup requirements

## Complete JSON Output Example

```json
{
  "interface_id": "INT_FIN_013",
  "interface_name": "GL Transaction Interface",
  "interface_type": "inbound",
  "client_name": "State of New Hampshire",
  "author": "Van Anthony Silleza",
  "environment": "NMR2N66J9P445R7P_AX4",
  "file_channel_name": "SoNH-INT-FIN-013-FileChannel",
  "sftp_server": "Tamics10_AX1",
  "user_roles": [
    "Process Server Administrator",
    "Staff Accountant"
  ],
  "test_data_requirements": "Sample CSV file with transactions",
  "configuration_prerequisites": "IPA process deployed\nFile Channel configured\nSFTP credentials set up",
  "scenarios": [
    // ... scenarios from template ...
  ]
}
```

## Usage in Test Scenario Builder

1. **Select Interface Type**: Choose Inbound, Outbound, or Approval
2. **Template Auto-Loads**: Predefined scenarios load from corresponding template
3. **Fill Interface Details**: Complete sidebar form (ID, name, client, etc.)
4. **Edit Scenarios**: Modify scenarios as needed (add/delete/reorder)
5. **Save JSON**: Complete JSON saved to `Projects/{ClientName}/TestScripts/{interface_type}/`

## Customizing Templates

To modify default scenarios:

1. Edit the appropriate template JSON file
2. Follow the structure shown above
3. Save changes
4. New test scenarios will use updated templates

## Template Best Practices

### Test Step Fields
- `number`: Sequential step number (1, 2, 3...)
- `description`: Clear, actionable step description
- `result`: Expected result ("PASS", "FAIL", "PENDING")
- `screenshot`: Screenshot filename without extension
- `test_data_file`: (Optional) Test data filename from `test_data/` folder
- `sftp_remote_path`: (Optional) SFTP path for file operations

### When to Include Optional Fields

**test_data_file**:
- Include when step involves uploading a file
- GUI shows browse button for these steps
- File should exist in `Projects/{ClientName}/TestScripts/test_data/`

**sftp_remote_path**:
- Include when step involves SFTP operations
- Common paths:
  - `/Infor_FSM/Inbound/` - Inbound files
  - `/Infor_FSM/Outbound/` - Outbound files
  - `/Infor_FSM/Inbound/{InterfaceName}/` - Interface-specific

### Scenario Results
- List expected outcomes
- Keep concise and measurable
- Focus on observable behavior

## File Channel & SFTP Configuration

### File Channel Name
The `file_channel_name` field enables manual File Channel triggering:

**Purpose**: Eliminate 5-6 minute wait times during testing

**How to Find**:
1. Navigate to FSM > Process Server Administrator
2. Go to Channels Administrator > File Channels
3. Find the File Channel for your interface
4. Copy the exact name (e.g., "SoNH-INT-FIN-013-FileChannel")

**Usage in Testing**:
- Test automation can navigate to the specific File Channel
- Right-click > "Scan Now" to trigger immediately
- No need to wait for scheduled scan interval

### SFTP Server
The `sftp_server` field enables multi-SFTP support:

**Purpose**: Different RICE items can use different SFTP servers

**Common Values**:
- `Tamics10_AX1` - Sandbox/POC environment
- `ACUITY_TST` - Test environment
- `ACUITY_PRD` - Production environment
- `Custom_SFTP` - Client-specific SFTP servers

**Credentials Organization**:
```
Projects/{ClientName}/Credentials/
├── .env.fsm                    # FSM environment credentials
├── .env.passwords              # FSM passwords
├── Tamics10_AX1.sftp          # Sandbox SFTP credentials
├── ACUITY_TST.sftp            # Test SFTP credentials
└── Production_SFTP.sftp       # Production SFTP credentials
```

## Version History

### 2026-02-14
- Added `file_channel_name` field for manual File Channel triggering
- Added `sftp_server` field for multi-SFTP support
- Updated GUI to include new fields in sidebar
- Enhanced test automation capabilities

### 2025
- Initial template structure
- Three interface types (Inbound, Outbound, Approval)
- Predefined scenarios for common test cases

---

**Note**: Templates are read-only during GUI operation. Edit these files directly to change default scenarios for new test scripts.
