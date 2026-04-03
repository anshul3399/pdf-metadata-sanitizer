# PDF Attachment Cleaner and Metadata Updater - Application Context

## Project Overview
This project is a Python-based utility script designed to process PDF files by removing embedded attachments and updating/resetting metadata. The application is self-contained, command-line driven, and uses the `pikepdf` library for PDF manipulation. It ensures output files are not overwritten by auto-incrementing filenames and includes verification steps to confirm successful cleaning.

**Project Name:** PDF Attachment Cleaner + Metadata Updater  
**Main File:** `Remove_attachments_and_Update_metadata.py`  
**Language:** Python 3.9+  
**Dependencies:** Listed in `requirements.txt` (primarily `pikepdf`)  
**Sample Data:** Located in `sample/` directory with example PDF files for testing  

## Purpose and Functionality
The core purpose of this application is to sanitize PDF documents by:
- Removing all embedded files/attachments from the PDF
- Clearing existing document information metadata (DocInfo) such as author, title, subject, keywords, creation date, etc.
- Optionally adding custom metadata fields to replace the cleared ones
- Removing XMP (Extensible Metadata Platform) metadata if present
- Saving the cleaned PDF with a unique filename to avoid overwriting existing files
- Verifying the output PDF to ensure attachments and unwanted metadata have been successfully removed

This is particularly useful for:
- Privacy protection (removing embedded sensitive files)
- Document standardization (resetting metadata for redistribution)
- Compliance with data handling policies
- Preparing PDFs for secure sharing or archiving

## Key Features
- **Attachment Removal:** Uses `pdf.attachments.clear()` to remove all embedded files
- **Metadata Clearing:** Resets DocInfo to an empty dictionary
- **Custom Metadata Addition:** Supports adding new metadata fields like Author, Subject, Keywords, Title, Creator
- **XMP Removal:** Deletes XMP metadata from the PDF root if present
- **Safe Saving:** Auto-increments output filename (e.g., `file.pdf` → `file_1.pdf` → `file_2.pdf`) to prevent overwrites
- **Verification:** Re-opens the saved PDF to confirm cleaning was successful
- **Logging:** Provides timestamped console output for each step with INFO, WARN, ERROR, and CRITICAL levels
- **Error Handling:** Comprehensive try-except blocks with traceback printing for debugging

## Dependencies
- **pikepdf:** Core library for PDF manipulation (reading, writing, metadata handling)
- **datetime:** Standard library for timestamp logging
- **os:** Standard library for file path operations
- **traceback:** Standard library for error reporting

**requirements.txt content:**
```
pikepdf
```

## Setup Instructions
1. **Clone or Download:** Obtain the project files to a local directory
2. **Create Virtual Environment:**
   ```bash
   python -m venv .venv
   ```
3. **Activate Virtual Environment:**
   - Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
   - Windows CMD: `.\.venv\Scripts\activate.bat`
   - macOS/Linux: `source .venv/bin/activate`
4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Prepare Input Files:** Place PDF files to process in an accessible directory (e.g., `sample/` folder)

## Code Structure and Architecture

### Main Script: `Remove_attachments_and_Update_metadata.py`

#### Global Functions
- **`log(msg, level="INFO")`**: Utility function for timestamped console logging with severity levels
- **`get_unique_filename(filepath)`**: Generates a unique output filename by appending incremental numbers if the target file exists

#### Main Function: `clean_pdf(input_pdf, output_pdf, custom_metadata=None)`
This is the core function that performs all PDF processing operations in sequence:

1. **Open PDF:** Uses `pikepdf.Pdf.open(input_pdf)` to load the input file
2. **Remove Attachments:** Calls `pdf.attachments.clear()` to delete all embedded files
3. **Clear DocInfo:** Resets `pdf.docinfo` to an empty indirect dictionary
4. **Add Custom Metadata:** If provided, iterates through `custom_metadata` dict and sets DocInfo fields (prefixing keys with '/' if needed)
5. **Remove XMP:** Checks for and deletes `/Metadata` from `pdf.Root` if present
6. **Save PDF:** Uses `get_unique_filename()` for safe saving with linearization and stream compression
7. **Verify Output:** Re-opens the saved PDF to check for remaining attachments, DocInfo, and XMP metadata

#### Execution Block: `if __name__ == "__main__"`
- Defines hardcoded paths for `input_file` and `output_file`
- Defines a `metadata` dictionary with custom fields
- Calls `clean_pdf()` with the specified parameters

### File Organization
```
project_root/
├── Remove_attachments_and_Update_metadata.py  # Main script
├── requirements.txt                           # Python dependencies
├── README.md                                  # Project documentation
└── sample/                                    # Sample input/output files
    ├── Sample PDF_with_attachments.pdf        # Example input PDF
    └── [output files generated here]          # Cleaned PDFs
```

## Usage Examples

### Basic Usage (No Custom Metadata)
```python
from Remove_attachments_and_Update_metadata import clean_pdf

clean_pdf("input.pdf", "output.pdf")
```

### With Custom Metadata
```python
metadata = {
    "Author": "John Doe",
    "Subject": "Confidential Document",
    "Keywords": "sensitive,internal",
    "Title": "Cleaned PDF",
    "Creator": "PDF Cleaner Script"
}

clean_pdf("input.pdf", "output.pdf", custom_metadata=metadata)
```

### Command Line Execution
```bash
python Remove_attachments_and_Update_metadata.py
```
This will open interactive file selection dialogs:
1. First dialog: Select the input PDF file to clean
2. Second dialog: Choose the output location and filename for the cleaned PDF

The script will exit gracefully if the user cancels either dialog.

## Configuration and Customization
- **Input/Output Paths:** Selected interactively via file dialogs when running the script
- **Custom Metadata:** Edit the `metadata` dictionary in the main block to set desired DocInfo fields
- **Logging Level:** The `log()` function supports different levels but currently uses INFO by default
- **Save Options:** The `pdf.save()` call uses `linearize=True` and `compress_streams=True` for optimization

## Error Handling and Edge Cases
- **File Not Found:** Script will fail with exception if input PDF doesn't exist
- **Permission Issues:** May fail if output directory is not writable
- **Corrupted PDF:** pikepdf may throw exceptions for invalid PDF files
- **Large Files:** Processing time depends on PDF size and attachment count
- **Unicode Issues:** Metadata values should be properly encoded strings

## Verification and Testing
The script includes built-in verification:
- Checks for remaining DocInfo metadata
- Confirms XMP metadata removal
- Verifies attachment removal
- Logs results with appropriate severity levels

For testing:
1. Use the provided sample PDF in `sample/`
2. Run the script and check console output
3. Open the output PDF to manually verify metadata (using PDF reader properties)
4. Check file size reduction (attachments removed)

## Future Enhancements
Potential improvements identified in the code comments:
- Add CLI argument parsing with `argparse` for flexible input/output specification
- Support for batch processing multiple PDFs
- Configuration file support for metadata templates
- Integration with PDF viewers for automated verification
- Progress indicators for large file processing

## Security and Privacy Considerations
- Removes embedded files that may contain sensitive data
- Clears metadata that could reveal document origins or authors
- Does not modify PDF content or structure beyond attachments and metadata
- Output files are verified to ensure cleaning was successful

## Platform Compatibility
- **Operating Systems:** Windows, macOS, Linux
- **Python Version:** 3.9+ (due to pikepdf requirements)
- **Dependencies:** pikepdf works across platforms with appropriate system libraries

## Maintenance Notes
- Regularly update `pikepdf` for security patches
- Test with various PDF types and sources
- Monitor for changes in PDF standards affecting metadata handling
- Consider adding unit tests for core functions

This comprehensive context should enable an AI agent to understand, modify, extend, or integrate this PDF cleaning application effectively.