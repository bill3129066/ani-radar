'use client';

import React from 'react';
import { cn } from '@/lib/utils'; // Assuming standard shadcn utils exist

// Soft Card with floating shadow
export const CreamCard = ({ 
  children, 
  className = '', 
  onClick 
}: { 
  children: React.ReactNode, 
  className?: string, 
  onClick?: () => void 
}) => {
  return (
    <div 
      onClick={onClick}
      className={cn(
        "bg-white/80 backdrop-blur-md rounded-3xl shadow-float border border-white/50 transition-all duration-300 hover:transform hover:-translate-y-1 hover:shadow-[0_15px_30px_rgba(0,0,0,0.07)]",
        className
      )}
    >
      {children}
    </div>
  );
};

// Button with "Apricot" gradient or simple soft style
export const CreamButton = ({ 
  children, 
  variant = 'primary', 
  onClick, 
  className = '',
  disabled = false
}: { 
  children: React.ReactNode, 
  variant?: 'primary' | 'secondary' | 'ghost', 
  onClick?: () => void, 
  className?: string,
  disabled?: boolean
}) => {
  const baseStyle = "px-6 py-3 rounded-full font-bold transition-all duration-300 flex items-center justify-center gap-2 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed";
  
  const variants = {
    primary: "bg-gradient-to-r from-apricot-400 to-apricot-500 text-white shadow-[0_4px_14px_rgba(255,159,89,0.4)] hover:shadow-[0_6px_20px_rgba(255,159,89,0.6)] hover:brightness-105",
    secondary: "bg-white text-cream-900 shadow-soft hover:shadow-float border border-cream-200",
    ghost: "bg-transparent text-cream-600 hover:bg-cream-100/50"
  };

  return (
    <button 
      onClick={onClick} 
      disabled={disabled}
      className={cn(baseStyle, variants[variant], className)}
    >
      {children}
    </button>
  );
};

// Soft Pill Badge
export const CreamBadge = ({ 
  children, 
  color = 'gray',
  className = ''
}: { 
  children: React.ReactNode, 
  color?: 'gray' | 'apricot' | 'blue' | 'purple',
  className?: string
}) => {
  const colors = {
    gray: "bg-cream-200 text-cream-600",
    apricot: "bg-apricot-100 text-apricot-500",
    blue: "bg-blue-50 text-blue-500",
    purple: "bg-purple-50 text-purple-500",
  };
  return (
    <span className={cn("px-3 py-1 rounded-full text-xs font-bold", colors[color], className)}>
      {children}
    </span>
  );
};

// Input with "inner soft" shadow feel
export const CreamInput = ({ 
  value, 
  onChange, 
  placeholder, 
  icon,
  className = ''
}: { 
  value: string, 
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void, 
  placeholder: string, 
  icon?: React.ReactNode,
  className?: string
}) => {
  return (
    <div className={cn("relative group", className)}>
      {icon && (
        <div className="absolute left-4 top-1/2 -translate-y-1/2 text-cream-400 group-focus-within:text-apricot-500 transition-colors pointer-events-none">
          {icon}
        </div>
      )}
      <input
        type="text"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className={cn(
          "w-full bg-cream-50 pr-4 py-3 rounded-3xl border-none shadow-inner-soft text-cream-900 placeholder-cream-400 focus:ring-2 focus:ring-apricot-200 focus:bg-white transition-all outline-none",
          icon ? "pl-11" : "pl-4"
        )}
      />
    </div>
  );
};

// Cute Slider
export const CreamSlider = ({ 
  value, 
  onChange, 
  label, 
  color = 'apricot',
  max = 100,
  className = '',
  disabled = false
}: { 
  value: number, 
  onChange: (val: number) => void, 
  label?: string, 
  color?: string,
  max?: number,
  className?: string,
  disabled?: boolean
}) => {
  return (
    <div className={cn("mb-2", className)}>
      {label && (
        <div className="flex justify-between mb-2">
          <span className="text-sm font-bold text-cream-600">{label}</span>
          <span className="text-sm font-bold text-apricot-500 bg-apricot-100 px-2 py-0.5 rounded-lg">{value}%</span>
        </div>
      )}
      <input 
        type="range" 
        min="0" 
        max={max} 
        value={value} 
        disabled={disabled}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full h-2 bg-cream-200 rounded-lg appearance-none cursor-pointer accent-apricot-500 hover:accent-apricot-400 disabled:opacity-50"
      />
    </div>
  );
};
