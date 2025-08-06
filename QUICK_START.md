# 🚀 URL Shortener - Quick Start Guide

## For Your Teammates (Eli & Derrick)

Perfect! Now that the URL shortener is working locally, here's how your teammates can get set up quickly:

### Option 1: Quick Development Setup (Recommended for Testing)

1. **Download the project files** (Luis should share the project folder or push to GitHub)

2. **Run the quick setup script:**
   ```bash
   python setup_dev.py
   ```
   This automatically configures mock development mode if Google Cloud isn't set up yet.

3. **Install dependencies:**
   ```bash
   pip install flask flask-cors python-dotenv
   ```

4. **Start the application:**
   ```bash
   python app.py
   ```

5. **Test it:** Open http://localhost:8080

### Option 2: Full Google Cloud Setup (For Production)

If you want teammates to use the real Google Cloud database:

1. **Luis needs to add teammates to Google Cloud:**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Select project: `url-shortener-luis-2025-dac25`
   - Go to IAM & Admin → IAM
   - Click "Add" and add teammate emails with "Editor" role

2. **Teammates get the service account file:**
   - Luis shares the `service-account-key.json` file
   - Place it in the project root folder

3. **Update .env file:**
   ```
   GOOGLE_CLOUD_PROJECT=url-shortener-luis-2025-dac25
   FIRESTORE_COLLECTION=url_mappings
   FLASK_DEBUG=true
   SECRET_KEY=your-secret-key
   USE_MOCK_DATABASE=false
   ```

### For Eli (Redirect Handler):
✅ Your redirect code is already integrated and working!
- Your `routes/redirect.py` file is connected to the Firestore database
- No changes needed - just run `python app.py` and test your redirects

### For Derrick (Deployment & Testing):
📋 Your remaining tasks:
1. **Create `app.yaml`** (Google App Engine configuration)
2. **Write tests** in the `tests/` folder
3. **Deploy to Google App Engine**
4. **Set up CI/CD pipeline**

### Quick Test Commands:

**Test URL creation:**
```bash
curl -X POST http://localhost:8080/api/shorten -H "Content-Type: application/json" -d "{\"url\":\"https://google.com\"}"
```

**Test redirect (replace abc123 with actual short code):**
```bash
curl -I http://localhost:8080/abc123
```

### Common Issues:

❌ **"Database connection failed"** → Run `python setup_dev.py` for mock mode
❌ **"Module not found"** → Run `pip install flask flask-cors python-dotenv`
❌ **"Permission denied"** → Luis needs to add you to Google Cloud project

### Next Steps:

1. **Everyone test locally first** with mock mode
2. **Luis shares Google Cloud access** for production database
3. **Derrick handles deployment** to make it live on the internet

The app is ready to go! 🎉
