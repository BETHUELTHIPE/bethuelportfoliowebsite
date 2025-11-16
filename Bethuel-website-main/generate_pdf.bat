@echo off
echo 📄 Generating PDF Documentation...

echo 📦 Installing required packages...
pip install markdown weasyprint

echo 🔄 Converting documentation to PDF...
python generate_pdf.py

echo ✅ PDF generation complete!
echo 📁 Check the 'documentation_pdf' folder for PDF files.

pause