#!/usr/bin/env python
"""
Deployment script for Bethuel Portfolio Website
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return None

def main():
    print("🚀 Deploying Bethuel Portfolio Website...")
    
    # Install dependencies
    run_command("pip install -r requirements.txt", "Installing dependencies")
    
    # Run migrations
    run_command("python manage.py makemigrations", "Creating migrations")
    run_command("python manage.py migrate", "Running migrations")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Setup project
    run_command("python manage.py setup_project", "Setting up project")
    
    print("\n🎉 Deployment completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your email credentials")
    print("2. Set DJANGO_DEBUG=False for production")
    print("3. Update DJANGO_ALLOWED_HOSTS with your domain")
    print("4. Run: python manage.py runserver")

if __name__ == "__main__":
    main()