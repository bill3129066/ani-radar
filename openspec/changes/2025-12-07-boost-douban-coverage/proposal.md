# Proposal: Boost Douban Rating Coverage

## Summary
Increase Douban rating coverage from ~50% to **80% of active Bahamut anime with valid Japanese titles** by implementing a robust multi-stage search strategy. This strategy leverages the fact that Douban indexes original Japanese titles well, effectively bypassing Traditional/Simplified Chinese mismatches.

## Problem
The current Douban integration relies solely on the "Suggestion API" (`/j/subject_suggest`) with the Bahamut-provided Traditional Chinese title. This fails when:
1.  **Language Mismatch:** Bahamut uses Traditional Chinese (TW), while Douban uses Simplified Chinese (CN) or different translation conventions (e.g., "葬送的芙莉蓮" vs "葬送的芙莉莲").
2.  **Weak API Indexing:** The Suggestion API has a smaller index than the full HTML search engine.
3.  **Title Format:** Extra metadata like season numbers (e.g., " [1]") can confuse exact match algorithms.

## Solution
1.  **Multi-Stage Fallback Search**:
    -   **Stage 1 (Fast)**: Existing Suggestion API with Cleaned Chinese Title.
    -   **Stage 2 (Primary Fallback)**: HTML Search with **Japanese Title** (`titleOriginal`). This is the most robust method for overcoming TW/CN translation differences as Douban indexes original titles extensively.
    -   **Stage 3 (Last Resort)**: HTML Search with **English Title** (`titleEnglish`).
2.  **Implement HTML Search Scraper**:
    -   Target `https://www.douban.com/search?cat=1002&q={query}`.
    -   Parse results to extract ID, Title, Year, and Rating directly from the search page (Fast Rejection) or fetch details if needed.
    -   **Strict Rate Limiting**: Enforce a global **5.0 second** delay between requests to avoid IP bans (consistent with `CLAUDE.md`).
3.  **Enhanced Matching Logic**:
    -   Verify results using **Release Year** (±1 year tolerance).
    -   Inspect the **top 3 results** to find the best match.

## Impact
-   **Coverage**: Expected to reach >80% for anime that have a valid `titleOriginal` (Japanese).
-   **Performance**: Slightly slower enrichment process due to HTML parsing and strict rate limits, but acceptable for the offline crawler.
-   **Data Quality**: Significantly reduced false negatives caused by translation differences.

## Risks
-   **HTML Structure Changes**: The search page layout may change. The scraper must be resilient or fail soft.
-   **Rate Limiting**: HTML scraping is more sensitive. We will strictly adhere to the 5s delay.