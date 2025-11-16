"""
Base scraper module for judicial data collection
Provides common utilities and base classes for web scraping
"""

import time
import logging
from typing import Optional, Dict, List
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class BaseJudicialScraper:
    """Base class for judicial court scrapers"""
    
    def __init__(self, tribunal_name: str, base_url: str, timeout: int = 30):
        """
        Initialize the scraper
        
        Args:
            tribunal_name: Name of the tribunal (e.g., 'TJSP')
            base_url: Base URL of the court system
            timeout: Request timeout in seconds
        """
        self.tribunal_name = tribunal_name
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def make_request(self, url: str, method: str = 'GET', 
                     params: Optional[Dict] = None, 
                     data: Optional[Dict] = None,
                     retries: int = 3) -> Optional[requests.Response]:
        """
        Make HTTP request with retry logic
        
        Args:
            url: Target URL
            method: HTTP method (GET or POST)
            params: Query parameters
            data: POST data
            retries: Number of retry attempts
            
        Returns:
            Response object or None if failed
        """
        for attempt in range(retries):
            try:
                if method.upper() == 'GET':
                    response = self.session.get(
                        url, params=params, timeout=self.timeout
                    )
                else:
                    response = self.session.post(
                        url, data=data, timeout=self.timeout
                    )
                
                response.raise_for_status()
                return response
                
            except requests.RequestException as e:
                logger.warning(
                    f"Request failed (attempt {attempt + 1}/{retries}): {e}"
                )
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All retries failed for {url}")
                    return None
    
    def parse_html(self, html_content: str) -> Optional[BeautifulSoup]:
        """
        Parse HTML content
        
        Args:
            html_content: HTML string
            
        Returns:
            BeautifulSoup object or None if parsing failed
        """
        try:
            return BeautifulSoup(html_content, 'lxml')
        except Exception as e:
            logger.error(f"Failed to parse HTML: {e}")
            return None
    
    def extract_process_info(self, soup: BeautifulSoup) -> Dict:
        """
        Extract process information from parsed HTML
        To be implemented by subclasses
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Dictionary with extracted data
        """
        raise NotImplementedError("Subclasses must implement extract_process_info")
    
    def search_processes(self, keywords: List[str], 
                        date_start: str, 
                        date_end: str) -> List[Dict]:
        """
        Search for processes matching keywords
        To be implemented by subclasses
        
        Args:
            keywords: List of search terms
            date_start: Start date (format: DD/MM/YYYY)
            date_end: End date (format: DD/MM/YYYY)
            
        Returns:
            List of process dictionaries
        """
        raise NotImplementedError("Subclasses must implement search_processes")
    
    def close(self):
        """Close the session"""
        self.session.close()
        logger.info(f"Session closed for {self.tribunal_name}")
