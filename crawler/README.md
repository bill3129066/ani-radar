# Ani-Radar Crawler

Python scripts for scraping anime data from Bahamut Anime Crazy (動畫瘋) and other platforms.

## Setup

### 1. Create Virtual Environment

```bash
cd crawler
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Phase 1: Bahamut Scraper

### Important Notes

⚠️ **Before running the scraper**, you need to verify and adjust the CSS selectors and HTML structure patterns to match the actual Bahamut Anime Crazy website.

The scraper uses generic patterns that may need adjustment:
- Chinese title selectors
- Japanese original title extraction (CRITICAL for cross-platform matching)
- Genre, year, episode count patterns
- Rating and vote count selectors
- Thumbnail image URLs

### Testing the Scraper

**Always test with a small dataset first:**

```bash
python test_scraper.py
```

This will:
1. Scrape only 10 anime
2. Validate all required fields are extracted
3. Check Japanese title coverage
4. Display detailed output for each anime
5. Save results to `../data/bahamut_test.json`

**Review the output carefully** to ensure:
- ✓ Chinese title is correct
- ✓ Japanese original title is extracted (CRITICAL!)
- ✓ Year, genres, episodes are accurate
- ✓ Bahamut rating (1-5 scale) and vote count are correct
- ✓ Thumbnail URL is valid

### Adjusting the Scraper

If the test scraper fails to extract data correctly, you need to:

1. **Inspect the Bahamut website** using browser DevTools
2. **Find the correct CSS selectors** for each field
3. **Update `bahamut_scraper.py`** in the `scrape_anime_detail()` function

Example adjustments:

```python
# Original (generic)
title_elem = soup.find('h1', class_='anime_name')

# Adjusted (after inspecting actual website)
title_elem = soup.find('div', class_='actual-title-class')
```

**Critical fields to verify:**
- `titleOriginal` - Japanese title (essential for Phase 2 cross-platform matching)
- `ratings.bahamut.score` - Must be 1-5 scale
- `ratings.bahamut.votes` - Number of ratings
- `year` - Release year as integer
- `genres` - Array of genre strings

### Running Full Scrape

Once the test scraper works correctly:

```bash
python bahamut_scraper.py
```

**Expected behavior:**
- Scrapes all anime from Bahamut Anime Crazy (~1500-1800 entries)
- Saves progress every 100 anime to avoid data loss
- Rate limiting: 2-4 seconds between requests
- Output: `../data/bahamut_raw.json`
- Estimated time: 1-2 hours

**Monitor the output** for:
- Success rate (should be >80%)
- Japanese title coverage (should be >90%)
- Any repeated errors that indicate selector issues

### Validating Results

After scraping is complete:

```bash
python validate_data.py
```

This checks:
- ✓ Total anime count >= 1500
- ✓ No missing required fields (title, rating, URL)
- ✓ Japanese title coverage >= 90%
- ✓ Rating values are valid (0-5 scale)
- ✓ No duplicate IDs
- ✓ Year data >= 95%
- ✓ Genre data >= 90%

**Acceptance criteria:**
- Total anime: 1500+ entries
- Japanese title: 90%+ coverage
- All ratings valid and in correct scale
- No data corruption or duplicates

## Rate Limiting

**ALWAYS respect rate limits to avoid getting blocked:**

- Bahamut: 2-4 seconds between requests
- User-Agent rotation (8 different agents)
- Random delays to appear more human-like

**If you get blocked:**
1. Increase `MIN_DELAY` and `MAX_DELAY` in `bahamut_scraper.py`
2. Add more User-Agent strings
3. Wait 30 minutes before retrying
4. Consider using proxies (last resort)

## Error Handling

The scraper is designed to **never crash**:
- Failed requests are logged and skipped
- Progress is saved every 100 anime
- Partial data is acceptable (not all fields required)
- Continues on error, provides summary at end

## Output Files

```
data/
├── bahamut_test.json       # Test run output (10 anime)
├── bahamut_raw.json        # Full scrape output (~1800 anime)
└── [future files for Phase 2]
```

## Troubleshooting

### No anime URLs found

**Problem:** `parse_anime_links()` returns empty list

**Solution:**
1. Check if the anime list URL is correct
2. Inspect the HTML structure of the list page
3. Update the regex pattern in `parse_anime_links()`:
   ```python
   anime_links = soup.find_all('a', href=re.compile(r'/animeRef\.php\?sn=\d+'))
   ```

### Missing Japanese titles

**Problem:** `titleOriginal` field is empty for most anime

**Solution:**
1. Inspect an anime detail page on Bahamut
2. Find where the Japanese title is displayed (look for "原文", "日文", or similar)
3. Update the extraction logic in `scrape_anime_detail()`:
   ```python
   # Example: If Japanese title is in a specific div
   original_title_elem = soup.find('div', class_='actual-japanese-title-class')
   if original_title_elem:
       anime['titleOriginal'] = original_title_elem.get_text(strip=True)
   ```

### Incorrect ratings

**Problem:** Ratings are not in 0-5 scale or seem wrong

**Solution:**
1. Check if Bahamut uses a different scale (e.g., 0-10)
2. Update the extraction and normalization logic
3. Verify vote count is extracted from the correct element

### Getting blocked / 403 errors

**Problem:** Requests fail with 403 or rate limiting errors

**Solution:**
1. Increase delay: `MIN_DELAY = 5.0`, `MAX_DELAY = 8.0`
2. Add more User-Agent strings
3. Wait 30-60 minutes before retrying
4. Check if IP is temporarily banned

## Next Steps

After completing Phase 1:

1. ✓ Verify `data/bahamut_raw.json` exists and is valid
2. ✓ Run `validate_data.py` and ensure all checks pass
3. ✓ Check Japanese title coverage is >= 90%
4. → Proceed to **Phase 2**: Cross-platform rating alignment (MAL, IMDb, Douban)

## Development Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Test scraper runs successfully (10 anime)
- [ ] Japanese title extraction verified (CRITICAL!)
- [ ] Selectors adjusted to match actual website
- [ ] Full scraper runs without crashes
- [ ] Data validation passes all checks
- [ ] Output file contains 1500+ anime entries
- [ ] Japanese title coverage >= 90%
- [ ] Ready for Phase 2

## Support

If you encounter issues:
1. Check this README first
2. Review error messages carefully
3. Inspect the actual website structure
4. Adjust selectors in `bahamut_scraper.py`
5. Test with `test_scraper.py` after changes

**Remember:** The scraper selectors are generic templates. You MUST verify them against the actual Bahamut Anime Crazy website before running the full scrape.
