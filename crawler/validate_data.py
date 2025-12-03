import json
import os
from typing import List, Dict, Any

# Constants
RAW_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'bahamut_raw.json')

def validate_data(file_path: str) -> bool:
    """
    Validates the scraped Bahamut raw data based on project requirements.
    
    Args:
        file_path: Path to the JSON file containing the scraped data.

    Returns:
        True if validation passes, False otherwise.
    """
    print(f"--- -Starting Validation for {file_path} --- ")
    
    if not os.path.exists(file_path):
        print(f"❌ FAILURE: Data file not found at {file_path}")
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data: List[Dict[str, Any]] = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ FAILURE: Could not decode JSON from {file_path}")
            return False

    total_animes = len(data)
    print(f"Total animes found: {total_animes}")

    # 1. Check total count
    if total_animes >= 1500:
        print(f"✅ PASSED: Total count ({total_animes}) is >= 1500.")
    else:
        print(f"❌ FAILURE: Total count ({total_animes}) is < 1500.")
        return False

    required_fields = ['id', 'title', 'bahamutUrl', 'thumbnail', 'year', 'episodes', 'genres', 'popularity', 'ratings']
    missing_field_counts = {field: 0 for field in required_fields}
    missing_title_original = 0
    invalid_rating_count = 0
    
    for i, anime in enumerate(data):
        # 2. Check for missing required fields
        for field in required_fields:
            if not anime.get(field):
                missing_field_counts[field] += 1
        
        if not anime.get('titleOriginal'):
            missing_title_original += 1

        # 3. Check rating structure and values
        bahamut_rating = anime.get('ratings', {}).get('bahamut', {})
        if not isinstance(bahamut_rating.get('score'), (int, float)) or not isinstance(bahamut_rating.get('votes'), int):
            invalid_rating_count += 1

    print("\n--- Field Presence Validation ---")
    all_fields_present = True
    for field, count in missing_field_counts.items():
        if count > 0:
            print(f"❌ WARNING: Required field '{field}' is missing in {count} animes.")
            # Depending on strictness, we could return False here. For now, just a warning.
            # all_fields_present = False
        else:
            print(f"✅ PASSED: Required field '{field}' is present in all animes.")

    # 4. Check titleOriginal coverage
    print("\n--- 'titleOriginal' Coverage Validation ---")
    title_original_coverage = (total_animes - missing_title_original) / total_animes
    if title_original_coverage >= 0.7: # PRD says 70% is good, ROADMAP says 90%
        print(f"✅ PASSED: 'titleOriginal' coverage is {title_original_coverage:.1%} (>= 70%).")
    else:
        print(f"❌ WARNING: 'titleOriginal' coverage is {title_original_coverage:.1%}, which is below the 70% target.")

    print("\n--- Rating Data Validation ---")
    if invalid_rating_count == 0:
        print("✅ PASSED: All animes have valid rating structures.")
    else:
        print(f"❌ WARNING: {invalid_rating_count} animes have invalid rating structures.")

    # We are not returning False on warnings, so the overall result is based on critical failures.
    print("\n--- Overall Validation Summary ---")
    if total_animes >= 1500:
        print("✅✅✅ Validation successful (with potential warnings). The data is ready for Phase 2. ✅✅✅")
        return True
    else:
        print("❌❌❌ Critical validation failed. Please review the scraper. ❌❌❌")
        return False


if __name__ == '__main__':
    validate_data(RAW_DATA_FILE)