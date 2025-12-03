'use client';

import { Anime } from '@/app/types/anime';
import { AnimeCard } from '@/app/components/anime-card';

interface AnimeGridProps {
  animes: Anime[];
  showCompositeScore?: boolean;
  getCompositeScore?: (anime: Anime) => number;
}

export function AnimeGrid({ animes, showCompositeScore, getCompositeScore }: AnimeGridProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
      {animes.map((anime) => (
        <div key={anime.id} className="h-full">
          <AnimeCard 
            anime={anime}
            showCompositeScore={showCompositeScore}
            compositeScore={getCompositeScore ? getCompositeScore(anime) : undefined}
          />
        </div>
      ))}
    </div>
  );
}