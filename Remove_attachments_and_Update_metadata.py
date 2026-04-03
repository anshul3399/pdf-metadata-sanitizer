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

    This will open file selection dialogs:
    1. Select the input PDF file to clean
    2. Choose the output location and filename for the cleaned PDF

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
import tkinter as tk
from tkinter import filedialog


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
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()
    
    # Select input PDF file
    input_file = filedialog.askopenfilename(
        title="Select PDF file to clean",
        filetypes=[("PDF files", "*.pdf")]
    )
    
    if not input_file:
        log("No input file selected. Exiting.", "INFO")
        exit()
    
    # Select output location for cleaned PDF
    default_output = os.path.splitext(os.path.basename(input_file))[0] + "_cleaned.pdf"
    output_file = filedialog.asksaveasfilename(
        title="Save cleaned PDF as",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile=default_output
    )
    
    if not output_file:
        log("No output file selected. Exiting.", "INFO")
        exit()

    # Define custom metadata to add to the PDF
    metadata = {
        "Author": "Anshul Sharma",
        "Subject": "Resume for Data Engineering Profile",
        "Keywords": "Data Engineering,professional,2.5 years of experience,Python,SQL,PySpark,Apache Spark,Apache Airflow,ETL,ELT,Data Pipelines,Data Engineering,Data Warehousing,Data Modeling,Batch Processing,Stream Processing,Big Data,Data Lake,Data Lakehouse,Distributed Computing,Schema Design,Star Schema,Snowflake Schema,SQL Optimization,Data Transformation,Data Ingestion,Data Processing,Data Integration,Workflow Orchestration,DAGs,Azure Data Factory,Azure Synapse Analytics,Azure Databricks,Azure Data Lake Storage,ADLS Gen2,Azure SQL Database,Azure Functions,Azure Event Hub,Azure Stream Analytics,Azure Purview,Azure Monitor,Amazon S3,AWS Glue,AWS Redshift,AWS Lambda,AWS RDS,AWS EMR,Amazon Athena,AWS Kinesis,Amazon MSK,AWS Step Functions,Amazon MWAA,Google Cloud Storage,BigQuery,Cloud SQL,Dataflow,Dataproc,Pub/Sub,Cloud Composer,Apache Beam,Kafka,Hadoop,Hive,Presto,Trino,Delta Lake,Parquet,ORC,Avro,Docker,Kubernetes,Git,CI/CD,Linux,Shell Scripting,PL/SQL,Apache Spark,Databricks,Git,GitHub,Apache Airflow,Apache Kafka,Snowflake,Oracle BI Publisher,IBM Cognos,Looker Studio,Oracle SQL,PostgreSQL,MySQL,MongoDB,Flutter,SonarQube,Microsoft Azure,Azure Data Factory,Google Cloud,Google Sheets,Google Apps Script,Zapier,REST APIs",
        "Title": "Resume_Anshul_Sharma",
        "Creator": "Anshul Sharma"
    }

    clean_pdf(input_file, output_file, custom_metadata=metadata)