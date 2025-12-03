import time
import requests
import logging
from typing import Optional, Dict, Any
from thefuzz import fuzz

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

LAST_REQUEST_TIME = 0
RATE_LIMIT_DELAY = 1.0  # Jikan allows ~3/sec, we play safe with 1/sec

def _rate_limit():
    global LAST_REQUEST_TIME
    current_time = time.time()
    elapsed = current_time - LAST_REQUEST_TIME
    if elapsed < RATE_LIMIT_DELAY:
        time.sleep(RATE_LIMIT_DELAY - elapsed)
    LAST_REQUEST_TIME = time.time()

def search_mal_by_japanese_title(japanese_title: str, year: int = None) -> Optional[Dict[str, Any]]:
    """
    Search MAL using Jikan API.
    
    Args:
        japanese_title: The original Japanese title of the anime.
        year: The release year (optional, used for validation/ranking).
        
    Returns:
        Dict containing MAL ID, score, members, and external links (IMDb ID), or None if not found.
    """
    if not japanese_title:
        return None

    _rate_limit()
    
    url = "https://api.jikan.moe/v4/anime"
    params = {
        "q": japanese_title,
        "limit": 5,  # Fetch top 5 to find best match
        "type": "tv", # Default to TV, but Bahamut has movies too... handle carefully.
                      # Actually Bahamut mixes them. Let's not filter by type initially.
    }
    
    # Bahamut often has "Title [Season]" or "Title (Year)". 
    # The 'japanese_title' from scraper is usually clean, but let's be careful.
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 429:
            logger.warning("MAL API Rate Limit Hit. Sleeping 5s...")
            time.sleep(5)
            return search_mal_by_japanese_title(japanese_title, year)
        
        response.raise_for_status()
        data = response.json()
        
        results = data.get('data', [])
        if not results:
            # Retry with less strict params? Or just return None.
            # Sometimes titles are slightly different. 
            return None
            
        # Find best match
        best_match = None
        best_score = 0
        
        for anime in results:
            # Titles to check: default title, title_english, title_japanese
            titles = [anime.get('title'), anime.get('title_english'), anime.get('title_japanese')]
            titles = [t for t in titles if t] # Filter None
            
            # Fuzzy match score
            current_score = 0
            for t in titles:
                score = fuzz.ratio(japanese_title.lower(), t.lower())
                if score > current_score:
                    current_score = score
            
            # Year penalty: if year is provided and differs significantly
            anime_year = anime.get('year')
            if year and anime_year:
                if abs(anime_year - year) > 1:
                    current_score -= 20 # Penalize wrong year
            
            if current_score > best_score:
                best_score = current_score
                best_match = anime
        
        if best_match and best_score > 60: # Threshold
            return _process_mal_result(best_match)
        
        return None

    except Exception as e:
        logger.error(f"Error searching MAL for '{japanese_title}': {e}")
        return None

def get_mal_details(mal_id: int) -> Optional[Dict[str, Any]]:
    """Fetch full details to get external links (IMDb)"""
    _rate_limit()
    url = f"https://api.jikan.moe/v4/anime/{mal_id}/full"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 429:
            time.sleep(5)
            return get_mal_details(mal_id)
        
        response.raise_for_status()
        data = response.json().get('data', {})
        return _process_mal_result(data)
    except Exception as e:
        logger.error(f"Error fetching MAL details {mal_id}: {e}")
        return None

def _process_mal_result(data: Dict) -> Dict:
    """Extract relevant fields from Jikan response"""
    
    # Extract IMDb ID from external links if available in full response
    imdb_id = None
    for link in data.get('external', []):
        if link.get('name') == 'IMDb':
            # URL format: https://www.imdb.com/title/tt1234567/
            url = link.get('url', '')
            if 'tt' in url:
                parts = url.split('/')
                for p in parts:
                    if p.startswith('tt'):
                        imdb_id = p
                        break
    
    # Jikan v4 'full' endpoint returns 'external' list. 
    # Search endpoint might not return external links.
    # If we need IMDb ID, we might need a second call if search result doesn't have it.
    # Note: Jikan search results typically DON'T have external links.
    # We will need to make a second call for the best match.
    
    return {
        'mal_id': data.get('mal_id'),
        'mal_score': data.get('score'),
        'mal_members': data.get('members'),
        'title': data.get('title'),
        'year': data.get('year'),
        'imdb_id': imdb_id # Might be None from search result
    }
