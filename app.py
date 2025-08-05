# TODO: LUIS - Main Flask Application Setup
"""
Main Flask application file for URL shortener service.

TASKS FOR LUIS:
1. Import Flask and necessary modules
2. Import route blueprints from routes/shorten.py and routes/redirect.py
3. Import database configuration from config/database.py
4. Set up Flask app with proper configuration
5. Register route blueprints
6. Add error handlers for 404, 500 errors
7. Initialize database connection
8. Add CORS support if needed for frontend
9. Set up logging configuration
10. Add health check endpoint (/health)

INTEGRATION POINTS:
- Register Eli's redirect blueprint: app.register_blueprint(redirect_bp)
- Register your shorten blueprint: app.register_blueprint(shorten_bp)
- Initialize database before first request

EXAMPLE STRUCTURE:
from flask import Flask, jsonify
from routes.shorten import shorten_bp  # Luis's work
from routes.redirect import redirect_bp  # Eli's work
from config.database import init_db     # Luis's work

app = Flask(__name__)
# Add your configuration here

if __name__ == '__main__':
    # Development server configuration
    app.run(debug=True, host='0.0.0.0', port=8080)
"""

# LUIS: Replace this comment block with actual Flask application code
