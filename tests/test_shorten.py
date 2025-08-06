import unittest
import json
import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

class TestShortenAPI(unittest.TestCase):
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
    
    def test_shorten_url_success(self):
        """Test successful URL shortening"""
        response = self.client.post('/api/shorten',
                                  data=json.dumps({'url': 'https://google.com'}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check required fields in response
        self.assertIn('short_url', data)
        self.assertIn('short_code', data)
        self.assertIn('original_url', data)
        self.assertEqual(data['original_url'], 'https://google.com')
        
        # Verify short_code is the right length (6 characters)
        self.assertEqual(len(data['short_code']), 6)
    
    def test_shorten_url_invalid_url(self):
        """Test invalid URL rejection"""
        response = self.client.post('/api/shorten',
                                  data=json.dumps({'url': 'not-a-url'}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_shorten_url_missing_url(self):
        """Test missing URL parameter"""
        response = self.client.post('/api/shorten',
                                  data=json.dumps({}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_shorten_url_malformed_json(self):
        """Test malformed JSON request"""
        response = self.client.post('/api/shorten',
                                  data='{"url":"https://example.com"}/',  # Broken JSON with trailing slash
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_shorten_url_statistics(self):
        """Test URL statistics endpoint"""
        # First create a URL
        response = self.client.post('/api/shorten',
                                  data=json.dumps({'url': 'https://example.com'}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        short_code = data['short_code']
        
        # Then get statistics
        response = self.client.get(f'/api/stats/{short_code}')
        self.assertEqual(response.status_code, 200)
        
        stats_data = json.loads(response.data)
        self.assertIn('click_count', stats_data)
        self.assertIn('created_at', stats_data)

if __name__ == '__main__':
    unittest.main()
