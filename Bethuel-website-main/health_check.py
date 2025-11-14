#!/usr/bin/env python
"""
Health Check Script for Production Services
Quick verification that all services are operational
"""

import subprocess
import requests
import redis
import psycopg2
import time
import sys

def check_docker_services():
    """Check if Docker services are running"""
    print("🐳 Checking Docker Services...")
    try:
        result = subprocess.run(['docker-compose', 'ps'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Docker Compose services are running")
            return True
        else:
            print("❌ Docker Compose services not running")
            return False
    except Exception as e:
        print(f"❌ Error checking Docker services: {e}")
        return False

def check_website():
    """Check if website is accessible"""
    print("🌐 Checking Website...")
    try:
        response = requests.get('http://localhost', timeout=10)
        if response.status_code == 200:
            print("✅ Website is accessible")
            return True
        else:
            print(f"❌ Website returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Website not accessible: {e}")
        return False

def check_redis():
    """Check Redis connection"""
    print("🔴 Checking Redis...")
    try:
        r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=5)
        r.ping()
        print("✅ Redis is connected")
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

def check_postgresql():
    """Check PostgreSQL connection"""
    print("🐘 Checking PostgreSQL...")
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='bethuel_portfolio',
            user='bethuel',
            password='bethuel123',
            connect_timeout=5
        )
        conn.close()
        print("✅ PostgreSQL is connected")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def check_pgadmin():
    """Check pgAdmin accessibility"""
    print("🔧 Checking pgAdmin...")
    try:
        response = requests.get('http://localhost:5050', timeout=10)
        if response.status_code == 200:
            print("✅ pgAdmin is accessible")
            return True
        else:
            print(f"❌ pgAdmin returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ pgAdmin not accessible: {e}")
        return False

def check_celery():
    """Check Celery worker status"""
    print("🔄 Checking Celery...")
    try:
        # Check if celery container is running
        result = subprocess.run(['docker-compose', 'logs', '--tail=10', 'celery'], 
                              capture_output=True, text=True, timeout=10)
        if 'ready' in result.stdout.lower():
            print("✅ Celery worker is ready")
            return True
        else:
            print("❌ Celery worker not ready")
            return False
    except Exception as e:
        print(f"❌ Error checking Celery: {e}")
        return False

def main():
    """Run all health checks"""
    print("🏥 Production Health Check")
    print("=" * 30)
    
    checks = [
        check_docker_services,
        check_website,
        check_redis,
        check_postgresql,
        check_pgadmin,
        check_celery
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            results.append(False)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 30)
    print(f"📊 Health Check Summary")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All services healthy! Production ready!")
        return True
    else:
        print("⚠️  Some services are unhealthy. Check logs.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)