# Tasks: Boost Douban Coverage

- [x] 1. **Prepare Test Data**: Create a script `crawler/test_douban_cases.py` with the following 5 "Hard" cases (known failures with CN title):
    - **Frieren** (`titleOriginal`: "葬送のフリーレン") - Fails due to "的" vs "の" or simplified.
    - **Fullmetal Alchemist: Brotherhood** (`titleOriginal`: "鋼の錬金術師 FULLMETAL ALCHEMIST") - Differentiates by year/title.
    - **Spy x Family** (`titleOriginal`: "SPY×FAMILY") - Special characters.
    - **Attack on Titan** (`titleOriginal`: "進撃の巨人") - Highly popular test.
    - **Mushoku Tensei** (`titleOriginal`: "無職転生") - Isekai genre check.
    <!-- id: 0 -->

- [x] 2. **Refactor `douban_api.py`**:
    - Update `RATE_LIMIT_DELAY` to 5.0.
    - Implement `search_douban_html(query, year)` with `div.result` selectors and top-3 inspection.
    - Handle HTTP 429/Timeout errors.
    <!-- id: 1 -->

- [x] 3. **Update `search_douban` Entry Point**:
    - Change signature to `search_douban(titles: Dict[str, str], year: int)`.
    - Implement the sequential fallback logic (CN -> JP -> EN).
    <!-- id: 2 -->

- [x] 4. **Update `cross_platform.py`**:
    - Modify `enrich_anime` to extract `titleOriginal` and `titleEnglish`.
    - Pass the dictionary to `search_douban`.
    <!-- id: 3 -->

- [x] 5. **Validation - Focused**: Run `crawler/test_douban_cases.py` and verify all 5 hard cases return valid Douban IDs. <!-- id: 4 -->

- [x] 6. **Validation - Full Coverage**: Run a partial enrichment (e.g., 50 items) or full pass to calculate the new hit rate.
    - Success Criteria: >80% match rate for items with `titleOriginal`.
    <!-- id: 5 -->