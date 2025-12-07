# Tasks: Improve IMDb Coverage

## Phase 1: Fix Data Pipeline (Quick Win) ✅

- [x] 1.1 Update `crawler/cross_platform.py` to sync base fields from raw data
  - Always copy `titleEnglish` and `titleOriginal` from raw record to enriched record
  - Even for already-processed entries, update these fields
- [x] 1.2 Update IMDb search priority in `cross_platform.py`
  - Use `titleEnglish` first for IMDb search (if available)
  - Fallback to `titleOriginal` if no English title
- [x] 1.3 Re-run enrichment pipeline to propagate titleEnglish
- [x] 1.4 Validate: verify titleEnglish coverage in animes.json is ~76%

## Phase 2: Add anime-lists Mapping ✅

- [x] 2.1 Download anime-lists data from GitHub
  - Source: https://github.com/Fribb/anime-lists (JSON format with direct MAL->IMDb mappings)
  - Saved to `data/anime-lists.json` (7.2MB, 7131 MAL->IMDb mappings)
- [x] 2.2 Create `crawler/services/anime_lists_service.py`
  - Parse JSON to extract MAL ID -> IMDb ID mappings
  - Build in-memory index for fast lookups
  - Handle missing/null IMDb entries gracefully
- [x] 2.3 Test anime-lists lookup with sample MAL IDs
  - Verified: MAL 52991 (Frieren) -> tt22248376
  - Verified: MAL 5114 (FMA:B) -> tt1355642
- [x] 2.4 Measure coverage: 1224/1330 (92%) of our MAL IDs have IMDb mappings in anime-lists

## Phase 3: Integrate and Re-enrich ✅

- [x] 3.1 Update `crawler/cross_platform.py` IMDb lookup chain:
  1. Check manual mapping
  2. Check existing data
  3. Check anime-lists (MAL ID -> IMDb ID) - instant, no API
  4. Check MAL external links
  5. Search IMDb using titleEnglish
  6. Search IMDb using titleOriginal
- [x] 3.2 Add logging for each lookup stage (imdb_lookup_method tracking)
- [x] 3.3 Backup current data files
- [x] 3.4 Run full re-enrichment on anime missing IMDb

## Phase 4: Validation ✅

- [x] 4.1 Run `validate_data.py` to check new coverage rates
- [x] 4.2 Verify IMDb coverage is 80%+ (target: ~1400/1745)
  - **RESULT: 88.6% (1546/1745)** - Exceeded target!
- [x] 4.3 Spot-check random anime for correct IMDb ratings
- [x] 4.4 Generate final `data/animes.json`

## Phase 5: TMDB Fallback (Optional - only if <80%) ⏭️ SKIPPED

- [x] ~~5.1 Register for TMDB API key~~ - Not needed
- [x] ~~5.2 Create `crawler/services/tmdb_service.py`~~ - Not needed
- [x] ~~5.3 Add TMDB to lookup chain~~ - Not needed

**Note:** Phase 5 skipped - anime-lists + English title search achieved 88.6% coverage, exceeding target.

## Dependencies

- Phase 1 is the critical fix - do this first
- Phase 2 can run in parallel with Phase 1
- Phase 3 depends on both Phase 1 and 2
- Phase 4 depends on Phase 3
- Phase 5 only needed if coverage still <80% after Phase 4

## Estimated Effort

| Phase | Time | API Calls |
|-------|------|-----------|
| Phase 1 | 1-2 hours | ~1600 (IMDb fetch) |
| Phase 2 | 1 hour | 0 (local data) |
| Phase 3 | 30 min | Included in Phase 1 |
| Phase 4 | 30 min | 0 |
| Phase 5 | 2-3 hours | ~800 (if needed) |

## Implementation Summary

### Code Changes Made:
1. `crawler/cross_platform.py`:
   - Added import for `AnimeListsService`
   - Added `ANIME_LISTS_FILE` path constant
   - Added `anime_lists_service` global
   - Updated `load_services()` to initialize anime-lists service
   - Added field sync for `titleEnglish`/`titleOriginal` in main loop
   - Restructured IMDb lookup chain with anime-lists as primary source
   - Added `imdb_lookup_method` tracking for debugging

2. `crawler/services/anime_lists_service.py`: New file
   - `AnimeListsService` class with MAL->IMDb lookup

3. `data/anime-lists.json`: New data file (7.2MB)
   - 7131 MAL->IMDb mappings from Fribb/anime-lists

### Final Results:
- Previous IMDb coverage: 5.3% (92/1745)
- **Final IMDb coverage: 88.6% (1546/1745)** ✅
- Target was 80%+ - Exceeded by 8.6%!

### Coverage Summary (Final):
| Platform | Coverage |
|----------|----------|
| Bahamut  | 100% (1745/1745) |
| MAL      | 80.7% (1409/1745) |
| **IMDb** | **88.6% (1546/1745)** |
| Douban   | 58.5% (1021/1745) |
