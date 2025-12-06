# Project Context

## Purpose

Ani-Radar is a personal anime rating dashboard that aggregates ratings from four major platforms:
- **Bahamut Anime Crazy (巴哈姆特動畫瘋)** - Primary data source and watch links
- **IMDb** - International movie database ratings
- **Douban (豆瓣)** - Chinese ratings platform
- **MyAnimeList (MAL)** - Dedicated anime database

Core goals:
1. Display multi-platform ratings side-by-side for easy comparison
2. Enable advanced filtering (genre, year range, minimum votes, full-text search)
3. Support custom weighted composite scoring across platforms
4. Provide direct watch links to Bahamut Anime Crazy

**Out of Scope**: Video playback, social features, user accounts, recommendations, rating history, multi-region support.

## Tech Stack

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5+ (strict mode)
- **Styling**: Tailwind CSS 4+
- **UI Components**: shadcn/ui (Radix UI + Tailwind)
- **Icons**: lucide-react
- **Utilities**: clsx, tailwind-merge, class-variance-authority

### Data Pipeline
- **Language**: Python 3.8+
- **HTTP**: requests library
- **Parsing**: BeautifulSoup4 with lxml
- **Data Format**: Static JSON files
- **Update Strategy**: Bi-weekly manual or GitHub Actions

### Development Tools
- **Package Manager**: npm
- **Linter**: ESLint (Next.js config)
- **Version Control**: Git + GitHub

## Project Conventions

### Code Style

**TypeScript/React**:
- Components: PascalCase files and exports (`anime-card.tsx` → `AnimeCard`)
- Utilities: kebab-case files, camelCase exports (`data-loader.ts` → `loadAnimeData`)
- Types: PascalCase for interfaces/types, use `interface` for objects, `type` for unions
- Import alias: Use `@/` for all app directory imports
- Avoid `any` - use `unknown` if type is truly unknown

**Python**:
- Follow PEP 8 style guide
- snake_case for functions/variables
- 4 spaces indentation
- Max line length: 100 characters

### Architecture Patterns

**Server vs Client Components**:
- Default to Server Components for performance
- Use `'use client'` only for: state, effects, event handlers, browser APIs

**Component Structure**:
1. Imports
2. Type definitions (interface)
3. Component function
4. Hooks (if client)
5. Helper functions
6. JSX return

**Data Flow**:
- Static JSON loaded at build time
- Filtering/sorting computed client-side with useMemo
- State lifted to page.tsx, passed down via props

### Testing Strategy

**Frontend**: Manual testing checklist before commits:
- All filters work and update results immediately
- Search clears other filters as expected
- Sort options produce correct order
- Missing ratings hidden (not "N/A")
- Composite score uses custom weights
- Weight validation (must equal 100%)
- Responsive on mobile
- No console errors
- TypeScript compilation succeeds

**Data Pipeline**: Always test with 10-20 anime before full scrape, then validate coverage rates.

### Git Workflow

**Commit Message Format**:
```
<type>: <description>

Types: feat, fix, docs, style, refactor, test, chore
```

**Branch Naming**: Use provided claude/ branches for Claude Code sessions.

## Domain Context

### Rating Systems
- **Bahamut**: 1-5 scale (must multiply by 2 for composite score normalization)
- **IMDb/Douban/MAL**: 0-10 scale

### Cross-Platform Matching
Japanese original title (`titleOriginal`) is the key for matching across platforms:
- Bahamut uses Chinese titles
- MAL uses Japanese/Romaji
- IMDb uses English
- Douban uses Chinese

### Composite Score Calculation
Weighted average using ONLY available ratings:
1. Normalize Bahamut (×2) to 0-10 scale
2. Sum (normalized_score × weight) for available platforms
3. Divide by sum of weights for available platforms

### Filter Behavior
- **Search**: MUST clear all other filters when active
- **Genres**: OR logic (not AND)
- **Missing ratings during sort**: Place at end, secondary sort by Bahamut

## Important Constraints

1. **Rate Limiting**: Always implement delays between scraping requests
   - Bahamut: 2-4 seconds
   - MAL API: 1.5 seconds
   - Douban: 5 seconds

2. **Error Handling**: Never crash on scraping errors - log and continue

3. **Coverage Expectations**: Accept ~70-80% MAL/IMDb, ~50-60% Douban (100% is not the goal)

4. **Performance Targets**:
   - Initial load: <2 seconds
   - Filter/sort response: <1 second
   - Total page weight: <5MB

5. **Browser Support**: Chrome/Edge 90+, Firefox 88+, Safari 14+, mobile browsers

## External Dependencies

### APIs
- **MyAnimeList API**: For MAL ratings and external ID links
- **OMDb API**: For IMDb ratings (optional, can web scrape)
- **ACG Database**: For Japanese title extraction (linked from Bahamut)

### Data Sources
- **Bahamut Anime Crazy**: Primary source (~1700+ anime)
- **Douban**: Best-effort matching via Chinese title + year

### Hosting
- **Recommended**: Vercel or Netlify
- **Alternative**: Static export to GitHub Pages
