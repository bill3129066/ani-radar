'use client';

import React, { useState } from 'react';
import { FilterState, SortOption, WeightConfig } from '@/app/types/anime';
import { CreamInput } from '@/components/ui/cream-components';
import { CreamWeightConfig } from './cream-weight-config';
import { Search, Sliders } from 'lucide-react';
import { cn } from '@/lib/utils';
import { GENRES } from '@/app/lib/constants';

const YEARS = ["2025", "2024", "2023", "2022", "2021", "2020", "2010-2019", "2000-2009", "1980-1999", "all"];

interface FilterBarProps {
  filters: FilterState;
  onFilterChange: (filters: FilterState) => void;
  sortOption: SortOption;
  onSortChange: (option: SortOption) => void;
  weights: WeightConfig;
  onWeightsChange: (weights: WeightConfig) => void;
}

export const FilterBar: React.FC<FilterBarProps> = ({
  filters,
  onFilterChange,
  sortOption,
  onSortChange,
  weights,
  onWeightsChange
}) => {
  const [showWeights, setShowWeights] = useState(false);

  const handleYearChange = (year: string) => {
    onFilterChange({ ...filters, yearOption: year });
  };

  const handleGenreToggle = (genre: string) => {
    const current = filters.genres;
    const newGenres = current.includes(genre)
      ? current.filter(g => g !== genre)
      : [...current, genre];
    onFilterChange({ ...filters, genres: newGenres });
  };

  const handleMinVotesChange = (val: number) => {
    onFilterChange({ ...filters, minVotes: val });
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onFilterChange({ ...filters, searchQuery: e.target.value });
  };

  return (
    <div className="flex flex-col gap-6 mb-8">
      {/* Top Row: Search | Sort | Weights | Min Votes */}
      <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center justify-between">
        
        {/* Search */}
        <div className="w-full lg:w-1/3 min-w-[300px]">
          <CreamInput 
            value={filters.searchQuery}
            onChange={handleSearchChange}
            placeholder="搜尋動畫標題 (中文/日文)..."
            icon={<Search size={18} />}
            className="shadow-sm"
          />
        </div>

        {/* Right Side Controls */}
        <div className="flex flex-wrap items-center gap-3 w-full lg:w-auto justify-end">
          
          {/* Min Votes Slider (Compact) */}
          <div className="flex flex-col w-40 px-2">
             <div className="flex justify-between text-[10px] text-cream-500 font-bold mb-1">
               <span>最低評分人數</span>
               <span>{filters.minVotes === 0 ? '關閉' : filters.minVotes}</span>
             </div>
             <input 
                type="range" 
                min="0" 
                max="5000" 
                step="100"
                value={filters.minVotes} 
                onChange={(e) => handleMinVotesChange(Number(e.target.value))}
                className="w-full h-1.5 bg-cream-300 rounded-lg appearance-none cursor-pointer accent-cream-600 hover:accent-apricot-500"
             />
          </div>

          <div className="h-8 w-px bg-cream-300 mx-2 hidden sm:block"></div>

          {/* Sort Options */}
          <div className="flex bg-white/50 p-1 rounded-full shadow-inner-soft">
            {(['composite', 'bahamut', 'imdb', 'douban', 'myanimelist'] as SortOption[]).map(opt => (
              <button
                key={opt}
                onClick={() => onSortChange(opt)}
                className={cn(
                  "px-4 py-2 rounded-full text-xs font-bold transition-all",
                  sortOption === opt 
                    ? "bg-cream-900 text-white shadow-md" 
                    : "text-cream-500 hover:text-cream-900 hover:bg-white/50"
                )}
              >
                {opt === 'composite' ? '綜合評分' :
                 opt === 'bahamut' ? '巴哈' :
                 opt === 'imdb' ? 'IMDb' :
                 opt === 'douban' ? '豆瓣' : 'MAL'}
              </button>
            ))}
          </div>

          {/* Weight Config Trigger */}
          <div className="relative">
            <button 
              onClick={() => setShowWeights(!showWeights)}
              className={cn(
                "p-3 rounded-full transition-all border",
                showWeights 
                  ? "bg-apricot-500 text-white border-apricot-500 shadow-md" 
                  : "bg-white text-cream-500 border-cream-200 hover:border-apricot-400 hover:text-apricot-500 shadow-soft"
              )}
              title="權重設定"
            >
              <Sliders size={18} />
            </button>
            
            {showWeights && (
              <div className="absolute right-0 top-full mt-4 z-50 w-80">
                <CreamWeightConfig 
                  weights={weights} 
                  onChange={onWeightsChange} 
                  onClose={() => setShowWeights(false)}
                />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Second Row: Year Chips */}
      <div className="flex flex-col gap-2">
         <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pb-2">
            <span className="text-xs font-bold text-cream-400 uppercase tracking-wider shrink-0 mr-2">年份</span>
            {YEARS.map(year => (
              <button
                key={year}
                onClick={() => handleYearChange(year)}
                className={cn(
                  "px-4 py-1.5 rounded-full text-sm font-bold whitespace-nowrap transition-all border",
                  (filters.yearOption === year || (!filters.yearOption && year === 'all'))
                    ? "bg-cream-900 text-white border-cream-900 shadow-md"
                    : "bg-white text-cream-500 border-cream-200 hover:border-cream-400 hover:text-cream-900"
                )}
              >
                {year === 'all' ? '全部年份' : year}
              </button>
            ))}
         </div>
      </div>

      {/* Third Row: Genre Chips */}
      <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs font-bold text-cream-400 uppercase tracking-wider shrink-0 mr-2">類型</span>
            {GENRES.map(genre => {
               const isSelected = filters.genres.includes(genre);
               return (
                <button
                  key={genre}
                  onClick={() => handleGenreToggle(genre)}
                  className={cn(
                    "px-3 py-1 rounded-xl text-xs font-bold transition-all border",
                    isSelected
                      ? "bg-apricot-100 text-apricot-600 border-apricot-200 shadow-sm"
                      : "bg-cream-50 text-cream-400 border-transparent hover:bg-white hover:shadow-sm"
                  )}
                >
                  {genre}
                </button>
               );
            })}
          </div>
      </div>
    </div>
  );
};