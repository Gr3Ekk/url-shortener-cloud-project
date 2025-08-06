# Cloud URL Shortener Project

## Team Responsibilities

### Luis - API Development & Database Integration
- **Short URL Generator API** (`routes/shorten.py`)
- **Database Setup & Integration** (`config/database.py`, `models/url_mapping.py`)
- **URL Encoding Logic** (`utils/url_encoder.py`)

### Eli - Redirect Handler API
- **Redirect Endpoint** (`routes/redirect.py`)
- **URL Retrieval Logic** (uses Luis's database functions)
- **404 Error Handling**

### Derrick - Deployment & Testing
- **App Engine Configuration** (`app.yaml`)
- **Deployment Scripts** 
- **API Testing & Documentation**

## Project Structure
```
CloudFinalProject/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── app.yaml                 # Google App Engine configuration
├── models/
│   └── url_mapping.py       # Database model (Luis)
├── utils/
│   └── url_encoder.py       # Short code generation (Luis)
├── routes/
│   ├── shorten.py          # URL shortening endpoint (Luis)
│   └── redirect.py         # Redirect endpoint (Eli)
├── config/
│   └── database.py         # Database configuration (Luis)
├── templates/
│   ├── index.html          # Simple frontend
│   └── 404.html           # Error page (Eli)
└── tests/
    ├── test_shorten.py     # Test shortening API
    └── test_redirect.py    # Test redirect API
```

## API Endpoints
- `POST /api/shorten` - Create short URL (Luis)
- `GET /{short_code}` - Redirect to original URL (Eli)
- `GET /api/stats/{short_code}` - Get URL statistics (Optional)

## Google Cloud Setup Required
1. Create Google Cloud Project
2. Enable Firestore API
3. Enable App Engine API
4. Set up service account credentials

## Getting Started
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Google Cloud credentials
4. Run locally: `python app.py`
5. Deploy: `gcloud app deploy`

## Testing
Use Postman or curl to test the APIs:
```bash
# Test shortening
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://example.com"}' http://localhost:8080/api/shorten

# Test redirect
curl -L http://localhost:8080/{short_code}
```
