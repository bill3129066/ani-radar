'use client';

import { useState } from 'react';
import { WeightConfig } from '@/app/types/anime';
import { Slider } from '@/components/ui/slider';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { ChevronDown, SlidersHorizontal, RotateCcw } from 'lucide-react';

interface WeightConfigProps {
  weights: WeightConfig;
  onChange: (weights: WeightConfig) => void;
}

const DEFAULT_WEIGHTS: WeightConfig = {
  bahamut: 25,
  imdb: 25,
  douban: 25,
  myanimelist: 25,
};

export function WeightConfigPanel({ weights, onChange }: WeightConfigProps) {
  const [isOpen, setIsOpen] = useState(false);

  const total = weights.bahamut + weights.imdb + weights.douban + weights.myanimelist;
  const isValid = total === 100;

  const handleReset = () => {
    onChange(DEFAULT_WEIGHTS);
  };

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen} className="glass-panel p-4 rounded-2xl">
      <CollapsibleTrigger className="flex items-center justify-between w-full group">
        <div className="flex items-center gap-2 font-medium text-sm text-muted-foreground group-hover:text-primary transition-colors">
          <SlidersHorizontal className="w-4 h-4" />
          <span>綜合評分設定</span>
        </div>
        <ChevronDown
          className={`w-4 h-4 text-muted-foreground transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`}
        />
      </CollapsibleTrigger>

      <CollapsibleContent className="mt-4 space-y-5">
        {/* Bahamut Weight */}
        <div className="space-y-2">
          <div className="flex justify-between text-xs">
            <span className="font-medium text-yellow-700">⭐ 巴哈姆特</span>
            <span className="font-mono">{weights.bahamut}%</span>
          </div>
          <Slider
            value={[weights.bahamut]}
            onValueChange={([value]) =>
              onChange({ ...weights, bahamut: value })
            }
            min={0}
            max={100}
            step={5}
            className="cursor-pointer"
          />
        </div>

        {/* IMDb Weight */}
        <div className="space-y-2">
          <div className="flex justify-between text-xs">
            <span className="font-medium text-yellow-800">🎬 IMDb</span>
            <span className="font-mono">{weights.imdb}%</span>
          </div>
          <Slider
            value={[weights.imdb]}
            onValueChange={([value]) =>
              onChange({ ...weights, imdb: value })
            }
            min={0}
            max={100}
            step={5}
            className="cursor-pointer"
          />
        </div>

        {/* Douban Weight */}
        <div className="space-y-2">
          <div className="flex justify-between text-xs">
            <span className="font-medium text-green-700">🎭 豆瓣</span>
            <span className="font-mono">{weights.douban}%</span>
          </div>
          <Slider
            value={[weights.douban]}
            onValueChange={([value]) =>
              onChange({ ...weights, douban: value })
            }
            min={0}
            max={100}
            step={5}
            className="cursor-pointer"
          />
        </div>

        {/* MyAnimeList Weight */}
        <div className="space-y-2">
          <div className="flex justify-between text-xs">
            <span className="font-medium text-blue-700">📺 MyAnimeList</span>
            <span className="font-mono">{weights.myanimelist}%</span>
          </div>
          <Slider
            value={[weights.myanimelist]}
            onValueChange={([value]) =>
              onChange({ ...weights, myanimelist: value })
            }
            min={0}
            max={100}
            step={5}
            className="cursor-pointer"
          />
        </div>

        <div className="pt-2 border-t border-dashed border-muted-foreground/20 flex items-center justify-between">
          <div className={`text-xs font-semibold ${isValid ? 'text-green-600' : 'text-red-600'}`}>
            總和: {total}% {isValid ? '✓' : '(需為 100%)'}
          </div>

          <Button
            variant="ghost"
            size="sm"
            onClick={handleReset}
            className="h-8 text-xs text-muted-foreground hover:text-primary hover:bg-white/50"
          >
            <RotateCcw className="w-3 h-3 mr-1" />
            重置
          </Button>
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
}
