# Tasks: Improve IMDb Coverage

## Phase 1: Fix Data Pipeline (Quick Win)

- [ ] 1.1 Update `crawler/cross_platform.py` to sync base fields from raw data
  - Always copy `titleEnglish` and `titleOriginal` from raw record to enriched record
  - Even for already-processed entries, update these fields
- [ ] 1.2 Update IMDb search priority in `cross_platform.py`
  - Use `titleEnglish` first for IMDb search (if available)
  - Fallback to `titleOriginal` if no English title
- [ ] 1.3 Re-run enrichment pipeline to propagate titleEnglish
- [ ] 1.4 Validate: verify titleEnglish coverage in animes.json is ~76%

## Phase 2: Add anime-lists Mapping

- [ ] 2.1 Download anime-lists data from GitHub
  - Source: https://github.com/Anime-Lists/anime-lists
  - Save to `data/anime-list.xml`
- [ ] 2.2 Create `crawler/services/anime_lists_service.py`
  - Parse XML to extract MAL ID -> IMDb ID mappings
  - Build in-memory index for fast lookups
  - Handle missing/null IMDb entries gracefully
- [ ] 2.3 Test anime-lists lookup with 50 sample MAL IDs
- [ ] 2.4 Measure coverage: count how many of 1408 MAL IDs have IMDb mappings

## Phase 3: Integrate and Re-enrich

- [ ] 3.1 Update `crawler/cross_platform.py` IMDb lookup chain:
  1. Check anime-lists (MAL ID -> IMDb ID) - instant, no API
  2. If not found, search IMDb using titleEnglish
  3. If not found, search IMDb using titleOriginal
  4. If not found, mark as `no_imdb_match`
- [ ] 3.2 Add logging for each lookup stage
- [ ] 3.3 Backup current data files
- [ ] 3.4 Run full re-enrichment on anime missing IMDb

## Phase 4: Validation

- [ ] 4.1 Run `validate_data.py` to check new coverage rates
- [ ] 4.2 Verify IMDb coverage is 80%+ (target: ~1400/1745)
- [ ] 4.3 Spot-check 20 random anime for correct IMDb ratings
- [ ] 4.4 Generate final `data/animes.json`

## Phase 5: TMDB Fallback (Optional - only if <80%)

- [ ] 5.1 Register for TMDB API key (if needed)
- [ ] 5.2 Create `crawler/services/tmdb_service.py` (if needed)
- [ ] 5.3 Add TMDB to lookup chain after anime-lists (if needed)

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
