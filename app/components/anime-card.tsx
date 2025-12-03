'use client';

import React from 'react';
import { Anime, SortOption } from '@/app/types/anime';
import { CreamCard, CreamBadge, CreamButton } from '@/components/ui/cream-components';
import { formatNumber } from '@/app/lib/utils';
import { Play, Star, Clapperboard, Monitor, Award } from 'lucide-react';
import { cn } from '@/lib/utils';

interface AnimeCardProps {
  anime: Anime;
  showCompositeScore?: boolean;
  compositeScore?: number;
  sortOption?: SortOption;
}

export function AnimeCard({ anime, showCompositeScore, compositeScore, sortOption }: AnimeCardProps) {
  
  // Calculate display score based on sortOption
  let displayScore = 0;
  let displayScoreLabel = "Bahamut";
  let displayIcon = <Star size={16} className="text-yellow-500 fill-yellow-500" />;

  if (sortOption === 'composite') {
    displayScore = compositeScore || 0;
    displayScoreLabel = "Radar";
    displayIcon = <Award size={16} className="text-apricot-500 fill-apricot-500" />;
  } else if (sortOption === 'imdb') {
    displayScore = anime.ratings.imdb?.score || 0;
    displayScoreLabel = "IMDb";
    displayIcon = <Clapperboard size={16} className="text-yellow-600" />;
  } else if (sortOption === 'douban') {
    displayScore = anime.ratings.douban?.score || 0;
    displayScoreLabel = "Douban";
    displayIcon = <span className="text-xs font-black text-green-600">豆</span>;
  } else if (sortOption === 'myanimelist') {
    displayScore = anime.ratings.myanimelist?.score || 0;
    displayScoreLabel = "MAL";
    displayIcon = <Monitor size={16} className="text-blue-500" />;
  } else {
    // Default Bahamut
    displayScore = anime.ratings.bahamut.score;
    displayScoreLabel = "Bahamut";
    displayIcon = <Star size={16} className="text-yellow-500 fill-yellow-500" />;
  }

  // Fallback if score is 0 or missing
  const formattedScore = displayScore > 0 ? displayScore.toFixed(1) : '-';

  return (
    <CreamCard className="h-full flex flex-col overflow-hidden relative group border-none shadow-float hover:shadow-[0_20px_40px_rgba(0,0,0,0.1)]">
      {/* Floating Score Badge (Now Dynamic) */}
      <div className="absolute top-3 right-3 z-10 bg-white/95 backdrop-blur shadow-float px-3 py-1.5 rounded-2xl flex items-center gap-2 border border-white/50">
        {displayIcon}
        <div className="flex flex-col items-end leading-none">
            <span className="font-black text-cream-900 text-lg">{formattedScore}</span>
            <span className="text-[8px] font-bold text-cream-400 uppercase tracking-wide">{displayScoreLabel}</span>
        </div>
      </div>

      {/* Image Area - Adjusted aspect ratio to 2:3 for better fit of typical anime posters */}
      <div className="relative aspect-[2/3] w-full overflow-hidden bg-cream-100">
        <img 
          src={anime.thumbnail} 
          alt={anime.title} 
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-cream-900/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      </div>

      {/* Content Area */}
      <div className="p-4 flex flex-col flex-grow">
        <h3 className="text-lg font-black text-cream-900 mb-1 leading-tight line-clamp-2 min-h-[1.5em]" title={anime.title}>
          {anime.title}
        </h3>
        <p className="text-xs text-cream-500 font-medium mb-3 truncate font-sans h-4">
          {anime.titleOriginal || ''}
        </p>
        
        {/* Badges - Show more info */}
        <div className="flex flex-wrap gap-1.5 mb-4 content-start min-h-[26px]">
          <CreamBadge color="gray">{anime.year}</CreamBadge>
          <CreamBadge color="apricot">{anime.episodes ? `${anime.episodes}集` : '?'}</CreamBadge>
          {anime.genres.slice(0, 2).map(g => (
            <CreamBadge key={g} color="blue">{g}</CreamBadge>
          ))}
          {anime.genres.length > 2 && (
             <span className="text-[10px] text-cream-400 self-center font-bold">+{anime.genres.length - 2}</span>
          )}
        </div>

        {/* Ratings Grid - Show ALL ratings */}
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
          <RatingItem 
            icon={<Clapperboard size={10} />} 
            color="text-yellow-600"
            label="IMDb"
            score={anime.ratings.imdb?.score}
            votes={anime.ratings.imdb?.votes}
            missing={!anime.ratings.imdb}
          />

          {/* Douban */}
          <RatingItem 
            icon={<span className="text-[8px] font-black">豆</span>} 
            color="text-green-600"
            label="Douban"
            score={anime.ratings.douban?.score}
            missing={!anime.ratings.douban}
          />

          {/* MAL */}
          <RatingItem 
            icon={<Monitor size={10} />} 
            color="text-blue-500"
            label="MAL"
            score={anime.ratings.myanimelist?.score}
            missing={!anime.ratings.myanimelist}
          />
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

function RatingItem({ icon, color, label, score, votes, missing }: { icon: React.ReactNode, color: string, label: string, score?: number, votes?: number, missing?: boolean }) {
  if (missing || score == null || score === 0) {
    return (
        <div className="flex items-center gap-1.5 p-1.5 rounded-xl bg-cream-50/50 border border-transparent opacity-50">
            <div className="bg-cream-100 p-1 rounded-full flex items-center justify-center w-5 h-5 text-cream-300">
                {icon}
            </div>
            <div className="flex flex-col leading-none">
                <span className="text-[9px] text-cream-300 font-bold uppercase tracking-tighter mb-0.5">{label}</span>
                <span className="text-xs font-bold text-cream-300">-</span>
            </div>
        </div>
    )
  }

  return (
    <div className="flex items-center gap-1.5 p-1.5 rounded-xl bg-cream-50 border border-cream-100">
      <div className={cn("bg-white p-1 rounded-full shadow-sm flex items-center justify-center w-5 h-5", color)}>
        {icon}
      </div>
      <div className="flex flex-col leading-none">
        <span className="text-[9px] text-cream-400 font-bold uppercase tracking-tighter mb-0.5">{label}</span>
        <span className="text-xs font-black text-cream-700">
          {score.toFixed(1)}
          {votes && votes > 0 ? <span className="text-[8px] text-cream-400 font-medium ml-0.5">({formatNumber(votes)})</span> : null}
        </span>
      </div>
    </div>
  );
}
