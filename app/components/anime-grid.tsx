'use client';

import { Anime, SortOption } from '@/app/types/anime';
import { AnimeCard } from '@/app/components/anime-card';

interface AnimeGridProps {
  animes: Anime[];
  getCompositeScore?: (anime: Anime) => number;
  sortOption?: SortOption;
}

export function AnimeGrid({ animes, getCompositeScore, sortOption }: AnimeGridProps) {
  // Use wider grid cells as requested (1 col mobile, 2 cols tablet, 3 cols desktop, 4 cols large)
  // Previous was 2/3/4/5 which made cards too narrow
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {animes.map((anime) => (
        <div key={anime.id} className="h-full">
          <AnimeCard 
            anime={anime}
            compositeScore={getCompositeScore ? getCompositeScore(anime) : undefined}
            sortOption={sortOption}
          />
        </div>
      ))}
    </div>
  );
}
