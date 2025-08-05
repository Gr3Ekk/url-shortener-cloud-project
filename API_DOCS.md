# TODO: API Documentation and Testing Guide
"""
API DOCUMENTATION FOR TEAM TESTING

BASE URL: 
- Local: http://localhost:8080
- Production: https://YOUR_PROJECT_ID.appspot.com

ENDPOINTS:

1. CREATE SHORT URL
   POST /api/shorten
   
   Request Headers:
   Content-Type: application/json
   
   Request Body:
   {
     "url": "https://example.com/very/long/url",
     "custom_alias": "my-custom-alias"  // optional
   }
   
   Success Response (200):
   {
     "success": true,
     "short_url": "https://yourapp.appspot.com/abc123",
     "short_code": "abc123", 
     "original_url": "https://example.com/very/long/url",
     "created_at": "2025-08-04T10:30:00Z"
   }
   
   Error Responses:
   400 - Invalid URL format
   409 - Custom alias already exists
   500 - Server error

2. REDIRECT TO ORIGINAL URL
   GET /{short_code}
   
   Success Response:
   302 Redirect to original URL
   
   Error Response:
   404 - Short code not found (returns 404.html page)

3. URL STATISTICS (Optional)
   GET /api/stats/{short_code}
   
   Success Response (200):
   {
     "short_code": "abc123",
     "original_url": "https://example.com/very/long/url",
     "click_count": 42,
     "created_at": "2025-08-04T10:30:00Z"
   }

TESTING WITH CURL:

# Create short URL
curl -X POST -H "Content-Type: application/json" \
  -d '{"url":"https://google.com"}' \
  http://localhost:8080/api/shorten

# Create with custom alias
curl -X POST -H "Content-Type: application/json" \
  -d '{"url":"https://github.com","custom_alias":"github"}' \
  http://localhost:8080/api/shorten

# Test redirect (follow redirects)
curl -L http://localhost:8080/abc123

# Get statistics
curl http://localhost:8080/api/stats/abc123

TESTING WITH POSTMAN:
1. Import these curl commands as requests
2. Create collection with all endpoints
3. Set environment variables for base URL
4. Add tests for response validation

ERROR TESTING:
# Invalid URL
curl -X POST -H "Content-Type: application/json" \
  -d '{"url":"not-a-valid-url"}' \
  http://localhost:8080/api/shorten

# Non-existent short code
curl -L http://localhost:8080/nonexistent

PERFORMANCE TESTING:
- Test with 100+ concurrent requests
- Measure response times
- Test database connection limits
- Monitor memory usage during load
"""

# DERRICK: Use this for API testing and documentation
