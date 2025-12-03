import { loadAnimeData } from '@/app/lib/data-loader';

export default function Home() {
  const animes = loadAnimeData();

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Ani-Radar</h1>
      <p>Total anime: {animes.length}</p>

      {/* Display first 10 anime as test */}
      <div className="grid gap-4 mt-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {animes.slice(0, 10).map(anime => (
          <div key={anime.id} className="border p-4 rounded shadow-sm">
            <h2 className="font-bold text-xl">{anime.title}</h2>
            <p className="text-gray-600">{anime.year} · {anime.genres.join(', ')}</p>
            <div className="mt-2 space-y-1 text-sm">
                <p>Bahamut: {anime.ratings.bahamut.score} ({anime.ratings.bahamut.votes} votes)</p>
                {anime.ratings.imdb && <p>IMDb: {anime.ratings.imdb.score} ({anime.ratings.imdb.votes} votes)</p>}
                {anime.ratings.myanimelist && <p>MAL: {anime.ratings.myanimelist.score}</p>}
                {anime.ratings.douban && <p>Douban: {anime.ratings.douban.score}</p>}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}