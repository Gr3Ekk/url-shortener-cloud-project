# TODO: DERRICK - Deployment and Setup Instructions
"""
DEPLOYMENT SETUP INSTRUCTIONS

TASKS FOR DERRICK:
1. Set up Google Cloud Project
2. Configure App Engine
3. Set up Firestore database
4. Deploy application
5. Test deployed endpoints
6. Create deployment scripts

GOOGLE CLOUD SETUP STEPS:
1. Create new Google Cloud Project
2. Enable required APIs:
   - App Engine Admin API
   - Cloud Firestore API
   - Cloud Build API

3. Set up Firestore:
   - Go to Firestore in Console
   - Create database in Native mode
   - Choose appropriate region

4. Set up authentication:
   - Create service account
   - Download JSON key file
   - Set GOOGLE_APPLICATION_CREDENTIALS environment variable

LOCAL DEVELOPMENT SETUP:
1. Install Google Cloud SDK
2. Run: gcloud auth application-default login
3. Set project: gcloud config set project YOUR_PROJECT_ID
4. Install dependencies: pip install -r requirements.txt
5. Run locally: python app.py

DEPLOYMENT COMMANDS:
# Initial deployment
gcloud app deploy

# Deploy specific version
gcloud app deploy --version=v1 --no-promote

# Promote version to receive traffic
gcloud app versions migrate v1

# View logs
gcloud app logs tail -s default

TESTING DEPLOYED APPLICATION:
# Test shortening endpoint
curl -X POST -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' \
  https://YOUR_PROJECT_ID.appspot.com/api/shorten

# Test redirect (in browser)
https://YOUR_PROJECT_ID.appspot.com/SHORT_CODE

MONITORING AND DEBUGGING:
- Use Google Cloud Console for monitoring
- Check App Engine logs for errors
- Use Cloud Monitoring for performance metrics
- Set up error reporting

ENVIRONMENT VARIABLES TO SET:
- GOOGLE_CLOUD_PROJECT: Your project ID
- FIRESTORE_COLLECTION: "url_mappings"
"""

# DERRICK: Use these instructions to deploy the application
