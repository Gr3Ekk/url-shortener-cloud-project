# routes/redirect.py

from flask import Blueprint, redirect, render_template, abort, jsonify
from models.url_mapping import URLMapping
from config.database import db

redirect_bp = Blueprint('redirect', __name__)

@redirect_bp.route('/<string:short_code>', methods=['GET'])
def redirect_url(short_code):
    # Validate short code format (basic length check)
    if not short_code or len(short_code) > 10:
        return render_template('404.html'), 404

    # Retrieve URL from database
    url_mapping = URLMapping.query.filter_by(short_code=short_code).first()

    if url_mapping:
        # Increment click count
        url_mapping.clicks += 1
        db.session.commit()

        # Redirect to original URL
        return redirect(url_mapping.original_url, code=302)
    else:
        # Return 404 page
        return render_template('404.html'), 404


# Optional: analytics endpoint
@redirect_bp.route('/api/stats/<string:short_code>', methods=['GET'])
def get_url_stats(short_code):
    url_mapping = URLMapping.query.filter_by(short_code=short_code).first()

    if url_mapping:
        return jsonify({
            'original_url': url_mapping.original_url,
            'short_code': url_mapping.short_code,
            'clicks': url_mapping.clicks
        }), 200
    else:
        return jsonify({'error': 'Short URL not found'}), 404


# Optional: custom 404 handler if needed for the whole blueprint
@redirect_bp.app_errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
