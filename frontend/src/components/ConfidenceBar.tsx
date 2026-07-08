import { motion } from 'framer-motion';
import { getConfidenceColor, getConfidenceBgColor } from '../lib/utils';

interface ConfidenceBarProps {
  score: number;
}

export default function ConfidenceBar({ score }: ConfidenceBarProps) {
  const colorClass = getConfidenceColor(score);
  const bgColorClass = getConfidenceBgColor(score);

  return (
    <div className="group relative">
      <div className="flex items-center gap-3">
        <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
          <motion.div
            className={`h-full rounded-full ${bgColorClass}`}
            initial={{ width: 0 }}
            animate={{ width: `${score}%` }}
            transition={{ duration: 1, ease: 'easeOut', delay: 0.5 }}
          />
        </div>
        <span className={`text-sm font-semibold tabular-nums ${colorClass}`}>
          {score}%
        </span>
      </div>
      <div className="absolute -top-8 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none">
        <div className="bg-background border border-border text-foreground text-xs px-3 py-1.5 rounded-lg whitespace-nowrap shadow-lg">
          How confident the AI is about this caption
        </div>
      </div>
    </div>
  );
}