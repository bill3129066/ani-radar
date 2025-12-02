#!/usr/bin/env python3
"""
Data Validation Script
Validates scraped Bahamut data quality
"""

import json
import sys
from pathlib import Path
from typing import List, Dict


def load_json(file_path: str) -> List[Dict]:
    """
    Load JSON file

    Args:
        file_path: Path to JSON file

    Returns:
        List of anime dictionaries
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)


def validate_bahamut_data(animes: List[Dict]):
    """
    Comprehensive validation of Bahamut data

    Args:
        animes: List of anime dictionaries
    """
    print("🔍 Validating Bahamut Data Quality")
    print("=" * 60)

    total = len(animes)
    print(f"\n📊 Total anime: {total}")

    if total == 0:
        print("❌ No anime data found!")
        sys.exit(1)

    # Check required fields
    print("\n🔎 Checking Required Fields...")
    missing_id = [a for a in animes if not a.get('id')]
    missing_title = [a for a in animes if not a.get('title')]
    missing_url = [a for a in animes if not a.get('bahamutUrl')]
    missing_ratings = [a for a in animes if not a.get('ratings') or not a['ratings'].get('bahamut')]

    print(f"   Missing ID: {len(missing_id)} ({len(missing_id)/total*100:.1f}%)")
    print(f"   Missing Chinese title: {len(missing_title)} ({len(missing_title)/total*100:.1f}%)")
    print(f"   Missing Bahamut URL: {len(missing_url)} ({len(missing_url)/total*100:.1f}%)")
    print(f"   Missing Bahamut rating: {len(missing_ratings)} ({len(missing_ratings)/total*100:.1f}%)")

    # Check important fields
    print("\n🔎 Checking Important Fields...")
    missing_japanese = [a for a in animes if not a.get('titleOriginal')]
    missing_thumbnail = [a for a in animes if not a.get('thumbnail')]
    missing_year = [a for a in animes if not a.get('year') or a['year'] == 0]
    missing_genres = [a for a in animes if not a.get('genres') or len(a['genres']) == 0]
    missing_episodes = [a for a in animes if not a.get('episodes') or a['episodes'] == 0]

    print(f"   Missing Japanese title: {len(missing_japanese)} ({len(missing_japanese)/total*100:.1f}%)")
    print(f"   Missing thumbnail: {len(missing_thumbnail)} ({len(missing_thumbnail)/total*100:.1f}%)")
    print(f"   Missing year: {len(missing_year)} ({len(missing_year)/total*100:.1f}%)")
    print(f"   Missing genres: {len(missing_genres)} ({len(missing_genres)/total*100:.1f}%)")
    print(f"   Missing episodes: {len(missing_episodes)} ({len(missing_episodes)/total*100:.1f}%)")

    # Check rating data quality
    print("\n🔎 Checking Rating Data Quality...")
    invalid_bahamut_score = []
    invalid_bahamut_votes = []

    for anime in animes:
        if anime.get('ratings') and anime['ratings'].get('bahamut'):
            bahamut = anime['ratings']['bahamut']
            score = bahamut.get('score', 0)
            votes = bahamut.get('votes', 0)

            # Bahamut uses 1-5 scale
            if score < 0 or score > 5:
                invalid_bahamut_score.append(anime)

            if votes < 0:
                invalid_bahamut_votes.append(anime)

    print(f"   Invalid Bahamut score (not 0-5): {len(invalid_bahamut_score)}")
    print(f"   Invalid Bahamut votes (negative): {len(invalid_bahamut_votes)}")

    # Check popularity
    print("\n🔎 Checking Popularity Data...")
    has_popularity = [a for a in animes if a.get('popularity', 0) > 0]
    print(f"   Has popularity data: {len(has_popularity)} ({len(has_popularity)/total*100:.1f}%)")

    # URL validation
    print("\n🔎 Checking URL Validity...")
    invalid_urls = [a for a in animes if a.get('bahamutUrl') and not a['bahamutUrl'].startswith('http')]
    duplicate_ids = []
    seen_ids = set()

    for anime in animes:
        anime_id = anime.get('id')
        if anime_id in seen_ids:
            duplicate_ids.append(anime_id)
        seen_ids.add(anime_id)

    print(f"   Invalid URLs (not starting with http): {len(invalid_urls)}")
    print(f"   Duplicate IDs: {len(duplicate_ids)}")

    if duplicate_ids:
        print(f"      Duplicates: {', '.join(map(str, duplicate_ids[:10]))}")

    # Sample data inspection
    print("\n📋 Sample Data (First 3 Anime):")
    for i, anime in enumerate(animes[:3], 1):
        print(f"\n   Anime {i}:")
        print(f"      ID: {anime.get('id', 'N/A')}")
        print(f"      Chinese: {anime.get('title', 'N/A')}")
        print(f"      Japanese: {anime.get('titleOriginal', 'N/A')}")
        print(f"      Year: {anime.get('year', 'N/A')}")
        print(f"      Genres: {', '.join(anime.get('genres', []))[:50]}")
        print(f"      Episodes: {anime.get('episodes', 'N/A')}")
        print(f"      Rating: {anime['ratings']['bahamut']['score']}/5 ({anime['ratings']['bahamut']['votes']} votes)")
        print(f"      Popularity: {anime.get('popularity', 'N/A')}")

    # Success criteria
    print("\n" + "=" * 60)
    print("✅ Validation Results:")
    print()

    checks = []

    # Critical checks (must pass)
    checks.append(("Total anime >= 1500", total >= 1500))
    checks.append(("No missing titles", len(missing_title) == 0))
    checks.append(("No missing ratings", len(missing_ratings) == 0))
    checks.append(("No duplicate IDs", len(duplicate_ids) == 0))
    checks.append(("All ratings valid (0-5 scale)", len(invalid_bahamut_score) == 0))

    # Important checks (should pass)
    checks.append(("Japanese title coverage >= 90%", len(missing_japanese) / total <= 0.1))
    checks.append(("Year data >= 95%", len(missing_year) / total <= 0.05))
    checks.append(("Genre data >= 90%", len(missing_genres) / total <= 0.1))

    critical_passed = 0
    important_passed = 0

    for i, (check_name, passed) in enumerate(checks, 1):
        status = "✓" if passed else "✗"
        print(f"   {status} {check_name}")

        if i <= 5:  # First 5 are critical
            if passed:
                critical_passed += 1
        else:  # Rest are important
            if passed:
                important_passed += 1

    print()
    print(f"   Critical checks: {critical_passed}/5 passed")
    print(f"   Important checks: {important_passed}/{len(checks)-5} passed")

    # Final verdict
    print("\n" + "=" * 60)
    if critical_passed == 5 and important_passed >= 2:
        print("🎉 ✅ All validation checks passed!")
        print("   Data quality is excellent. Ready for Phase 2.")
        sys.exit(0)
    elif critical_passed == 5:
        print("⚠️  Critical checks passed, but some important checks failed.")
        print("   Data quality is acceptable, but could be improved.")
        sys.exit(0)
    else:
        print("❌ Validation failed! Please fix critical issues before proceeding.")
        sys.exit(1)


def main():
    """
    Main validation function
    """
    file_path = '../data/bahamut_raw.json'

    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        print("   Please run bahamut_scraper.py first to generate data.")
        sys.exit(1)

    animes = load_json(file_path)
    validate_bahamut_data(animes)


if __name__ == '__main__':
    main()
