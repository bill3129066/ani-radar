# Ani-Radar Data Crawler

This directory contains the complete data collection pipeline for **Ani-Radar**. It is designed to aggregate anime data from Bahamut Anime Crazy and enrich it with ratings from global platforms (MyAnimeList, IMDb, Douban).

## 📂 Directory Structure

```
crawler/
├── bahamut_scraper.py    # Phase 1: Scrapes basic data from Bahamut
├── cross_platform.py     # Phase 2: Fetches ratings from MAL, IMDb, Douban
├── generate_json.py      # Phase 3: Validates and generates final frontend JSON
├── validate_data.py      # Utility: Checks data health (coverage, missing fields)
├── test_scraper.py       # Utility: Quick 10-item test to verify selectors
├── manual_mapping.json   # Config: Manual overrides for failed matches
├── requirements.txt      # Python dependencies
└── README.md             # This guide
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- `pip`

### Installation

1. **Setup Virtual Environment** (Recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # venv\Scripts\activate   # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🛠️ Data Pipeline Workflow

The data collection process consists of three sequential steps.

### Step 1: Foundation (Bahamut Scraper)
Scrapes the catalog and details from Bahamut Anime Crazy.

- **Command**: `python bahamut_scraper.py`
- **Output**: `../data/bahamut_raw.json`
- **Duration**: ~1-2 hours (due to rate limiting)
- **Key Features**:
  - Fetches list pages to get all IDs.
  - Scrapes individual detail pages.
  - **Crucial**: Navigates to the linked "Work Info" (ACG Database) page to extract the **Japanese Original Title**, which is essential for cross-platform matching.

### Step 2: Enrichment (Cross-Platform Orchestrator)
Uses the Japanese title to find corresponding entries on other platforms.

- **Command**: `python cross_platform.py`
- **Input**: `../data/bahamut_raw.json`
- **Output**: `../data/animes_enriched.json`
- **Duration**: ~1-2 hours
- **Logic**:
  1. **MyAnimeList**: Search Jikan API (v4) using Japanese Title.
  2. **IMDb**: 
     - First, check if MAL provided an IMDb ID.
     - If not, use IMDb Suggestion API to search by title.
     - Scrape rating via JSON-LD on the IMDb page.
  3. **Douban**: Search using Chinese title + Year (Best effort).
- **Resumable**: The script saves progress every 10 items. You can stop and restart it safely.

### Step 3: Production Build (Generator)
Finalizes the dataset for the Next.js frontend.

- **Command**: `python generate_json.py`
- **Input**: `../data/animes_enriched.json` + `manual_mapping.json`
- **Output**: `../data/animes.json` (The actual file used by the App)
- **Features**:
  - Applies manual mappings.
  - Validates required fields (title, year).
  - Normalizes data structures.

---

## ⚙️ Configuration & Maintenance

### Rate Limiting
To prevent IP bans, the scripts include hardcoded delays:
- **Bahamut**: 1-3 seconds between requests.
- **Jikan (MAL)**: ~1.5 seconds (API limit is strict).
- **Douban**: 2+ seconds (Strict anti-scraping).

### Manual Mapping (`manual_mapping.json`)
If the automated matching fails (e.g., wrong IMDb link or missing rating), you can manually enforce IDs in this file.

**Format**:
```json
{
  "bahamut_id_here": {
    "imdb_id": "tt1234567",
    "mal_id": 12345,
    "douban_id": "123456"
  }
}
```

### Data Validation
Run `python validate_data.py` to check the health of `bahamut_raw.json` or `animes.json` (modify script input path as needed). It reports:
- Missing critical fields (Episodes, Popularity).
- Coverage of Japanese titles.

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **429 Too Many Requests** | The script auto-sleeps. If persistent, stop and wait 1 hour. |
| **IMDb/Douban not found** | Verify the title. Add entry to `manual_mapping.json`. |
| **Selectors broken** | Bahamut may have changed their UI. Run `python test_scraper.py` to debug specific fields. |

---

## 📦 API Reference

- **Jikan API (MAL)**: [https://jikan.moe/](https://jikan.moe/)
- **IMDb**: Uses undocumented Suggestion API (`v2.sg.media-imdb.com`).
- **Douban**: Uses internal suggestion API (`movie.douban.com/j/subject_suggest`).
