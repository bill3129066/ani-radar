import React from 'react';
import { Radar } from 'lucide-react';

export default function Loading() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-cream-200 gap-4">
      <div className="relative">
        <div className="bg-white p-6 rounded-full shadow-float animate-bounce">
          <Radar size={48} className="text-apricot-500 animate-pulse" />
        </div>
        <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-12 h-2 bg-black/10 rounded-full blur-sm animate-pulse"></div>
      </div>
      <h2 className="text-xl font-bold text-cream-600 animate-pulse">
        正在掃描動畫頻率...
      </h2>
    </div>
  );
}
