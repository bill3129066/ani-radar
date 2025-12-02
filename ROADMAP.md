# Ani-Radar - Phased Implementation Roadmap

This roadmap provides a detailed, phase-by-phase implementation plan for building the Ani-Radar project. Each phase is designed to be completed independently and includes specific deliverables and acceptance criteria.

**For AI Agents**: Each phase can be executed sequentially. Complete all tasks in one phase before moving to the next. Verify acceptance criteria before proceeding.

---

## Phase 0: Project Setup & Dependencies

**Goal**: Set up the development environment and install all required dependencies.

### Tasks

#### 0.1 Initialize Next.js Application
```bash
cd app
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
```

**Configuration**:
- TypeScript: Yes
- Tailwind CSS: Yes
- App Router: Yes
- No src directory
- Import alias: `@/*`

#### 0.2 Install Frontend Dependencies
```bash
npm install @radix-ui/react-select @radix-ui/react-slider @radix-ui/react-checkbox
npm install lucide-react class-variance-authority clsx tailwind-merge
npm install -D @types/node
```

#### 0.3 Setup Python Environment
```bash
cd crawler
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Create `crawler/requirements.txt`:
```
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
```

Install dependencies:
```bash
pip install -r requirements.txt
```

#### 0.4 Create Base Configuration Files

**app/tsconfig.json** - Verify paths configuration:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

**app/tailwind.config.ts** - Verify content paths include all component directories

### Acceptance Criteria
- [ ] Next.js app runs successfully (`npm run dev`)
- [ ] Python virtual environment activates without errors
- [ ] All dependencies installed without conflicts
- [ ] TypeScript compilation works

---

## Phase 1: Data Collection Foundation (Bahamut Scraper)

**Goal**: Build a reliable scraper for Bahamut Anime Crazy that collects all required anime data.

### Tasks

#### 1.1 Create Bahamut Scraper Core

**File**: `crawler/bahamut_scraper.py`

**Key Functions**:
```python
def get_anime_list_page(page_num: int) -> str:
    """Fetch anime list page HTML"""
    # Add rate limiting (2-3 seconds)
    # Rotate User-Agent

def parse_anime_links(html: str) -> List[str]:
    """Extract anime detail page URLs"""

def scrape_anime_detail(url: str) -> Dict:
    """Scrape individual anime page"""
    # Extract: title, titleOriginal (Japanese), thumbnail,
    #          year, genres, episodes, bahamutUrl,
    #          ratings (Bahamut score + votes), popularity

def main():
    """Orchestrate full scraping process"""
    # Start with first 10 anime for testing
    # Save to data/bahamut_raw.json
```

**Requirements**:
- Rate limiting: `time.sleep(random.uniform(2, 4))` between requests
- User-Agent rotation (prepare 5-10 agents)
- Error handling: log errors, continue on failure
- Save progress incrementally (every 100 anime)

#### 1.2 Test with Small Dataset

**Test Script**: `crawler/test_scraper.py`
```python
# Scrape only 10 anime
# Verify all fields are correctly extracted
# Check Japanese original title is captured
```

**Validation Checklist**:
- [ ] Chinese title extracted correctly
- [ ] Japanese original title (原文) extracted
- [ ] Thumbnail URL valid
- [ ] Year parsed as integer
- [ ] Genres array populated
- [ ] Episode count correct
- [ ] Bahamut rating (1-5 scale) + vote count
- [ ] Popularity (view count) captured
- [ ] Bahamut URL correct

#### 1.3 Full Bahamut Scrape

Run scraper for all anime (~1800 entries):
```bash
python bahamut_scraper.py
```

**Output**: `data/bahamut_raw.json`

**Estimated Time**: 1-2 hours

#### 1.4 Data Quality Validation

**File**: `crawler/validate_data.py`

```python
def validate_bahamut_data(json_path: str):
    """
    Check:
    - Total count >= 1500
    - No missing required fields (title, year, etc.)
    - All ratings are valid numbers
    - All URLs accessible (sample check)
    - Japanese original title coverage >= 90%
    """
```

### Deliverables
- `crawler/bahamut_scraper.py` - Working scraper
- `crawler/test_scraper.py` - Test suite
- `crawler/validate_data.py` - Data validator
- `data/bahamut_raw.json` - Raw Bahamut data (~1800 entries)

### Acceptance Criteria
- [ ] 1500+ anime entries collected
- [ ] Japanese original title field present in 90%+ entries
- [ ] All required fields populated
- [ ] No crashes during scraping
- [ ] Data validation passes all checks

---

## Phase 2: Cross-Platform Rating Alignment

**Goal**: Integrate ratings from IMDb, Douban, and MyAnimeList using the Japanese original title as a bridge.

### Tasks

#### 2.1 MyAnimeList Integration

**File**: `crawler/mal_api.py`

**Key Functions**:
```python
def search_mal_by_japanese_title(japanese_title: str, year: int) -> Optional[Dict]:
    """
    Search MAL using Jikan API (free MAL API)
    URL: https://api.jikan.moe/v4/anime?q={title}&start_date={year}
    Rate limit: 1 request per second

    Returns: {
        'mal_id': int,
        'mal_score': float,
        'mal_members': int,
        'imdb_id': str  # From external links if available
    }
    """

def get_mal_anime_details(mal_id: int) -> Dict:
    """Fetch detailed MAL data including external links"""

def extract_imdb_id_from_mal(mal_data: Dict) -> Optional[str]:
    """Extract IMDb ID from MAL external links"""
```

**Rate Limiting**: `time.sleep(1.5)` between requests

#### 2.2 IMDb Integration

**File**: `crawler/imdb_api.py`

**Option A: OMDb API** (requires free API key)
```python
def get_imdb_rating(imdb_id: str) -> Optional[Dict]:
    """
    Fetch from OMDb: http://www.omdbapi.com/?i={imdb_id}

    Returns: {
        'imdb_score': float,
        'imdb_votes': int
    }
    """
```

**Option B: Web Scraping** (fallback)
```python
def scrape_imdb_page(imdb_id: str) -> Optional[Dict]:
    """Direct scrape from IMDb page (careful with rate limits)"""
```

#### 2.3 Douban Integration

**File**: `crawler/douban_api.py`

**Approach**: Chinese title + year search

```python
def search_douban(chinese_title: str, year: int) -> Optional[Dict]:
    """
    Search Douban by Chinese title + year
    Very strict anti-scraping - use with caution

    Rate limit: 5 seconds between requests
    Consider: 50% coverage is acceptable

    Returns: {
        'douban_id': str,
        'douban_score': float,
        'douban_votes': int
    }
    """
```

**Note**: Douban is the most difficult. If coverage <50%, consider manual mapping for top 100 anime.

#### 2.4 Cross-Platform Orchestrator

**File**: `crawler/cross_platform.py`

```python
def enrich_anime_with_ratings(anime: Dict) -> Dict:
    """
    Pipeline:
    1. Use Japanese title → Search MAL
    2. Get MAL rating + IMDb ID
    3. Use IMDb ID → Get IMDb rating
    4. Use Chinese title + year → Search Douban
    5. Merge all ratings into anime object

    Return anime with populated ratings dict
    """

def process_all_anime(input_json: str, output_json: str):
    """
    Load bahamut_raw.json
    For each anime: enrich_anime_with_ratings()
    Save to data/animes_enriched.json

    Progress: Print every 50 anime
    Error handling: Continue on failure, log errors
    """
```

**Test First**: Run on 10 anime to verify pipeline

#### 2.5 Manual Mapping (Optional)

**File**: `crawler/manual_mapping.json`

For anime where automatic matching fails, provide manual ID mapping:
```json
{
  "bahamut_id_123": {
    "mal_id": "39535",
    "imdb_id": "tt13146488",
    "douban_id": "34895145"
  }
}
```

Create helper script to apply manual mappings:
```python
def apply_manual_mappings(anime_data: List[Dict], mappings: Dict) -> List[Dict]:
    """Override automatic matches with manual mappings"""
```

#### 2.6 Generate Final Dataset

**File**: `crawler/generate_json.py`

```python
def generate_final_json():
    """
    1. Load data/animes_enriched.json
    2. Apply manual mappings (if any)
    3. Validate data structure
    4. Transform to final schema (see PRD section 2)
    5. Save to data/animes.json
    """
```

**Final Schema Validation**:
- [ ] All anime have required fields
- [ ] Ratings normalized to correct scales (Bahamut 1-5, others 0-10)
- [ ] Missing ratings set to `null`, not omitted

### Deliverables
- `crawler/mal_api.py` - MAL integration
- `crawler/imdb_api.py` - IMDb integration
- `crawler/douban_api.py` - Douban integration
- `crawler/cross_platform.py` - Orchestrator
- `crawler/generate_json.py` - Final data generator
- `crawler/manual_mapping.json` - Manual overrides (if needed)
- `data/animes.json` - Final dataset

### Acceptance Criteria
- [ ] MAL coverage >= 70%
- [ ] IMDb coverage >= 70%
- [ ] Douban coverage >= 50% (acceptable)
- [ ] Final dataset: 1500+ anime entries
- [ ] Data structure matches PRD schema
- [ ] Validation script passes

---

## Phase 3: Frontend Foundation (Next.js Core)

**Goal**: Build the basic Next.js application structure with static data loading.

### Tasks

#### 3.1 Create Type Definitions

**File**: `app/types/anime.ts`

```typescript
export interface AnimeRating {
  score: number;
  votes?: number;
  members?: number;
}

export interface Anime {
  id: string;
  title: string;
  titleOriginal?: string;
  thumbnail: string;
  year: number;
  genres: string[];
  episodes: number;
  bahamutUrl: string;
  popularity: number;
  tags?: string[];
  ratings: {
    bahamut: AnimeRating;
    imdb?: AnimeRating;
    douban?: AnimeRating;
    myanimelist?: AnimeRating;
  };
}

export type SortOption =
  | 'bahamut'
  | 'imdb'
  | 'douban'
  | 'myanimelist'
  | 'composite';

export interface FilterState {
  genres: string[];
  yearStart?: number;
  yearEnd?: number;
  minVotes: number;
  searchQuery: string;
}

export interface WeightConfig {
  bahamut: number;
  imdb: number;
  douban: number;
  myanimelist: number;
}
```

#### 3.2 Create Data Loader

**File**: `app/lib/data-loader.ts`

```typescript
import animeData from '@/data/animes.json';
import { Anime } from '@/types/anime';

export function loadAnimeData(): Anime[] {
  return animeData as Anime[];
}

export function getAllGenres(animes: Anime[]): string[] {
  const genreSet = new Set<string>();
  animes.forEach(anime => {
    anime.genres.forEach(genre => genreSet.add(genre));
  });
  return Array.from(genreSet).sort();
}

export function getYearRange(animes: Anime[]): [number, number] {
  const years = animes.map(a => a.year);
  return [Math.min(...years), Math.max(...years)];
}
```

#### 3.3 Create Utility Functions

**File**: `app/lib/utils.ts`

```typescript
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function normalizeRating(rating: number, scale: '1-5' | '0-10'): number {
  if (scale === '1-5') {
    return rating * 2; // Convert to 0-10
  }
  return rating;
}

export function formatNumber(num: number): string {
  if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`;
  }
  return num.toString();
}
```

#### 3.4 Create Basic Layout

**File**: `app/layout.tsx`

```typescript
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Ani-Radar - Anime Rating Dashboard",
  description: "Discover the best anime with multi-platform ratings",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-TW">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

#### 3.5 Create Basic Home Page (Testing)

**File**: `app/page.tsx`

```typescript
import { loadAnimeData } from '@/lib/data-loader';

export default function Home() {
  const animes = loadAnimeData();

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Ani-Radar</h1>
      <p>Total anime: {animes.length}</p>

      {/* Display first 10 anime as test */}
      <div className="grid gap-4 mt-8">
        {animes.slice(0, 10).map(anime => (
          <div key={anime.id} className="border p-4 rounded">
            <h2>{anime.title}</h2>
            <p>Year: {anime.year}</p>
            <p>Bahamut: {anime.ratings.bahamut.score}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
```

#### 3.6 Configure Static Data Import

Copy `data/animes.json` to `app/data/animes.json` or adjust import path.

### Deliverables
- `app/types/anime.ts` - Type definitions
- `app/lib/data-loader.ts` - Data loading functions
- `app/lib/utils.ts` - Utility functions
- `app/layout.tsx` - Root layout
- `app/page.tsx` - Basic home page
- Working Next.js app displaying anime data

### Acceptance Criteria
- [ ] Next.js dev server runs without errors
- [ ] Anime data loads successfully
- [ ] TypeScript types compile without errors
- [ ] Basic page displays anime count and sample data
- [ ] No console errors in browser

---

## Phase 4: Core UI Components

**Goal**: Build reusable UI components for the anime dashboard.

### Tasks

#### 4.1 Install shadcn/ui Components

```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add card button input select slider checkbox
```

#### 4.2 Create Anime Card Component

**File**: `app/components/anime-card.tsx`

```typescript
import { Anime } from '@/types/anime';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { formatNumber } from '@/lib/utils';

interface AnimeCardProps {
  anime: Anime;
}

export function AnimeCard({ anime }: AnimeCardProps) {
  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow">
      <img
        src={anime.thumbnail}
        alt={anime.title}
        className="w-full h-48 object-cover"
      />
      <CardContent className="p-4">
        <h3 className="font-bold text-lg mb-2 line-clamp-2">
          {anime.title}
        </h3>

        <div className="text-sm text-gray-600 mb-3">
          {anime.year} · {anime.genres.join(', ')} · {anime.episodes}集
        </div>

        {/* Ratings Display */}
        <div className="space-y-1 mb-4 text-sm">
          <div className="flex items-center gap-2">
            <span>⭐</span>
            <span className="font-semibold">{anime.ratings.bahamut.score.toFixed(1)}</span>
            <span className="text-gray-500">({formatNumber(anime.ratings.bahamut.votes)})</span>
          </div>

          {anime.ratings.imdb && (
            <div className="flex items-center gap-2">
              <span>🎬</span>
              <span className="font-semibold">{anime.ratings.imdb.score.toFixed(1)}</span>
              <span className="text-gray-500">({formatNumber(anime.ratings.imdb.votes!)})</span>
            </div>
          )}

          {anime.ratings.douban && (
            <div className="flex items-center gap-2">
              <span>🎭</span>
              <span className="font-semibold">{anime.ratings.douban.score.toFixed(1)}</span>
              <span className="text-gray-500">({formatNumber(anime.ratings.douban.votes!)})</span>
            </div>
          )}

          {anime.ratings.myanimelist && (
            <div className="flex items-center gap-2">
              <span>📺</span>
              <span className="font-semibold">{anime.ratings.myanimelist.score.toFixed(1)}</span>
              <span className="text-gray-500">({formatNumber(anime.ratings.myanimelist.members!)})</span>
            </div>
          )}
        </div>

        <Button
          className="w-full"
          onClick={() => window.open(anime.bahamutUrl, '_blank')}
        >
          觀看
        </Button>
      </CardContent>
    </Card>
  );
}
```

#### 4.3 Create Anime Grid Component

**File**: `app/components/anime-grid.tsx`

```typescript
import { Anime } from '@/types/anime';
import { AnimeCard } from './anime-card';

interface AnimeGridProps {
  animes: Anime[];
}

export function AnimeGrid({ animes }: AnimeGridProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {animes.map(anime => (
        <AnimeCard key={anime.id} anime={anime} />
      ))}
    </div>
  );
}
```

#### 4.4 Create Search Input Component

**File**: `app/components/search-input.tsx`

```typescript
'use client';

import { Input } from '@/components/ui/input';
import { Search } from 'lucide-react';

interface SearchInputProps {
  value: string;
  onChange: (value: string) => void;
}

export function SearchInput({ value, onChange }: SearchInputProps) {
  return (
    <div className="relative">
      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
      <Input
        type="text"
        placeholder="搜尋動畫標題..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="pl-10"
      />
    </div>
  );
}
```

#### 4.5 Create Genre Filter Component

**File**: `app/components/genre-filter.tsx`

```typescript
'use client';

import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';

interface GenreFilterProps {
  genres: string[];
  selectedGenres: string[];
  onChange: (genres: string[]) => void;
}

export function GenreFilter({ genres, selectedGenres, onChange }: GenreFilterProps) {
  const handleToggle = (genre: string) => {
    if (selectedGenres.includes(genre)) {
      onChange(selectedGenres.filter(g => g !== genre));
    } else {
      onChange([...selectedGenres, genre]);
    }
  };

  return (
    <div className="space-y-2">
      <h3 className="font-semibold mb-3">類型</h3>
      {genres.map(genre => (
        <div key={genre} className="flex items-center space-x-2">
          <Checkbox
            id={`genre-${genre}`}
            checked={selectedGenres.includes(genre)}
            onCheckedChange={() => handleToggle(genre)}
          />
          <Label
            htmlFor={`genre-${genre}`}
            className="cursor-pointer text-sm"
          >
            {genre}
          </Label>
        </div>
      ))}
    </div>
  );
}
```

#### 4.6 Create Year Filter Component

**File**: `app/components/year-filter.tsx`

```typescript
'use client';

import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface YearFilterProps {
  yearStart?: number;
  yearEnd?: number;
  minYear: number;
  maxYear: number;
  onChange: (start?: number, end?: number) => void;
}

export function YearFilter({
  yearStart,
  yearEnd,
  minYear,
  maxYear,
  onChange
}: YearFilterProps) {
  return (
    <div className="space-y-3">
      <h3 className="font-semibold">年份</h3>

      <div className="flex gap-2 items-center">
        <div className="flex-1">
          <Label htmlFor="year-start" className="text-xs">從</Label>
          <Input
            id="year-start"
            type="number"
            min={minYear}
            max={maxYear}
            value={yearStart || ''}
            onChange={(e) => onChange(
              e.target.value ? parseInt(e.target.value) : undefined,
              yearEnd
            )}
            placeholder={minYear.toString()}
          />
        </div>

        <span className="text-gray-500 mt-5">-</span>

        <div className="flex-1">
          <Label htmlFor="year-end" className="text-xs">到</Label>
          <Input
            id="year-end"
            type="number"
            min={minYear}
            max={maxYear}
            value={yearEnd || ''}
            onChange={(e) => onChange(
              yearStart,
              e.target.value ? parseInt(e.target.value) : undefined
            )}
            placeholder={maxYear.toString()}
          />
        </div>
      </div>
    </div>
  );
}
```

#### 4.7 Create Sort Selector Component

**File**: `app/components/sort-selector.tsx`

```typescript
'use client';

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { SortOption } from '@/types/anime';

interface SortSelectorProps {
  value: SortOption;
  onChange: (value: SortOption) => void;
}

export function SortSelector({ value, onChange }: SortSelectorProps) {
  return (
    <div className="space-y-2">
      <h3 className="font-semibold">排序方式</h3>
      <Select value={value} onValueChange={onChange}>
        <SelectTrigger>
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="bahamut">巴哈評分最高</SelectItem>
          <SelectItem value="imdb">IMDb 評分最高</SelectItem>
          <SelectItem value="douban">豆瓣評分最高</SelectItem>
          <SelectItem value="myanimelist">MyAnimeList 評分最高</SelectItem>
          <SelectItem value="composite">綜合評分最高</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
}
```

### Deliverables
- All UI components listed above
- shadcn/ui properly configured
- Components properly typed with TypeScript

### Acceptance Criteria
- [ ] All components render without errors
- [ ] AnimeCard displays all rating platforms correctly
- [ ] Missing ratings are hidden (not shown as "N/A")
- [ ] Components are responsive (mobile/tablet/desktop)
- [ ] TypeScript compilation succeeds

---

## Phase 5: Filtering & Sorting Logic

**Goal**: Implement the core filtering, sorting, and searching logic.

### Tasks

#### 5.1 Create Filter Logic

**File**: `app/lib/filters.ts`

```typescript
import { Anime, FilterState } from '@/types/anime';

export function filterAnimes(animes: Anime[], filters: FilterState): Anime[] {
  let filtered = animes;

  // Search query - clears other filters
  if (filters.searchQuery.trim()) {
    const query = filters.searchQuery.toLowerCase();
    return animes.filter(anime =>
      anime.title.toLowerCase().includes(query) ||
      anime.titleOriginal?.toLowerCase().includes(query)
    );
  }

  // Genre filter (OR logic)
  if (filters.genres.length > 0) {
    filtered = filtered.filter(anime =>
      anime.genres.some(genre => filters.genres.includes(genre))
    );
  }

  // Year range filter
  if (filters.yearStart) {
    filtered = filtered.filter(anime => anime.year >= filters.yearStart!);
  }
  if (filters.yearEnd) {
    filtered = filtered.filter(anime => anime.year <= filters.yearEnd!);
  }

  // Minimum votes filter
  if (filters.minVotes > 0) {
    filtered = filtered.filter(anime =>
      anime.ratings.bahamut.votes >= filters.minVotes
    );
  }

  return filtered;
}
```

#### 5.2 Create Sort Logic

**File**: `app/lib/sorting.ts`

```typescript
import { Anime, SortOption, WeightConfig } from '@/types/anime';
import { normalizeRating } from './utils';

export function sortAnimes(
  animes: Anime[],
  sortBy: SortOption,
  weights?: WeightConfig
): Anime[] {
  const sorted = [...animes];

  switch (sortBy) {
    case 'bahamut':
      return sorted.sort((a, b) => {
        const scoreA = a.ratings.bahamut.score;
        const scoreB = b.ratings.bahamut.score;
        return scoreB - scoreA;
      });

    case 'imdb':
      return sorted.sort((a, b) => {
        const scoreA = a.ratings.imdb?.score ?? -1;
        const scoreB = b.ratings.imdb?.score ?? -1;

        if (scoreA === -1 && scoreB === -1) {
          return b.ratings.bahamut.score - a.ratings.bahamut.score;
        }
        if (scoreA === -1) return 1;
        if (scoreB === -1) return -1;

        if (scoreB !== scoreA) {
          return scoreB - scoreA;
        }
        // Secondary sort by Bahamut
        return b.ratings.bahamut.score - a.ratings.bahamut.score;
      });

    case 'douban':
      return sorted.sort((a, b) => {
        const scoreA = a.ratings.douban?.score ?? -1;
        const scoreB = b.ratings.douban?.score ?? -1;

        if (scoreA === -1 && scoreB === -1) {
          return b.ratings.bahamut.score - a.ratings.bahamut.score;
        }
        if (scoreA === -1) return 1;
        if (scoreB === -1) return -1;

        if (scoreB !== scoreA) {
          return scoreB - scoreA;
        }
        return b.ratings.bahamut.score - a.ratings.bahamut.score;
      });

    case 'myanimelist':
      return sorted.sort((a, b) => {
        const scoreA = a.ratings.myanimelist?.score ?? -1;
        const scoreB = b.ratings.myanimelist?.score ?? -1;

        if (scoreA === -1 && scoreB === -1) {
          return b.ratings.bahamut.score - a.ratings.bahamut.score;
        }
        if (scoreA === -1) return 1;
        if (scoreB === -1) return -1;

        if (scoreB !== scoreA) {
          return scoreB - scoreA;
        }
        return b.ratings.bahamut.score - a.ratings.bahamut.score;
      });

    case 'composite':
      if (!weights) {
        weights = { bahamut: 25, imdb: 25, douban: 25, myanimelist: 25 };
      }
      return sorted.sort((a, b) => {
        const scoreA = calculateCompositeScore(a, weights!);
        const scoreB = calculateCompositeScore(b, weights!);
        return scoreB - scoreA;
      });

    default:
      return sorted;
  }
}

function calculateCompositeScore(anime: Anime, weights: WeightConfig): number {
  let totalScore = 0;
  let totalWeight = 0;

  // Bahamut (normalize 1-5 to 0-10)
  const bahamutNormalized = normalizeRating(anime.ratings.bahamut.score, '1-5');
  totalScore += bahamutNormalized * (weights.bahamut / 100);
  totalWeight += weights.bahamut / 100;

  // IMDb
  if (anime.ratings.imdb) {
    totalScore += anime.ratings.imdb.score * (weights.imdb / 100);
    totalWeight += weights.imdb / 100;
  }

  // Douban
  if (anime.ratings.douban) {
    totalScore += anime.ratings.douban.score * (weights.douban / 100);
    totalWeight += weights.douban / 100;
  }

  // MyAnimeList
  if (anime.ratings.myanimelist) {
    totalScore += anime.ratings.myanimelist.score * (weights.myanimelist / 100);
    totalWeight += weights.myanimelist / 100;
  }

  return totalWeight > 0 ? totalScore / totalWeight : 0;
}

export { calculateCompositeScore };
```

#### 5.3 Create Tests for Filter/Sort Logic

**File**: `app/lib/__tests__/filters.test.ts`

Create basic tests to verify:
- Genre filtering (OR logic)
- Year range filtering
- Search clears other filters
- Minimum votes filtering

**File**: `app/lib/__tests__/sorting.test.ts`

Test:
- Each sort option
- Missing rating handling (sorted last)
- Secondary Bahamut sort
- Composite score calculation

### Deliverables
- `app/lib/filters.ts` - Filtering logic
- `app/lib/sorting.ts` - Sorting logic
- Test files (optional but recommended)

### Acceptance Criteria
- [ ] Genre filter works with OR logic
- [ ] Search query clears other filters
- [ ] Year range filter works correctly
- [ ] Sort options place missing ratings last
- [ ] Composite score calculation matches PRD formula
- [ ] All tests pass (if implemented)

---

## Phase 6: Main Dashboard Integration

**Goal**: Integrate all components and logic into a fully functional dashboard.

### Tasks

#### 6.1 Create Filter Sidebar Component

**File**: `app/components/filter-sidebar.tsx`

```typescript
'use client';

import { FilterState, SortOption } from '@/types/anime';
import { SearchInput } from './search-input';
import { GenreFilter } from './genre-filter';
import { YearFilter } from './year-filter';
import { SortSelector } from './sort-selector';
import { Slider } from '@/components/ui/slider';
import { Label } from '@/components/ui/label';

interface FilterSidebarProps {
  filters: FilterState;
  sortBy: SortOption;
  genres: string[];
  yearRange: [number, number];
  onFiltersChange: (filters: FilterState) => void;
  onSortChange: (sort: SortOption) => void;
}

export function FilterSidebar({
  filters,
  sortBy,
  genres,
  yearRange,
  onFiltersChange,
  onSortChange,
}: FilterSidebarProps) {
  return (
    <aside className="w-64 p-6 border-r bg-gray-50 h-screen overflow-y-auto sticky top-0">
      <h2 className="text-2xl font-bold mb-6">篩選</h2>

      {/* Search */}
      <div className="mb-6">
        <SearchInput
          value={filters.searchQuery}
          onChange={(value) =>
            onFiltersChange({ ...filters, searchQuery: value })
          }
        />
      </div>

      {/* Genre Filter */}
      <div className="mb-6">
        <GenreFilter
          genres={genres}
          selectedGenres={filters.genres}
          onChange={(genres) =>
            onFiltersChange({ ...filters, genres })
          }
        />
      </div>

      {/* Year Filter */}
      <div className="mb-6">
        <YearFilter
          yearStart={filters.yearStart}
          yearEnd={filters.yearEnd}
          minYear={yearRange[0]}
          maxYear={yearRange[1]}
          onChange={(start, end) =>
            onFiltersChange({
              ...filters,
              yearStart: start,
              yearEnd: end,
            })
          }
        />
      </div>

      {/* Min Votes Slider */}
      <div className="mb-6">
        <Label className="font-semibold mb-2 block">
          最低評分人數: {filters.minVotes}
        </Label>
        <Slider
          value={[filters.minVotes]}
          onValueChange={([value]) =>
            onFiltersChange({ ...filters, minVotes: value })
          }
          min={0}
          max={500}
          step={10}
        />
      </div>

      {/* Sort Selector */}
      <div className="mb-6">
        <SortSelector value={sortBy} onChange={onSortChange} />
      </div>
    </aside>
  );
}
```

#### 6.2 Update Main Page with State Management

**File**: `app/page.tsx`

```typescript
'use client';

import { useState, useMemo } from 'react';
import { loadAnimeData, getAllGenres, getYearRange } from '@/lib/data-loader';
import { filterAnimes } from '@/lib/filters';
import { sortAnimes } from '@/lib/sorting';
import { FilterSidebar } from '@/components/filter-sidebar';
import { AnimeGrid } from '@/components/anime-grid';
import { FilterState, SortOption } from '@/types/anime';

export default function Home() {
  const animes = loadAnimeData();
  const genres = getAllGenres(animes);
  const yearRange = getYearRange(animes);

  const [filters, setFilters] = useState<FilterState>({
    genres: [],
    searchQuery: '',
    minVotes: 0,
  });

  const [sortBy, setSortBy] = useState<SortOption>('bahamut');

  // Apply filters and sorting
  const displayedAnimes = useMemo(() => {
    const filtered = filterAnimes(animes, filters);
    return sortAnimes(filtered, sortBy);
  }, [animes, filters, sortBy]);

  return (
    <div className="flex min-h-screen">
      <FilterSidebar
        filters={filters}
        sortBy={sortBy}
        genres={genres}
        yearRange={yearRange}
        onFiltersChange={setFilters}
        onSortChange={setSortBy}
      />

      <main className="flex-1 p-8">
        <div className="mb-6">
          <h1 className="text-4xl font-bold mb-2">Ani-Radar</h1>
          <p className="text-gray-600">
            找到 {displayedAnimes.length} 部動畫
          </p>
        </div>

        <AnimeGrid animes={displayedAnimes} />
      </main>
    </div>
  );
}
```

#### 6.3 Test Full Dashboard Functionality

Manual testing checklist:
- [ ] Genre filter updates results immediately
- [ ] Search clears other filters
- [ ] Year range filter works
- [ ] Min votes slider updates results
- [ ] All sort options work correctly
- [ ] Result count displays correctly
- [ ] Anime cards display all information
- [ ] "觀看" button opens Bahamut URL in new tab
- [ ] Responsive on mobile/tablet/desktop

### Deliverables
- `app/components/filter-sidebar.tsx` - Complete sidebar
- `app/page.tsx` - Fully functional dashboard
- Working application with all features

### Acceptance Criteria
- [ ] All filters work correctly and update in real-time
- [ ] Search behavior matches PRD (clears other filters)
- [ ] Sorting works for all options
- [ ] UI is responsive across device sizes
- [ ] No console errors
- [ ] Performance is acceptable (<1s for filtering)

---

## Phase 7: Composite Score Customization

**Goal**: Allow users to customize rating weights for composite scoring.

### Tasks

#### 7.1 Create Weight Configuration Component

**File**: `app/components/weight-config.tsx`

```typescript
'use client';

import { useState } from 'react';
import { WeightConfig } from '@/types/anime';
import { Slider } from '@/components/ui/slider';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { ChevronDown } from 'lucide-react';

interface WeightConfigProps {
  weights: WeightConfig;
  onChange: (weights: WeightConfig) => void;
}

const DEFAULT_WEIGHTS: WeightConfig = {
  bahamut: 25,
  imdb: 25,
  douban: 25,
  myanimelist: 25,
};

export function WeightConfigPanel({ weights, onChange }: WeightConfigProps) {
  const [isOpen, setIsOpen] = useState(false);

  const total = weights.bahamut + weights.imdb + weights.douban + weights.myanimelist;
  const isValid = total === 100;

  const handleReset = () => {
    onChange(DEFAULT_WEIGHTS);
  };

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen}>
      <CollapsibleTrigger className="flex items-center justify-between w-full">
        <span className="font-semibold">綜合評分設定</span>
        <ChevronDown
          className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
        />
      </CollapsibleTrigger>

      <CollapsibleContent className="mt-4 space-y-4">
        {/* Bahamut Weight */}
        <div>
          <Label className="text-sm">巴哈姆特: {weights.bahamut}%</Label>
          <Slider
            value={[weights.bahamut]}
            onValueChange={([value]) =>
              onChange({ ...weights, bahamut: value })
            }
            min={0}
            max={100}
            step={5}
          />
        </div>

        {/* IMDb Weight */}
        <div>
          <Label className="text-sm">IMDb: {weights.imdb}%</Label>
          <Slider
            value={[weights.imdb]}
            onValueChange={([value]) =>
              onChange({ ...weights, imdb: value })
            }
            min={0}
            max={100}
            step={5}
          />
        </div>

        {/* Douban Weight */}
        <div>
          <Label className="text-sm">豆瓣: {weights.douban}%</Label>
          <Slider
            value={[weights.douban]}
            onValueChange={([value]) =>
              onChange({ ...weights, douban: value })
            }
            min={0}
            max={100}
            step={5}
          />
        </div>

        {/* MyAnimeList Weight */}
        <div>
          <Label className="text-sm">MyAnimeList: {weights.myanimelist}%</Label>
          <Slider
            value={[weights.myanimelist]}
            onValueChange={([value]) =>
              onChange({ ...weights, myanimelist: value })
            }
            min={0}
            max={100}
            step={5}
          />
        </div>

        {/* Total Display */}
        <div className={`text-sm font-semibold ${isValid ? 'text-green-600' : 'text-red-600'}`}>
          總和: {total}% {isValid ? '✓' : '(需為 100%)'}
        </div>

        {/* Reset Button */}
        <Button
          variant="outline"
          size="sm"
          onClick={handleReset}
          className="w-full"
        >
          重置為預設
        </Button>
      </CollapsibleContent>
    </Collapsible>
  );
}
```

#### 7.2 Integrate Weight Config into Sidebar

Update `app/components/filter-sidebar.tsx`:

```typescript
// Add WeightConfig import and props
import { WeightConfig } from '@/types/anime';
import { WeightConfigPanel } from './weight-config';

interface FilterSidebarProps {
  // ... existing props
  weights: WeightConfig;
  onWeightsChange: (weights: WeightConfig) => void;
}

// Inside FilterSidebar component, add after Sort Selector:
<div className="mb-6">
  <WeightConfigPanel
    weights={weights}
    onChange={onWeightsChange}
  />
</div>
```

#### 7.3 Update Main Page with Weight State

Update `app/page.tsx`:

```typescript
const [weights, setWeights] = useState<WeightConfig>({
  bahamut: 25,
  imdb: 25,
  douban: 25,
  myanimelist: 25,
});

// Update sortAnimes call
const displayedAnimes = useMemo(() => {
  const filtered = filterAnimes(animes, filters);
  return sortAnimes(filtered, sortBy, weights);
}, [animes, filters, sortBy, weights]);

// Pass weights to FilterSidebar
<FilterSidebar
  // ... existing props
  weights={weights}
  onWeightsChange={setWeights}
/>
```

#### 7.4 Add Composite Score Display to Anime Card (Optional)

Update `app/components/anime-card.tsx` to show composite score when sorted by composite:

```typescript
// Add prop to indicate if composite sort is active
interface AnimeCardProps {
  anime: Anime;
  showCompositeScore?: boolean;
  compositeScore?: number;
}

// Display composite score if available
{showCompositeScore && compositeScore && (
  <div className="text-sm font-bold text-blue-600 mb-2">
    綜合評分: {compositeScore.toFixed(2)}
  </div>
)}
```

### Deliverables
- `app/components/weight-config.tsx` - Weight configuration panel
- Updated `filter-sidebar.tsx` with weight config
- Updated `page.tsx` with weight state management
- Working composite score customization

### Acceptance Criteria
- [ ] Weight sliders adjust independently
- [ ] Total weight validation (must equal 100%)
- [ ] Invalid state shows error message
- [ ] Reset button restores default weights
- [ ] Composite sort uses custom weights
- [ ] Panel collapses/expands smoothly

---

## Phase 8: Polish & Optimization

**Goal**: Improve UI/UX, add loading states, optimize performance, and handle edge cases.

### Tasks

#### 8.1 Add Loading States

**File**: `app/loading.tsx`

```typescript
export default function Loading() {
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
        <p className="text-gray-600">載入中...</p>
      </div>
    </div>
  );
}
```

#### 8.2 Add Empty States

**File**: `app/components/empty-state.tsx`

```typescript
import { Button } from '@/components/ui/button';

interface EmptyStateProps {
  message: string;
  onReset?: () => void;
}

export function EmptyState({ message, onReset }: EmptyStateProps) {
  return (
    <div className="text-center py-12">
      <p className="text-gray-600 text-lg mb-4">{message}</p>
      {onReset && (
        <Button onClick={onReset} variant="outline">
          清空篩選
        </Button>
      )}
    </div>
  );
}
```

Update `app/page.tsx` to use EmptyState:

```typescript
{displayedAnimes.length === 0 ? (
  <EmptyState
    message="找不到符合的動畫"
    onReset={() => setFilters({
      genres: [],
      searchQuery: '',
      minVotes: 0,
    })}
  />
) : (
  <AnimeGrid animes={displayedAnimes} />
)}
```

#### 8.3 Optimize Performance

**Implement virtual scrolling** (optional, for large datasets):

```bash
npm install react-window
```

Update `anime-grid.tsx` to use virtual scrolling if needed.

**Memoize expensive calculations**:
- Ensure `useMemo` is used for filtering/sorting
- Add React.memo to AnimeCard component

#### 8.4 Add Accessibility Features

- Add proper ARIA labels to interactive elements
- Ensure keyboard navigation works
- Add focus indicators
- Test with screen reader

#### 8.5 Improve Mobile Experience

- Make sidebar collapsible on mobile
- Adjust grid columns for mobile (1-2 cols)
- Ensure touch targets are 44x44px minimum
- Test on various screen sizes

**File**: `app/components/mobile-filter-drawer.tsx` (optional)

Create a drawer/modal for filters on mobile devices.

#### 8.6 Add Error Boundaries

**File**: `app/components/error-boundary.tsx`

```typescript
'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui/button';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-4">發生錯誤</h2>
        <p className="text-gray-600 mb-4">無法載入動畫資料</p>
        <Button onClick={reset}>重試</Button>
      </div>
    </div>
  );
}
```

#### 8.7 Add Metadata and SEO

Update `app/layout.tsx`:

```typescript
export const metadata: Metadata = {
  title: 'Ani-Radar - 巴哈姆特動畫瘋評分 Dashboard',
  description: '聚合巴哈姆特、IMDb、豆瓣、MyAnimeList 四大平台動畫評分，快速找到值得看的動畫',
  keywords: ['動畫', '評分', '巴哈姆特', 'IMDb', '豆瓣', 'MyAnimeList'],
};
```

#### 8.8 Add Analytics (Optional)

If deploying publicly, add Google Analytics or similar:

```bash
npm install @next/third-parties
```

#### 8.9 Final Testing Checklist

- [ ] All filters work correctly
- [ ] All sort options work correctly
- [ ] Search clears other filters as expected
- [ ] Composite score calculation is accurate
- [ ] Weight customization works
- [ ] Mobile responsive design works
- [ ] No console errors or warnings
- [ ] Performance is acceptable (<1s filter response)
- [ ] Accessibility basics covered
- [ ] Error states handled gracefully

### Deliverables
- Loading states
- Empty states
- Error boundaries
- Mobile optimizations
- Performance optimizations
- Final polished application

### Acceptance Criteria
- [ ] App loads quickly (<2s initial load)
- [ ] Filtering/sorting feels instant (<500ms)
- [ ] Mobile experience is smooth
- [ ] No JavaScript errors in console
- [ ] Passes basic accessibility audit
- [ ] All edge cases handled

---

## Phase 9: Deployment Preparation

**Goal**: Prepare the application for deployment and set up update automation.

### Tasks

#### 9.1 Build and Test Production Bundle

```bash
cd app
npm run build
npm run start
```

Verify:
- [ ] Build completes without errors
- [ ] Production bundle size is reasonable (<1MB JS)
- [ ] App works correctly in production mode
- [ ] Data loads correctly from static JSON

#### 9.2 Create Data Update Script

**File**: `crawler/update_latest.py`

```python
"""
Incremental update script:
1. Fetch latest anime from Bahamut (last 2 weeks)
2. Enrich with cross-platform ratings
3. Merge with existing animes.json
4. Validate and save
"""

def get_latest_anime(days=14):
    """Fetch anime added in last N days"""
    pass

def update_existing_ratings(anime_id):
    """Update ratings for existing anime"""
    pass

def merge_with_existing(new_animes, existing_path):
    """Merge new data with existing JSON"""
    pass
```

#### 9.3 Create GitHub Actions Workflow (Optional)

**File**: `.github/workflows/update-data.yml`

```yaml
name: Update Anime Data

on:
  schedule:
    - cron: '0 0 */14 * *'  # Every 2 weeks
  workflow_dispatch:  # Manual trigger

jobs:
  update-data:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          cd crawler
          pip install -r requirements.txt

      - name: Run update script
        run: |
          cd crawler
          python update_latest.py

      - name: Commit and push changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/animes.json
          git diff --quiet && git diff --staged --quiet || \
            (git commit -m "Auto-update anime data $(date +'%Y-%m-%d')" && git push)
```

#### 9.4 Choose Deployment Platform

**Option A: Vercel** (Recommended for Next.js)
```bash
npm install -g vercel
vercel login
vercel
```

**Option B: Netlify**
```bash
npm install -g netlify-cli
netlify login
netlify deploy
```

**Option C: GitHub Pages** (Static export)
```bash
# Update next.config.js
output: 'export'
npm run build
```

#### 9.5 Environment Setup

Create `.env.local` if needed:
```
NEXT_PUBLIC_SITE_URL=https://your-domain.com
```

Update `.gitignore`:
```
.env*.local
node_modules/
.next/
out/
venv/
__pycache__/
*.pyc
data/bahamut_raw.json
data/animes_enriched.json
```

#### 9.6 Create Documentation

**File**: `CONTRIBUTING.md` (if open-sourcing)

**File**: `crawler/README.md`
- How to run crawler
- API keys needed (if any)
- Rate limiting guidelines
- Data validation steps

#### 9.7 Final Deployment

1. Push all code to GitHub
2. Deploy to chosen platform
3. Verify deployment works
4. Test on multiple devices
5. Set up domain (if applicable)

### Deliverables
- Production build configuration
- Update automation script
- GitHub Actions workflow (optional)
- Deployment to hosting platform
- Complete documentation

### Acceptance Criteria
- [ ] Production build succeeds
- [ ] App deployed and accessible via URL
- [ ] Data updates can be run manually
- [ ] GitHub Actions workflow configured (if using)
- [ ] Documentation is complete and clear
- [ ] Project is ready for maintenance mode

---

## Post-Launch: Maintenance Tasks

### Regular Maintenance

**Bi-weekly Data Updates**:
```bash
cd crawler
python update_latest.py
git add data/animes.json
git commit -m "Update anime data"
git push
```

**Monthly Tasks**:
- Check for broken Bahamut URLs
- Verify cross-platform API endpoints still work
- Review error logs from data collection
- Update dependencies (`npm update`, `pip list --outdated`)

**Quarterly Tasks**:
- Full re-scrape to fix any data drift
- Performance audit
- Accessibility audit
- User feedback review (if applicable)

### Future Enhancements (Out of Scope)

These features are explicitly NOT in the current roadmap but could be added later:
- User accounts and authentication
- Personal watchlist/favorites
- Rating history tracking
- Social features (sharing, comments)
- Advanced recommendation engine
- Region/language filters
- Streaming platform integration (beyond Bahamut)

---

## Success Metrics

### Data Quality
- ✅ 1500+ anime entries
- ✅ 70%+ cross-platform rating coverage
- ✅ <5% data validation errors

### Performance
- ✅ <2s initial page load
- ✅ <1s filter/sort response time
- ✅ <5MB total page weight

### Functionality
- ✅ All filters working correctly
- ✅ All sort options working correctly
- ✅ Search behavior correct (clears other filters)
- ✅ Composite score calculation accurate

### User Experience
- ✅ Intuitive UI (no instructions needed)
- ✅ Mobile responsive
- ✅ No JavaScript errors
- ✅ Graceful error handling

---

## Troubleshooting Guide

### Common Issues

**Issue: Python scraper fails with rate limiting**
- Solution: Increase `time.sleep()` duration
- Solution: Add more User-Agent rotation
- Solution: Use proxy rotation (advanced)

**Issue: Cross-platform matching rate too low**
- Solution: Verify Japanese title extraction is correct
- Solution: Add manual_mapping.json for top anime
- Solution: Try alternative APIs

**Issue: Next.js build fails**
- Solution: Check TypeScript errors (`npm run type-check`)
- Solution: Verify all imports are correct
- Solution: Check data/animes.json format

**Issue: Filters not updating UI**
- Solution: Verify state management in page.tsx
- Solution: Check useMemo dependencies
- Solution: Add console.logs to debug

**Issue: Composite score seems wrong**
- Solution: Verify normalization (Bahamut × 2)
- Solution: Check weight total === 100
- Solution: Review calculateCompositeScore logic

---

## Conclusion

This roadmap provides a complete, phase-by-phase guide for building Ani-Radar. Each phase builds upon the previous one, allowing for incremental development and testing.

**For AI Agents**: Execute phases sequentially. Complete all acceptance criteria before moving to the next phase. If you encounter issues, refer to the Troubleshooting Guide.

**For Human Developers**: Feel free to adapt phases based on your expertise and preferences. The roadmap is designed to be flexible while ensuring all critical functionality is implemented.

**Timeline Estimate**:
- Phase 0-1: 4-6 hours (Data collection)
- Phase 2: 6-8 hours (Cross-platform alignment)
- Phase 3-4: 4-6 hours (Frontend foundation)
- Phase 5-6: 4-6 hours (Logic and dashboard)
- Phase 7: 2-3 hours (Composite scoring)
- Phase 8: 3-4 hours (Polish)
- Phase 9: 2-3 hours (Deployment)

**Total: 25-36 hours of development time**

Good luck building Ani-Radar! 🎬🎭📺
