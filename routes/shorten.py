# TODO: LUIS - URL Shortening API Endpoint
"""
TASKS FOR LUIS:
1. Create Flask blueprint for shortening endpoints
2. Implement POST /api/shorten endpoint
3. Add request validation and error handling
4. Integrate with URL encoder and database model
5. Return proper JSON responses
6. Add rate limiting if needed

ENDPOINT SPECIFICATION:
POST /api/shorten
Content-Type: application/json

REQUEST BODY:
{
    "url": "https://example.com/very/long/url",
    "custom_alias": "optional-custom-name"  # optional
}

SUCCESS RESPONSE (200):
{
    "success": true,
    "short_url": "https://yourapp.appspot.com/abc123",
    "short_code": "abc123",
    "original_url": "https://example.com/very/long/url",
    "created_at": "2025-08-04T10:30:00Z"
}

ERROR RESPONSES:
400 - Invalid URL format
409 - Custom alias already exists
429 - Rate limit exceeded
500 - Server error

INTEGRATION POINTS:
- Use utils.url_encoder for code generation and validation
- Use models.url_mapping for database operations
- Provide functions that Eli can use for redirect logic

EXAMPLE STRUCTURE:
from flask import Blueprint, request, jsonify
from utils.url_encoder import URLEncoder
from models.url_mapping import URLMapping

shorten_bp = Blueprint('shorten', __name__)

@shorten_bp.route('/api/shorten', methods=['POST'])
def shorten_url():
    # Get JSON data from request
    # Validate input
    # Generate or validate custom alias
    # Create database entry
    # Return response
    pass

# Helper functions for Eli to use:
def get_original_url_for_redirect(short_code):
    # Function that Eli will import and use
    # Returns dict with original_url and exists status
    pass
"""

# LUIS: Replace this comment block with actual shortening endpoint code
