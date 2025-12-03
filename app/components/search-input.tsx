'use client';

import { Input } from '@/components/ui/input';
import { Search } from 'lucide-react';

interface SearchInputProps {
  value: string;
  onChange: (value: string) => void;
}

export function SearchInput({ value, onChange }: SearchInputProps) {
  return (
    <div className="relative group">
      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground/60 w-4 h-4 transition-colors group-hover:text-primary/60" />
      <Input
        type="text"
        placeholder="搜尋動畫標題..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="pl-10 h-12 bg-white/50 border-white/60 focus:bg-white/80 transition-all rounded-2xl shadow-sm hover:shadow-md focus:ring-accent"
      />
    </div>
  );
}
