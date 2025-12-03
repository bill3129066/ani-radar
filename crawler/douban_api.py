import requests
import logging
import time
import json
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

LAST_REQUEST_TIME = 0
RATE_LIMIT_DELAY = 2.0 # Douban is strict

def _rate_limit():
    global LAST_REQUEST_TIME
    current_time = time.time()
    elapsed = current_time - LAST_REQUEST_TIME
    if elapsed < RATE_LIMIT_DELAY:
        time.sleep(RATE_LIMIT_DELAY - elapsed)
    LAST_REQUEST_TIME = time.time()

def search_douban(title: str, year: int = None) -> Optional[Dict[str, Any]]:
    """
    Search Douban using the internal suggestion API which is lighter and less likely to block 
    than scraping the search result HTML.
    
    API: https://movie.douban.com/j/subject_suggest?q={query}
    """
    if not title:
        return None
        
    _rate_limit()
    
    # We clean the title a bit (remove season numbers if possible, or just try as is)
    # Bahamut title: "鬼滅之刃 柱訓練篇 [1]" -> "鬼滅之刃 柱訓練篇"
    clean_title = title.split('[')[0].strip()
    
    url = "https://movie.douban.com/j/subject_suggest"
    params = {"q": clean_title}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://movie.douban.com/"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            logger.debug(f"Douban API failed: {response.status_code}")
            return None
            
        results = response.json()
        
        if not results:
            return None
            
        # Results are a list of dicts: {'id': '...', 'title': '...', 'sub_title': '...', 'year': '...', 'img': '...'}
        # Find best match
        best_match = None
        
        for item in results:
            # Check year if available
            item_year = item.get('year')
            if year and item_year:
                # Douban year might be string "2024"
                try:
                    if abs(int(item_year) - year) <= 1:
                        best_match = item
                        break
                except:
                    pass
            else:
                # If no year check, take the first one that looks like an exact match or just the first one
                best_match = item
                break
                
        if not best_match and results:
            best_match = results[0] # Fallback to first result
            
        if best_match:
            return _get_douban_details(best_match['id'])
            
        return None

    except Exception as e:
        logger.error(f"Error searching Douban for '{title}': {e}")
        return None

def _get_douban_details(douban_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch details for a specific Douban ID to get the rating.
    """
    _rate_limit()
    url = f"https://movie.douban.com/subject/{douban_id}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 404:
            return None
            
        # Parse HTML for rating
        # <strong class="ll rating_num" property="v:average">9.1</strong>
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rating_tag = soup.find('strong', property="v:average")
        votes_tag = soup.find('span', property="v:votes")
        
        if rating_tag and rating_tag.text.strip():
            score = float(rating_tag.text.strip())
            votes = int(votes_tag.text.strip()) if votes_tag else 0
            
            return {
                'douban_id': douban_id,
                'douban_score': score,
                'douban_votes': votes
            }
            
        return None
        
    except Exception as e:
        logger.error(f"Error details Douban {douban_id}: {e}")
        return None
