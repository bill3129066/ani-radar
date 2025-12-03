import animeData from '@/data/animes.json';
import { Anime } from '@/app/types/anime';

// Type assertion because JSON import might be inferred loosely
const animes = animeData as unknown as Anime[];

export function loadAnimeData(): Anime[] {
  return animes;
}

export function getAllGenres(animes: Anime[]): string[] {
  const genreSet = new Set<string>();
  animes.forEach(anime => {
    anime.genres.forEach(genre => genreSet.add(genre));
  });
  return Array.from(genreSet).sort();
}

export function getYearRange(animes: Anime[]): [number, number] {
  if (animes.length === 0) return [2000, new Date().getFullYear()];
  const years = animes.map(a => a.year).filter(y => y > 0);
  if (years.length === 0) return [2000, new Date().getFullYear()];
  return [Math.min(...years), Math.max(...years)];
}
