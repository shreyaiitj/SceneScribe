import type { CaptionStyle, CaptionResult } from '../types';

export function generateConfidence(style: CaptionStyle, text: string): number {
  let hash = 0;
  for (let i = 0; i < text.length; i++) {
    hash = ((hash << 5) - hash) + text.charCodeAt(i);
    hash |= 0;
  }

  const base = Math.abs(hash) % 25;
  const styleBonus: Record<CaptionStyle, number> = {
    formal: 10,
    sarcastic: 5,
    humorous_tech: 8,
    humorous_non_tech: 6,
  };

  const score = 65 + base + styleBonus[style];
  return Math.min(99, Math.max(60, score));
}

export function mapCaptionsToResults(
  captions: Record<CaptionStyle, string>
): CaptionResult[] {
  const styles: { style: CaptionStyle; label: string; icon: string }[] = [
    { style: 'formal', label: 'Formal', icon: 'formal' },
    { style: 'sarcastic', label: 'Sarcastic', icon: 'sarcastic' },
    { style: 'humorous_tech', label: 'Humorous Tech', icon: 'humorous_tech' },
    { style: 'humorous_non_tech', label: 'Humorous Non-Tech', icon: 'humorous_non_tech' },
  ];

  return styles.map(({ style, label, icon }) => ({
    style,
    label,
    icon,
    text: captions[style],
    confidence: generateConfidence(style, captions[style]),
  }));
}

export function formatDuration(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return mins > 0 ? `${mins}m ${secs}s` : `${secs.toFixed(1)}s`;
}

export function formatNumber(num: number): string {
  return num.toLocaleString();
}

export function getConfidenceColor(score: number): string {
  if (score >= 70) return 'text-success';
  if (score >= 50) return 'text-warning';
  return 'text-destructive';
}

export function getConfidenceBgColor(score: number): string {
  if (score >= 70) return 'bg-success';
  if (score >= 50) return 'bg-warning';
  return 'bg-destructive';
}