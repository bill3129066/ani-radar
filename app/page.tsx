'use client';

import { useState, useMemo, useEffect } from 'react';
import { loadAnimeData, getAllGenres } from '@/app/lib/data-loader';
import { filterAnimes } from '@/app/lib/filters';
import { sortAnimes, calculateCompositeScore } from '@/app/lib/sorting';
import { FilterSidebar } from '@/app/components/filter-sidebar';
import { AnimeGrid } from '@/app/components/anime-grid';
import { FilterState, SortOption, WeightConfig, Anime } from '@/app/types/anime';
import { SlidersHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';

export default function Home() {
  // Load data
  // In a real app with large data, we might want to load this differently or use SSG/ISR
  // For this static JSON approach, simple load is fine.
  const allAnimes = useMemo(() => loadAnimeData(), []);
  const allGenres = useMemo(() => getAllGenres(allAnimes), [allAnimes]);

  // State
  const [filters, setFilters] = useState<FilterState>({
    genres: [],
    searchQuery: '',
    minVotes: 50, // Default minimum votes to filter out noise
    yearOption: 'all',
  });

  const [sortBy, setSortBy] = useState<SortOption>('bahamut');
  
  const [weights, setWeights] = useState<WeightConfig>({
    bahamut: 25,
    imdb: 25,
    douban: 25,
    myanimelist: 25,
  });

  // Derived State (Filtered & Sorted)
  const displayedAnimes = useMemo(() => {
    // 1. Filter
    const filtered = filterAnimes(allAnimes, filters);
    
    // 2. Sort
    return sortAnimes(filtered, sortBy, weights);
  }, [allAnimes, filters, sortBy, weights]);

  // Helper for AnimeGrid to show composite score
  const getCompositeScore = (anime: Anime) => calculateCompositeScore(anime, weights);

  return (
    <div className="min-h-screen bg-[#F7F5F2] text-[#3A3A3A] font-sans selection:bg-[#FFE5EC] selection:text-[#3A3A3A]">
      {/* Header / Top Bar */}
      <header className="sticky top-0 z-50 w-full glass-panel border-b border-white/20 px-6 py-4 flex items-center justify-between md:hidden">
        <h1 className="text-xl font-medium tracking-tight text-primary">Ani-Radar</h1>
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon" className="md:hidden">
              <SlidersHorizontal className="h-5 w-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-[300px] sm:w-[400px] overflow-y-auto bg-[#F7F5F2] p-0">
             <div className="p-6">
                <FilterSidebar
                  filters={filters}
                  sortBy={sortBy}
                  weights={weights}
                  genres={allGenres}
                  onFiltersChange={setFilters}
                  onSortChange={setSortBy}
                  onWeightsChange={setWeights}
                />
             </div>
          </SheetContent>
        </Sheet>
      </header>

      <div className="container mx-auto px-4 py-8 md:py-12 md:flex md:gap-12">
        {/* Desktop Sidebar */}
        <div className="hidden md:block">
          <div className="sticky top-12">
            <h1 className="text-3xl font-light tracking-tight text-primary mb-8 pl-2">
              Ani-Radar
              <span className="text-accent-foreground text-sm ml-2 font-normal opacity-50">v1.0</span>
            </h1>
            <FilterSidebar
              filters={filters}
              sortBy={sortBy}
              weights={weights}
              genres={allGenres}
              onFiltersChange={setFilters}
              onSortChange={setSortBy}
              onWeightsChange={setWeights}
            />
          </div>
        </div>

        {/* Main Content */}
        <main className="flex-1 min-w-0 mt-4 md:mt-0">
          <div className="mb-8 flex items-end justify-between px-2">
            <div>
              <h2 className="text-2xl font-light mb-1">
                {filters.searchQuery 
                  ? `搜尋 "${filters.searchQuery}"`
                  : filters.yearOption && filters.yearOption !== 'all' 
                    ? `${filters.yearOption} 動畫` 
                    : '熱門動畫'}
              </h2>
              <p className="text-sm text-muted-foreground">
                共找到 {displayedAnimes.length} 部作品
              </p>
            </div>
          </div>

          <AnimeGrid 
            animes={displayedAnimes} 
            showCompositeScore={sortBy === 'composite'}
            getCompositeScore={getCompositeScore}
          />
          
          {/* Footer / Credits */}
          <footer className="mt-20 py-8 text-center text-xs text-muted-foreground/60">
            <p>Data sources: Bahamut Anime Crazy, IMDb, Douban, MyAnimeList.</p>
            <p className="mt-2">Designed with Japanese Creamy UI Esthetics.</p>
          </footer>
        </main>
      </div>
    </div>
  );
}
