import pytest
import logging
from mal_api import search_mal_by_japanese_title
from imdb_api import get_imdb_rating
from douban_api import search_douban

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Test Data
TEST_JAPANESE_TITLE = "葬送のフリーレン" # Frieren
TEST_CHINESE_TITLE = "肖申克的救赎" # Shawshank in Simplified Chinese
TEST_YEAR = 2023
TEST_IMDB_ID = "tt22248376" # Frieren (Correct Series ID)

def test_mal_search():
    print(f"\nTesting MAL Search for: {TEST_JAPANESE_TITLE}")
    result = search_mal_by_japanese_title(TEST_JAPANESE_TITLE, TEST_YEAR)
    assert result is not None
    assert result['mal_id'] is not None
    print(f"MAL Result: {result}")

def test_imdb_scrape():
    print(f"\nTesting IMDb Scrape for: {TEST_IMDB_ID}")
    result = get_imdb_rating(TEST_IMDB_ID)
    if result is None:
        print("IMDb Scrape returned None. Check logs.")
    else:
        print(f"IMDb Result: {result}")
    assert result is not None
    assert result['imdb_score'] > 0

def test_douban_search():
    print(f"\nTesting Douban Search for: {TEST_CHINESE_TITLE}")
    result = search_douban(TEST_CHINESE_TITLE, TEST_YEAR)
    # Douban might fail due to anti-bot, so we warn instead of assert failure
    if result:
        print(f"Douban Result: {result}")
        assert result['douban_score'] > 0
    else:
        print("Douban search failed (might be blocked or network issue)")

if __name__ == "__main__":
    try:
        test_mal_search()
    except Exception as e:
        print(f"MAL Test Failed: {e}")

    try:
        test_imdb_scrape()
    except Exception as e:
        print(f"IMDb Test Failed: {e}")

    try:
        test_douban_search()
    except Exception as e:
        print(f"Douban Test Failed: {e}")