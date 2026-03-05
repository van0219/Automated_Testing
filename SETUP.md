# FSM Automated Testing Workspace - Setup Guide

## Quick Start

Follow these steps to set up the workspace on your machine.

## Prerequisites

- **Python 3.10+** (Python 3.14 recommended)
- **Git** (for version control)
- **Windows OS** (current setup is Windows-optimized)

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs all required Python libraries:
- python-docx (document processing)
- PyPDF2 (PDF reading)
- pillow (image processing)
- pytesseract (OCR wrapper)
- pandas (data analysis)
- requests (API calls)
- And more...

### 2. Install Tesseract-OCR (Required for Image Analysis)

Tesseract-OCR is needed for the TES-070 analyzer to read text from screenshots.

**Windows Installation:**

1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (tesseract-ocr-w64-setup-*.exe)
3. During installation, note the installation path (default: `C:\Program Files\Tesseract-OCR`)
4. Add Tesseract to your PATH:
   - Open System Properties > Environment Variables
   - Edit "Path" variable
   - Add: `C:\Program Files\Tesseract-OCR`
5. Verify installation:
   ```bash
   tesseract --version
   ```

**Alternative (if PATH doesn't work):**

Set the tesseract path in your Python code:
```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 3. Configure Credentials

**CRITICAL**: Never commit credential files to git!

1. Navigate to `Credentials/` folder
2. Create/update these files:
   - `.env.fsm` - FSM environment URLs and usernames
   - `.env.passwords` - Actual passwords (git-ignored)
   - `*.ionapi` - ION API credentials for OAuth2

See `Credentials/README.md` for format details.

### 4. Configure Playwright (for Browser Automation)

Playwright is managed via MCP server (already configured in `.kiro/settings/mcp.json`).

No additional installation needed - Kiro handles this automatically.

## Workspace Structure

```
Automated_Testing/
├── .kiro/                  # Kiro configuration
│   ├── steering/          # AI guidance files
│   └── settings/          # MCP and other configs
├── Credentials/           # Auth credentials (NEVER commit!)
├── ReusableTools/         # Python utilities
│   ├── tes070_analyzer.py # TES-070 document analyzer
│   ├── docx_image_extractor.py
│   └── ...
├── TES-070/              # Test results documents
│   ├── Sample_Documents/  # Reference examples
│   ├── Generated_TES070s/ # New test outputs
│   └── extracted_images/  # Analysis artifacts
├── Temp/                 # Temporary files
├── requirements.txt      # Python dependencies
└── SETUP.md             # This file
```

## Verification

Test your setup:

```bash
# Test Python libraries
python -c "import docx, PyPDF2, PIL, pytesseract; print('✅ All libraries installed')"

# Test Tesseract-OCR
tesseract --version

# Test TES-070 analyzer
python ReusableTools/tes070_analyzer.py "TES-070/Sample_Documents/your_document.docx"
```

## Troubleshooting

### "tesseract not found" error

- Verify Tesseract is installed: `tesseract --version`
- Check PATH environment variable includes Tesseract directory
- Restart terminal/IDE after PATH changes

### "Module not found" errors

- Ensure you're using the correct Python environment
- Re-run: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.10+)

### Credential errors

- Verify credential files exist in `Credentials/` folder
- Check file formats match examples
- Ensure passwords are correct

## Team Collaboration

When sharing this workspace:

1. **DO commit**:
   - All Python scripts
   - requirements.txt
   - SETUP.md
   - Steering files
   - .gitignore

2. **DO NOT commit**:
   - Credentials/ folder contents
   - Temp/ folder contents
   - __pycache__/ folders
   - *.pyc files
   - Personal test data

3. **Each team member should**:
   - Run `pip install -r requirements.txt`
   - Install Tesseract-OCR
   - Add their own credentials to Credentials/ folder
   - Test setup with verification commands

## Support

For issues or questions:
- Check steering files in `.kiro/steering/`
- Review tool documentation in ReusableTools/
- Ask Kiro for help! 🤖
