# Team Setup Instructions

## 🚀 Getting Started - Team Members (Eli & Derrick)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Gr3Ekk/url-shortener-cloud-project.git
cd url-shortener-cloud-project
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Get Google Cloud Access
**Luis needs to:**
1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Select project: `url-shortener-luis-2025-dac25`
3. Go to **IAM & Admin** → **IAM**
4. Click **"Add"**
5. Add team member emails with **"Editor"** role
6. Each team member creates their own service account key

**OR Luis can share the service account key file (less secure but easier for development)**

### Step 4: Set Up Environment Variables
Create a `.env` file with:
```
GOOGLE_CLOUD_PROJECT=url-shortener-luis-2025-dac25
FIRESTORE_COLLECTION=url_mappings
FLASK_DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production
GOOGLE_APPLICATION_CREDENTIALS=service-account-key.json
```

### Step 5: Run the Application
```bash
python app.py
```

## 🔄 Alternative: Mock/Offline Development
If you can't set up Google Cloud access, you can work on your parts without the database:

### For Eli (Redirect Development):
- Modify `routes/redirect.py` to use mock data for testing
- Test with hardcoded URL mappings

### For Derrick (Testing & Deployment):
- Write tests that mock the database
- Set up deployment configurations
- Test API endpoints structure

## 📝 What Each Person Should Work On:

### Eli:
- File: `routes/redirect.py` ✅ (already done, but can enhance)
- File: `templates/404.html` ✅ (already done)
- Test redirect functionality
- Add analytics features

### Derrick:
- File: `app.yaml` (for Google App Engine deployment)
- Files: `tests/test_*.py` (write comprehensive tests)
- Set up CI/CD pipeline
- Deploy to Google App Engine
- Create deployment documentation

### Luis: ✅ Complete
- All API and database functions implemented
- Firestore integration working
- Frontend JavaScript implemented
