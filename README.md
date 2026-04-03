# PDF Attachment Cleaner + Metadata Updater

A small Python script that:
- removes embedded attachments from PDFs
- clears all existing PDF doc info metadata
- removes XMP metadata if present
- optionally writes new custom metadata fields (Author, Subject, Keywords, Title, Creator, etc.)
- saves output without overwriting existing files by auto-incrementing filename (`example.pdf`, `example_1.pdf`, etc.)
- verifies the output PDF is cleaned

## 📦 Files
- `Remove_attachments_and_Update_metadata.py` - main script
- `requirements.txt` - dependencies
- `sample/Sample_PDF_with_attachments.pdf` - sample input PDF with embedded attachments (for testing)

## 🛠️ Requirements
- Python 3.9+ (recommended)
- `pikepdf` library

## ⚡ Setup (Windows / macOS / Linux)
1. Clone repository:
   ```bash
   git clone <your-repo-url>
   cd attachment_validator
   ```
2. Create virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate virtualenv:
   - Windows PowerShell:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - Windows cmd:
     ```cmd
     .\.venv\Scripts\activate.bat
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Run
Open and edit `Remove_attachments_and_Update_metadata.py` to set:
- `input_file`:
- `output_file`:
- `metadata` dict

Then run:
```bash
python Remove_attachments_and_Update_metadata.py
```

Outputs are saved to auto-incremented file if output file already exists (e.g. `current_filename_1.pdf`).

## 🧩 How it works
Inside `clean_pdf`:
1. opens input PDF using pikepdf
2. removes attachments with `pdf.attachments.clear()`
3. clears docinfo with `pdf.make_indirect(pikepdf.Dictionary())`
4. adds custom docinfo fields if passed
5. removes `pdf.Root['/Metadata']`
6. saves with unique pathname
7. re-opens saved PDF and verifies expected state

## 🛠️ Customization
Use `custom_metadata` dict:
```python
metadata = {
    "Author": "Your Name",
    "Subject": "My Document",
    "Keywords": "tag1,tag2",
    "Title": "Document Title",
    "Creator": "Your Script"
}
clean_pdf(input_file, output_file, custom_metadata=metadata)
```

## ✅ GitHub Project Tips
- Add README and requirements (done)
- Add `.gitignore` (e.g. ignore `.venv/`, `*.pdf` output)
- Add sample `input/` and `output/` directory patterns

## 💡 Notes
- Ensure the input PDF path exists.
- Require pikepdf behind the scenes to operate on metadata and attachments.
- You can parametrize script for CLI with `argparse` if needed later.
