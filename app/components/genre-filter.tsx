'use client';

import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';

interface GenreFilterProps {
  genres: string[];
  selectedGenres: string[];
  onChange: (genres: string[]) => void;
}

export function GenreFilter({ genres, selectedGenres, onChange }: GenreFilterProps) {
  const handleToggle = (genre: string) => {
    if (selectedGenres.includes(genre)) {
      onChange(selectedGenres.filter(g => g !== genre));
    } else {
      onChange([...selectedGenres, genre]);
    }
  };

  return (
    <div className="space-y-3">
      <h3 className="font-medium text-sm text-muted-foreground flex items-center gap-2">
        <span>類型</span>
        <span className="text-xs bg-muted px-2 py-0.5 rounded-full">{selectedGenres.length} 選取</span>
      </h3>
      <div className="flex flex-wrap gap-2">
        {genres.map(genre => {
          const isSelected = selectedGenres.includes(genre);
          return (
            <div 
              key={genre}
              onClick={() => handleToggle(genre)}
              className={`
                cursor-pointer px-3 py-1.5 rounded-xl text-xs transition-all duration-300 border
                ${isSelected 
                  ? 'bg-primary text-primary-foreground border-primary shadow-md transform scale-105' 
                  : 'bg-white/40 text-muted-foreground border-transparent hover:bg-white/80 hover:shadow-sm'
                }
              `}
            >
              {genre}
            </div>
          );
        })}
      </div>
    </div>
  );
}
