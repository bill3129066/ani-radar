import { Anime, SortOption, WeightConfig } from '@/app/types/anime';
import { normalizeRating } from '@/app/lib/utils';

export function sortAnimes(
  animes: Anime[],
  sortBy: SortOption,
  weights?: WeightConfig
): Anime[] {
  // Create a shallow copy to avoid mutating the original array
  const sorted = [...animes];

  switch (sortBy) {
    case 'bahamut':
      return sorted.sort((a, b) => {
        const scoreA = a.ratings.bahamut.score;
        const scoreB = b.ratings.bahamut.score;
        if (scoreB !== scoreA) return scoreB - scoreA;
        return (b.ratings.bahamut.votes || 0) - (a.ratings.bahamut.votes || 0); // Tie-breaker: votes
      });

    case 'imdb':
      return sorted.sort((a, b) => compareWithSecondary(a, b, 'imdb'));

    case 'douban':
      return sorted.sort((a, b) => compareWithSecondary(a, b, 'douban'));

    case 'myanimelist':
      return sorted.sort((a, b) => compareWithSecondary(a, b, 'myanimelist'));

    case 'composite':
      const config = weights || { bahamut: 25, imdb: 25, douban: 25, myanimelist: 25 };
      return sorted.sort((a, b) => {
        const scoreA = calculateCompositeScore(a, config);
        const scoreB = calculateCompositeScore(b, config);
        if (scoreB !== scoreA) return scoreB - scoreA;
        // Secondary sort by Bahamut score
        return b.ratings.bahamut.score - a.ratings.bahamut.score;
      });

    default:
      return sorted;
  }
}

/**
 * Helper to compare two animes based on a specific rating platform,
 * treating missing ratings as lowest priority (-1),
 * and using Bahamut score as a tie-breaker.
 */
function compareWithSecondary(a: Anime, b: Anime, platform: 'imdb' | 'douban' | 'myanimelist'): number {
  const ratingA = a.ratings[platform];
  const ratingB = b.ratings[platform];

  const scoreA = ratingA?.score ?? -1;
  const scoreB = ratingB?.score ?? -1;

  // Both missing
  if (scoreA === -1 && scoreB === -1) {
    return b.ratings.bahamut.score - a.ratings.bahamut.score;
  }
  
  // One missing (missing goes to bottom)
  if (scoreA === -1) return 1;
  if (scoreB === -1) return -1;

  // Compare scores
  if (scoreB !== scoreA) {
    return scoreB - scoreA;
  }

  // Tie-breaker: Bahamut score
  return b.ratings.bahamut.score - a.ratings.bahamut.score;
}

export function calculateCompositeScore(anime: Anime, weights: WeightConfig): number {
  let totalScore = 0;
  let totalWeight = 0;

  // Bahamut (Normalize 1-5 to 0-10)
  if (anime.ratings.bahamut.score > 0) {
    const w = weights.bahamut;
    const normalized = normalizeRating(anime.ratings.bahamut.score, '1-5');
    totalScore += normalized * w;
    totalWeight += w;
  }

  // IMDb
  if (anime.ratings.imdb?.score && anime.ratings.imdb.score > 0) {
    const w = weights.imdb;
    totalScore += anime.ratings.imdb.score * w;
    totalWeight += w;
  }

  // Douban
  if (anime.ratings.douban?.score && anime.ratings.douban.score > 0) {
    const w = weights.douban;
    totalScore += anime.ratings.douban.score * w;
    totalWeight += w;
  }

  // MyAnimeList
  if (anime.ratings.myanimelist?.score && anime.ratings.myanimelist.score > 0) {
    const w = weights.myanimelist;
    totalScore += anime.ratings.myanimelist.score * w;
    totalWeight += w;
  }

  if (totalWeight === 0) return 0;
  
  // Return weighted average
  // Formula: (S1*W1 + S2*W2...) / (W1+W2...)
  // Since weights sum to 100 usually, but if data is missing, we re-normalize based on available weights.
  return totalScore / totalWeight;
}
