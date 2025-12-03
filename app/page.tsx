'use client';

import { useState, useMemo } from 'react';
import { loadAnimeData } from '@/app/lib/data-loader';
import { filterAnimes } from '@/app/lib/filters';
import { sortAnimes, calculateCompositeScore } from '@/app/lib/sorting';
import { FilterBar } from '@/app/components/filter-bar';
import { AnimeGrid } from '@/app/components/anime-grid';
import { FilterState, SortOption, WeightConfig, Anime } from '@/app/types/anime';
import { Radar } from 'lucide-react';

export default function Home() {
  // Load data
  const allAnimes = useMemo(() => loadAnimeData(), []);

  // State
  const [filters, setFilters] = useState<FilterState>({
    genres: [],
    searchQuery: '',
    minVotes: 0, // Default 0 (Off) per requirements
    yearOption: 'all',
  });

  const [sortBy, setSortBy] = useState<SortOption>('composite'); // Default sort by Radar Score
  
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
    <div className="min-h-screen bg-cream-200 text-cream-900 font-sans selection:bg-apricot-200 selection:text-apricot-900">
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6">
        {/* Branding Title */}
        <div className="flex items-center gap-3 mb-6">
           <div className="bg-apricot-500 p-2 rounded-xl text-white shadow-[0_4px_14px_rgba(255,159,89,0.4)]">
              <Radar size={24} strokeWidth={2.5} />
           </div>
           <h1 className="text-3xl font-black text-cream-900 tracking-tight">
             Ani-Radar
           </h1>
           <span className="text-sm font-bold text-cream-400 bg-white px-2 py-1 rounded-lg shadow-sm">
              {displayedAnimes.length} Animes
           </span>
        </div>

        {/* Top Controls Area */}
        <FilterBar 
          filters={filters}
          onFilterChange={setFilters}
          sortOption={sortBy}
          onSortChange={setSortBy}
          weights={weights}
          onWeightsChange={setWeights}
        />

        {/* Main Content Grid */}
        <main>
          {displayedAnimes.length === 0 ? (
             <div className="flex flex-col items-center justify-center py-20 text-center">
                <div className="bg-white p-6 rounded-full shadow-float mb-4">
                   <Radar size={48} className="text-apricot-300" />
                </div>
                <h3 className="text-xl font-extrabold text-cream-900 mb-2">找不到動畫</h3>
                <p className="text-cream-500 max-w-xs">試著調整篩選條件或搜尋其他關鍵字。</p>
                <button 
                  onClick={() => setFilters({ genres: [], searchQuery: '', minVotes: 0, yearOption: 'all' })}
                  className="mt-6 px-6 py-2 bg-white text-apricot-500 font-bold rounded-full shadow-soft hover:shadow-md transition-all"
                >
                  清除篩選
                </button>
             </div>
          ) : (
             <AnimeGrid 
               animes={displayedAnimes} 
               showCompositeScore={sortBy === 'composite'}
               getCompositeScore={getCompositeScore}
             />
          )}
          
          {/* Footer */}
          <footer className="mt-20 py-8 text-center text-xs text-cream-400 font-bold">
            <p>Data sources: Bahamut Anime Crazy, IMDb, Douban, MyAnimeList.</p>
            <p className="mt-2 opacity-50">Designed with Creamy UI.</p>
          </footer>
        </main>
      </div>
    </div>
  );
}