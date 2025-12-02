#!/usr/bin/env python3
"""
Test Scraper - Test with small dataset (10 anime)
Run this before full scrape to verify scraper logic
"""

import json
from bahamut_scraper import (
    get_anime_list_page,
    parse_anime_links,
    scrape_anime_detail,
    rate_limit
)

# Test configuration
TEST_SIZE = 10  # Number of anime to test
OUTPUT_FILE = '../data/bahamut_test.json'


def validate_anime_data(anime: dict) -> bool:
    """
    Validate that anime data has all required fields

    Args:
        anime: Anime dictionary

    Returns:
        True if valid, False otherwise
    """
    required_fields = ['id', 'title', 'bahamutUrl', 'ratings']
    important_fields = ['titleOriginal', 'thumbnail', 'year', 'genres', 'episodes']

    # Check required fields
    for field in required_fields:
        if field not in anime or not anime[field]:
            print(f"      ⚠️  Missing required field: {field}")
            return False

    # Check important fields (warn but don't fail)
    for field in important_fields:
        if field not in anime or not anime[field]:
            print(f"      ⚠️  Missing important field: {field}")

    # Check rating structure
    if 'bahamut' not in anime['ratings']:
        print(f"      ⚠️  Missing Bahamut rating")
        return False

    if 'score' not in anime['ratings']['bahamut'] or 'votes' not in anime['ratings']['bahamut']:
        print(f"      ⚠️  Incomplete Bahamut rating data")
        return False

    return True


def main():
    """
    Test scraper with small dataset
    """
    print("🧪 Testing Bahamut Scraper with Small Dataset")
    print("=" * 60)

    # Step 1: Get anime URLs
    print("\n📋 Step 1: Fetching test anime URLs...")
    html = get_anime_list_page(1)

    if not html:
        print("❌ Failed to fetch anime list page")
        return

    all_links = parse_anime_links(html)
    test_links = all_links[:TEST_SIZE]

    print(f"   ✓ Found {len(test_links)} anime for testing")

    if not test_links:
        print("❌ No anime URLs found. Please check scraper logic.")
        return

    # Step 2: Scrape test anime
    print(f"\n📺 Step 2: Scraping {len(test_links)} test anime...")
    print()

    scraped_animes = []
    valid_count = 0
    has_japanese_title = 0

    for idx, url in enumerate(test_links, 1):
        print(f"   [{idx}/{len(test_links)}] Testing: {url}")

        anime = scrape_anime_detail(url)

        if anime:
            scraped_animes.append(anime)
            print(f"      ✓ Title: {anime['title']}")
            print(f"      ✓ Japanese: {anime.get('titleOriginal', 'MISSING')}")
            print(f"      ✓ Year: {anime.get('year', 'MISSING')}")
            print(f"      ✓ Genres: {', '.join(anime.get('genres', []))}")
            print(f"      ✓ Episodes: {anime.get('episodes', 'MISSING')}")
            print(f"      ✓ Bahamut Rating: {anime['ratings']['bahamut']['score']}/5 ({anime['ratings']['bahamut']['votes']} votes)")
            print(f"      ✓ Popularity: {anime.get('popularity', 'MISSING')}")

            # Validate data
            if validate_anime_data(anime):
                valid_count += 1
                print(f"      ✅ Validation: PASSED")
            else:
                print(f"      ❌ Validation: FAILED")

            # Check for Japanese title
            if anime.get('titleOriginal'):
                has_japanese_title += 1

        else:
            print(f"      ❌ Failed to scrape")

        print()
        rate_limit()

    # Save test results
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(scraped_animes, f, ensure_ascii=False, indent=2)
        print(f"💾 Test results saved to: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Failed to save test results: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   Total tested: {len(test_links)}")
    print(f"   Successfully scraped: {len(scraped_animes)}")
    print(f"   Validation passed: {valid_count}/{len(scraped_animes)}")
    print(f"   Japanese title coverage: {has_japanese_title}/{len(scraped_animes)} ({has_japanese_title/len(scraped_animes)*100:.1f}%)")
    print()

    # Validation Checklist
    print("✅ Validation Checklist:")
    print(f"   {'✓' if len(scraped_animes) >= TEST_SIZE * 0.8 else '✗'} At least 80% scrape success rate")
    print(f"   {'✓' if valid_count == len(scraped_animes) else '✗'} All scraped anime passed validation")
    print(f"   {'✓' if has_japanese_title >= len(scraped_animes) * 0.9 else '✗'} 90%+ have Japanese title")

    if len(scraped_animes) >= TEST_SIZE * 0.8 and valid_count == len(scraped_animes) and has_japanese_title >= len(scraped_animes) * 0.9:
        print("\n🎉 All checks passed! Ready for full scrape.")
        print("   Run: python bahamut_scraper.py")
    else:
        print("\n⚠️  Some checks failed. Please review scraper logic before full scrape.")

    print("=" * 60)


if __name__ == '__main__':
    main()
