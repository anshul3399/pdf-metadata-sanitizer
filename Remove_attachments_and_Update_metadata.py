'''
Remove attachments + reset/replace PDF metadata

This script:
- opens an input PDF
- removes all embedded files/attachments (`pdf.attachments.clear()`)
- clears existing DocInfo (author/title/subject/keywords/creation date/etc.)
- optionally sets custom metadata fields (Author, Subject, Keywords, etc.)
- removes XMP metadata if present
- saves output PDF and avoids overwrite by auto-incrementing filename:
    example.pdf -> example_1.pdf -> example_2.pdf ...
- re-opens output PDF to verify attachments + metadata removal/addition

Usage:
    python Remove_attachments_and_Update_metadata.py

Main function:
    clean_pdf(input_path, output_path, custom_metadata={...})

Custom metadata:
    { "Author":"...", "Subject":"...", "Keywords":"...", ... }

NOTE: Requires `pikepdf` installed (pip install pikepdf).
'''

import pikepdf
import traceback
import datetime
import os


def log(msg, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")


def get_unique_filename(filepath):
    """
    If file exists, append _1, _2, etc. before the extension.
    Example: Resume.pdf -> Resume_1.pdf -> Resume_2.pdf
    """
    if not os.path.exists(filepath):
        return filepath
    
    # Split filename and extension
    base, ext = os.path.splitext(filepath)
    counter = 1
    
    # Keep incrementing until we find a unique filename
    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1
    
    new_filepath = f"{base}_{counter}{ext}"
    log(f"Output file exists, using: {os.path.basename(new_filepath)}")
    return new_filepath


def clean_pdf(input_pdf, output_pdf, custom_metadata=None):
    unique_output = None  # Track the actual output filename used
    try:
        log(f"Opening PDF: {input_pdf}")
        pdf = pikepdf.Pdf.open(input_pdf)

        # =========================
        # 🔍 STEP 1: REMOVE ATTACHMENTS
        # =========================
        log("Checking for embedded attachments...")

        try:
            pdf.attachments.clear()
            log("All embedded attachments removed ✅")
        except Exception as e:
            log(f"Error removing attachments: {e}", "ERROR")

        # =========================
        # 🔍 STEP 2: CLEAR DOCINFO
        # =========================
        log("Clearing DOCINFO metadata...")

        try:
            pdf.docinfo = pdf.make_indirect(pikepdf.Dictionary())
            log("DOCINFO cleared ✅")
        except Exception as e:
            log(f"Failed to clear docinfo: {e}", "ERROR")

        # =========================
        # 🔍 STEP 2.5: SET CUSTOM METADATA
        # =========================
        if custom_metadata:
            log("Adding custom metadata...")
            try:
                for key, value in custom_metadata.items():
                    # Ensure key starts with /
                    pdf_key = key if key.startswith('/') else f'/{key}'
                    pdf.docinfo[pdf_key] = value
                log(f"Added {len(custom_metadata)} metadata field(s) ✅")
            except Exception as e:
                log(f"Failed to add custom metadata: {e}", "ERROR")
        else:
            log("No custom metadata provided")

        # =========================
        # 🔍 STEP 3: REMOVE XMP METADATA
        # =========================
        log("Checking XMP metadata...")

        try:
            if "/Metadata" in pdf.Root:
                del pdf.Root["/Metadata"]
                log("XMP metadata removed ✅")
            else:
                log("No XMP metadata found")
        except Exception as e:
            log(f"Error removing XMP: {e}", "ERROR")

        # =========================
        # 🔍 STEP 4: FORCE CLEAN SAVE
        # =========================
        log("Saving cleaned PDF...")

        try:
            # Get unique filename if output file already exists
            unique_output = get_unique_filename(output_pdf)
            
            pdf.save(
                unique_output,
                linearize=True,      # rebuild structure
                compress_streams=True
            )
            log(f"PDF saved successfully to: {os.path.basename(unique_output)} ✅")
        except Exception as e:
            log(f"Save failed: {e}", "CRITICAL")
            return

        # =========================
        # 🔍 STEP 5: VERIFY CLEAN
        # =========================
        log("Verifying cleaned PDF...")

        try:
            # Use the saved unique filename for verification
            new_pdf = pikepdf.Pdf.open(unique_output)

            if new_pdf.docinfo:
                log(f"Remaining docinfo: {new_pdf.docinfo}", "WARN")
            else:
                log("No docinfo metadata found ✅")

            if "/Metadata" in new_pdf.Root:
                log("XMP metadata STILL PRESENT ❌", "ERROR")
            else:
                log("No XMP metadata found ✅")

            if new_pdf.attachments:
                log("Attachments STILL PRESENT ❌", "ERROR")
            else:
                log("No attachments found ✅")

        except Exception as e:
            log(f"Verification failed: {e}", "ERROR")

        log("🎉 CLEANING COMPLETE")

    except Exception as e:
        log("CRITICAL FAILURE", "CRITICAL")
        log(str(e), "CRITICAL")
        traceback.print_exc()


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    input_file = r"D:\Python_Projects\POC_Remove_attachments_and_Update_metadata\sample\Sample PDF_with_attachments.pdf"
    output_file = r"D:\Python_Projects\POC_Remove_attachments_and_Update_metadata\sample\Sample PDF_with_(removed attachments).pdf"

    # Define custom metadata to add to the PDF
    metadata = {
        "Author": "update the author name",
        "Subject": "Sample PDF file with removed attachments and metadata",
        "Keywords": "Removed attachments,Removed non-required Metadata,Updated PDF",
        "Title": "Sample PDF_with_(removed attachments)",
        "Creator": "Script"
    }

    clean_pdf(input_file, output_file, custom_metadata=metadata)