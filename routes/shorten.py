from flask import Blueprint, request, jsonify
from utils.url_encoder import URLEncoder
from models.url_mapping import URLMapping, get_original_url_for_redirect
from datetime import datetime
import logging

# Create blueprint for shortening routes
shorten_bp = Blueprint('shorten', __name__)

@shorten_bp.route('/api/shorten', methods=['POST'])
def shorten_url():
    """
    Create a short URL from a long URL
    Request body: {"url": "https://example.com", "custom_alias": "optional"}
    Returns: JSON response with short URL details or error
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        original_url = data.get('url')
        custom_alias = data.get('custom_alias')
        
        # Validate required fields
        if not original_url:
            return jsonify({
                "success": False,
                "error": "URL is required"
            }), 400
        
        # Validate URL format
        if not URLEncoder.validate_url(original_url):
            return jsonify({
                "success": False,
                "error": "Invalid URL format"
            }), 400
        
        # Handle custom alias
        if custom_alias:
            # Validate custom alias format
            if not URLEncoder.is_valid_custom_alias(custom_alias):
                return jsonify({
                    "success": False,
                    "error": "Invalid custom alias. Must be 3-20 characters, alphanumeric and hyphens only"
                }), 400
            
            # Check if custom alias already exists
            if URLMapping.validate_short_code_exists(custom_alias):
                return jsonify({
                    "success": False,
                    "error": "Custom alias already exists"
                }), 409
            
            short_code = custom_alias
        else:
            # Generate unique short code
            short_code = URLEncoder.generate_unique_code(
                check_existence_func=URLMapping.validate_short_code_exists,
                length=6,
                max_retries=5
            )
            
            if not short_code:
                return jsonify({
                    "success": False,
                    "error": "Unable to generate unique short code. Please try again."
                }), 500
        
        # Get client IP for analytics
        client_ip = request.remote_addr
        
        # Create database entry
        mapping_data = URLMapping.create_mapping(
            original_url=original_url,
            short_code=short_code,
            client_ip=client_ip
        )
        
        if not mapping_data:
            return jsonify({
                "success": False,
                "error": "Failed to create URL mapping"
            }), 500
        
        # Build response
        # Note: In production, use your actual domain
        base_url = request.host_url.rstrip('/')
        short_url = f"{base_url}/{short_code}"
        
        response = {
            "success": True,
            "short_url": short_url,
            "short_code": short_code,
            "original_url": original_url,
            "created_at": mapping_data.get("created_at")
        }
        
        logging.info(f"Created short URL: {short_code} -> {original_url}")
        return jsonify(response), 200
        
    except Exception as e:
        logging.error(f"Error in shorten_url: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@shorten_bp.route('/api/stats/<short_code>', methods=['GET'])
def get_url_statistics(short_code):
    """
    Get statistics for a short URL
    Returns: JSON response with URL statistics
    """
    try:
        # Get URL statistics
        stats = URLMapping.get_url_stats(short_code)
        
        if not stats:
            return jsonify({
                "success": False,
                "error": "Short URL not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": stats
        }), 200
        
    except Exception as e:
        logging.error(f"Error getting URL stats: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@shorten_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring
    Returns: JSON response with service health status
    """
    try:
        from config.database import health_check as db_health
        
        db_status = db_health()
        
        return jsonify({
            "status": "healthy",
            "service": "url-shortener",
            "timestamp": datetime.utcnow().isoformat(),
            "database": db_status
        }), 200
        
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "service": "url-shortener",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }), 500

# Helper functions for Eli to use in redirect.py
def get_original_url_for_redirect(short_code):
    """
    Helper function for Eli's redirect handler
    Args:
        short_code: The short code to look up
    Returns:
        dict: Contains original_url and exists status
    """
    return URLMapping.get_mapping(short_code)

def increment_click_count_for_redirect(short_code):
    """
    Helper function for Eli to increment click counter
    Args:
        short_code: The short code to increment
    Returns:
        boolean: True if successful
    """
    return URLMapping.increment_clicks(short_code)
