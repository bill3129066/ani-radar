# Change: Improve IMDb Rating Coverage to 80%+

## Why

Current IMDb coverage is critically low at **5.3%** (92/1745 anime), while MAL coverage is healthy at 80.7%. This severely limits the value proposition of the multi-platform rating comparison feature.

**Root Cause Analysis:**
1. The Bahamut scraper already extracts `titleEnglish` (76.2% coverage) but this field is **not flowing through** to the final dataset
2. The enrichment pipeline was run before the scraper update, so `animes_enriched.json` has 0% English titles
3. IMDb search without English titles fails frequently

**Key Insight:** We already have the data - we just need to use it properly.

## What Changes

### Phase 1: Fix Data Pipeline (Quick Win)

1. **Ensure `titleEnglish` flows through enrichment pipeline**
   - Update `cross_platform.py` to always sync base fields from raw data
   - Re-run enrichment to propagate existing English titles
   - Expected coverage: 76.2% English titles available for IMDb search

2. **Use English titles for IMDb search**
   - Prioritize `titleEnglish` over `titleOriginal` for IMDb lookups
   - This alone should significantly boost IMDb match rate

### Phase 2: Add anime-lists Mapping (High Impact, Low Effort)

3. **Add anime-lists community mapping database**
   - Import `anime-lists` project data (MAL ID -> IMDb ID mappings)
   - Creates local lookup table - instant lookups, no API calls
   - Provides direct MAL ID -> IMDb ID mapping

### Phase 3: TMDB Fallback (Optional, if needed)

4. **TMDB API as fallback** (only if Phase 1+2 don't reach 80%)
   - Use title + year to find TMDB entry, extract IMDb ID
   - Rate-limited, use only for remaining gaps

### Simplified Strategy

| Priority | Source | Expected Coverage | Effort |
|----------|--------|-------------------|--------|
| 1 | Fix pipeline + use existing `titleEnglish` | +30-40% | Low |
| 2 | anime-lists MAL->IMDb mapping | +20-30% | Low |
| 3 | TMDB API fallback | +10-15% | Medium |

### Target Outcome

- IMDb coverage: **5.3% -> 80%+**
- Minimal new dependencies
- Leverage existing data before adding complexity

## Impact

- **Affected specs**: `data-enrichment` (new capability)
- **Affected code**:
  - `crawler/cross_platform.py` - Sync titleEnglish, use for IMDb search
  - `crawler/services/anime_lists_service.py` - New MAL->IMDb lookup
- **New dependencies**:
  - anime-lists data file (GitHub download, ~2MB)
  - TMDB API key (only if Phase 3 needed)
- **Breaking changes**: None (additive improvement)
