# FSM Approval Testing Power

Automated regression testing for FSM approval workflows using existing TES-070 documents.

## Installation

### Option 1: From Local Path (Development)

1. Open Kiro Powers panel (⚡ icon)
2. Click "Add power from Local Path"
3. Select `powers/fsm-approval-testing/` directory
4. Click Install

### Option 2: From GitHub (Production)

1. Push this directory to GitHub repository
2. Open Kiro Powers panel
3. Click "Add power from GitHub"
4. Enter repository URL
5. Click Install

## Structure

```
fsm-approval-testing/
├── POWER.md              # Power metadata and instructions
├── steering/             # Detailed workflow guides
│   ├── tes070-parsing.md
│   ├── test-execution.md
│   └── evidence-collection.md
└── README.md             # This file
```

**Note**: No `mcp.json` file needed - Playwright MCP tools are built into Kiro.

## Activation

Power activates automatically when you mention keywords:
- "FSM approval testing"
- "TES-070"
- "regression testing"
- "expense invoice approval"
- "approval workflow"

## Usage

**Example Request:**
```
Test the expense invoice approval workflow using TES-070 document EXT_FIN_004
```

**Power Will:**
1. Parse TES-070 document
2. Extract test scenarios
3. Execute tests with browser automation
4. Capture evidence screenshots
5. Report results

## Requirements

- Kiro IDE with built-in Playwright MCP support
- FSM credentials configured
- TES-070 documents in Word format
- Python tools in ReusableTools/

**Note**: Playwright MCP tools are built into Kiro. No external MCP server installation needed.

## Configuration

### FSM Credentials

Store in `Projects/{ClientName}/Credentials/`:

**`.env.fsm`:**
```
FSM_PORTAL_URL=https://mingle-portal.inforcloudsuite.com/v2/...
FSM_USERNAME=user@example.com
ENVIRONMENT=Other
```

**`.env.passwords`:**
```
FSM_PASSWORD=password123
```

### MCP Server

Playwright MCP tools are **built into Kiro** - no external server configuration needed.

No `mcp.json` file is included because Kiro provides Playwright tools natively.

## Supported Approval Types

- Expense Invoice Approval (Payables)
- Manual Journal Approval (General Ledger)
- Cash Ledger Transaction Approval (Cash Management)

## Output

### Test Instructions JSON
`Projects/{Client}/TestScripts/approval/{extension_id}_test_instructions.json`

### Evidence Screenshots
`Projects/{Client}/Temp/evidence/{scenario_id}/`

### Results Summary
Displayed in chat after execution

## Troubleshooting

### Power Not Activating

- Check keywords in your request
- Try explicit mention: "FSM approval testing"
- Verify power is installed (Powers panel)

### MCP Tools Not Available

- Playwright MCP tools are built into Kiro (no external server)
- Restart Kiro if tools not showing up
- Verify you're using latest Kiro version

### Browser Automation Fails

- Check FSM credentials
- Verify FSM URL accessible
- Review browser console for errors

## Development

### Testing Locally

1. Install power from local path
2. Test with sample TES-070 document
3. Verify browser automation works
4. Check evidence collection

### Updating Power

1. Edit POWER.md or steering files
2. Power updates automatically (no reinstall needed)
3. Test changes with sample request

### Publishing

1. Push to GitHub repository
2. Share repository URL
3. Others can install via "Add power from GitHub"

## Version History

- **1.0.1** (2026-03-10) - Test execution validation
  - Successfully validated Scenario 3.1 (garnishment invoice auto-approval)
  - Confirmed browser automation works end-to-end
  - Added work unit monitoring guidance
  - Documented async approval workflow behavior
  - Added troubleshooting for common issues

- **1.0.0** (2026-03-06) - Initial release

## License

Proprietary - For internal use only

## Support

For issues or questions, check:
1. Steering files for detailed workflows
2. APPROVAL_TESTING_SOLUTIONS_HISTORY.md for known issues
3. Contact development team
