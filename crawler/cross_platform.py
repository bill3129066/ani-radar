import json
import logging
import time
import os
import sys
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add local directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mal_api import search_mal_by_japanese_title, get_mal_details
from imdb_api import get_imdb_rating, search_imdb
from douban_api import search_douban
from services.aod_service import AnimeOfflineDatabase
from lib.text_cleaner import clean_bahamut_title

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
AOD_FILE = '../data/anime-offline-database.jsonl'
MANUAL_MAPPING_FILE = 'manual_mapping.json'

# Global Services
aod_service = None
manual_mapping = {}

def load_services():
    global aod_service, manual_mapping
    
    # Load Manual Mapping
    if os.path.exists(MANUAL_MAPPING_FILE):
        try:
            with open(MANUAL_MAPPING_FILE, 'r', encoding='utf-8') as f:
                manual_mapping = json.load(f)
            logger.info(f"Loaded {len(manual_mapping)} manual mappings.")
        except Exception as e:
            logger.error(f"Failed to load manual mappings: {e}")
            manual_mapping = {}

    # Initialize AOD
    aod_service = AnimeOfflineDatabase(AOD_FILE)
    # Lazy load will happen on first lookup, or we can force it here
    # aod_service.load() 

def load_data(filepath: str) -> List[Dict]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data: List[Dict], filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def enrich_anime(anime: Dict) -> Dict:
    """
    Enrich a single anime record with cross-platform ratings.
    """
    anime_id = str(anime.get('id'))
    title_chinese = anime.get('title')
    title_original = anime.get('titleOriginal')
    title_english = anime.get('titleEnglish') # New field from scraper
    year = anime.get('year')
    
    # Initialize ratings structure if missing
    if 'ratings' not in anime:
        anime['ratings'] = {}

    # --- 0. Clean Titles ---
    clean_cn = clean_bahamut_title(title_chinese)
    clean_jp = clean_bahamut_title(title_original)
    clean_en = clean_bahamut_title(title_english)

    # --- 1. MyAnimeList (MAL) ---
    mal_id = None
    mal_data = None
    
    # 1.1 Check Manual Mapping
    if anime_id in manual_mapping and 'mal_id' in manual_mapping[anime_id]:
        mal_id = manual_mapping[anime_id]['mal_id']
        logger.info(f"[{clean_cn}] Found in Manual Mapping: MAL ID {mal_id}")
    
    # 1.2 Check Existing Data
    elif 'myanimelist' in anime['ratings'] and anime['ratings']['myanimelist'].get('id'):
        mal_id = anime['ratings']['myanimelist']['id']
    
    # 1.3 AOD Lookup (Local)
    if not mal_id and clean_jp:
        mal_id = aod_service.lookup(clean_jp, year)
        if mal_id:
             logger.info(f"[{clean_cn}] AOD Match (JP): {clean_jp} -> {mal_id}")
    
    if not mal_id and clean_en:
        mal_id = aod_service.lookup(clean_en, year)
        if mal_id:
             logger.info(f"[{clean_cn}] AOD Match (EN): {clean_en} -> {mal_id}")

    # 1.4 Legacy Fallback (API)
    if not mal_id and clean_jp:
        # Only fallback if AOD failed. This is the "5%" case.
        logger.info(f"[{clean_cn}] AOD Failed. Fallback to API Search: {clean_jp}")
        search_result = search_mal_by_japanese_title(clean_jp, year)
        if search_result:
            mal_id = search_result['mal_id']
            mal_data = search_result # Contains score/members
    
    # Fetch MAL Details if we have ID but no Data (or if we need IMDb ID)
    # We always fetch details if we have a fresh MAL ID to get the score and IMDb link
    if mal_id:
        # Check if we already have full data
        current_mal = anime['ratings'].get('myanimelist', {})
        if not current_mal.get('score') or not current_mal.get('id'):
            # Fetch fresh details
            details = get_mal_details(mal_id)
            if details:
                mal_data = details
                anime['ratings']['myanimelist'] = {
                    'score': details.get('mal_score'),
                    'members': details.get('mal_members'),
                    'id': mal_id
                }
            else:
                logger.warning(f"[{clean_cn}] Failed to fetch details for MAL ID {mal_id}")
        else:
             # We have existing data, but we might check if we have the cached 'mal_data' from search
             if not mal_data:
                 # Re-construct mal_data for IMDb step if needed (though we can't get imdb_id from just existing rating dict easily unless stored)
                 # If we are enriching, likely we want to update.
                 # For now, let's assume if we have score, we are good, UNLESS we are missing IMDb.
                 pass

    # --- 2. IMDb ---
    imdb_id = None
    
    # 2.1 Check Manual Mapping
    if anime_id in manual_mapping and 'imdb_id' in manual_mapping[anime_id]:
        imdb_id = manual_mapping[anime_id]['imdb_id']
        
    # 2.2 Check Existing
    elif 'imdb' in anime['ratings'] and anime['ratings']['imdb'].get('id'):
        imdb_id = anime['ratings']['imdb']['id']
        
    # 2.3 Extract from MAL Data
    elif mal_data and mal_data.get('imdb_id'):
        imdb_id = mal_data.get('imdb_id')
        
    # 2.4 Search IMDb (Last Resort)
    if not imdb_id:
        # Try searching with English title first (better for IMDb)
        query = clean_en if clean_en else clean_jp
        # Or even Chinese? IMDb search supports Chinese sometimes but English is safer.
        # Fallback to Jikan search result title if available?
        
        if query:
             logger.info(f"[{clean_cn}] Searching IMDb fallback: {query}")
             imdb_id = search_imdb(query)

    # Fetch IMDb Rating
    if imdb_id:
        # Only fetch if we don't have score or if we just found the ID
        if 'imdb' not in anime['ratings'] or not anime['ratings']['imdb'].get('score'):
            logger.info(f"[{clean_cn}] Fetching IMDb Rating: {imdb_id}")
            imdb_data = get_imdb_rating(imdb_id)
            if imdb_data:
                anime['ratings']['imdb'] = {
                    'score': imdb_data.get('imdb_score'),
                    'votes': imdb_data.get('imdb_votes'),
                    'id': imdb_id
                }
    
    # --- 3. Douban ---
    # Use Cleaned Chinese Title
    if 'douban' not in anime['ratings'] and clean_cn:
        logger.info(f"[{clean_cn}] Searching Douban...")
        douban_data = search_douban(clean_cn, year)
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

    # Initialize Services
    load_services()
    if aod_service:
        aod_service.load()

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
    enriched_animes = []
    total = len(animes)
    
    for i, anime in enumerate(animes):
        anime_id = str(anime['id'])
        
        # Use existing record if available as base, but we might want to Re-Enrich 
        # if the existing record is missing data?
        # For now, adhere to "Update missing".
        
        if anime_id in enriched_map:
            current_record = enriched_map[anime_id]
        else:
            current_record = anime.copy()
            
        # Optimization: Skip if fully enriched? 
        # (Has MAL + IMDb + Douban ratings)
        r = current_record.get('ratings', {})
        has_mal = 'myanimelist' in r
        has_imdb = 'imdb' in r
        has_douban = 'douban' in r
        
        # We process if ANY is missing. 
        # But for testing/updating AOD logic, we might want to force MAL check even if present?
        # Let's stick to standard flow: Enrich if missing.
        
        if not (has_mal and has_imdb and has_douban):
            try:
                updated_anime = enrich_anime(current_record)
                enriched_animes.append(updated_anime)
                enriched_map[anime_id] = updated_anime
                
                count += 1
                if count % 10 == 0:
                    logger.info(f"Progress: {i+1}/{total} (Updated {count})")
                    save_data(list(enriched_map.values()), OUTPUT_FILE)
                
            except Exception as e:
                logger.error(f"Error processing {anime_id}: {e}")
                enriched_animes.append(current_record)
        else:
            enriched_animes.append(current_record)
            
    save_data(enriched_animes, OUTPUT_FILE)
    logger.info("Enrichment Complete!")

if __name__ == "__main__":
    main()
