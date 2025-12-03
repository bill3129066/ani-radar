export function formatNumber(num: number): string {
  if (!num) return '0';
  if (num >= 10000) {
    return (num / 10000).toFixed(1).replace(/\.0$/, '') + '萬';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'k';
  }
  return num.toString();
}

export function cn(...classes: (string | undefined | null | false)[]) {
  return classes.filter(Boolean).join(' ');
}

export function normalizeRating(score: number, scale: '1-5' | '0-10' = '0-10'): number {
  if (scale === '1-5') {
    return score * 2;
  }
  return score;
}