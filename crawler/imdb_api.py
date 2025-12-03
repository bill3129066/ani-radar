import requests
import logging
import json
import re
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup

import urllib.parse

logger = logging.getLogger(__name__)

def search_imdb(query: str) -> Optional[str]:
    """
    Search IMDb for a title and return the best matching IMDb ID (tt...).
    Uses the undocumented Suggestion API (v2).
    """
    if not query:
        return None
        
    try:
        # API requires the first character for sharding
        # Clean query: remove special chars if needed, but usually urlencode is enough
        safe_query = urllib.parse.quote(query)
        first_char = query[0].lower()
        if not first_char.isalnum(): 
            first_char = 'x' # Fallback
            
        url = f"https://v2.sg.media-imdb.com/suggestion/{first_char}/{safe_query}.json"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        logger.debug(f"Searching IMDb: {url}")
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('d', [])
            
            if results:
                # Prioritize Anime/Animation?
                # The API returns 'qid': 'tvSeries', 'movie', etc.
                # We just take the first result for now as it's usually the best match by popularity
                return results[0]['id']
                
    except Exception as e:
        logger.error(f"Error searching IMDb for '{query}': {e}")
        
    return None

def get_imdb_rating(imdb_id: str) -> Optional[Dict[str, Any]]:
    """
    Scrape IMDb rating from the title page.
    """
    if not imdb_id or not imdb_id.startswith('tt'):
        return None

    url = f"https://www.imdb.com/title/{imdb_id}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        logger.debug(f"Fetching IMDb URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 404:
            logger.warning(f"IMDb ID {imdb_id} not found.")
            return None
            
        if response.status_code != 200:
            logger.warning(f"IMDb request failed for {imdb_id}. Status: {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Method 1: JSON-LD
        # IMDb embeds data in a <script type="application/ld+json"> tag
        script = soup.find('script', type='application/ld+json')
        data = {}
        if script:
            try:
                # Use get_text() as .string can be None if there are internal tags (unlikely for script but safe)
                json_text = script.get_text()
                data = json.loads(json_text)
                
                # Check if it's the main entity or a graph
                candidate = None
                
                if '@graph' in data:
                    # Look for ANY entity with aggregateRating
                    for item in data['@graph']:
                        if 'aggregateRating' in item:
                            candidate = item
                            break
                        # Fallback: Prefer Movie/TVSeries if multiple exist
                        if item.get('@type') in ['Movie', 'TVSeries', 'CreativeWork', 'TVSeason']:
                             if not candidate:
                                 candidate = item
                else:
                    candidate = data

                if candidate:
                    data = candidate
                
                aggregate_rating = data.get('aggregateRating', {})
                
                score = aggregate_rating.get('ratingValue')
                votes = aggregate_rating.get('ratingCount')
                
                if score:
                    return {
                        'imdb_score': float(score),
                        'imdb_votes': int(votes) if votes else 0
                    }
                else:
                    logger.debug(f"IMDb JSON-LD found but no aggregateRating for {imdb_id}")
            except Exception as e:
                logger.debug(f"JSON-LD parse failed for {imdb_id}: {e}")
        else:
            logger.debug(f"IMDb JSON-LD script tag not found for {imdb_id}")
            
        # Method 2: Regex Fallback
        # Look for ratingValue in text patterns
        match = re.search(r'"ratingValue":\s*"?(\d+\.?\d*)"?', response.text)
        if match:
            score = match.group(1)
            # Try to find vote count
            match_votes = re.search(r'"ratingCount":\s*(\d+)', response.text)
            votes = match_votes.group(1) if match_votes else 0
            
            return {
                'imdb_score': float(score),
                'imdb_votes': int(votes)
            }
            
        return None

    except Exception as e:
        logger.error(f"Error fetching IMDb {imdb_id}: {e}")
        return None