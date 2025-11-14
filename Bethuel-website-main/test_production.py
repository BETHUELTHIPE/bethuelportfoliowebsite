#!/usr/bin/env python
"""
Production Testing Script for Bethuel Portfolio
Tests all functionalities to ensure production readiness
"""

import requests
import time
import json
import sys
from urllib.parse import urljoin

class ProductionTester:
    def __init__(self, base_url="http://localhost"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message
        })
        
    def test_service_health(self):
        """Test if all services are running"""
        print("\n🔍 Testing Service Health...")
        
        # Test main website
        try:
            response = self.session.get(self.base_url, timeout=10)
            self.log_test("Website Accessibility", 
                         response.status_code == 200,
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Website Accessibility", False, str(e))
            
        # Test pgAdmin
        try:
            response = requests.get(f"{self.base_url}:5050", timeout=5)
            self.log_test("pgAdmin Service", 
                         response.status_code == 200,
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("pgAdmin Service", False, str(e))
            
    def test_page_navigation(self):
        """Test all main pages load correctly"""
        print("\n🧭 Testing Page Navigation...")
        
        pages = [
            ('/', 'Home Page'),
            ('/about/', 'About Page'),
            ('/projects/', 'Projects Page'),
            ('/experience/', 'Experience Page'),
            ('/contact/', 'Contact Page'),
            ('/resume-page/', 'Resume Page'),
            ('/login/', 'Login Page'),
            ('/register/', 'Register Page'),
        ]
        
        for path, name in pages:
            try:
                url = urljoin(self.base_url, path)
                response = self.session.get(url, timeout=10)
                self.log_test(name, 
                             response.status_code == 200,
                             f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(name, False, str(e))
                
    def test_static_files(self):
        """Test static files are served correctly"""
        print("\n📁 Testing Static Files...")
        
        # Test CSS
        try:
            response = self.session.get(f"{self.base_url}/static/css/style.css", timeout=5)
            self.log_test("CSS Files", 
                         response.status_code == 200,
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("CSS Files", False, str(e))
            
        # Test JS
        try:
            response = self.session.get(f"{self.base_url}/static/js/animations.js", timeout=5)
            self.log_test("JavaScript Files", 
                         response.status_code == 200,
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("JavaScript Files", False, str(e))
            
    def test_authentication_flow(self):
        """Test registration and login functionality"""
        print("\n🔐 Testing Authentication Flow...")
        
        # Test registration page loads
        try:
            response = self.session.get(f"{self.base_url}/register/")
            self.log_test("Registration Page Load", 
                         response.status_code == 200 and 'csrf' in response.text.lower(),
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Registration Page Load", False, str(e))
            
        # Test login page loads
        try:
            response = self.session.get(f"{self.base_url}/login/")
            self.log_test("Login Page Load", 
                         response.status_code == 200 and 'csrf' in response.text.lower(),
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Login Page Load", False, str(e))
            
    def test_password_reset(self):
        """Test password reset functionality"""
        print("\n🔑 Testing Password Reset...")
        
        try:
            response = self.session.get(f"{self.base_url}/password-reset/")
            self.log_test("Password Reset Page", 
                         response.status_code == 200,
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Password Reset Page", False, str(e))
            
    def test_contact_form(self):
        """Test contact form functionality"""
        print("\n📧 Testing Contact Form...")
        
        try:
            # Get contact page with CSRF token
            response = self.session.get(f"{self.base_url}/contact/")
            self.log_test("Contact Form Load", 
                         response.status_code == 200 and 'name' in response.text.lower(),
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Contact Form Load", False, str(e))
            
    def test_resume_protection(self):
        """Test resume download protection"""
        print("\n📄 Testing Resume Protection...")
        
        try:
            # Test direct resume access (should redirect to login)
            response = self.session.get(f"{self.base_url}/resume/", allow_redirects=False)
            self.log_test("Resume Protection", 
                         response.status_code in [302, 403],
                         f"Status: {response.status_code} (Protected)")
        except Exception as e:
            self.log_test("Resume Protection", False, str(e))
            
    def test_security_headers(self):
        """Test security headers are present"""
        print("\n🛡️ Testing Security Headers...")
        
        try:
            response = self.session.get(self.base_url)
            headers = response.headers
            
            # Check for security headers
            security_checks = [
                ('X-Content-Type-Options', 'nosniff'),
                ('X-Frame-Options', 'SAMEORIGIN'),
                ('X-XSS-Protection', '1; mode=block'),
            ]
            
            for header, expected in security_checks:
                present = header in headers
                self.log_test(f"Security Header: {header}", 
                             present,
                             f"Present: {present}")
                             
        except Exception as e:
            self.log_test("Security Headers", False, str(e))
            
    def test_performance(self):
        """Test website performance"""
        print("\n⚡ Testing Performance...")
        
        try:
            start_time = time.time()
            response = self.session.get(self.base_url)
            load_time = time.time() - start_time
            
            self.log_test("Page Load Time", 
                         load_time < 3.0,
                         f"{load_time:.2f}s (Target: <3s)")
                         
            # Test gzip compression
            gzip_enabled = 'gzip' in response.headers.get('Content-Encoding', '')
            self.log_test("Gzip Compression", 
                         gzip_enabled,
                         f"Enabled: {gzip_enabled}")
                         
        except Exception as e:
            self.log_test("Performance Test", False, str(e))
            
    def test_responsive_design(self):
        """Test responsive design elements"""
        print("\n📱 Testing Responsive Design...")
        
        try:
            # Test with mobile user agent
            mobile_headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
            }
            response = self.session.get(self.base_url, headers=mobile_headers)
            
            # Check for viewport meta tag
            has_viewport = 'viewport' in response.text.lower()
            self.log_test("Mobile Viewport", 
                         has_viewport,
                         f"Viewport meta tag present: {has_viewport}")
                         
            # Check for Bootstrap responsive classes
            has_responsive = 'col-md' in response.text or 'col-lg' in response.text
            self.log_test("Responsive Grid", 
                         has_responsive,
                         f"Bootstrap responsive classes found: {has_responsive}")
                         
        except Exception as e:
            self.log_test("Responsive Design", False, str(e))
            
    def run_all_tests(self):
        """Run all production tests"""
        print("🚀 Starting Production Readiness Tests...")
        print("=" * 50)
        
        # Run all test suites
        self.test_service_health()
        self.test_page_navigation()
        self.test_static_files()
        self.test_authentication_flow()
        self.test_password_reset()
        self.test_contact_form()
        self.test_resume_protection()
        self.test_security_headers()
        self.test_performance()
        self.test_responsive_design()
        
        # Generate summary
        self.generate_summary()
        
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   - {result['test']}: {result['message']}")
                    
        print("\n" + "=" * 50)
        
        if failed_tests == 0:
            print("🎉 ALL TESTS PASSED! Production ready! 🎉")
        else:
            print("⚠️  Some tests failed. Review before production deployment.")
            
        return failed_tests == 0

if __name__ == "__main__":
    # Allow custom base URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost"
    
    tester = ProductionTester(base_url)
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)