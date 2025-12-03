'use client';

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { SortOption } from '@/app/types/anime';

interface SortSelectorProps {
  value: SortOption;
  onChange: (value: SortOption) => void;
}

export function SortSelector({ value, onChange }: SortSelectorProps) {
  return (
    <div className="space-y-2">
      <h3 className="font-medium text-sm text-muted-foreground">排序方式</h3>
      <Select value={value} onValueChange={onChange}>
        <SelectTrigger className="w-full bg-white/50 border-white/60 rounded-2xl h-11 focus:ring-accent">
          <SelectValue />
        </SelectTrigger>
        <SelectContent className="bg-white/90 backdrop-blur-xl border-white/50 rounded-xl shadow-xl">
          <SelectItem value="bahamut">⭐ 巴哈評分最高</SelectItem>
          <SelectItem value="imdb">🎬 IMDb 評分最高</SelectItem>
          <SelectItem value="douban">🎭 豆瓣評分最高</SelectItem>
          <SelectItem value="myanimelist">📺 MyAnimeList 評分最高</SelectItem>
          <SelectItem value="composite">✨ 綜合評分最高</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
}
