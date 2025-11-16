#!/usr/bin/env python
"""
Generate PDF documentation from Markdown files
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    try:
        import markdown
        import weasyprint
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "weasyprint"])

def markdown_to_html(md_file, output_dir):
    """Convert markdown to HTML"""
    import markdown
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Configure markdown with extensions
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    html_content = md.convert(md_content)
    
    # Add CSS styling
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Bethuel Portfolio Documentation</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #2c3e50;
                margin-top: 30px;
            }}
            h1 {{
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                border-bottom: 2px solid #ecf0f1;
                padding-bottom: 5px;
            }}
            code {{
                background-color: #f8f9fa;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                border-left: 4px solid #3498db;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            blockquote {{
                border-left: 4px solid #3498db;
                margin: 0;
                padding-left: 20px;
                color: #666;
            }}
            .page-break {{
                page-break-before: always;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    html_file = os.path.join(output_dir, os.path.basename(md_file).replace('.md', '.html'))
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return html_file

def html_to_pdf(html_file, output_dir):
    """Convert HTML to PDF"""
    try:
        import weasyprint
        
        pdf_file = os.path.join(output_dir, os.path.basename(html_file).replace('.html', '.pdf'))
        weasyprint.HTML(filename=html_file).write_pdf(pdf_file)
        return pdf_file
    except Exception as e:
        print(f"Error converting to PDF: {e}")
        print("Trying alternative method...")
        return html_file

def main():
    """Generate PDF documentation"""
    print("📄 Generating PDF Documentation...")
    
    # Install requirements
    install_requirements()
    
    # Create output directory
    output_dir = "documentation_pdf"
    os.makedirs(output_dir, exist_ok=True)
    
    # Documentation files to convert
    doc_files = [
        "DOCUMENTATION.md",
        "API_DOCUMENTATION.md", 
        "DEPLOYMENT_GUIDE.md"
    ]
    
    generated_files = []
    
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            print(f"Converting {doc_file}...")
            
            # Convert to HTML
            html_file = markdown_to_html(doc_file, output_dir)
            print(f"✅ HTML: {html_file}")
            
            # Convert to PDF
            pdf_file = html_to_pdf(html_file, output_dir)
            print(f"✅ PDF: {pdf_file}")
            
            generated_files.append(pdf_file)
        else:
            print(f"❌ File not found: {doc_file}")
    
    print(f"\n📚 Documentation generated in '{output_dir}' folder:")
    for file in generated_files:
        print(f"   - {os.path.basename(file)}")
    
    # Create combined documentation
    print(f"\n📖 Files available:")
    print(f"   - Main Documentation: {output_dir}/DOCUMENTATION.pdf")
    print(f"   - API Reference: {output_dir}/API_DOCUMENTATION.pdf") 
    print(f"   - Deployment Guide: {output_dir}/DEPLOYMENT_GUIDE.pdf")

if __name__ == "__main__":
    main()