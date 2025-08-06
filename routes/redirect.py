# routes/redirect.py

from flask import Blueprint, redirect, render_template, abort, jsonify
from routes.shorten import get_original_url_for_redirect, increment_click_count_for_redirect
import logging

redirect_bp = Blueprint('redirect', __name__)

@redirect_bp.route('/<string:short_code>', methods=['GET'])
def redirect_url(short_code):
    """Handle redirection from short URL to original URL"""
    try:
        # Validate short code format (basic length check)
        if not short_code or len(short_code) > 20:
            logging.warning(f"Invalid short code format: {short_code}")
            return render_template('404.html'), 404

        # Retrieve URL from database using Luis's function
        result = get_original_url_for_redirect(short_code)

        if result['exists'] and result['original_url']:
            # Increment click count using Luis's function
            increment_click_count_for_redirect(short_code)
            
            logging.info(f"Redirecting {short_code} to {result['original_url']}")
            
            # Redirect to original URL
            return redirect(result['original_url'], code=302)
        else:
            # Log the reason for 404
            error_reason = result.get('error', 'Short code not found')
            logging.info(f"404 for {short_code}: {error_reason}")
            
            # Return 404 page
            return render_template('404.html'), 404
            
    except Exception as e:
        logging.error(f"Error in redirect_url: {e}")
        return render_template('404.html'), 404


# Analytics endpoint (using Luis's function)
@redirect_bp.route('/api/stats/<string:short_code>', methods=['GET'])
def get_url_stats(short_code):
    """Get statistics for a short URL"""
    try:
        from models.url_mapping import URLMapping
        
        stats = URLMapping.get_url_stats(short_code)

        if stats:
            return jsonify({
                'success': True,
                'data': {
                    'original_url': stats['original_url'],
                    'short_code': stats['short_code'],
                    'click_count': stats['click_count'],
                    'created_at': stats['created_at'],
                    'is_active': stats['is_active']
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Short URL not found'
            }), 404
            
    except Exception as e:
        logging.error(f"Error getting URL stats: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


# Custom 404 handler for this blueprint
@redirect_bp.app_errorhandler(404)
def not_found(error):
    """Handle 404 errors for redirect blueprint"""
    return render_template('404.html'), 404
