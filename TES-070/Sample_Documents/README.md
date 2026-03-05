# Sample TES-070 Documents

Reference TES-070 test results documents from previous FSM testing projects.

## 📚 Available Samples

1. **INT_FIN_010** - Receivables Invoice Import
   - Inbound interface testing
   - File-based data import
   - Validation and error handling

2. **INT_FIN_013** - GL Transaction Interface
   - GL transaction processing
   - Data validation workflows
   - Status tracking

3. **INT_FIN_127** - ACH Files Outbound Interface (Citizens Bank)
   - Outbound file generation
   - Bank-specific formatting
   - File transfer validation

## 🎯 How to Use These Samples

- **Template Reference**: Use as formatting guide for new TES-070 documents
- **Structure Examples**: See how test scenarios are organized
- **Evidence Standards**: Learn what screenshots and evidence to include
- **Analysis Practice**: Test the tes070_analyzer.py tool on these documents

## 🛠️ Analyze These Documents

```bash
# Analyze a sample document
python ReusableTools/tes070_analyzer.py "TES-070/Sample_Documents/SoNH_TES-070_INT_FIN_013.docx"

# Extract images from a sample
python ReusableTools/docx_image_extractor.py "TES-070/Sample_Documents/SoNH_TES-070_INT_FIN_010.docx"
```

## 📝 Note

These are reference documents only. Do not modify or delete. Create new test documents in the `Generated_TES070s/` folder.
