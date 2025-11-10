"""
Text analysis and topic modeling module.
Uses TF-IDF and keyword extraction to identify important terms.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List, Any
import numpy as np
import re
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

logger = logging.getLogger(__name__)

# Download NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    logger.info("Downloading required NLTK data...")
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)

# Extended stop words list
STOP_WORDS = set(stopwords.words('english')).union({
    'said', 'say', 'says', 'would', 'could', 'also', 'may', 'might',
    'one', 'two', 'three', 'first', 'second', 'new', 'like', 'well',
    'get', 'got', 'make', 'made', 'take', 'taken', 'go', 'going',
    'come', 'coming', 'see', 'seen', 'know', 'known', 'think', 'thought',
    'tell', 'told', 'find', 'found', 'give', 'given', 'use', 'used',
    'want', 'wanted', 'look', 'looked', 'year', 'years', 'time', 'times',
    'people', 'person', 'thing', 'things', 'way', 'ways', 'day', 'days'
})


def analyze_text(text: str, max_words: int = 50) -> Dict[str, Any]:
    """
    Analyze text and extract important keywords using TF-IDF.
    
    Args:
        text: Article text to analyze
        max_words: Maximum number of keywords to return
        
    Returns:
        Dictionary containing word data and metadata
    """
    try:
        logger.info("Starting text analysis...")
        
        # Preprocess text
        cleaned_text = preprocess_text(text)
        
        if not cleaned_text:
            logger.warning("No text to analyze after preprocessing")
            return None
        
        # Tokenize for word count
        words = word_tokenize(cleaned_text.lower())
        word_count = len(words)
        
        # Extract keywords using TF-IDF on sentences
        keywords = extract_keywords_tfidf(cleaned_text, max_words)
        
        if not keywords:
            logger.warning("No keywords extracted")
            return None
        
        logger.info(f"Extracted {len(keywords)} keywords from {word_count} words")
        
        return {
            'words': keywords,
            'word_count': word_count
        }
        
    except Exception as e:
        logger.error(f"Error in text analysis: {str(e)}", exc_info=True)
        return None


def preprocess_text(text: str) -> str:
    """
    Preprocess text for analysis.
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned and preprocessed text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove numbers (but keep words with numbers)
    text = re.sub(r'\b\d+\b', '', text)
    
    # Remove special characters but keep spaces and basic punctuation
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def extract_keywords_tfidf(text: str, max_words: int = 50) -> List[Dict[str, Any]]:
    """
    Extract keywords using TF-IDF vectorization.
    Split text into sentences to give TF-IDF multiple documents to work with.
    
    Args:
        text: Preprocessed text
        max_words: Maximum number of keywords to extract
        
    Returns:
        List of dictionaries with word, weight, and frequency
    """
    try:
        # Split text into sentences to create "documents" for TF-IDF
        sentences = sent_tokenize(text)
        
        # If too few sentences, split by periods as backup
        if len(sentences) < 3:
            sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
        
        # Need at least 2 "documents" for TF-IDF
        if len(sentences) < 2:
            logger.warning("Text too short for TF-IDF, using simple frequency")
            return extract_keywords_frequency(text, max_words)
        
        logger.info(f"Analyzing {len(sentences)} sentences")
        
        # Create TF-IDF vectorizer with adjusted parameters
        vectorizer = TfidfVectorizer(
            max_features=max_words * 3,  # Get more initially for filtering
            stop_words=list(STOP_WORDS),
            ngram_range=(1, 2),  # Include single words and bigrams
            min_df=1,  # Minimum document frequency (must appear in at least 1 doc)
            max_df=0.95,  # Maximum document frequency (ignore if in >95% of docs)
            token_pattern=r'\b[a-zA-Z]{3,}\b'  # Only words with 3+ letters
        )
        
        # Fit and transform on sentences
        tfidf_matrix = vectorizer.fit_transform(sentences)
        
        # Get feature names and average scores across all sentences
        feature_names = vectorizer.get_feature_names_out()
        avg_tfidf_scores = np.asarray(tfidf_matrix.mean(axis=0)).flatten()
        
        # Get word frequencies from original text
        word_freq = get_word_frequencies(text)
        
        # Create word data with scores and frequencies
        word_data = []
        for word, score in zip(feature_names, avg_tfidf_scores):
            if score > 0:
                # Clean word (handle bigrams)
                clean_word = word.replace(' ', '_')
                
                word_data.append({
                    'word': clean_word,
                    'weight': float(score),
                    'frequency': word_freq.get(word, 1)
                })
        
        # Sort by TF-IDF score
        word_data.sort(key=lambda x: x['weight'], reverse=True)
        
        # Normalize weights to 0-1 range
        if word_data:
            max_weight = word_data[0]['weight']
            if max_weight > 0:
                for item in word_data:
                    item['weight'] = round(item['weight'] / max_weight, 3)
        
        # Return top N words
        result = word_data[:max_words]
        logger.info(f"Successfully extracted {len(result)} keywords")
        return result
        
    except Exception as e:
        logger.error(f"Error in TF-IDF extraction: {str(e)}", exc_info=True)
        # Fallback to frequency-based extraction
        return extract_keywords_frequency(text, max_words)


def extract_keywords_frequency(text: str, max_words: int = 50) -> List[Dict[str, Any]]:
    """
    Fallback method: Extract keywords based on frequency alone.
    
    Args:
        text: Preprocessed text
        max_words: Maximum number of keywords to extract
        
    Returns:
        List of dictionaries with word, weight, and frequency
    """
    try:
        logger.info("Using frequency-based keyword extraction")
        
        # Get word frequencies
        word_freq = get_word_frequencies(text)
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Take top N
        top_words = sorted_words[:max_words]
        
        if not top_words:
            return []
        
        # Normalize weights
        max_freq = top_words[0][1]
        
        word_data = []
        for word, freq in top_words:
            word_data.append({
                'word': word,
                'weight': round(freq / max_freq, 3),
                'frequency': freq
            })
        
        logger.info(f"Extracted {len(word_data)} keywords using frequency")
        return word_data
        
    except Exception as e:
        logger.error(f"Error in frequency extraction: {str(e)}")
        return []


def get_word_frequencies(text: str) -> Dict[str, int]:
    """
    Get word frequencies from text.
    
    Args:
        text: Preprocessed text
        
    Returns:
        Dictionary mapping words to frequencies
    """
    try:
        # Tokenize
        words = word_tokenize(text)
        
        # Count frequencies
        freq_dict = {}
        for word in words:
            if len(word) >= 3 and word not in STOP_WORDS:
                freq_dict[word] = freq_dict.get(word, 0) + 1
        
        return freq_dict
        
    except Exception as e:
        logger.error(f"Error calculating frequencies: {str(e)}")
        return {}