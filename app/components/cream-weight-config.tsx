'use client';

import React from 'react';
import { WeightConfig } from '@/app/types/anime';
import { CreamCard, CreamSlider } from '@/components/ui/cream-components';
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
      const split = Math.floor(remainingTotal / otherKeys.length);
      let remainder = remainingTotal % otherKeys.length;
      
      otherKeys.forEach(k => {
        newWeights[k] = split + (remainder > 0 ? 1 : 0);
        remainder--;
      });
    } else {
      let distributed = 0;
      otherKeys.forEach((k, index) => {
        if (index === otherKeys.length - 1) {
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
    <CreamCard className="p-0 relative max-w-md w-full bg-white shadow-xl overflow-hidden ring-1 ring-black/5">
      <div className="bg-cream-50 p-4 border-b border-cream-100 flex items-center justify-between">
         <h3 className="text-sm font-black text-cream-900">綜合評分權重設定</h3>
         <div className="flex items-center gap-2">
            <button 
              onClick={resetWeights}
              className="p-1.5 rounded-full hover:bg-cream-200 text-apricot-500 transition-colors"
              title="重置"
            >
              <RotateCcw size={14} />
            </button>
            {onClose && (
              <button 
                onClick={onClose} 
                className="p-1.5 rounded-full hover:bg-cream-200 text-cream-400 transition-colors"
              >
                <X size={16} />
              </button>
            )}
         </div>
      </div>
      
      <div className="p-6 space-y-5">
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
        
        <div className="pt-2">
          <p className="text-[10px] text-cream-400 text-center leading-relaxed">
            調整任一數值時，系統會自動平衡其他權重以維持總和 100%
          </p>
        </div>
      </div>
    </CreamCard>
  );
};