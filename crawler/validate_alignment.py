import json
import os
import sys
import logging

# Add path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.aod_service import AnimeOfflineDatabase
from lib.text_cleaner import clean_bahamut_title

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

INPUT_FILE = '../data/bahamut_raw.json'
AOD_FILE = '../data/anime-offline-database.jsonl'

def main():
    if not os.path.exists(INPUT_FILE):
        logger.error(f"Input file not found: {INPUT_FILE}")
        return

    logger.info("Initializing AOD...")
    aod = AnimeOfflineDatabase(AOD_FILE)
    aod.load()
    
    logger.info("Loading Bahamut Data...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        animes = json.load(f)
    
    total = len(animes)
    matches_jp = 0
    matches_en = 0
    failures = 0
    
    # We'll check a sample or all
    # Let's check all but only print failures periodically
    
    logger.info(f"Validating Alignment for {total} items...")
    
    failed_items = []
    
    for anime in animes:
        title_cn = anime.get('title')
        title_jp = anime.get('titleOriginal')
        title_en = anime.get('titleEnglish') # Might be missing if not re-scraped yet
        year = anime.get('year')
        
        clean_jp = clean_bahamut_title(title_jp)
        clean_en = clean_bahamut_title(title_en)
        
        found = False
        
        # JP Lookup
        if clean_jp:
            mal_id = aod.lookup(clean_jp, year)
            if mal_id:
                matches_jp += 1
                found = True
        
        # EN Lookup (Secondary)
        if not found and clean_en:
            mal_id = aod.lookup(clean_en, year)
            if mal_id:
                matches_en += 1
                found = True
                
        if not found:
            failures += 1
            if len(failed_items) < 20: # Keep first 20 failures
                failed_items.append({
                    'cn': title_cn,
                    'jp': title_jp,
                    'clean_jp': clean_jp,
                    'year': year
                })
                
    print("\n" + "="*40)
    print(f"Validation Results")
    print("="*40)
    print(f"Total Animes: {total}")
    print(f"Matches (JP): {matches_jp} ({(matches_jp/total)*100:.2f}%)")
    print(f"Matches (EN): {matches_en} ({(matches_en/total)*100:.2f}%)")
    print(f"Total Matches: {matches_jp + matches_en} ({((matches_jp + matches_en)/total)*100:.2f}%)")
    print(f"Failures:     {failures} ({(failures/total)*100:.2f}%)")
    print("-" * 40)
    
    if failures > 0:
        print("\nSample Failures (First 20):")
        for item in failed_items:
            print(f"- [{item['cn']}] JP:'{item['jp']}' (Clean:'{item['clean_jp']}') Year:{item['year']}")

if __name__ == "__main__":
    main()
