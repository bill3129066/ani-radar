import json
import os
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

INPUT_FILE = '../data/animes_enriched.json'
OUTPUT_FILE = '../data/animes.json'
MANUAL_MAPPING_FILE = 'manual_mapping.json'

def load_json(filepath: str) -> List[Dict]:
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: List[Dict], filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def apply_manual_mappings(animes: List[Dict], mappings: Dict) -> List[Dict]:
    """
    Override/Inject ratings based on manual mapping file.
    Mapping format:
    {
        "bahamut_id": {
            "imdb_id": "tt...",
            "mal_id": 123,
            "imdb_score": 8.5,
            ...
        }
    }
    """
    count = 0
    for anime in animes:
        anime_id = str(anime['id'])
        if anime_id in mappings:
            mapping = mappings[anime_id]
            logger.info(f"Applying manual mapping for {anime['title']} ({anime_id})")
            
            # Update ratings
            if 'ratings' not in anime:
                anime['ratings'] = {}
                
            # IMDb Override
            if 'imdb_id' in mapping:
                anime['ratings']['imdb'] = {
                    'id': mapping['imdb_id'],
                    'score': mapping.get('imdb_score', 0),
                    'votes': mapping.get('imdb_votes', 0)
                }
            
            # MAL Override
            if 'mal_id' in mapping:
                anime['ratings']['myanimelist'] = {
                    'id': mapping['mal_id'],
                    'score': mapping.get('mal_score', 0),
                    'members': mapping.get('mal_members', 0)
                }

            # Douban Override
            if 'douban_id' in mapping:
                anime['ratings']['douban'] = {
                    'id': mapping['douban_id'],
                    'score': mapping.get('douban_score', 0),
                    'votes': mapping.get('douban_votes', 0)
                }
                
            count += 1
            
    logger.info(f"Applied manual mappings to {count} animes.")
    return animes

def validate_and_clean(animes: List[Dict]) -> List[Dict]:
    """
    Final validation and cleaning before frontend usage.
    """
    cleaned = []
    for anime in animes:
        # Ensure required fields
        if not anime.get('title'):
            continue
            
        # Normalize ratings (Frontend expects 0-10 for others, Bahamut is 1-5 but we keep it 1-5 here)
        # The frontend utils.ts handles normalization.
        # We just ensure structure exists.
        
        # Ensure year is int
        try:
            anime['year'] = int(anime['year'])
        except:
            anime['year'] = 0
            
        cleaned.append(anime)
        
    return cleaned

def main():
    logger.info("Generating final dataset...")
    
    animes = load_json(INPUT_FILE)
    if not animes:
        return
        
    # Load manual mappings
    mappings = {}
    if os.path.exists(MANUAL_MAPPING_FILE):
        try:
            with open(MANUAL_MAPPING_FILE, 'r', encoding='utf-8') as f:
                mappings = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load manual mappings: {e}")
            
    # Apply mappings
    if mappings:
        animes = apply_manual_mappings(animes, mappings)
        
    # Validate
    final_data = validate_and_clean(animes)
    
    # Save
    save_json(final_data, OUTPUT_FILE)
    logger.info(f"Successfully generated {OUTPUT_FILE} with {len(final_data)} items.")

if __name__ == "__main__":
    main()
