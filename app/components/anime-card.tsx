'use client';

import React from 'react';
import { Anime } from '@/app/types/anime';
import { CreamCard, CreamBadge, CreamButton } from '@/components/ui/cream-components';
import { formatNumber } from '@/app/lib/utils';
import { Play, Star, Clapperboard, Monitor, Award } from 'lucide-react';
import { cn } from '@/lib/utils';

interface AnimeCardProps {
  anime: Anime;
  showCompositeScore?: boolean;
  compositeScore?: number;
}

export function AnimeCard({ anime, showCompositeScore, compositeScore }: AnimeCardProps) {
  // Truncate title logic could be handled by CSS line-clamp
  
  // Calculate display score (Composite or Bahamut if not composite mode)
  // Actually, if composite mode is on, we show the badge.
  // If not, maybe we show Bahamut score in the badge? 
  // The user requirement says: "Floating Score Badge - Super cute". 
  // I will show composite score if available, otherwise Bahamut score.
  
  const displayScore = showCompositeScore && compositeScore 
    ? compositeScore.toFixed(1) 
    : (anime.ratings.bahamut.score || 0).toFixed(1);

  const displayScoreLabel = showCompositeScore ? "Radar" : "Bahamut";

  return (
    <CreamCard className="h-full flex flex-col overflow-hidden relative group border-none shadow-float hover:shadow-[0_20px_40px_rgba(0,0,0,0.1)]">
      {/* Floating Score Badge */}
      <div className="absolute top-3 right-3 z-10 bg-white/90 backdrop-blur shadow-float px-3 py-1.5 rounded-2xl flex items-center gap-1.5 border border-white/50">
        {showCompositeScore ? (
            <Award size={16} className="text-apricot-500 fill-apricot-500" />
        ) : (
            <Star size={16} className="text-yellow-500 fill-yellow-500" />
        )}
        <div className="flex flex-col items-end leading-none">
            <span className="font-black text-cream-900 text-base">{displayScore}</span>
            <span className="text-[8px] font-bold text-cream-400 uppercase tracking-wide">{displayScoreLabel}</span>
        </div>
      </div>

      {/* Image Area */}
      <div className="relative aspect-[3/4] w-full overflow-hidden">
        <img 
          src={anime.thumbnail} 
          alt={anime.title} 
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-cream-900/40 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      </div>

      {/* Content Area */}
      <div className="p-4 flex flex-col flex-grow">
        <h3 className="text-lg font-black text-cream-900 mb-1 leading-tight line-clamp-2 min-h-[1.5em]" title={anime.title}>
          {anime.title}
        </h3>
        <p className="text-xs text-cream-500 font-medium mb-3 truncate font-sans">
          {anime.titleOriginal || '　'}
        </p>
        
        {/* Badges */}
        <div className="flex flex-wrap gap-1.5 mb-4">
          <CreamBadge color="gray">{anime.year}</CreamBadge>
          <CreamBadge color="apricot">{anime.episodes ? `${anime.episodes}集` : '?'}</CreamBadge>
          {anime.genres.slice(0, 1).map(g => (
            <CreamBadge key={g} color="blue">{g}</CreamBadge>
          ))}
        </div>

        {/* Ratings Grid */}
        <div className="grid grid-cols-2 gap-2 mb-4 mt-auto">
          {/* Bahamut */}
          <RatingItem 
            icon={<Star size={10} className="fill-current"/>} 
            color="text-yellow-500"
            label="Bahamut"
            score={anime.ratings.bahamut.score}
            votes={anime.ratings.bahamut.votes}
          />

          {/* IMDb */}
          {anime.ratings.imdb && (
             <RatingItem 
                icon={<Clapperboard size={10} />} 
                color="text-yellow-600"
                label="IMDb"
                score={anime.ratings.imdb.score}
                votes={anime.ratings.imdb.votes}
              />
          )}

          {/* Douban */}
          {anime.ratings.douban && (
             <RatingItem 
                icon={<span className="text-[8px] font-black">豆</span>} 
                color="text-green-600"
                label="Douban"
                score={anime.ratings.douban.score}
              />
          )}

          {/* MAL */}
          {anime.ratings.myanimelist && (
             <RatingItem 
                icon={<Monitor size={10} />} 
                color="text-blue-500"
                label="MAL"
                score={anime.ratings.myanimelist.score}
              />
          )}
        </div>

        {/* Watch Button */}
        <CreamButton 
          variant="secondary" 
          className="w-full !py-2.5 text-sm mt-1 group-hover:bg-apricot-500 group-hover:text-white group-hover:border-apricot-500 group-hover:shadow-lg transition-all"
          onClick={() => window.open(anime.bahamutUrl, '_blank')}
        >
          <Play size={14} className="fill-current" />
          <span>Watch</span>
        </CreamButton>
      </div>
    </CreamCard>
  );
}

function RatingItem({ icon, color, label, score, votes }: { icon: React.ReactNode, color: string, label: string, score: number, votes?: number }) {
  return (
    <div className="flex items-center gap-1.5 p-1.5 rounded-xl bg-cream-50 border border-cream-100">
      <div className={cn("bg-white p-1 rounded-full shadow-sm flex items-center justify-center w-5 h-5", color)}>
        {icon}
      </div>
      <div className="flex flex-col leading-none">
        <span className="text-[9px] text-cream-400 font-bold uppercase tracking-tighter mb-0.5">{label}</span>
        <span className="text-xs font-black text-cream-700">
          {score ? score.toFixed(1) : 'N/A'}
          {votes && votes > 0 ? <span className="text-[8px] text-cream-400 font-medium ml-0.5">({formatNumber(votes)})</span> : null}
        </span>
      </div>
    </div>
  );
}