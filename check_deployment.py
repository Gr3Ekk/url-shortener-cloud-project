#!/usr/bin/env python3
"""
Deployment Verification Script
Checks if all files are ready for Google App Engine deployment
"""

import os
import sys

def check_app_yaml():
    """Check if app.yaml is properly configured"""
    print("🔍 Checking app.yaml...")
    
    if not os.path.exists('app.yaml'):
        print("❌ app.yaml not found!")
        return False
    
    try:
        with open('app.yaml', 'r') as f:
            content = f.read()
        
        # Check required content
        required_content = [
            'runtime: python39',
            'GOOGLE_CLOUD_PROJECT: url-shortener-luis-2025-dac25',
            'FIRESTORE_COLLECTION: url_mappings',
            'FLASK_DEBUG: false'
        ]
        
        for item in required_content:
            if item not in content:
                print(f"❌ Missing or incorrect in app.yaml: {item}")
                return False
        
        if 'TODO' in content or 'DERRICK' in content:
            print("❌ app.yaml still contains TODO comments")
            return False
        
        print("✅ app.yaml is properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Error reading app.yaml: {e}")
        return False

def check_requirements():
    """Check if requirements.txt exists and has required packages"""
    print("🔍 Checking requirements.txt...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        return False
    
    with open('requirements.txt', 'r') as f:
        requirements = f.read().lower()
    
    required_packages = ['flask', 'google-cloud-firestore', 'flask-cors', 'python-dotenv']
    
    for package in required_packages:
        if package not in requirements:
            print(f"❌ Missing required package: {package}")
            return False
    
    print("✅ requirements.txt contains all required packages")
    return True

def check_tests():
    """Check if test files exist and are not empty"""
    print("🔍 Checking test files...")
    
    test_files = ['tests/test_shorten.py', 'tests/test_redirect.py']
    
    for test_file in test_files:
        if not os.path.exists(test_file):
            print(f"❌ {test_file} not found!")
            return False
        
        with open(test_file, 'r') as f:
            content = f.read()
        
        if 'TODO' in content or 'pass' in content:
            print(f"❌ {test_file} still contains TODO or placeholder code")
            return False
        
        if len(content) < 500:  # Basic check for substantial content
            print(f"❌ {test_file} appears to be empty or too short")
            return False
    
    print("✅ Test files are properly implemented")
    return True

def check_gcloudignore():
    """Check if .gcloudignore exists and excludes sensitive files"""
    print("🔍 Checking .gcloudignore...")
    
    if not os.path.exists('.gcloudignore'):
        print("❌ .gcloudignore not found!")
        return False
    
    with open('.gcloudignore', 'r') as f:
        content = f.read()
    
    sensitive_patterns = ['*.json', 'service-account-key.json', '.env']
    
    for pattern in sensitive_patterns:
        if pattern not in content:
            print(f"❌ .gcloudignore should exclude: {pattern}")
            return False
    
    print("✅ .gcloudignore properly excludes sensitive files")
    return True

def check_security():
    """Check for security issues"""
    print("🔍 Checking security...")
    
    # Check if service account key exists (should not be deployed)
    if os.path.exists('service-account-key.json'):
        print("⚠️  service-account-key.json found - make sure it's in .gcloudignore")
    
    # Check .env file
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()
        
        if 'dev-secret-key' in env_content:
            print("⚠️  .env still contains development secret key")
    
    print("✅ Security check passed")
    return True

def main():
    """Run all deployment checks"""
    print("🚀 DEPLOYMENT READINESS CHECK")
    print("=" * 50)
    
    checks = [
        check_app_yaml,
        check_requirements,
        check_tests,
        check_gcloudignore,
        check_security
    ]
    
    all_passed = True
    
    for check in checks:
        if not check():
            all_passed = False
        print()
    
    print("=" * 50)
    if all_passed:
        print("🎉 ALL CHECKS PASSED! Ready for deployment!")
        print()
        print("Next steps:")
        print("1. gcloud config set project url-shortener-luis-2025-dac25")
        print("2. gcloud app deploy")
        print("3. Test with: curl -X POST -H 'Content-Type: application/json' -d '{\"url\":\"https://example.com\"}' https://url-shortener-luis-2025-dac25.ue.r.appspot.com/api/shorten")
    else:
        print("❌ Some checks failed. Please fix the issues above before deploying.")
        sys.exit(1)

if __name__ == '__main__':
    main()
