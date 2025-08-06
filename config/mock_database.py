# Mock Database for Development
# This allows teammates to work without Google Cloud setup

class MockURLMapping:
    # In-memory storage for development
    _storage = {}
    _click_counts = {}
    
    @staticmethod
    def create_mapping(original_url, short_code, client_ip=None):
        """Mock create mapping - stores in memory"""
        MockURLMapping._storage[short_code] = {
            "short_code": short_code,
            "original_url": original_url,
            "created_at": "2025-08-06T10:30:00Z",
            "click_count": 0,
            "is_active": True,
            "created_by_ip": client_ip
        }
        return MockURLMapping._storage[short_code]
    
    @staticmethod
    def get_mapping(short_code):
        """Mock get mapping"""
        if short_code in MockURLMapping._storage:
            data = MockURLMapping._storage[short_code]
            return {
                "original_url": data["original_url"],
                "exists": True,
                "click_count": data["click_count"],
                "created_at": data["created_at"]
            }
        return {"original_url": None, "exists": False, "error": "Short code not found"}
    
    @staticmethod
    def increment_clicks(short_code):
        """Mock increment clicks"""
        if short_code in MockURLMapping._storage:
            MockURLMapping._storage[short_code]["click_count"] += 1
            return True
        return False
    
    @staticmethod
    def validate_short_code_exists(short_code):
        """Mock validation"""
        return short_code in MockURLMapping._storage
    
    @staticmethod
    def get_url_stats(short_code):
        """Mock get stats"""
        if short_code in MockURLMapping._storage:
            return MockURLMapping._storage[short_code]
        return None

def mock_init_db():
    """Mock database initialization"""
    print("🔧 Using MOCK database for development")
    return True

def mock_get_collection():
    """Mock collection"""
    return "mock_collection"
