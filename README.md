# Ani-Radar - Bahamut Anime Rating Dashboard

A comprehensive anime rating dashboard that aggregates ratings from Bahamut Anime Crazy (巴哈姆特動畫瘋), IMDb, Douban, and MyAnimeList to help you discover the best anime to watch.

## Overview

Ani-Radar provides a multi-dimensional view of anime ratings from 4 major platforms, allowing you to filter and sort anime based on your preferences. Quickly find high-quality anime and jump directly to Bahamut Anime Crazy to watch.

### Key Features

- **Multi-Platform Ratings**: Aggregate ratings from Bahamut, IMDb, Douban, and MyAnimeList
- **Advanced Filtering**: Filter by year, genre, rating count, and search by title
- **Multiple Sorting Options**: Sort by individual platform ratings or custom weighted composite scores
- **Custom Weighting**: Define your own rating weights across platforms
- **Direct Watch Links**: One-click access to anime on Bahamut Anime Crazy
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## Tech Stack

### Frontend
- **Framework**: Next.js (App Router)
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Language**: TypeScript

### Data Pipeline
- **Crawler**: Python scripts
- **Data Storage**: Static JSON file
- **Update Strategy**: Bi-weekly updates via GitHub Actions (or manual)

## Project Structure

```
ani-radar/
├── app/                    # Next.js application
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Main dashboard page
│   ├── components/        # React components
│   └── lib/               # Utilities and helpers
├── crawler/               # Data collection scripts
│   ├── bahamut_scraper.py    # Scrape Bahamut Anime Crazy
│   ├── cross_platform.py     # Cross-platform rating alignment
│   ├── generate_json.py      # Generate final JSON data
│   └── update_latest.py      # Incremental update script
├── data/                  # Static data storage
│   └── animes.json       # Main anime database (~1800 entries)
├── prd.md                # Product Requirements Document
└── ROADMAP.md            # Phased implementation plan
```

## Data Schema

Each anime entry contains:

```typescript
interface Anime {
  id: string;                  // Unique identifier
  title: string;               // Chinese title
  titleOriginal?: string;      // Japanese original title
  thumbnail: string;           // Thumbnail URL
  year: number;                // Release year
  genres: string[];            // Genres (multiple)
  episodes: number;            // Episode count
  bahamutUrl: string;         // Watch link
  popularity: number;          // View count
  tags?: string[];            // Optional tags from Bahamut

  ratings: {
    bahamut: { score: number; votes: number };        // 1-5 scale
    imdb?: { score: number; votes: number };          // 0-10 scale
    douban?: { score: number; votes: number };        // 0-10 scale
    myanimelist?: { score: number; members: number }; // 0-10 scale
  };
}
```

## Core Features

### 1. Filtering

- **Genre Filter**: Multi-select (OR logic) - select Action + Comedy to show anime with either tag
- **Year Filter**: Single year or year range (e.g., 2024 or 2020-2023)
- **Rating Count Filter**: Hide anime with insufficient ratings (e.g., minimum 100 votes)
- **Full-Text Search**: Search by title (Chinese + Japanese) - clears other filters when active

### 2. Sorting Options

1. Highest Bahamut Rating
2. Highest IMDb Rating
3. Highest Douban Rating
4. Highest MyAnimeList Rating
5. Highest Composite Score (custom weighted)

**Missing Rating Handling**: Anime without a specific platform's rating are sorted last, with Bahamut rating as secondary sort.

### 3. Composite Score Calculation

Users can customize rating weights:
- Bahamut: 0-100%
- IMDb: 0-100%
- Douban: 0-100%
- MyAnimeList: 0-100%
- Total must equal 100%

**Calculation Process**:
1. Normalize all ratings to 0-10 scale (Bahamut 1-5 × 2)
2. Weighted average using only available ratings
3. Default: 25% each platform

**Example**:
```
Weights: Bahamut 40% / IMDb 30% / Douban 20% / MAL 10%

Anime with:
- Bahamut: 4.5 → 9.0
- IMDb: 8.5
- Douban: N/A
- MAL: 8.0

Composite = (9.0 × 0.4 + 8.5 × 0.3 + 8.0 × 0.1) / (0.4 + 0.3 + 0.1)
         = 8.69
```

## Getting Started

### Prerequisites

- Node.js 18+ (for Next.js app)
- Python 3.8+ (for crawler)
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ani-radar.git
   cd ani-radar
   ```

2. **Install frontend dependencies**
   ```bash
   cd app
   npm install
   ```

3. **Install crawler dependencies**
   ```bash
   cd crawler
   pip install -r requirements.txt
   ```

### Running the Application

```bash
cd app
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Data Collection

#### Initial Data Collection (Manual)

```bash
cd crawler
python bahamut_scraper.py      # Scrape Bahamut (~1-2 hours)
python cross_platform.py       # Align cross-platform ratings
python generate_json.py        # Generate animes.json
```

#### Bi-weekly Updates

**Option A: Manual Update**
```bash
cd crawler
python update_latest.py        # Only scrape new anime
git add data/animes.json
git commit -m "Update anime data"
git push
```

**Option B: GitHub Actions** (See `.github/workflows/update-data.yml`)

## Data Collection Strategy

### Cross-Platform Data Alignment

The core challenge is matching anime across platforms that use different titles:
- Bahamut uses Chinese titles (葬送的芙莉蓮)
- MAL uses Japanese/Romaji (Sousou no Frieren)
- IMDb uses English (Frieren: Beyond Journey's End)
- Douban uses Chinese (葬送的芙莉蓮)

**Solution**: Use Japanese original title as the bridge

```
1. Scrape Bahamut → Get Chinese title + Japanese original title
2. Search MAL using Japanese title → Get MAL rating + IMDb ID
3. Fetch IMDb rating using IMDb ID
4. Search Douban using Chinese title + year (best effort)
```

**Expected Coverage**:
- Total anime: 1500+ entries
- Cross-platform coverage: 70%+ (acceptable)
- Douban coverage: 50%+ (difficult to align)

### Rate Limiting & Best Practices

- **Bahamut**: 2-3 seconds between requests
- **MAL API**: 1.5 seconds between requests (1 req/sec limit)
- **Douban**: 5 seconds between requests (strict anti-scraping)
- **User-Agent**: Rotate 5-10 different user agents
- **Error Handling**: Continue on failure, leave ratings empty

## Development Phases

See [ROADMAP.md](ROADMAP.md) for detailed phased implementation plan.

**Quick Overview**:
1. **Phase 1**: Data collection foundation (Bahamut scraper)
2. **Phase 2**: Cross-platform alignment (MAL, IMDb, Douban)
3. **Phase 3**: Frontend core (Next.js app + basic UI)
4. **Phase 4**: Advanced filtering & sorting
5. **Phase 5**: Composite scoring & customization
6. **Phase 6**: Polish & optimization

## Success Criteria

### Functionality
- Initial dataset: 1500+ anime entries
- Cross-platform rating coverage: 70%+
- Filter response time: <1 second

### User Experience
- Time to find target anime: <30 seconds
- Intuitive filters (no instructions needed)
- Clear rating display (understand at a glance)

## Design Reference

Inspired by [awwrated.com](https://awwrated.com):
- Fixed sidebar filters
- Card-based layout
- Real-time filtering (no search button needed)
- Clean and minimal UI

**What we DON'T include**:
- Social features
- Comments
- User accounts
- Recommendation algorithms
- Historical rating tracking

## Contributing

This project is designed for personal use. If you have suggestions or find bugs, feel free to open an issue.

## License

See [LICENSE](LICENSE) file for details.

## Acknowledgments

- Data sourced from Bahamut Anime Crazy, IMDb, Douban, and MyAnimeList
- Designed for anime enthusiasts in Taiwan
- Built with Claude Code

---

**Note**: This project is for personal, non-commercial use only. Please respect the terms of service of all data sources.
