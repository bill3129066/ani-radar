export interface AnimeRating {
  score: number;
  votes?: number;
  members?: number;
  id?: string | number;
}

export interface Anime {
  id: string;
  title: string;
  titleOriginal?: string;
  thumbnail: string;
  year: number;
  genres: string[];
  episodes: number;
  bahamutUrl: string;
  popularity: number;
  tags?: string[];
  ratings: {
    bahamut: AnimeRating;
    imdb?: AnimeRating;
    douban?: AnimeRating;
    myanimelist?: AnimeRating;
  };
}

export type SortOption =
  | 'bahamut'
  | 'imdb'
  | 'douban'
  | 'myanimelist'
  | 'composite';

export interface FilterState {
  genres: string[];
  yearStart?: number;
  yearEnd?: number;
  minVotes: number;
  searchQuery: string;
}

export interface WeightConfig {
  bahamut: number;
  imdb: number;
  douban: number;
  myanimelist: number;
}
