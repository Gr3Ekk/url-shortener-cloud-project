import os
from google.cloud import firestore
from google.cloud.exceptions import GoogleCloudError
import logging

class DatabaseConfig:
    def __init__(self):
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        self.collection_name = os.getenv('FIRESTORE_COLLECTION', 'url_mappings')
        self.client = None
        self.is_initialized = False
        self.use_mock = os.getenv('USE_MOCK_DATABASE', 'false').lower() == 'true'
    
    def init_db(self):
        """
        Initialize Firestore client
        Returns: boolean indicating success
        """
        # Check if we should use mock database
        if self.use_mock:
            print("🔧 Using mock database for development")
            self.is_initialized = True
            return True
            
        try:
            # Initialize Firestore client
            if self.project_id:
                self.client = firestore.Client(project=self.project_id)
            else:
                # Use application default credentials
                self.client = firestore.Client()
            
            # Test connection
            if self.test_connection():
                self.is_initialized = True
                logging.info("Database connection initialized successfully")
                return True
            else:
                logging.error("Database connection test failed")
                return False
                
        except GoogleCloudError as e:
            logging.error(f"Failed to initialize Firestore client: {e}")
            print("💡 Tip: Run 'python setup_dev.py' to set up mock development mode")
            return False
        except Exception as e:
            logging.error(f"Unexpected error initializing database: {e}")
            print("💡 Tip: Run 'python setup_dev.py' to set up mock development mode")
            return False
    
    def get_client(self):
        """
        Return initialized Firestore client
        Returns: Firestore client or None
        """
        if self.use_mock:
            return None  # Mock mode doesn't use Firestore client
            
        if not self.is_initialized:
            if not self.init_db():
                return None
        return self.client
    
    def test_connection(self):
        """
        Test database connectivity
        Returns: boolean success status
        """
        if self.use_mock:
            return True  # Mock mode always "connects"
            
        try:
            if not self.client:
                return False
            
            # Try to access the collection (this will create it if it doesn't exist)
            collection_ref = self.client.collection(self.collection_name)
            
            # Try a simple query to test connectivity
            docs = collection_ref.limit(1).get()
            
            return True
        except Exception as e:
            logging.error(f"Database connection test failed: {e}")
            return False
    
    def get_collection(self):
        """
        Get the URL mappings collection reference
        Returns: Collection reference or None
        """
        if self.use_mock:
            return None  # Mock mode doesn't use collections
            
        client = self.get_client()
        if client:
            return client.collection(self.collection_name)
        return None

# Global database instance
db_config = DatabaseConfig()

def init_db():
    """
    Function to call from app.py to initialize database
    Returns: boolean indicating success
    """
    return db_config.init_db()

def get_db():
    """
    Function to get database client
    Returns: Firestore client or None
    """
    return db_config.get_client()

def get_collection():
    """
    Function to get the URL mappings collection
    Returns: Collection reference or None
    """
    return db_config.get_collection()

def health_check():
    """
    Check database health for monitoring
    Returns: dict with status and details
    """
    try:
        if db_config.test_connection():
            return {
                "status": "healthy",
                "database": "connected",
                "collection": db_config.collection_name
            }
        else:
            return {
                "status": "unhealthy",
                "database": "connection_failed",
                "collection": db_config.collection_name
            }
    except Exception as e:
        return {
            "status": "error",
            "database": "error",
            "error": str(e)
        }
