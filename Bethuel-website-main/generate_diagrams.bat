@echo off
echo 🎨 Generating Website Architecture Diagrams...

echo 📦 Installing required packages...
pip install matplotlib pillow

echo 🔄 Creating diagrams...
python generate_diagrams.py

echo ✅ Diagram generation complete!
echo 📁 Check the 'diagrams' folder for all generated diagrams.

pause