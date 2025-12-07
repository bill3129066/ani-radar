import sys
import os
import logging
import json

# Add local directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# logging.getLogger("douban_api").setLevel(logging.DEBUG)

# Mock or Import
try:
    from douban_api import search_douban
except ImportError:
    logger.error("Could not import douban_api. Make sure you run this from the project root or crawler directory.")
    sys.exit(1)

def run_tests():
    test_cases = [
        {
            "name": "Frieren",
            "titles": {"cn": "葬送的芙莉蓮", "jp": "葬送のフリーレン", "en": "Frieren: Beyond Journey's End"},
            "year": 2023
        },
        {
            "name": "Fullmetal Alchemist: Brotherhood",
            "titles": {"cn": "鋼之鍊金術師 BROTHERHOOD", "jp": "鋼の錬金術師 FULLMETAL ALCHEMIST", "en": "Fullmetal Alchemist: Brotherhood"},
            "year": 2009
        },
        {
            "name": "Spy x Family",
            "titles": {"cn": "SPY×FAMILY 間諜家家酒", "jp": "SPY×FAMILY", "en": "Spy x Family"},
            "year": 2022
        },
        {
            "name": "Attack on Titan",
            "titles": {"cn": "進擊的巨人", "jp": "進撃の巨人", "en": "Attack on Titan"},
            "year": 2013
        },
        {
            "name": "Mushoku Tensei",
            "titles": {"cn": "無職轉生～到了異世界就拿出真本事～", "jp": "無職転生", "en": "Mushoku Tensei: Jobless Reincarnation"},
            "year": 2021
        }
    ]

    logger.info("Starting Douban 'Hard Cases' Validation...")
    success_count = 0

    for case in test_cases:
        logger.info(f"Testing: {case['name']} (Year: {case['year']})")
        logger.info(f"Titles: {case['titles']}")
        
        try:
            # Note: This expects the NEW signature of search_douban(titles, year)
            # If the API hasn't been updated yet, this might fail or need adjustment.
            result = search_douban(case['titles'], case['year'])
            
            if result:
                logger.info(f"✅ SUCCESS: Found {result['douban_id']} | Score: {result.get('douban_score')} | Votes: {result.get('douban_votes')}")
                success_count += 1
            else:
                logger.error(f"❌ FAILED: No result found for {case['name']}")
                
        except TypeError:
             # Fallback for old signature if refactor isn't done yet, just to show it fails
            logger.warning("⚠️  API signature mismatch. Attempting old signature...")
            try:
                result = search_douban(case['titles']['cn'], case['year'])
                if result:
                     logger.info(f"✅ SUCCESS (Old API): Found {result['douban_id']}")
                     success_count += 1
                else:
                     logger.error(f"❌ FAILED (Old API): No result found for {case['name']}")
            except Exception as e:
                logger.error(f"❌ ERROR: {e}")
        except Exception as e:
            logger.error(f"❌ ERROR: {e}")
            
        print("-" * 50)

    logger.info(f"Result: {success_count}/{len(test_cases)} Passed")

if __name__ == "__main__":
    run_tests()
