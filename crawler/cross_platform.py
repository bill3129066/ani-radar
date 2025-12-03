import json
import logging
import time
import os
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from mal_api import search_mal_by_japanese_title, get_mal_details
from imdb_api import get_imdb_rating, search_imdb
from douban_api import search_douban

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("cross_platform.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

INPUT_FILE = '../data/bahamut_raw.json'
OUTPUT_FILE = '../data/animes_enriched.json'

def load_data(filepath: str) -> List[Dict]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data: List[Dict], filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def enrich_anime(anime: Dict) -> Dict:
    """
    Enrich a single anime record with cross-platform ratings.
    This function modifies the anime dictionary in place but also returns it.
    """
    title_original = anime.get('titleOriginal')
    title_chinese = anime.get('title')
    year = anime.get('year')
    
    # Initialize ratings structure if missing
    if 'ratings' not in anime:
        anime['ratings'] = {}

    # 1. MyAnimeList (MAL)
    mal_data = None
    # Check if we already have valid MAL data to avoid re-fetching
    if 'myanimelist' in anime['ratings'] and anime['ratings']['myanimelist'].get('id'):
         # We assume existing data is good, but we might need it for IMDb linking
         # Reconstruct basic mal_data from existing
         mal_data = {
             'mal_id': anime['ratings']['myanimelist']['id'],
             'title': None # We don't store the MAL title in JSON, so we can't retrieve it easily.
                           # If we need it for IMDb search, we might need to re-fetch or use titleOriginal.
         }
    elif title_original:
        # Search MAL
        logger.info(f"[{title_chinese}] Searching MAL: {title_original}")
        search_result = search_mal_by_japanese_title(title_original, year)
        
        if search_result:
            mal_id = search_result['mal_id']
            mal_data = search_result
            
            # Update Anime Object
            anime['ratings']['myanimelist'] = {
                'score': mal_data.get('mal_score'),
                'members': mal_data.get('mal_members'),
                'id': mal_data.get('mal_id')
            }
    
    # 2. IMDb
    # Use IMDb ID from MAL if available, otherwise Search
    imdb_id = None
    
    # Check if already enriched
    if 'imdb' in anime['ratings'] and anime['ratings']['imdb'].get('id'):
        pass # Already has IMDb
    else:
        # Try to get ID from MAL data
        if mal_data:
            imdb_id = mal_data.get('imdb_id')
            
            # If MAL didn't have ID, try searching IMDb with MAL title or Original Title
            if not imdb_id:
                search_query = mal_data.get('title') or title_original
                if search_query:
                    logger.info(f"[{title_chinese}] Searching IMDb for: {search_query}")
                    imdb_id = search_imdb(search_query)
        
        # If still no ID but we have Japanese title, try that directly
        if not imdb_id and title_original:
             logger.info(f"[{title_chinese}] Searching IMDb fallback: {title_original}")
             imdb_id = search_imdb(title_original)

        if imdb_id:
            logger.info(f"[{title_chinese}] Fetching IMDb Rating: {imdb_id}")
            imdb_data = get_imdb_rating(imdb_id)
            if imdb_data:
                anime['ratings']['imdb'] = {
                    'score': imdb_data.get('imdb_score'),
                    'votes': imdb_data.get('imdb_votes'),
                    'id': imdb_id
                }
    
    # 3. Douban
    if 'douban' not in anime['ratings']:
        logger.info(f"[{title_chinese}] Searching Douban...")
        douban_data = search_douban(title_chinese, year)
        if douban_data:
            anime['ratings']['douban'] = {
                'score': douban_data.get('douban_score'),
                'votes': douban_data.get('douban_votes'),
                'id': douban_data.get('douban_id')
            }
        
    return anime

def main():
    logger.info("Starting Cross-Platform Enrichment...")
    
    if not os.path.exists(INPUT_FILE):
        logger.error(f"Input file not found: {INPUT_FILE}")
        return

    animes = load_data(INPUT_FILE)
    logger.info(f"Loaded {len(animes)} animes.")
    
    # Load existing enriched data if available
    enriched_map = {}
    if os.path.exists(OUTPUT_FILE):
        logger.info("Found existing enriched data. Loading...")
        try:
            existing = load_data(OUTPUT_FILE)
            for item in existing:
                enriched_map[str(item['id'])] = item
        except:
            logger.warning("Could not load existing file, starting fresh.")
    
    count = 0
    # Process ALL animes (updating existing ones if they are missing data is handled in enrich_anime)
    # But to save time, we should only process those missing critical data?
    # No, enrich_anime now checks if fields exist. So we can iterate all safely.
    
    enriched_animes = []
    
    # We want to preserve order of original list? Or existing list?
    # Let's base on original list to ensure we have all.
    
    total = len(animes)
    
    for i, anime in enumerate(animes):
        anime_id = str(anime['id'])
        
        # Use existing record if available as base
        if anime_id in enriched_map:
            current_record = enriched_map[anime_id]
        else:
            current_record = anime.copy()
            
        # Check if we need to enrich (missing MAL or IMDb or Douban)
        # For efficiency, only skip if ALL are present?
        # Or just run logic which has internal checks.
        
        try:
            updated_anime = enrich_anime(current_record)
            enriched_animes.append(updated_anime)
            enriched_map[anime_id] = updated_anime # Update map
            
            count += 1
            if count % 10 == 0:
                logger.info(f"Progress: {i+1}/{total}")
                save_data(list(enriched_map.values()), OUTPUT_FILE)
            
            # Rate limit only if we actually did something?
            # It's hard to know from outside. Just sleep a bit to be safe if we are hitting APIs.
            # If everything is cached/skipped, this slows us down.
            # But safety first.
            # time.sleep(0.1) 
            
        except Exception as e:
            logger.error(f"Error processing {anime_id}: {e}")
            enriched_animes.append(current_record) # Keep old
            
    save_data(enriched_animes, OUTPUT_FILE)
    logger.info("Enrichment Complete!")

if __name__ == "__main__":
    main()
