# Ani-Radar - Phased Implementation Roadmap

**For AI Agents**: Execute phases sequentially.

---

## Phase 0: Project Setup (Completed)
- [x] Next.js 16+ Setup
- [x] Tailwind v4 Setup
- [x] Python Environment

## Phase 1: Data Collection (Completed)
- [x] Bahamut Scraper
- [x] ACG Database (Japanese Title)
- [x] Validate Data

## Phase 2: Cross-Platform Data (Completed)
- [x] MAL Integration
- [x] IMDb Integration
- [x] Douban Integration
- [x] Data Generation (`data/animes.json`)

## Phase 3: UI Redesign & Core Components (Current Focus)

**Goal**: Implement the new "Cream" aesthetic and "Top Filter" layout.

### Tasks
1.  **Style Foundation**:
    - Update `app/globals.css` with Cream/Apricot variables (Tailwind v4 theme).
    - Create base UI components (`CreamCard`, `CreamButton`, `CreamBadge`, `CreamSlider`, `CreamInput`) in `components/ui/cream-*.tsx`.

2.  **Top Filter Bar (Refactor FilterSidebar)**:
    - Create `components/filter-bar.tsx`.
    - Implement **Year Filter** as Single-select Chips.
    - Implement **Sort Control** (No emojis, prominent).
    - Implement **Min Votes Slider** (Left = Off).

3.  **Weight Configuration Logic**:
    - Refactor `WeightConfigPanel`.
    - Implement **Auto-balancing logic** (Drag one -> others adjust).

4.  **Anime Card Redesign**:
    - Update `components/anime-card.tsx` to match the new visual style.
    - Show **ALL 5 scores** (Radar, Bahamut, IMDb, Douban, MAL).
    - Fix layout spacing.

5.  **Page Layout Integration**:
    - Update `app/page.tsx` to use the Top Filter layout.
    - Remove sidebar.

## Phase 4: Polish & Deployment
- [ ] Loading / Empty States.
- [ ] Mobile Responsiveness check.
- [ ] Build & Deploy.