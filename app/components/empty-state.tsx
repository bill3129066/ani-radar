'use client';

import React from 'react';
import { Radar } from 'lucide-react';
import { CreamButton } from '@/components/ui/cream-components';

interface EmptyStateProps {
  onReset: () => void;
}

export function EmptyState({ onReset }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center animate-in fade-in zoom-in duration-500">
      <div className="bg-white p-8 rounded-full shadow-float mb-6 relative overflow-hidden group">
         <Radar size={64} className="text-apricot-300 group-hover:text-apricot-400 transition-colors" />
         <div className="absolute inset-0 bg-apricot-100/30 scale-0 group-hover:scale-100 rounded-full transition-transform duration-500"></div>
      </div>
      <h3 className="text-2xl font-black text-cream-900 mb-2">找不到相關動畫</h3>
      <p className="text-cream-500 font-medium max-w-xs mb-8">
        目前的篩選條件沒有任何結果。<br/>試著放寬一些條件吧？
      </p>
      <CreamButton 
        variant="primary" 
        onClick={onReset}
        className="shadow-lg hover:shadow-xl hover:scale-105"
      >
        清除所有篩選
      </CreamButton>
    </div>
  );
}
