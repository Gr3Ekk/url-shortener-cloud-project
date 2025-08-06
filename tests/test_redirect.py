import unittest
import json
import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

class TestRedirectAPI(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        # Force mock database for testing
        os.environ['USE_MOCK_DATABASE'] = 'true'
        
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()
    
    def test_redirect_existing_short_code(self):
        """Test successful redirect to original URL"""
        # First create a short URL
        response = self.client.post('/api/shorten',
                                  data=json.dumps({'url': 'https://google.com'}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        short_code = data['short_code']
        
        # Then test the redirect
        response = self.client.get(f'/{short_code}', follow_redirects=False)
        self.assertEqual(response.status_code, 302)  # Redirect status
        self.assertEqual(response.location, 'https://google.com')
    
    def test_redirect_nonexistent_short_code(self):
        """Test 404 for non-existent short codes"""
        response = self.client.get('/nonexistent', follow_redirects=False)
        self.assertEqual(response.status_code, 404)
    
    def test_redirect_malformed_short_code(self):
        """Test handling of malformed short codes"""
        # Test with special characters
        response = self.client.get('/abc!@#', follow_redirects=False)
        self.assertEqual(response.status_code, 404)
        
        # Test with too long code
        response = self.client.get('/verylongcode123456789', follow_redirects=False)
        self.assertEqual(response.status_code, 404)
    
    def test_click_counter_increment(self):
        """Test that click counter increments on redirect"""
        # Create a short URL
        response = self.client.post('/api/shorten',
                                  data=json.dumps({'url': 'https://example.com'}),
                                  content_type='application/json')
        
        data = json.loads(response.data)
        short_code = data['short_code']
        
        # Get initial stats
        response = self.client.get(f'/api/stats/{short_code}')
        initial_stats = json.loads(response.data)
        initial_clicks = initial_stats.get('click_count', 0)
        
        # Access the short URL (trigger redirect)
        self.client.get(f'/{short_code}', follow_redirects=False)
        
        # Check that click count increased
        response = self.client.get(f'/api/stats/{short_code}')
        new_stats = json.loads(response.data)
        new_clicks = new_stats.get('click_count', 0)
        
        self.assertEqual(new_clicks, initial_clicks + 1)
    
    def test_redirect_stats_endpoint(self):
        """Test the URL statistics endpoint"""
        # Create a short URL
        response = self.client.post('/api/shorten',
                                  data=json.dumps({'url': 'https://example.com'}),
                                  content_type='application/json')
        
        data = json.loads(response.data)
        short_code = data['short_code']
        
        # Test stats endpoint
        response = self.client.get(f'/api/stats/{short_code}')
        self.assertEqual(response.status_code, 200)
        
        stats_data = json.loads(response.data)
        self.assertIn('click_count', stats_data)
        self.assertIn('original_url', stats_data)
        self.assertEqual(stats_data['original_url'], 'https://example.com')
    
    def test_stats_nonexistent_code(self):
        """Test stats endpoint for non-existent codes"""
        response = self.client.get('/api/stats/nonexistent')
        self.assertEqual(response.status_code, 404)
    
    def test_end_to_end_functionality(self):
        """Test complete end-to-end functionality"""
        original_url = 'https://github.com/python/cpython'
        
        # 1. Create short URL
        response = self.client.post('/api/shorten',
                                  data=json.dumps({'url': original_url}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        short_code = data['short_code']
        
        # 2. Test redirect works
        response = self.client.get(f'/{short_code}', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, original_url)
        
        # 3. Test stats tracking
        response = self.client.get(f'/api/stats/{short_code}')
        self.assertEqual(response.status_code, 200)
        
        stats_data = json.loads(response.data)
        self.assertEqual(stats_data['click_count'], 1)
        self.assertEqual(stats_data['original_url'], original_url)

if __name__ == '__main__':
    unittest.main()
