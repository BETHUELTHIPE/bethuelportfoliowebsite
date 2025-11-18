#!/usr/bin/env python
import os
import sys
import subprocess

os.chdir(r'c:\Users\Bethuel\Downloads\Bethuel-website-main\Bethuel-website-main')

# Run migrations
print("Running migrations...")
subprocess.run([sys.executable, 'manage.py', 'migrate'], check=False)

# Collect static files
print("Collecting static files...")
subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=False)

# Start development server
print("Starting development server...")
print("Access the website at http://127.0.0.1:8000")
subprocess.run([sys.executable, 'manage.py', 'runserver'])
