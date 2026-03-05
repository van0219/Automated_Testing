# Automated Testing Framework - Changelog

All notable changes to the FSM automated testing framework will be documented in this file.

## [Unreleased]

### Added - February 14, 2026

#### Test Scenario Builder GUI Updates
- Added `file_channel_name` field to capture File Channel name for manual triggering
- Added `sftp_server` field to support multiple SFTP server configurations
- Updated `test_scenario_builder_modern.py` GUI with new form fields in sidebar

#### SFTP Helper Multi-Server Support
- Updated `sftp_helper.py` `load_sftp_credentials()` function to accept optional `server_name` parameter
- Now supports server-specific credential files (e.g., `Tamics10_AX1.sftp`, `ACUITY_TST.sftp`)
- Maintains backward compatibility with `.env.passwords` file

### Benefits
- **File Channel Manual Triggering**: Test automation can now trigger File Channel scans immediately instead of waiting 5-6 minutes
- **Multi-SFTP Support**: Different RICE items can specify different SFTP servers
- **Better Organization**: SFTP credentials can be organized by server in separate files
- **Test Portability**: Test scenarios are now self-contained with all necessary configuration

### Migration Notes
For existing test scenarios:
1. Open JSON file in Test Scenario Builder GUI
2. Add File Channel name from FSM (Process Server Administrator > Channels Administrator > File Channels)
3. Add SFTP server identifier (e.g., "Tamics10_AX1")
4. Save - new fields will be included

### Files Modified
- `ReusableTools/test_scenario_builder_modern.py` - Added form fields and data handling
- `ReusableTools/sftp_helper.py` - Added multi-server credential support
- `.kiro/templates/README.md` - Updated documentation

---

## Version History

### Initial Release - February 2026
- Test Scenario Builder GUI with card-based interface
- SFTP helper for file upload/download operations
- TES-070 document generator
- Test data generator with FSM field discovery
- Playwright-based FSM automation examples
