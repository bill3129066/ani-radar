import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function normalizeRating(rating: number, scale: '1-5' | '0-10'): number {
  if (scale === '1-5') {
    return rating * 2; // Convert to 0-10
  }
  return rating;
}

export function formatNumber(num?: number): string {
  if (num === undefined || num === null) return '-';
  if (num >= 10000) {
    return `${(num / 10000).toFixed(1)}W`;
  }
  if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`;
  }
  return num.toString();
}
