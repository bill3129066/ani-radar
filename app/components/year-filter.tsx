'use client';

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

interface YearFilterProps {
  value?: string;
  onChange: (value: string) => void;
}

export function YearFilter({ value, onChange }: YearFilterProps) {
  return (
    <div className="space-y-2">
      <h3 className="font-medium text-sm text-muted-foreground">年份</h3>
      <Select value={value || 'all'} onValueChange={onChange}>
        <SelectTrigger className="w-full bg-white/50 border-white/60 rounded-2xl h-11 focus:ring-accent">
          <SelectValue placeholder="選擇年份" />
        </SelectTrigger>
        <SelectContent className="bg-white/90 backdrop-blur-xl border-white/50 rounded-xl shadow-xl">
          <SelectItem value="all">所有時間</SelectItem>
          <SelectItem value="2025">2025</SelectItem>
          <SelectItem value="2024">2024</SelectItem>
          <SelectItem value="2023">2023</SelectItem>
          <SelectItem value="2022">2022</SelectItem>
          <SelectItem value="2021">2021</SelectItem>
          <SelectItem value="2020">2020</SelectItem>
          <SelectItem value="2010-2019">2010-2019</SelectItem>
          <SelectItem value="2000-2009">2000-2009</SelectItem>
          <SelectItem value="1980-1999">1980-1999</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
}
