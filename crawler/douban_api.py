import requests
import logging
import time
import re
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import unquote

logger = logging.getLogger(__name__)

LAST_REQUEST_TIME = 0
RATE_LIMIT_DELAY = 5.0 # Douban is strict, 5s delay

def _rate_limit():
    global LAST_REQUEST_TIME
    current_time = time.time()
    elapsed = current_time - LAST_REQUEST_TIME
    if elapsed < RATE_LIMIT_DELAY:
        time.sleep(RATE_LIMIT_DELAY - elapsed)
    LAST_REQUEST_TIME = time.time()

def search_douban(titles: Dict[str, str], year: int = None) -> Optional[Dict[str, Any]]:
    """
    Search Douban using a multi-stage fallback strategy:
    1. Suggestion API (Chinese Title)
    2. HTML Search (Japanese Title)
    3. HTML Search (English Title)
    """
    # 1. Stage 1: Suggestion API with Chinese Title
    if titles.get('cn'):
        logger.info(f"Douban Stage 1 (Suggest CN): {titles['cn']}")
        result = _search_suggest_api(titles['cn'], year)
        if result:
            return result
    
    # 2. Stage 2: HTML Search with Japanese Title
    if titles.get('jp'):
        logger.info(f"Douban Stage 2 (HTML JP): {titles['jp']}")
        result = search_douban_html(titles['jp'], year)
        if result:
            return result

    # 3. Stage 3: HTML Search with English Title
    if titles.get('en'):
        logger.info(f"Douban Stage 3 (HTML EN): {titles['en']}")
        result = search_douban_html(titles['en'], year)
        if result:
            return result
            
    return None

def _search_suggest_api(title: str, year: int = None) -> Optional[Dict[str, Any]]:
    """
    Original search using internal suggestion API.
    """
    if not title:
        return None
        
    _rate_limit()
    
    # Clean title
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
            
        best_match = None
        for item in results:
            item_year = item.get('year')
            if year and item_year:
                try:
                    if abs(int(item_year) - year) <= 1:
                        best_match = item
                        break
                except:
                    pass
            else:
                best_match = item
                break
                
        if not best_match and results:
            best_match = results[0]
            
        if best_match:
            return _get_douban_details(best_match['id'])
            
        return None

    except Exception as e:
        logger.error(f"Error searching Douban API for '{title}': {e}")
        return None

def search_douban_html(query: str, year: int = None) -> Optional[Dict[str, Any]]:
    """
    Scrape Douban search results page.
    URL: https://www.douban.com/search?cat=1002&q={query}
    """
    if not query:
        return None
        
    _rate_limit()
    
    url = "https://www.douban.com/search"
    params = {"cat": "1002", "q": query} # cat 1002 = Movie/TV
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 429:
            logger.warning("Douban 429 Rate Limit Hit! Backing off...")
            time.sleep(60) # Backoff
            return None
            
        if response.status_code != 200:
            logger.debug(f"Douban Search failed: {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.select('div.result')
        
        # Inspect top 3 results
        for item in results[:3]:
            # Extract basic info
            try:
                title_tag = item.select_one('div.content > div.title > h3 > a')
                if not title_tag:
                    continue
                
                href = title_tag['href']
                # Decode the URL to handle redirect links
                decoded_href = unquote(href)
                
                douban_id = None
                match = re.search(r'subject/(\d+)', decoded_href)
                if match:
                    douban_id = match.group(1)

                logger.debug(f"Item: {item.get_text()[:30]}... | HREF: {href[:30]}... | Decoded: {decoded_href[:50]}... | ID: {douban_id}")

                if not douban_id:
                    continue

                # Year check
                full_text = item.get_text() # Restore this!
                found_year = False
                if year:
                    # Check if year is in text
                    # Regex for 4 digits (non-capturing group for prefix)
                    years_in_text = re.findall(r'\b(?:19|20)\d{2}\b', full_text)
                    logger.debug(f"Target Year: {year} | Found Years: {years_in_text}")
                    for y_str in years_in_text:
                        y = int(y_str)
                        if abs(y - year) <= 1:
                            found_year = True
                            break
                    
                    if not found_year:
                        logger.debug("Year mismatch, skipping.")
                        continue # Skip this result if year doesn't match
                
                # If we are here, we have ID and Year matches (or year not required)
                # We can now fetch details or extract rating from search page
                
                # Search page has rating: <span class="rating_nums">9.4</span>
                rating_tag = item.select_one('span.rating_nums')
                votes_tag = item.select_one('span.pl') # (1234人评价)
                
                score = 0.0
                votes = 0
                
                if rating_tag and rating_tag.text.strip():
                    try:
                        score = float(rating_tag.text.strip())
                    except:
                        pass
                
                if votes_tag and votes_tag.text.strip():
                    # Parse "(105807人评价)"
                    v_text = votes_tag.text.strip()
                    v_match = re.search(r'(\d+)', v_text)
                    if v_match:
                        votes = int(v_match.group(1))
                        
                if score > 0:
                     return {
                        'douban_id': douban_id,
                        'douban_score': score,
                        'douban_votes': votes
                    }
                else:
                     return {
                        'douban_id': douban_id,
                        'douban_score': 0.0,
                        'douban_votes': 0
                    }

            except Exception as e:
                logger.warning(f"Error parsing search result item: {e}")
                continue
                
        return None

    except Exception as e:
        logger.error(f"Error searching Douban HTML for '{query}': {e}")
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
        
        if response.status_code == 429:
             logger.warning("Douban 429 Rate Limit Hit (Details)! Backing off...")
             time.sleep(60)
             return None

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
