import os
import json
import pytest
from bahamut_scraper import main as run_scraper, OUTPUT_FILE

@pytest.fixture(scope="module")
def scraper_run():
    """Fixture to run the scraper for a small test set and clean up after."""
    output_dir = os.path.dirname(OUTPUT_FILE)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        
    print("\n--- Running HTML Scraper Test (limit=10) ---")
    run_scraper(limit=10)
    print("--- HTML Scraper Test Run Finished ---")

    yield

    print("\n--- Cleaning up test files ---")
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f"Removed: {OUTPUT_FILE}")

def test_html_scraper_output_file_created(scraper_run):
    """Tests if the HTML scraper creates the output JSON file."""
    print("--- Test: HTML Scraper output file creation ---")
    assert os.path.exists(OUTPUT_FILE), "Output file was not created by HTML scraper."
    print("✅ Passed: Output file exists.")

def test_html_scraper_output_file_content(scraper_run):
    """Tests the content and structure of the output JSON file from the HTML scraper."""
    print("--- Test: HTML Scraper output file content and structure ---")
    assert os.path.exists(OUTPUT_FILE), "Cannot test content, output file not found."
    
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) > 0, "HTML scraper did not save any anime data."
    assert len(data) <= 10
    print(f"✅ Passed: Found {len(data)} animes (which is > 0 and <= 10).")

    anime = data[0]
    print(f"\n--- Validating structure of first anime: {anime.get('title')} ---")
    
    required_fields = [
        'id', 'title', 'bahamutUrl', 'ratings',
        'year', 'episodes', 'genres', 'popularity', 'thumbnail'
    ]
    
    missing_fields = [field for field in required_fields if field not in anime or not anime[field]]
    assert not missing_fields, f"Anime object is missing required fields: {missing_fields}"

    if 'titleOriginal' not in anime or not anime['titleOriginal']:
        print("⚠️ Warning: 'titleOriginal' is missing. This might affect Phase 2.")
    
    print("✅ Passed: All required fields are present.")
    assert 'bahamut' in anime['ratings']
    assert 'score' in anime['ratings']['bahamut']
    assert 'votes' in anime['ratings']['bahamut']
    print("✅ Passed: Ratings structure is correct.")

    assert isinstance(anime['year'], int)
    assert isinstance(anime['ratings']['bahamut']['score'], float)
    print("✅ Passed: Key data types are correct.")

    print("\n--- Sample Data (HTML Scraper) ---")
    print(json.dumps(anime, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    pytest.main(['-s', __file__])
