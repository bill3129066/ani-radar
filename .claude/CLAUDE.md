# CLAUDE.md - AI Assistant Guide for Ani-Radar

**Last Updated**: 2025-12-02
**Project Status**: Phase 1.5 (Data Remediation - ACG Database Integration)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Codebase Structure](#codebase-structure)
3. [Tech Stack](#tech-stack)
4. [Current Implementation Status](#current-implementation-status)
5. [Development Workflows](#development-workflows)
6. [Key Conventions](#key-conventions)
7. [Core Business Logic](#core-business-logic)
8. [Data Pipeline Architecture](#data-pipeline-architecture)
9. [Common Tasks](#common-tasks)
10. [Testing Strategy](#testing-strategy)
11. [Deployment](#deployment)
12. [Critical Information](#critical-information)

---

## Project Overview

### What is Ani-Radar?

Ani-Radar is a personal anime rating dashboard that aggregates ratings from four major platforms:
- **巴哈姆特動畫瘋** (Bahamut Anime Crazy) - Primary data source
- **IMDb** - International movie database ratings
- **豆瓣** (Douban) - Chinese ratings platform
- **MyAnimeList** (MAL) - Dedicated anime database

### Core Features

1. **Multi-Platform Ratings Display** - Show ratings from all 4 platforms side-by-side
2. **Advanced Filtering** - Genre, year range, minimum vote count, full-text search
3. **Multiple Sorting Options** - Sort by any platform's rating or custom composite score
4. **Custom Weighted Scoring** - Users can define their own rating weights across platforms
5. **Direct Watch Links** - One-click access to Bahamut Anime Crazy

### What We DON'T Build

- ❌ Video playback functionality
- ❌ Social features (comments, sharing, user profiles)
- ❌ User accounts or authentication
- ❌ Recommendation algorithms
- ❌ Rating history tracking
- ❌ Multiple region support (focused on Taiwan/Bahamut)

---

## Codebase Structure

### Current Structure (Phase 0)

```
ani-radar/
├── .claude/                    # Claude Code configuration
│   ├── config.yaml            # Claude Code settings
│   └── skills/                # Project-specific skills
├── app/                       # Next.js App Router
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Main page (default Next.js template)
│   ├── globals.css           # Global styles
│   └── favicon.ico           # Favicon
├── public/                    # Static assets
├── .gitignore                # Git ignore rules
├── eslint.config.mjs         # ESLint configuration
├── next.config.ts            # Next.js configuration
├── package.json              # Node.js dependencies
├── postcss.config.mjs        # PostCSS configuration
├── tsconfig.json             # TypeScript configuration
├── LICENSE                   # MIT License
├── README.md                 # User-facing documentation
├── PRD.md                    # Product Requirements Document (Chinese)
├── ROADMAP.md                # Detailed implementation roadmap
└── CLAUDE.md                 # This file (AI assistant guide)
```

### Target Structure (After Full Implementation)

```
ani-radar/
├── app/                       # Next.js application
│   ├── components/           # React components
│   │   ├── anime-card.tsx       # Individual anime display card
│   │   ├── anime-grid.tsx       # Grid layout for cards
│   │   ├── filter-sidebar.tsx   # Main filter sidebar
│   │   ├── search-input.tsx     # Search component
│   │   ├── genre-filter.tsx     # Genre multi-select
│   │   ├── year-filter.tsx      # Year range selector
│   │   ├── sort-selector.tsx    # Sort dropdown
│   │   ├── weight-config.tsx    # Composite score weight config
│   │   ├── empty-state.tsx      # No results display
│   │   └── ui/                  # shadcn/ui components
│   ├── lib/                  # Utilities and helpers
│   │   ├── data-loader.ts       # Load anime data from JSON
│   │   ├── filters.ts           # Filtering logic
│   │   ├── sorting.ts           # Sorting algorithms
│   │   └── utils.ts             # Utility functions (cn, formatNumber, etc.)
│   ├── types/                # TypeScript type definitions
│   │   └── anime.ts             # Core data types
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Main dashboard page
│   ├── loading.tsx           # Loading state
│   ├── error.tsx             # Error boundary
│   └── globals.css           # Global styles
├── crawler/                  # Python data collection scripts
│   ├── bahamut_scraper.py       # Scrape Bahamut Anime Crazy
│   ├── mal_api.py               # MyAnimeList API integration
│   ├── imdb_api.py              # IMDb data fetching
│   ├── douban_api.py            # Douban scraper
│   ├── cross_platform.py        # Cross-platform data alignment
│   ├── generate_json.py         # Generate final JSON output
│   ├── update_latest.py         # Incremental update script
│   ├── validate_data.py         # Data quality validation
│   ├── test_scraper.py          # Test scraper with small dataset
│   ├── manual_mapping.json      # Manual ID mappings (fallback)
│   ├── requirements.txt         # Python dependencies
│   └── venv/                    # Python virtual environment
├── data/                     # Data storage
│   ├── animes.json              # Final dataset (~1800 anime)
│   ├── bahamut_raw.json         # Raw Bahamut data (intermediate)
│   └── animes_enriched.json     # Enriched data (intermediate)
├── .github/
│   └── workflows/
│       └── update-data.yml      # Automated bi-weekly updates (optional)
└── [config files as above]
```

---

## Tech Stack

### Frontend

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 4+
- **UI Components**: shadcn/ui (Radix UI + Tailwind)
- **Icons**: lucide-react
- **Utilities**: clsx, tailwind-merge, class-variance-authority

### Data Pipeline

- **Crawler Language**: Python 3.8+
- **HTTP Requests**: requests library
- **HTML Parsing**: BeautifulSoup4 with lxml
- **Data Format**: JSON (static file)
- **Update Strategy**: Bi-weekly manual or automated via GitHub Actions

### Development Tools

- **Package Manager**: npm
- **Linter**: ESLint (Next.js config)
- **Type Checking**: TypeScript strict mode
- **Version Control**: Git + GitHub

---

## Current Implementation Status

### ✅ Completed (Phase 1)

- [x] Next.js project initialized
- [x] Basic file structure in place
- [x] Documentation files created (README, PRD, ROADMAP, CLAUDE.md)
- [x] **Bahamut Scraper**: Implemented and working (`crawler/bahamut_scraper.py`)
- [x] **Raw Data**: Scraped 1700+ animes (`data/bahamut_raw.json`)
- [x] **Validation**: Script implemented (`crawler/validate_data.py`)

### ⚠️ Critical Issues (Phase 1.5)

- [ ] **Japanese Title Missing**: Coverage is 0.0%. This blocks Phase 2.
- [ ] **Action Required**: Modify scraper to follow "Work Info" link to ACG Database page.

### 📋 Planned (See ROADMAP.md for details)

- **Phase 1.5**: Data Remediation (ACG Database Integration)
- **Phase 2**: Cross-platform rating alignment (MAL, IMDb, Douban)
- **Phase 3**: Frontend foundation (types, data loader, basic layout)
- **Phase 4**: Core UI components
- **Phase 5**: Filtering & sorting logic
- **Phase 6**: Main dashboard integration
- **Phase 7**: Composite score customization
- **Phase 8**: Polish & optimization
- **Phase 9**: Deployment preparation

---

## Development Workflows

### Initial Setup (First Time)

```bash
# Frontend setup
cd app
npm install
npm run dev

# Backend setup (when starting Phase 1)
cd crawler
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Daily Development Workflow

#### Working on Frontend

```bash
cd app
npm run dev          # Start dev server (http://localhost:3000)
npm run build        # Test production build
npm run lint         # Run ESLint
```

#### Working on Data Pipeline

```bash
cd crawler
source venv/bin/activate  # Activate virtual environment

# Test with small dataset first
python test_scraper.py

# Run full pipeline
python bahamut_scraper.py
python cross_platform.py
python generate_json.py
```

### Git Workflow

**Branch Naming**: Use the provided branch `claude/claude-md-miofdlieozuzw69s-018EZDqdYrv1rEZ63gYrDVfj`

**Commit Message Format**:
```
<type>: <description>

Types: feat, fix, docs, style, refactor, test, chore
Examples:
- feat: add anime card component
- fix: correct composite score calculation
- docs: update CLAUDE.md with new conventions
```

**Pushing Changes**:
```bash
git add .
git commit -m "feat: add filtering logic"
git push -u origin claude/claude-md-miofdlieozuzw69s-018EZDqdYrv1rEZ63gYrDVfj
```

**CRITICAL**: Always use the exact branch name. Push will fail with 403 if branch doesn't start with 'claude/' and match session ID.

---

## Key Conventions

### TypeScript Conventions

#### File Organization

- **Components**: Use PascalCase for files and exports
  ```typescript
  // app/components/anime-card.tsx
  export function AnimeCard({ anime }: AnimeCardProps) { ... }
  ```

- **Utilities**: Use kebab-case for files, camelCase for exports
  ```typescript
  // app/lib/data-loader.ts
  export function loadAnimeData(): Anime[] { ... }
  ```

- **Types**: Use PascalCase for interfaces and types
  ```typescript
  // app/types/anime.ts
  export interface Anime { ... }
  export type SortOption = 'bahamut' | 'imdb' | ...;
  ```

#### Import Aliases

Use `@/` for all imports from the app directory:

```typescript
import { Anime } from '@/types/anime';
import { loadAnimeData } from '@/lib/data-loader';
import { AnimeCard } from '@/components/anime-card';
```

#### Type Safety

- **Always** define proper TypeScript types for all props and functions
- Use `interface` for object types, `type` for unions/primitives
- Avoid `any` - use `unknown` if type is truly unknown
- Enable strict mode (already configured in tsconfig.json)

### React Conventions

#### Client vs Server Components

- **Default to Server Components** for better performance
- Use `'use client'` directive ONLY when needed:
  - Components with state (useState, useReducer)
  - Components with effects (useEffect)
  - Components with event handlers (onClick, onChange)
  - Components using browser APIs

```typescript
// Server Component (default)
export function AnimeGrid({ animes }: AnimeGridProps) {
  return <div>...</div>;
}

// Client Component (needs interactivity)
'use client';
export function SearchInput({ value, onChange }: SearchInputProps) {
  return <input onChange={onChange} />;
}
```

#### Component Structure

```typescript
// 1. Imports
import { Anime } from '@/types/anime';
import { Button } from '@/components/ui/button';

// 2. Type definitions
interface AnimeCardProps {
  anime: Anime;
}

// 3. Component
export function AnimeCard({ anime }: AnimeCardProps) {
  // 4. Hooks (if client component)
  // 5. Helper functions
  // 6. JSX return
  return (
    <div>...</div>
  );
}
```

### CSS/Styling Conventions

#### Tailwind CSS Usage

- Use Tailwind utility classes for all styling
- Use `cn()` utility for conditional classes:
  ```typescript
  import { cn } from '@/lib/utils';

  <div className={cn(
    "base classes",
    condition && "conditional classes"
  )}>
  ```

- Follow responsive design pattern:
  ```typescript
  // Mobile-first approach
  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
  ```

#### Color Scheme

- Use Tailwind's default color palette
- Primary UI: gray scale
- Accent: Use sparingly for CTAs
- Dark mode: Implement with `dark:` prefix

### Python Conventions

#### Code Style

- Follow PEP 8 style guide
- Use snake_case for functions and variables
- Use 4 spaces for indentation
- Maximum line length: 100 characters

#### Error Handling

**CRITICAL**: Never crash on scraping errors. Always continue.

```python
# Good: Log error and continue
try:
    anime_data = scrape_anime_page(url)
except Exception as e:
    print(f"Failed to scrape {url}: {e}")
    continue  # Skip this anime, continue with next

# Bad: Let exception crash the script
anime_data = scrape_anime_page(url)  # Will crash on error
```

#### Rate Limiting

**ALWAYS** implement rate limiting to avoid getting blocked:

```python
import time
import random

# Bahamut: 2-3 seconds between requests
time.sleep(random.uniform(2, 4))

# MyAnimeList API: 1.5 seconds (1 req/sec limit)
time.sleep(1.5)

# Douban: 5 seconds (strict anti-scraping)
time.sleep(5)
```

#### User-Agent Rotation

```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...',
    # Prepare 5-10 different user agents
]

headers = {
    'User-Agent': random.choice(USER_AGENTS)
}
```

---

## Core Business Logic

### Data Schema

Every anime entry follows this structure:

```typescript
interface Anime {
  // Identifiers
  id: string;                    // Unique ID (Bahamut ID)

  // Basic Info
  title: string;                 // Chinese title
  titleOriginal?: string;        // Japanese original title (CRITICAL for cross-platform matching)
  thumbnail: string;             // Image URL
  year: number;                  // Release year
  genres: string[];              // Array of genre tags
  episodes: number;              // Episode count
  bahamutUrl: string;           // Watch link
  popularity: number;            // View count on Bahamut
  tags?: string[];              // Optional additional tags

  // Ratings (all 4 platforms)
  ratings: {
    bahamut: {
      score: number;             // 1-5 scale
      votes: number;             // Number of ratings
    };
    imdb?: {
      score: number;             // 0-10 scale
      votes: number;
    };
    douban?: {
      score: number;             // 0-10 scale
      votes: number;
    };
    myanimelist?: {
      score: number;             // 0-10 scale
      members: number;           // MyAnimeList uses "members" not "votes"
    };
  };
}
```

### Filtering Logic (app/lib/filters.ts)

#### Search Behavior (CRITICAL)

**When user searches**:
1. Clear ALL other filters (genres, year, minVotes)
2. Search in: Chinese title + Japanese original title
3. Case-insensitive matching
4. Preserve sort order setting

**When search is cleared**:
- Restore previous filter state OR show all anime

#### Genre Filter

- Logic: **OR** (not AND)
- Example: Select "Action" + "Comedy" = Show anime with Action OR Comedy
- Empty selection = Show all genres

#### Year Range Filter

- Support single year OR year range
- Example: 2024 (single), 2020-2023 (range)
- Optional: yearStart and yearEnd can be independently set

#### Minimum Votes Filter

- Hide anime with insufficient ratings
- Apply to Bahamut vote count (primary platform)
- Default: 0 (show all)
- Suggested default: 50-100 for better quality

### Sorting Logic (app/lib/sorting.ts)

#### Sort Options

1. **bahamut**: Sort by Bahamut rating (1-5 scale)
2. **imdb**: Sort by IMDb rating (0-10 scale)
3. **douban**: Sort by Douban rating (0-10 scale)
4. **myanimelist**: Sort by MyAnimeList rating (0-10 scale)
5. **composite**: Sort by custom weighted composite score

#### Missing Rating Handling (CRITICAL)

For platform-specific sorting (IMDb, Douban, MAL):
1. Anime WITH the rating → Sort by that rating (descending)
2. Anime WITHOUT the rating → Place at the end
3. Within each group → Secondary sort by Bahamut rating

```typescript
// Example: Sort by IMDb
sorted.sort((a, b) => {
  const scoreA = a.ratings.imdb?.score ?? -1;
  const scoreB = b.ratings.imdb?.score ?? -1;

  // Both missing IMDb → Sort by Bahamut
  if (scoreA === -1 && scoreB === -1) {
    return b.ratings.bahamut.score - a.ratings.bahamut.score;
  }

  // One missing → Put at end
  if (scoreA === -1) return 1;
  if (scoreB === -1) return -1;

  // Both have IMDb → Sort by IMDb, then Bahamut
  if (scoreB !== scoreA) return scoreB - scoreA;
  return b.ratings.bahamut.score - a.ratings.bahamut.score;
});
```

### Composite Score Calculation (CRITICAL)

#### Formula

**Step 1**: Normalize all ratings to 0-10 scale
- Bahamut: Multiply by 2 (1-5 → 2-10)
- Others: Already 0-10

**Step 2**: Calculate weighted average using ONLY available ratings

```typescript
function calculateCompositeScore(anime: Anime, weights: WeightConfig): number {
  let totalScore = 0;
  let totalWeight = 0;

  // Bahamut (always available)
  const bahamutNormalized = anime.ratings.bahamut.score * 2;
  totalScore += bahamutNormalized * (weights.bahamut / 100);
  totalWeight += weights.bahamut / 100;

  // IMDb (if available)
  if (anime.ratings.imdb) {
    totalScore += anime.ratings.imdb.score * (weights.imdb / 100);
    totalWeight += weights.imdb / 100;
  }

  // Douban (if available)
  if (anime.ratings.douban) {
    totalScore += anime.ratings.douban.score * (weights.douban / 100);
    totalWeight += weights.douban / 100;
  }

  // MyAnimeList (if available)
  if (anime.ratings.myanimelist) {
    totalScore += anime.ratings.myanimelist.score * (weights.myanimelist / 100);
    totalWeight += weights.myanimelist / 100;
  }

  return totalWeight > 0 ? totalScore / totalWeight : 0;
}
```

#### Example Calculation

```
User weights: Bahamut 40%, IMDb 30%, Douban 20%, MAL 10%

Anime ratings:
- Bahamut: 4.5 → Normalized: 9.0
- IMDb: 8.5
- Douban: N/A (missing)
- MAL: 8.0

Composite = (9.0 × 0.4 + 8.5 × 0.3 + 8.0 × 0.1) / (0.4 + 0.3 + 0.1)
          = (3.6 + 2.55 + 0.8) / 0.8
          = 6.95 / 0.8
          = 8.69
```

#### Weight Validation

- Sum of all weights MUST equal 100%
- Each weight: 0-100%
- Default: 25% each (equal weight)
- UI should show error if total ≠ 100%

---

## Data Pipeline Architecture

### Overview

The most challenging aspect of this project is **cross-platform data alignment**. Different platforms use different titles:

- Bahamut: Chinese (葬送的芙莉蓮)
- MAL: Japanese/Romaji (Sousou no Frieren)
- IMDb: English (Frieren: Beyond Journey's End)
- Douban: Chinese (葬送的芙莉蓮)

**Solution**: Use Japanese original title as the bridge.

### Pipeline Flow

```
Step 1: Scrape Bahamut
├─ Extract Chinese title
├─ Extract Japanese original title (CRITICAL!)
├─ Extract Bahamut rating
└─ Save to bahamut_raw.json

Step 2: Search MyAnimeList
├─ Use Japanese title to search MAL API
├─ Get MAL rating + MAL ID
├─ Extract IMDb ID from MAL external links
└─ Handle mismatches (log and skip)

Step 3: Fetch IMDb Rating
├─ Use IMDb ID from Step 2
├─ Fetch via OMDb API or web scraping
└─ Handle missing IMDb IDs gracefully

Step 4: Search Douban (Best Effort)
├─ Use Chinese title + year
├─ Match with fuzzy logic
├─ Accept 50% coverage as success
└─ Consider manual mapping for top 100

Step 5: Generate Final JSON
├─ Merge all ratings
├─ Apply manual mappings (if any)
├─ Validate data structure
└─ Save to data/animes.json
```

### Expected Coverage Rates

- **Total anime**: 1500-1800 entries
- **MAL coverage**: 70-80% (good)
- **IMDb coverage**: 70-80% (good)
- **Douban coverage**: 50-60% (acceptable, due to difficulty)

**Important**: Don't aim for 100% coverage. Accept that some anime won't have all ratings.

### Data Quality Validation

Before using the final dataset, validate:

```python
def validate_data(animes):
    print(f"Total anime: {len(animes)}")

    # Check required fields
    missing_title = [a for a in animes if not a.get('title')]
    missing_japanese = [a for a in animes if not a.get('titleOriginal')]

    print(f"Missing title: {len(missing_title)}")
    print(f"Missing Japanese title: {len(missing_japanese)}")

    # Check rating coverage
    has_imdb = sum(1 for a in animes if a['ratings'].get('imdb'))
    has_douban = sum(1 for a in animes if a['ratings'].get('douban'))
    has_mal = sum(1 for a in animes if a['ratings'].get('myanimelist'))

    print(f"IMDb coverage: {has_imdb / len(animes) * 100:.1f}%")
    print(f"Douban coverage: {has_douban / len(animes) * 100:.1f}%")
    print(f"MAL coverage: {has_mal / len(animes) * 100:.1f}%")

    # Success criteria
    assert len(animes) >= 1500, "Need at least 1500 anime"
    assert has_mal / len(animes) >= 0.7, "MAL coverage should be >= 70%"
```

### Manual Mapping Fallback

For anime where automatic matching fails:

```json
// crawler/manual_mapping.json
{
  "123456": {  // Bahamut ID
    "mal_id": "39535",
    "imdb_id": "tt13146488",
    "douban_id": "34895145"
  }
}
```

Apply these mappings AFTER automatic processing but BEFORE final JSON generation.

---

## Common Tasks

### Adding a New UI Component

1. **Create component file**:
   ```bash
   # Create in app/components/
   touch app/components/my-component.tsx
   ```

2. **Define types and component**:
   ```typescript
   'use client'; // If needs interactivity

   import { SomeType } from '@/types/anime';

   interface MyComponentProps {
     data: SomeType;
     onAction: () => void;
   }

   export function MyComponent({ data, onAction }: MyComponentProps) {
     return <div>...</div>;
   }
   ```

3. **Import and use**:
   ```typescript
   import { MyComponent } from '@/components/my-component';
   ```

### Adding shadcn/ui Components

```bash
cd app
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
# etc.
```

Components will be added to `app/components/ui/`

### Modifying Filter Logic

1. **Update filter state type** (app/types/anime.ts):
   ```typescript
   export interface FilterState {
     // Add your new filter
     myNewFilter: string;
   }
   ```

2. **Implement filter logic** (app/lib/filters.ts):
   ```typescript
   export function filterAnimes(animes: Anime[], filters: FilterState): Anime[] {
     // Add your filter logic
     if (filters.myNewFilter) {
       filtered = filtered.filter(/* your condition */);
     }
   }
   ```

3. **Add UI control** (app/components/filter-sidebar.tsx)

4. **Update state management** (app/page.tsx)

### Adding a New Sort Option

1. **Add to SortOption type** (app/types/anime.ts):
   ```typescript
   export type SortOption =
     | 'bahamut'
     | 'imdb'
     | 'myNewSort'; // Add here
   ```

2. **Implement sort logic** (app/lib/sorting.ts):
   ```typescript
   export function sortAnimes(animes: Anime[], sortBy: SortOption): Anime[] {
     switch (sortBy) {
       case 'myNewSort':
         return sorted.sort((a, b) => {
           // Your sort logic
         });
     }
   }
   ```

3. **Add to UI dropdown** (app/components/sort-selector.tsx):
   ```typescript
   <SelectItem value="myNewSort">My New Sort</SelectItem>
   ```

### Running the Data Pipeline

#### First Time (Full Scrape)

```bash
cd crawler
source venv/bin/activate

# Test with 10 anime first
python test_scraper.py

# If successful, run full scrape
python bahamut_scraper.py        # ~1-2 hours
python cross_platform.py         # ~2-3 hours
python generate_json.py          # ~1 minute

# Validate
python validate_data.py

# Copy to frontend
cp data/animes.json ../app/data/animes.json
```

#### Bi-weekly Updates

```bash
cd crawler
source venv/bin/activate

# Only fetch new anime
python update_latest.py

# Copy to frontend
cp data/animes.json ../app/data/animes.json

# Commit and push
cd ..
git add data/animes.json app/data/animes.json
git commit -m "chore: update anime data"
git push
```

### Debugging Common Issues

#### "Cannot find module @/..."

- Check tsconfig.json has correct paths configuration
- Ensure you're importing from app directory
- Restart TypeScript server in IDE

#### Filters not updating UI

- Check that state is properly lifted to page.tsx
- Verify useMemo dependencies include all relevant state
- Add console.logs to track state changes

#### Composite score seems wrong

- Verify Bahamut rating is multiplied by 2
- Check that weight total equals 100%
- Ensure only available ratings are included in calculation
- Log the calculation step-by-step

#### Scraper getting blocked

- Increase sleep duration between requests
- Add more User-Agent rotation
- Check if IP is rate-limited (try from different network)
- Use proxies as last resort

---

## Testing Strategy

### Frontend Testing

#### Manual Testing Checklist

Before committing frontend changes:

- [ ] All filters work and update results immediately
- [ ] Search clears other filters as expected
- [ ] All sort options produce correct order
- [ ] Missing ratings are hidden (not shown as "N/A")
- [ ] Composite score uses custom weights
- [ ] Weight validation works (must equal 100%)
- [ ] "Watch" buttons open correct Bahamut URLs
- [ ] Responsive on mobile (test with DevTools)
- [ ] No console errors or warnings
- [ ] TypeScript compilation succeeds (`npm run build`)

#### Performance Testing

```bash
# Test production build performance
npm run build
npm run start

# Check bundle size
npm run build -- --analyze  # If analyzer is configured
```

Targets:
- Initial load: <2 seconds
- Filter/sort response: <1 second
- Total page weight: <5MB

### Data Pipeline Testing

#### Test with Small Dataset First

**Always** test scraper with 10-20 anime before full scrape:

```python
# In test_scraper.py
ANIME_LIST = anime_urls[:10]  # Only test 10 anime

for url in ANIME_LIST:
    anime = scrape_anime_detail(url)
    print(f"✓ {anime['title']}")
    # Verify all fields are present
```

#### Validation After Scraping

```python
# Run validation script
python validate_data.py

# Expected output:
# Total anime: 1523
# Missing title: 0
# Missing Japanese title: 78 (5.1%)
# IMDb coverage: 72.3%
# Douban coverage: 54.1%
# MAL coverage: 75.8%
# ✓ All checks passed
```

---

## Deployment

### Build for Production

```bash
cd app
npm run build
npm run start  # Test production build locally
```

### Deployment Options

#### Option A: Vercel (Recommended)

```bash
npm install -g vercel
vercel login
vercel  # Deploy to preview
vercel --prod  # Deploy to production
```

#### Option B: Netlify

```bash
npm install -g netlify-cli
netlify login
netlify deploy
netlify deploy --prod
```

#### Option C: Static Export (GitHub Pages)

```typescript
// next.config.ts
export default {
  output: 'export',
};
```

```bash
npm run build
# Deploy 'out' directory to GitHub Pages
```

### Environment Variables

If needed, create `.env.local`:

```
NEXT_PUBLIC_SITE_URL=https://ani-radar.example.com
```

### Automated Data Updates

Set up GitHub Actions to run `update_latest.py` bi-weekly:

See `.github/workflows/update-data.yml` in ROADMAP.md Phase 9.

---

## Critical Information

### DO NOT Modify

- `tsconfig.json` paths configuration
- `tailwind.config.ts` content paths
- `next.config.ts` (unless necessary)
- Git branch naming format

### ALWAYS Consider

1. **Rate Limiting**: Never scrape without delays
2. **Error Handling**: Always continue on error, never crash
3. **Type Safety**: Always define TypeScript types
4. **Missing Ratings**: Handle gracefully (don't show "N/A", hide instead)
5. **Search Behavior**: Must clear other filters when searching
6. **Composite Score**: Must normalize Bahamut (×2) and only use available ratings
7. **Japanese Title**: CRITICAL for cross-platform matching - must be extracted
8. **Data Validation**: Always validate before committing data files

### Performance Considerations

- Use `useMemo` for expensive filtering/sorting operations
- Use `React.memo` for frequently re-rendering components
- Keep anime card images optimized (<100KB each)
- Consider virtual scrolling if dataset grows >2000 anime

### Accessibility

- Use semantic HTML elements
- Add ARIA labels to interactive elements
- Ensure keyboard navigation works
- Test with screen reader (basic level)
- Maintain 4.5:1 color contrast ratio

### Browser Support

Target modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile Safari 14+
- Chrome Android 90+

---

## Getting Help

### Documentation Priority

1. **This file (CLAUDE.md)** - Development conventions and workflows
2. **ROADMAP.md** - Detailed implementation plan with code examples
3. **PRD.md** - Product requirements and business logic (Chinese)
4. **README.md** - User-facing documentation

### When Stuck

1. Check the relevant section in this file
2. Look at ROADMAP.md for implementation examples
3. Check PRD.md for business logic clarification
4. Review existing code for patterns
5. Search for similar patterns in the codebase

### Common Gotchas

- **Search must clear other filters** - This is a requirement, not a bug
- **Missing ratings go to the end** - When sorting by a platform
- **Weights must equal 100%** - Validate before applying
- **Japanese title is the key** - For cross-platform matching
- **Bahamut ratings are 1-5** - Must multiply by 2 for composite score
- **Client components need 'use client'** - Server components are default

---

## Update History

- **2025-12-02**: Phase 1.5 update: Critical data remediation required.
- **2025-12-02**: Initial CLAUDE.md created (Phase 0 complete)

---

**Remember**: This is a personal project focused on functionality over perfection. Aim for 70% cross-platform coverage, not 100%. Keep it simple, maintainable, and focused on the core use case: finding good anime to watch on Bahamut.
