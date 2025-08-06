from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import route blueprints
from routes.shorten import shorten_bp
from routes.redirect import redirect_bp

# Import database configuration
from config.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Enable CORS for API endpoints
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize database
    with app.app_context():
        init_db()
    
    # Register blueprints
    app.register_blueprint(shorten_bp)  # Luis's shortening endpoints
    app.register_blueprint(redirect_bp)  # Eli's redirect endpoints
    
    # Main route for simple frontend
    @app.route('/')
    def index():
        """Serve the main page"""
        try:
            return render_template('index.html')
        except Exception as e:
            logging.error(f"Error serving index page: {e}")
            return jsonify({"error": "Failed to load page"}), 500
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        if request.path.startswith('/api/'):
            return jsonify({"error": "API endpoint not found"}), 404
        try:
            return render_template('404.html'), 404
        except:
            return jsonify({"error": "Page not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logging.error(f"Internal server error: {error}")
        return jsonify({"error": "Internal server error"}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors"""
        return jsonify({"error": "Bad request"}), 400
    
    return app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Development server configuration
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logging.info(f"Starting URL Shortener service on port {port}")
    logging.info(f"Debug mode: {debug}")
    
    app.run(
        debug=debug,
        host='0.0.0.0',
        port=port
    )
