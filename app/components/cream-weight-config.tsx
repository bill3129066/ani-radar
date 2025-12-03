'use client';

import React from 'react';
import { WeightConfig } from '@/app/types/anime';
import { CreamCard, CreamSlider, CreamButton } from '@/components/ui/cream-components';
import { RotateCcw, X } from 'lucide-react';

interface CreamWeightConfigProps {
  weights: WeightConfig;
  onChange: (weights: WeightConfig) => void;
  onClose?: () => void;
}

const DEFAULT_WEIGHTS: WeightConfig = {
  bahamut: 25,
  imdb: 25,
  douban: 25,
  myanimelist: 25,
};

export const CreamWeightConfig: React.FC<CreamWeightConfigProps> = ({ weights, onChange, onClose }) => {
  
  const handleWeightChange = (key: keyof WeightConfig, newValue: number) => {
    // Clamp new value between 0 and 100
    if (newValue < 0) newValue = 0;
    if (newValue > 100) newValue = 100;

    const oldValue = weights[key];
    if (oldValue === newValue) return;

    const remainingTotal = 100 - newValue;
    const otherKeys = (Object.keys(weights) as Array<keyof WeightConfig>).filter(k => k !== key);
    
    const currentOthersTotal = otherKeys.reduce((sum, k) => sum + weights[k], 0);

    const newWeights = { ...weights, [key]: newValue };

    if (currentOthersTotal === 0) {
      // If others were 0, distribute remaining equally
      const split = Math.floor(remainingTotal / otherKeys.length);
      let remainder = remainingTotal % otherKeys.length;
      
      otherKeys.forEach(k => {
        newWeights[k] = split + (remainder > 0 ? 1 : 0);
        remainder--;
      });
    } else {
      // Scale others proportionally
      // We need to be careful with integer math to sum exactly to 100
      let distributed = 0;
      otherKeys.forEach((k, index) => {
        if (index === otherKeys.length - 1) {
          // Last one takes the rest to ensure sum is 100
          newWeights[k] = remainingTotal - distributed;
        } else {
          const ratio = weights[k] / currentOthersTotal;
          const val = Math.round(remainingTotal * ratio);
          newWeights[k] = val;
          distributed += val;
        }
      });
    }

    onChange(newWeights);
  };

  const resetWeights = () => {
    onChange(DEFAULT_WEIGHTS);
  };

  return (
    <CreamCard className="p-6 relative max-w-md w-full">
      {onClose && (
        <button onClick={onClose} className="absolute top-4 right-4 text-cream-400 hover:text-cream-600">
          <X size={20} />
        </button>
      )}
      
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-bold text-cream-900">綜合評分權重設定</h3>
        <button 
          onClick={resetWeights}
          className="text-xs font-bold text-apricot-500 hover:text-apricot-600 flex items-center gap-1"
        >
          <RotateCcw size={12} />
          重置
        </button>
      </div>

      <div className="space-y-4">
        <CreamSlider
          label="巴哈姆特 (Bahamut)"
          value={weights.bahamut}
          onChange={(v) => handleWeightChange('bahamut', v)}
        />
        <CreamSlider
          label="IMDb"
          value={weights.imdb}
          onChange={(v) => handleWeightChange('imdb', v)}
        />
        <CreamSlider
          label="豆瓣 (Douban)"
          value={weights.douban}
          onChange={(v) => handleWeightChange('douban', v)}
        />
        <CreamSlider
          label="MyAnimeList"
          value={weights.myanimelist}
          onChange={(v) => handleWeightChange('myanimelist', v)}
        />
      </div>

      <div className="mt-6 p-3 bg-cream-50 rounded-xl text-xs text-cream-500 text-center">
        調整任一滑桿，其他權重將自動平衡以維持總和 100%。
      </div>
    </CreamCard>
  );
};
