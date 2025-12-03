# Ani-Radar - Bahamut Anime Rating Dashboard

## Project Overview
Ani-Radar is a personal anime rating dashboard designed to aggregate and compare ratings from **Bahamut Anime Crazy (巴哈姆特動畫瘋)**, **IMDb**, **Douban (豆瓣)**, and **MyAnimeList (MAL)**. It helps users discover high-quality anime by providing multi-dimensional filtering, sorting, and custom weighted scoring.

**Core Goal:** Help users find what to watch on Bahamut by leveraging global rating data.

### Tech Stack
*   **Frontend:** Next.js 16+ (App Router), TypeScript, Tailwind CSS, shadcn/ui.
*   **Data Pipeline:** Python 3.8+ (BeautifulSoup4, Requests).
*   **Data Storage:** Static JSON files.

## Building and Running

### 1. Frontend (Next.js)
The project is configured as a Next.js application at the root directory.

*   **Install Dependencies:**
    ```bash
    npm install
    ```
*   **Start Development Server:**
    ```bash
    npm run dev
    ```
    Access at `http://localhost:3000`.
*   **Build for Production:**
    ```bash
    npm run build
    ```
*   **Linting:**
    ```bash
    npm run lint
    ```

### 2. Data Pipeline (Crawler)
Located in the `crawler/` directory.

*   **Setup Python Environment:**
    ```bash
    cd crawler
    python3 -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
*   **Workflow:**
    1.  `python test_scraper.py`: Run a quick test (10 items) to verify selectors.
    2.  `python bahamut_scraper.py`: Scrape all anime from Bahamut (~1-2 hours).
    3.  `python cross_platform.py`: Align data with MAL, IMDb, and Douban.
    4.  `python generate_json.py`: Generate the final `data/animes.json`.
    5.  `python validate_data.py`: Verify data integrity.

## Development Conventions

### TypeScript & React
*   **Components:** PascalCase (e.g., `AnimeCard.tsx`). Default to **Server Components**. Use `'use client'` only when interactivity (hooks, event listeners) is required.
*   **Imports:** Use the `@/` alias for local imports (e.g., `import { cn } from '@/lib/utils'`).
*   **Styling:** Tailwind CSS with `shadcn/ui`. Use `clsx` or `cn()` for conditional class names. Design **Mobile-First**.
*   **Type Safety:** Strict mode enabled. Define interfaces in `app/types/`. Avoid `any`.

### Python (Crawler)
*   **Rate Limiting:** **CRITICAL**. Always sleep between requests (Bahamut: 2-4s, MAL: 1.5s, Douban: 5s).
*   **Error Handling:** "Fail Soft". If a single anime fails to scrape, log the error and **continue**. Do not crash the entire script.
*   **Selectors:** Selectors in `bahamut_scraper.py` must be verified against the live site, as they break easily with layout changes.

### Git & Version Control
*   **Commit Messages:** Conventional Commits (e.g., `feat: add sort logic`, `fix: scraper selector`).
*   **Branches:** Use specific branch names if provided (e.g., `claude/claude-md-...`).

## Core Business Logic

### Data Structure
*   **Primary Key:** Bahamut ID.
*   **Key Field:** `titleOriginal` (Japanese Title) is the **critical bridge** for finding the anime on MAL and IMDb.
*   **Ratings:**
    *   Bahamut: 1-5 scale (Normalized: x2).
    *   IMDb/MAL/Douban: 0-10 scale.

### Filtering & Sorting
*   **Search:** Searching by title (Chinese/Japanese) **clears all other filters** (Year, Genre).
*   **Genres:** Multi-select uses **OR** logic.
*   **Sorting:**
    *   Missing ratings handled by placing item at the **bottom**.
    *   Secondary sort key is always **Bahamut Rating**.
*   **Composite Score:** Calculated dynamically based on user-defined weights (0-100% for each platform).

## Directory Structure
*   `app/`: Next.js application source (App Router structure).
*   `crawler/`: Python scripts for data collection.
*   `data/`: Storage for `animes.json` (generated) and raw data.
*   `public/`: Static assets (images, icons).
*   `.claude/`: Context configurations (reference only).
