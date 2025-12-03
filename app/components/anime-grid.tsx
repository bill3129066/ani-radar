import { Anime } from '@/app/types/anime';
import { AnimeCard } from './anime-card';

interface AnimeGridProps {
  animes: Anime[];
  showCompositeScore?: boolean;
  getCompositeScore?: (anime: Anime) => number;
}

export function AnimeGrid({ animes, showCompositeScore, getCompositeScore }: AnimeGridProps) {
  if (animes.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-muted-foreground glass-card rounded-3xl mx-auto max-w-md">
        <div className="text-6xl mb-4">🍃</div>
        <p className="text-lg">沒有找到符合的動畫</p>
        <p className="text-sm opacity-60 mt-2">試著調整篩選條件看看？</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      {animes.map((anime) => (
        <AnimeCard 
          key={anime.id} 
          anime={anime} 
          showCompositeScore={showCompositeScore}
          compositeScore={getCompositeScore ? getCompositeScore(anime) : undefined}
        />
      ))}
    </div>
  );
}
