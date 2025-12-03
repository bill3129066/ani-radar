import { Anime, FilterState } from '@/app/types/anime';

export function filterAnimes(animes: Anime[], filters: FilterState): Anime[] {
  // Search query takes precedence and ignores other filters (as per PRD)
  if (filters.searchQuery && filters.searchQuery.trim()) {
    const query = filters.searchQuery.toLowerCase().trim();
    return animes.filter(anime =>
      anime.title.toLowerCase().includes(query) ||
      (anime.titleOriginal && anime.titleOriginal.toLowerCase().includes(query))
    );
  }

  let filtered = animes;

  // Genre filter (OR logic)
  if (filters.genres.length > 0) {
    filtered = filtered.filter(anime =>
      anime.genres.some(genre => filters.genres.includes(genre))
    );
  }

  // Year filter
  if (filters.yearOption && filters.yearOption !== 'all') {
    filtered = filtered.filter(anime => checkYear(anime.year, filters.yearOption!));
  }

  // Minimum votes filter
  if (filters.minVotes > 0) {
    filtered = filtered.filter(anime =>
      (anime.ratings.bahamut.votes || 0) >= filters.minVotes
    );
  }

  return filtered;
}

function checkYear(animeYear: number, yearOption: string): boolean {
  if (!yearOption || yearOption === 'all') return true;

  // Single year "2024"
  if (/^\d{4}$/.test(yearOption)) {
    return animeYear === parseInt(yearOption);
  }

  // Range "2010-2019"
  if (/^\d{4}-\d{4}$/.test(yearOption)) {
    const [start, end] = yearOption.split('-').map(Number);
    return animeYear >= start && animeYear <= end;
  }

  return true;
}
