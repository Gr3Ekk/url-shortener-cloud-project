# 🚀 Derrick's Deployment & Testing Guide
## Google App Engine Deployment Setup

Hey Derrick! This is your comprehensive guide for handling the deployment and testing parts of our URL shortener project.

## 📋 Your Responsibilities:
1. **Create App Engine configuration (`app.yaml`)**
2. **Write comprehensive tests**
3. **Deploy to Google App Engine**
4. **Set up CI/CD pipeline (optional)**

---

## Part 1: Google App Engine Configuration

### Step 1: Create `app.yaml` file
Create a file called `app.yaml` in the project root with this configuration:

```yaml
runtime: python39

# Environment variables for production
env_variables:
  GOOGLE_CLOUD_PROJECT: url-shortener-luis-2025-dac25
  FIRESTORE_COLLECTION: url_mappings
  FLASK_DEBUG: false
  SECRET_KEY: your-production-secret-key-here
  USE_MOCK_DATABASE: false

# Automatic scaling configuration
automatic_scaling:
  min_instances: 0
  max_instances: 10
  target_cpu_utilization: 0.6

# Instance configuration
instance_class: F1

# Static file handling
handlers:
- url: /static
  static_dir: static
- url: /.*
  script: auto
```

### Step 2: Create `requirements.txt`
Create this file to specify dependencies for App Engine:

```txt
Flask==2.3.3
Flask-CORS==4.0.0
python-dotenv==1.0.0
google-cloud-firestore==2.11.1
```

### Step 3: Update the production secret key
In your `app.yaml`, replace `your-production-secret-key-here` with a strong secret:
- Generate a random 32+ character string
- **NEVER use the dev secret key in production!**

---

## Part 2: Testing Implementation

### Step 1: Test Structure
Create these test files in the `tests/` directory:

#### `tests/test_url_encoder.py`
```python
import unittest
from utils.url_encoder import URLEncoder

class TestURLEncoder(unittest.TestCase):
    def setUp(self):
        self.encoder = URLEncoder()
    
    def test_validate_url_valid(self):
        # Test valid URLs
        self.assertTrue(self.encoder.validate_url("https://google.com"))
        self.assertTrue(self.encoder.validate_url("http://example.org"))
    
    def test_validate_url_invalid(self):
        # Test invalid URLs
        self.assertFalse(self.encoder.validate_url("not-a-url"))
        self.assertFalse(self.encoder.validate_url(""))
        self.assertFalse(self.encoder.validate_url("javascript:alert('xss')"))
    
    def test_generate_short_code_length(self):
        # Test short code generation
        code = self.encoder.generate_short_code()
        self.assertEqual(len(code), 6)
    
    def test_generate_short_code_characters(self):
        # Test short code uses valid characters
        valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        code = self.encoder.generate_short_code()
        for char in code:
            self.assertIn(char, valid_chars)

if __name__ == '__main__':
    unittest.main()
```

#### `tests/test_api_endpoints.py`
```python
import unittest
import json
from app import create_app

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_shorten_url_success(self):
        # Test successful URL shortening
        response = self.client.post('/api/shorten',
                                  data=json.dumps({'url': 'https://google.com'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('short_url', data)
        self.assertIn('short_code', data)
    
    def test_shorten_url_invalid(self):
        # Test invalid URL rejection
        response = self.client.post('/api/shorten',
                                  data=json.dumps({'url': 'not-a-url'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_health_check(self):
        # Test health check endpoint
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
    
    def test_redirect_nonexistent(self):
        # Test redirect for non-existent code
        response = self.client.get('/nonexistent')
        # Should redirect to error page or return 404
        self.assertIn(response.status_code, [404, 302])

if __name__ == '__main__':
    unittest.main()
```

#### `tests/test_database_mock.py`
```python
import unittest
import os
from config.mock_database import MockURLMapping

class TestMockDatabase(unittest.TestCase):
    def setUp(self):
        # Ensure we're using mock database
        os.environ['USE_MOCK_DATABASE'] = 'true'
        self.mock_db = MockURLMapping()
    
    def test_create_and_get_mapping(self):
        # Test creating and retrieving a mapping
        result = self.mock_db.create_mapping('https://google.com', 'test123')
        self.assertIsNotNone(result)
        
        retrieved = self.mock_db.get_mapping('test123')
        self.assertEqual(retrieved['original_url'], 'https://google.com')
        self.assertTrue(retrieved['exists'])
    
    def test_increment_clicks(self):
        # Test click counting
        self.mock_db.create_mapping('https://example.com', 'click123')
        
        # Initial clicks should be 0
        mapping = self.mock_db.get_mapping('click123')
        self.assertEqual(mapping['click_count'], 0)
        
        # Increment and check
        self.mock_db.increment_clicks('click123')
        mapping = self.mock_db.get_mapping('click123')
        self.assertEqual(mapping['click_count'], 1)

if __name__ == '__main__':
    unittest.main()
```

### Step 2: Run Tests
```bash
# Run individual test files
python -m pytest tests/test_url_encoder.py -v
python -m pytest tests/test_api_endpoints.py -v
python -m pytest tests/test_database_mock.py -v

# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
pip install pytest-cov
python -m pytest tests/ --cov=. --cov-report=html
```

---

## Part 3: Deployment to Google App Engine

### Step 1: Install Google Cloud SDK
1. Download from: https://cloud.google.com/sdk/docs/install
2. Run the installer
3. Open new terminal and verify: `gcloud --version`

### Step 2: Authenticate and Set Project
```bash
# Login to Google Cloud
gcloud auth login

# Set the project
gcloud config set project url-shortener-luis-2025-dac25

# Verify you have access
gcloud projects describe url-shortener-luis-2025-dac25
```

### Step 3: Enable Required APIs
```bash
# Enable App Engine API
gcloud services enable appengine.googleapis.com

# Enable Firestore API (if not already enabled)
gcloud services enable firestore.googleapis.com
```

### Step 4: Initialize App Engine
```bash
# Initialize App Engine (choose region when prompted)
gcloud app create --region=us-central1
```

### Step 5: Deploy the Application
```bash
# Deploy to App Engine
gcloud app deploy

# View your deployed app
gcloud app browse
```

### Step 6: Monitor and Debug
```bash
# View logs
gcloud app logs tail -s default

# View app versions
gcloud app versions list

# Set traffic to specific version
gcloud app services set-traffic default --splits=VERSION_ID=1
```

---

## Part 4: Security & Environment Setup

### Important Security Notes:
1. **Never commit `service-account-key.json` to Git!**
2. **App Engine uses built-in service accounts** - no need for the JSON file in production
3. **Change the SECRET_KEY** in `app.yaml` to a strong production value
4. **Set `FLASK_DEBUG=false`** in production

### Environment Variables in Production:
- App Engine automatically uses the project's default service account
- Firestore permissions are handled through IAM
- No need to set `GOOGLE_APPLICATION_CREDENTIALS` in `app.yaml`

---

## Part 5: CI/CD Pipeline (Optional Advanced)

### GitHub Actions Setup
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to App Engine

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v
    
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v0
      with:
        project_id: url-shortener-luis-2025-dac25
        service_account_key: ${{ secrets.GCP_SA_KEY }}
    
    - name: Deploy to App Engine
      run: gcloud app deploy --quiet
```

---

## 🎯 Your Checklist:

- [ ] Create `app.yaml` with proper configuration
- [ ] Create `requirements.txt` with dependencies
- [ ] Write comprehensive tests (at least 3 test files)
- [ ] Install Google Cloud SDK
- [ ] Set up authentication and project access
- [ ] Deploy to App Engine successfully
- [ ] Verify the deployed app works
- [ ] Set up monitoring and logging
- [ ] (Optional) Set up CI/CD pipeline

## 🆘 Troubleshooting:

**"Permission denied"** → Ask Luis to add you as Editor in Google Cloud Console
**"App Engine not found"** → Run `gcloud app create` first
**"Tests failing"** → Make sure mock database is working locally first
**"Deployment fails"** → Check logs with `gcloud app logs tail`

## 📞 Need Help?
- Check Google Cloud documentation: https://cloud.google.com/appengine/docs
- Ask Luis for Google Cloud project access
- Test locally first with mock database before deploying

Good luck with the deployment! 🚀
