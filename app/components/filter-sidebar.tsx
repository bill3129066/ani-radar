'use client';

import { FilterState, SortOption, WeightConfig } from '@/app/types/anime';
import { SearchInput } from './search-input';
import { GenreFilter } from './genre-filter';
import { YearFilter } from './year-filter';
import { SortSelector } from './sort-selector';
import { WeightConfigPanel } from './weight-config';
import { Slider } from '@/components/ui/slider';
import { Label } from '@/components/ui/label';
import { Filter } from 'lucide-react';

interface FilterSidebarProps {
  filters: FilterState;
  sortBy: SortOption;
  weights: WeightConfig;
  genres: string[];
  onFiltersChange: (filters: FilterState) => void;
  onSortChange: (sort: SortOption) => void;
  onWeightsChange: (weights: WeightConfig) => void;
  className?: string;
}

export function FilterSidebar({
  filters,
  sortBy,
  weights,
  genres,
  onFiltersChange,
  onSortChange,
  onWeightsChange,
  className,
}: FilterSidebarProps) {
  return (
    <aside className={`w-full md:w-80 flex-shrink-0 flex flex-col gap-8 ${className}`}>
      {/* Search Section */}
      <div className="space-y-4">
        <h2 className="text-xl font-medium flex items-center gap-2 text-primary/80">
          <Filter className="w-5 h-5" />
          篩選與排序
        </h2>
        <SearchInput
          value={filters.searchQuery}
          onChange={(value) =>
            onFiltersChange({ ...filters, searchQuery: value })
          }
        />
      </div>

      <div className="glass-panel p-6 rounded-3xl space-y-8">
        {/* Genre Filter */}
        <GenreFilter
          genres={genres}
          selectedGenres={filters.genres}
          onChange={(newGenres) =>
            onFiltersChange({ ...filters, genres: newGenres })
          }
        />

        {/* Year Filter */}
        <YearFilter
          value={filters.yearOption}
          onChange={(value) =>
            onFiltersChange({ ...filters, yearOption: value })
          }
        />

        {/* Sort Selector */}
        <SortSelector value={sortBy} onChange={onSortChange} />

        {/* Min Votes Slider */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <Label className="font-medium text-sm text-muted-foreground">最低評分人數</Label>
            <span className="text-xs font-mono bg-white/50 px-2 py-1 rounded-md">
              {filters.minVotes}
            </span>
          </div>
          <Slider
            value={[filters.minVotes]}
            onValueChange={([value]) =>
              onFiltersChange({ ...filters, minVotes: value })
            }
            min={0}
            max={2000}
            step={50}
            className="cursor-pointer"
          />
          <p className="text-[10px] text-muted-foreground/60 text-right">
            過濾掉冷門作品
          </p>
        </div>

        {/* Weight Config */}
        <WeightConfigPanel
          weights={weights}
          onChange={onWeightsChange}
        />
      </div>
    </aside>
  );
}
