import json
import logging
import os
import sys
import random

# Add local directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cross_platform import enrich_anime, load_services

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

INPUT_FILE = '../data/bahamut_raw.json'

def main():
    if not os.path.exists(INPUT_FILE):
        logger.error(f"Input file not found: {INPUT_FILE}")
        return

    # Load Services (Manual Mapping, AOD, etc.)
    load_services()

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        animes = json.load(f)

    # Filter for items with Japanese titles (our target for improvement)
    candidates = [a for a in animes if a.get('titleOriginal')]
    
    if not candidates:
        logger.error("No candidates with titleOriginal found.")
        return

    # Pick 20 random items
    sample = random.sample(candidates, 20)
    
    logger.info(f"Testing enrichment on {len(sample)} random anime...")
    
    enriched_count = 0
    douban_found = 0
    
    for i, anime in enumerate(sample):
        # Clear existing douban rating to force search
        if 'ratings' in anime and 'douban' in anime['ratings']:
            del anime['ratings']['douban']
            
        logger.info(f"[{i+1}/{len(sample)}] Enriching: {anime['title']} ({anime.get('titleOriginal')})")
        
        try:
            enriched = enrich_anime(anime)
            if 'ratings' in enriched and 'douban' in enriched['ratings']:
                douban_found += 1
                d = enriched['ratings']['douban']
                logger.info(f"  -> Found Douban: ID {d['id']}, Score {d['score']}")
            else:
                logger.warning("  -> Douban NOT found.")
        except Exception as e:
            logger.error(f"  -> Error: {e}")

    logger.info("-" * 30)
    logger.info(f"Douban Coverage: {douban_found}/{len(sample)} ({douban_found/len(sample)*100:.1f}%)")

if __name__ == "__main__":
    main()
