import { Anime } from '@/app/types/anime';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { formatNumber } from '@/app/lib/utils';
import { Badge } from '@/components/ui/badge';
import { Star, Tv, Clapperboard, MonitorPlay } from 'lucide-react';

interface AnimeCardProps {
  anime: Anime;
  showCompositeScore?: boolean;
  compositeScore?: number;
}

export function AnimeCard({ anime, showCompositeScore, compositeScore }: AnimeCardProps) {
  // Define rating badges
  const ratings = [
    {
      source: 'bahamut',
      icon: <Star className="w-3 h-3 text-yellow-500 fill-yellow-500" />,
      score: anime.ratings.bahamut.score,
      votes: anime.ratings.bahamut.votes,
      label: '巴哈',
      color: 'bg-yellow-50 text-yellow-700 border-yellow-200'
    },
    {
      source: 'imdb',
      icon: <Clapperboard className="w-3 h-3 text-yellow-600" />,
      score: anime.ratings.imdb?.score,
      votes: anime.ratings.imdb?.votes,
      label: 'IMDb',
      color: 'bg-yellow-100 text-yellow-800 border-yellow-300'
    },
    {
      source: 'douban',
      icon: <div className="text-[10px] font-bold text-green-600">豆</div>,
      score: anime.ratings.douban?.score,
      votes: anime.ratings.douban?.votes,
      label: '豆瓣',
      color: 'bg-green-50 text-green-700 border-green-200'
    },
    {
      source: 'mal',
      icon: <Tv className="w-3 h-3 text-blue-500" />,
      score: anime.ratings.myanimelist?.score,
      votes: anime.ratings.myanimelist?.members, // MAL uses members usually
      label: 'MAL',
      color: 'bg-blue-50 text-blue-700 border-blue-200'
    }
  ].filter(r => r.score !== undefined && r.score !== null && r.score > 0);

  return (
    <Card className="glass-card overflow-hidden group flex flex-col h-full border-none">
      <div className="relative aspect-[3/4] overflow-hidden rounded-t-xl">
        <img
          src={anime.thumbnail}
          alt={anime.title}
          className="object-cover w-full h-full transition-transform duration-700 group-hover:scale-105"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end p-4">
          <Button 
            className="w-full bg-white/90 text-black hover:bg-white neumorphic-button"
            onClick={() => window.open(anime.bahamutUrl, '_blank')}
          >
            <MonitorPlay className="w-4 h-4 mr-2" />
            前往觀看
          </Button>
        </div>
        
        {showCompositeScore && compositeScore !== undefined && (
          <div className="absolute top-2 right-2 bg-white/90 backdrop-blur-md px-2 py-1 rounded-lg text-xs font-bold text-primary shadow-sm border border-white/50">
            {compositeScore.toFixed(1)}
          </div>
        )}
      </div>

      <CardContent className="p-4 flex-grow flex flex-col gap-2">
        <h3 className="font-medium text-lg leading-tight line-clamp-2 text-primary" title={anime.title}>
          {anime.title}
        </h3>
        
        <div className="text-xs text-muted-foreground flex items-center gap-2 mb-2">
          <span>{anime.year}</span>
          <span>·</span>
          <span className="line-clamp-1">{anime.genres.slice(0, 3).join(' / ')}</span>
          <span>·</span>
          <span>{anime.episodes || '?'} 集</span>
        </div>

        <div className="grid grid-cols-2 gap-2 mt-auto">
          {ratings.map((rating) => (
            <div 
              key={rating.source} 
              className={`flex items-center gap-1.5 px-2 py-1 rounded-md border ${rating.color} bg-opacity-50`}
            >
              {rating.icon}
              <span className="text-xs font-bold">{rating.score?.toFixed(1)}</span>
              {rating.votes && (
                <span className="text-[10px] opacity-70">({formatNumber(rating.votes)})</span>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
