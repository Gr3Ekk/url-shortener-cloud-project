import os
from google.cloud import firestore
from datetime import datetime
import logging
from config.database import get_collection
from config.mock_database import MockURLMapping

class URLMapping:
    def __init__(self):
        """Initialize URL mapping model"""
        # Check if we should use mock database
        self.use_mock = os.getenv('USE_MOCK_DATABASE', 'false').lower() == 'true'
        if self.use_mock:
            self.mock_db = MockURLMapping()
    
    @staticmethod
    def create_mapping(original_url, short_code, client_ip=None):
        """
        Create new URL mapping in Firestore
        Args:
            original_url: The original long URL
            short_code: The generated short code
            client_ip: Optional client IP for analytics
        Returns:
            dict: Created mapping data or None if failed
        """
        # Check if using mock database
        use_mock = os.getenv('USE_MOCK_DATABASE', 'false').lower() == 'true'
        if use_mock:
            mock_db = MockURLMapping()
            return mock_db.create_mapping(original_url, short_code, client_ip)
            
        try:
            collection = get_collection()
            if not collection:
                logging.error("Database collection not available")
                return None
            
            # Create mapping document
            mapping_data = {
                "short_code": short_code,
                "original_url": original_url,
                "created_at": datetime.utcnow().isoformat(),
                "click_count": 0,
                "is_active": True,
                "created_by_ip": client_ip,
                "expires_at": None  # Can be set for expiring URLs
            }
            
            # Use short_code as document ID for fast lookups
            doc_ref = collection.document(short_code)
            doc_ref.set(mapping_data)
            
            logging.info(f"Created URL mapping: {short_code} -> {original_url}")
            return mapping_data
            
        except Exception as e:
            logging.error(f"Failed to create URL mapping: {e}")
            return None
    
    @staticmethod
    def get_mapping(short_code):
        """
        Retrieve URL mapping by short code
        Args:
            short_code: The short code to look up
        Returns:
            dict: Mapping data with original_url and exists status
        """
        # Check if using mock database
        use_mock = os.getenv('USE_MOCK_DATABASE', 'false').lower() == 'true'
        if use_mock:
            mock_db = MockURLMapping()
            return mock_db.get_mapping(short_code)
            
        try:
            collection = get_collection()
            if not collection:
                return {"original_url": None, "exists": False, "error": "Database unavailable"}
            
            # Get document by short_code
            doc_ref = collection.document(short_code)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                # Check if URL is active
                if data.get("is_active", True):
                    return {
                        "original_url": data.get("original_url"),
                        "exists": True,
                        "click_count": data.get("click_count", 0),
                        "created_at": data.get("created_at")
                    }
                else:
                    return {"original_url": None, "exists": False, "error": "URL deactivated"}
            else:
                return {"original_url": None, "exists": False, "error": "Short code not found"}
                
        except Exception as e:
            logging.error(f"Failed to get URL mapping: {e}")
            return {"original_url": None, "exists": False, "error": str(e)}
    
    @staticmethod
    def increment_clicks(short_code):
        """
        Increment click counter for analytics
        Args:
            short_code: The short code to increment
        Returns:
            boolean: True if successful, False otherwise
        """
        # Check if using mock database
        use_mock = os.getenv('USE_MOCK_DATABASE', 'false').lower() == 'true'
        if use_mock:
            mock_db = MockURLMapping()
            return mock_db.increment_clicks(short_code)
            
        try:
            collection = get_collection()
            if not collection:
                return False
            
            doc_ref = collection.document(short_code)
            
            # Use Firestore transaction to safely increment
            @firestore.transactional
            def update_clicks(transaction):
                doc = doc_ref.get(transaction=transaction)
                if doc.exists:
                    current_count = doc.to_dict().get("click_count", 0)
                    transaction.update(doc_ref, {"click_count": current_count + 1})
                    return True
                return False
            
            # Execute transaction
            from config.database import get_db
            db = get_db()
            if db:
                transaction = db.transaction()
                result = update_clicks(transaction)
                if result:
                    logging.info(f"Incremented click count for: {short_code}")
                return result
            
            return False
            
        except Exception as e:
            logging.error(f"Failed to increment click count: {e}")
            return False
    
    @staticmethod
    def validate_short_code_exists(short_code):
        """
        Check if short code exists in database
        Args:
            short_code: The short code to check
        Returns:
            boolean: True if exists, False otherwise
        """
        try:
            collection = get_collection()
            if not collection:
                return False
            
            doc_ref = collection.document(short_code)
            doc = doc_ref.get()
            
            return doc.exists
            
        except Exception as e:
            logging.error(f"Failed to validate short code: {e}")
            return False
    
    @staticmethod
    def get_url_stats(short_code):
        """
        Get URL statistics
        Args:
            short_code: The short code to get stats for
        Returns:
            dict: Statistics data or None if not found
        """
        try:
            collection = get_collection()
            if not collection:
                return None
            
            doc_ref = collection.document(short_code)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                return {
                    "short_code": short_code,
                    "original_url": data.get("original_url"),
                    "click_count": data.get("click_count", 0),
                    "created_at": data.get("created_at"),
                    "is_active": data.get("is_active", True),
                    "created_by_ip": data.get("created_by_ip")
                }
            else:
                return None
                
        except Exception as e:
            logging.error(f"Failed to get URL stats: {e}")
            return None
    
    @staticmethod
    def deactivate_mapping(short_code):
        """
        Deactivate a URL mapping (soft delete)
        Args:
            short_code: The short code to deactivate
        Returns:
            boolean: True if successful, False otherwise
        """
        try:
            collection = get_collection()
            if not collection:
                return False
            
            doc_ref = collection.document(short_code)
            doc_ref.update({"is_active": False})
            
            logging.info(f"Deactivated URL mapping: {short_code}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to deactivate URL mapping: {e}")
            return False

# Helper functions for teammates to use
def get_original_url_for_redirect(short_code):
    """
    Helper function for Eli's redirect handler
    Args:
        short_code: The short code to look up
    Returns:
        dict: Contains original_url and exists status
    """
    return URLMapping.get_mapping(short_code)

def increment_click_count(short_code):
    """
    Helper function for Eli to increment click counter
    Args:
        short_code: The short code to increment
    Returns:
        boolean: True if successful
    """
    return URLMapping.increment_clicks(short_code)
