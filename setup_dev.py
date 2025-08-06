# Quick Setup Script for Teammates
import os
import sys

def setup_for_development():
    """Set up the project for development without Google Cloud"""
    
    print("🚀 Setting up URL Shortener for development...")
    
    # Check if service account file exists
    if not os.path.exists('service-account-key.json'):
        print("⚠️  No Google Cloud credentials found.")
        print("🔧 Setting up MOCK mode for development...")
        
        # Create a development .env file
        env_content = """# Environment variables for DEVELOPMENT (MOCK MODE)
GOOGLE_CLOUD_PROJECT=mock-project
FIRESTORE_COLLECTION=url_mappings
FLASK_DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production
USE_MOCK_DATABASE=true
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Created .env file for mock development")
        print("✅ You can now run: python app.py")
        print("📝 The app will use in-memory storage instead of Google Cloud")
        
    else:
        print("✅ Google Cloud credentials found")
        print("✅ You can run: python app.py")
    
    print("\n🎯 Next steps:")
    print("1. Run: python app.py")
    print("2. Open: http://localhost:8080")
    print("3. Test the URL shortener!")

if __name__ == "__main__":
    setup_for_development()
