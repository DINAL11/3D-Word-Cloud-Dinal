"""
Article scraping and content extraction module.
Fetches article content from URLs and extracts meaningful text.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re
import logging

logger = logging.getLogger(__name__)

# Common selectors for article content
ARTICLE_SELECTORS = [
    'article',
    '[role="article"]',
    '.article-body',
    '.article-content',
    '.post-content',
    '.entry-content',
    'main',
    '[itemprop="articleBody"]',
]

# Tags to remove (navigation, ads, etc.)
REMOVE_TAGS = [
    'script', 'style', 'nav', 'header', 'footer', 
    'aside', 'iframe', 'noscript', 'form'
]


def fetch_article(url: str) -> Optional[Dict[str, str]]:
    """
    Fetch and parse article content from a URL.
    
    Args:
        url: The article URL to fetch
        
    Returns:
        Dictionary containing 'title', 'text', and 'url', or None if failed
    """
    try:
        logger.info(f"Fetching article from: {url}")
        
        # Set headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = extract_title(soup)
        
        # Extract main content
        text = extract_content(soup)
        
        if not text or len(text.strip()) < 100:
            logger.warning(f"Insufficient content extracted from {url}")
            return None
        
        logger.info(f"Successfully extracted {len(text)} characters from article")
        
        return {
            'title': title,
            'text': text,
            'url': url
        }
        
    except requests.RequestException as e:
        logger.error(f"Error fetching URL {url}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error processing {url}: {str(e)}")
        return None


def extract_title(soup: BeautifulSoup) -> str:
    """
    Extract article title from HTML.
    
    Args:
        soup: BeautifulSoup object
        
    Returns:
        Article title or default
    """
    # Try different title locations
    title_candidates = [
        soup.find('h1'),
        soup.find('meta', property='og:title'),
        soup.find('meta', attrs={'name': 'title'}),
        soup.find('title'),
    ]
    
    for candidate in title_candidates:
        if candidate:
            if candidate.name == 'meta':
                title = candidate.get('content', '')
            else:
                title = candidate.get_text()
            
            if title:
                return clean_text(title)
    
    return "Untitled Article"


def extract_content(soup: BeautifulSoup) -> str:
    """
    Extract main article content from HTML.
    
    Args:
        soup: BeautifulSoup object
        
    Returns:
        Cleaned article text
    """
    # Remove unwanted tags
    for tag in REMOVE_TAGS:
        for element in soup.find_all(tag):
            element.decompose()
    
    # Try to find article content using common selectors
    content = None
    for selector in ARTICLE_SELECTORS:
        try:
            if selector.startswith('['):
                # Handle attribute selectors
                content = soup.select_one(selector)
            else:
                content = soup.find(selector)
            
            if content:
                break
        except:
            continue
    
    # If no article content found, use body as fallback
    if not content:
        content = soup.find('body')
    
    if not content:
        return ""
    
    # Extract text from paragraphs
    paragraphs = content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    if paragraphs:
        text = ' '.join([p.get_text() for p in paragraphs])
    else:
        # Fallback to all text
        text = content.get_text()
    
    # Clean the text
    text = clean_text(text)
    
    return text


def clean_text(text: str) -> str:
    """
    Clean extracted text.
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:\-\'\"()]', ' ', text)
    
    # Remove multiple spaces
    text = re.sub(r' +', ' ', text)
    
    return text.strip()


def is_boilerplate(text: str) -> bool:
    """
    Check if text is likely boilerplate/navigation content.
    
    Args:
        text: Text to check
        
    Returns:
        True if likely boilerplate
    """
    text_lower = text.lower()
    boilerplate_indicators = [
        'cookie', 'subscribe', 'newsletter', 'sign up',
        'terms of service', 'privacy policy', 'copyright',
        'all rights reserved', 'click here', 'read more'
    ]
    
    return any(indicator in text_lower for indicator in boilerplate_indicators)