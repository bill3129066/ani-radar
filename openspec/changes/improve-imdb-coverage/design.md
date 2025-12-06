# Design: IMDb Coverage Improvement

## Context

Current IMDb coverage is 5.3% (92/1745), making the multi-platform comparison feature nearly useless for IMDb.

**Root Cause Discovery:**
- The Bahamut scraper already extracts `titleEnglish` with **76.2% coverage**
- However, this field shows **0%** in `animes_enriched.json` and `animes.json`
- The enrichment pipeline was run before the scraper update, so the field never propagated
- The enricher skips already-processed entries, never picking up new fields from raw data

**Key Insight:** We don't need complex title generation - we already have the data.

## Goals / Non-Goals

### Goals
- Achieve 80%+ IMDb coverage
- Fix the data pipeline to use existing `titleEnglish`
- Add anime-lists for direct MAL->IMDb mapping
- Keep solution simple and maintainable

### Non-Goals
- 100% coverage (some anime don't exist on IMDb)
- Complex title transliteration (not needed with 76% English coverage)
- TMDB integration (only as last resort)

## Decision 1: Fix Data Pipeline First

**Problem:** `titleEnglish` exists in raw data (76.2%) but isn't flowing through.

**Solution:** Update `cross_platform.py` to always sync base fields:

```python
# In enrich_anime(), always update these from raw:
current_record['titleEnglish'] = anime.get('titleEnglish') or current_record.get('titleEnglish')
current_record['titleOriginal'] = anime.get('titleOriginal') or current_record.get('titleOriginal')
```

**Why this works:**
- Raw data already has the English titles
- Just need to propagate them through the pipeline
- No new dependencies or API calls needed

## Decision 2: Use anime-lists for Direct ID Mapping

**What:** Download anime-lists community data for MAL ID -> IMDb ID lookups.

**Why:**
- Community-maintained, regularly updated
- Direct ID mapping - no fuzzy matching needed
- Local file - instant lookups, no API rate limits
- ~2MB download from GitHub

**Data Source:** https://github.com/Anime-Lists/anime-lists

## Decision 3: Simplified IMDb Lookup Chain

```
1. anime-lists lookup (MAL ID -> IMDb ID)
   ↓ if not found
2. IMDb search using titleEnglish (76% have this)
   ↓ if not found
3. IMDb search using titleOriginal (Japanese)
   ↓ if not found
4. Mark as no_imdb_match
```

**Why this order:**
- anime-lists is instant and accurate (ID-based)
- English titles match IMDb better than Japanese
- Keep Japanese as fallback for non-English entries

## Decision 4: TMDB as Optional Phase 5

**When:** Only if coverage is still <80% after implementing Phases 1-4.

**Why defer:**
- Adds API key dependency
- Rate limiting complexity
- May not be needed if anime-lists + English titles are sufficient

## Removed from Original Plan

| Originally Proposed | Removed Because |
|---------------------|-----------------|
| pykakasi Romaji transliteration | 76% already have English titles |
| MAL API title_english extraction | Bahamut already has this |
| AOD synonym extraction | Not needed with existing English titles |
| Complex title variant generation | Over-engineering given available data |

## Data Flow (Simplified)

```
bahamut_raw.json (titleEnglish: 76.2%)
        │
        ▼
cross_platform.py (sync titleEnglish)
        │
        ├─── anime-lists lookup (MAL ID -> IMDb ID)
        │           │
        │           ▼ (if not found)
        ├─── IMDb search (using titleEnglish)
        │           │
        │           ▼ (if not found)
        └─── IMDb search (using titleOriginal)
                    │
                    ▼
animes_enriched.json
        │
        ▼
animes.json (IMDb: 80%+ target)
```

## Risks

### Risk 1: anime-lists Missing Mappings
- **Impact:** Some MAL IDs won't have IMDb mapping
- **Mitigation:** Fallback to title-based IMDb search

### Risk 2: IMDb Search False Positives
- **Impact:** Wrong IMDb ratings
- **Mitigation:** Year validation, existing confidence scoring

## Open Questions

1. **anime-lists update frequency?**
   - Recommendation: Download fresh copy with each bi-weekly update

2. **What if still <80% after Phase 4?**
   - Recommendation: Implement TMDB fallback (Phase 5)
