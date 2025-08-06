import random
import string
import re
import requests
from urllib.parse import urlparse

class URLEncoder:
    BASE62_CHARS = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    
    @staticmethod
    def generate_short_code(length=6):
        """Generate random short code using Base62 encoding"""
        return ''.join(random.choices(URLEncoder.BASE62_CHARS, k=length))
    
    @staticmethod
    def validate_url(url):
        """
        Validate URL format and basic accessibility
        Returns: boolean
        """
        try:
            # Parse the URL
            parsed = urlparse(url)
            
            # Check if scheme is http or https
            if parsed.scheme not in ['http', 'https']:
                return False
            
            # Check if netloc (domain) exists
            if not parsed.netloc:
                return False
            
            # Basic domain format validation
            domain_pattern = re.compile(
                r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
            )
            
            if not domain_pattern.match(parsed.netloc):
                return False
            
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def is_valid_custom_alias(alias):
        """
        Validate custom alias format
        Rules: 3-20 characters, alphanumeric and hyphens only, no consecutive hyphens
        """
        if not alias or len(alias) < 3 or len(alias) > 20:
            return False
        
        # Pattern: alphanumeric and hyphens, no consecutive hyphens, no start/end with hyphen
        pattern = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?$')
        
        if not pattern.match(alias):
            return False
        
        # Check for consecutive hyphens
        if '--' in alias:
            return False
        
        return True
    
    @staticmethod
    def generate_unique_code(check_existence_func, length=6, max_retries=5):
        """
        Generate unique code with collision detection
        Args:
            check_existence_func: Function that returns True if code exists
            length: Length of the code to generate
            max_retries: Maximum number of attempts
        Returns:
            Unique short code or None if max retries exceeded
        """
        for attempt in range(max_retries):
            code = URLEncoder.generate_short_code(length)
            
            # Check if code already exists
            if not check_existence_func(code):
                return code
        
        # If we get here, we couldn't generate a unique code
        return None
    
    @staticmethod
    def encode_base62(number):
        """
        Encode a number to Base62 string
        Useful for sequential ID encoding
        """
        if number == 0:
            return URLEncoder.BASE62_CHARS[0]
        
        result = ""
        base = len(URLEncoder.BASE62_CHARS)
        
        while number > 0:
            result = URLEncoder.BASE62_CHARS[number % base] + result
            number //= base
        
        return result
    
    @staticmethod
    def decode_base62(encoded_string):
        """
        Decode a Base62 string to number
        Useful for sequential ID decoding
        """
        base = len(URLEncoder.BASE62_CHARS)
        result = 0
        
        for char in encoded_string:
            result = result * base + URLEncoder.BASE62_CHARS.index(char)
        
        return result
