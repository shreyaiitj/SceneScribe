import { motion } from 'framer-motion';
import { HiOutlineClock, HiOutlineFilm, HiOutlineRectangleStack, HiOutlineServer, HiOutlineBolt } from 'react-icons/hi2';
import type { ProcessSummary as ProcessSummaryType } from '../types';

interface ProcessSummaryProps {
  summary: ProcessSummaryType;
}

const metrics = [
  {
    key: 'videoDuration',
    icon: <HiOutlineClock className="w-5 h-5" />,
    label: 'Duration',
    format: (v: string) => v,
  },
  {
    key: 'framesAnalyzed',
    icon: <HiOutlineFilm className="w-5 h-5" />,
    label: 'Frames',
    format: (v: number) => `${v} frames`,
  },
  {
    key: 'stylesGenerated',
    icon: <HiOutlineRectangleStack className="w-5 h-5" />,
    label: 'Styles',
    format: (v: number) => `${v} styles`,
  },
  {
    key: 'apiCalls',
    icon: <HiOutlineServer className="w-5 h-5" />,
    label: 'API Calls',
    format: (v: number) => `${v} calls`,
  },
  {
    key: 'processingTime',
    icon: <HiOutlineBolt className="w-5 h-5" />,
    label: 'Time',
    format: (v: number) => `${v.toFixed(1)}s`,
  },
] as const;

export default function ProcessSummary({ summary }: ProcessSummaryProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 1 }}
      className="glass rounded-2xl p-6"
    >
      <h3 className="text-sm font-semibold text-foreground/50 uppercase tracking-wider mb-5">
        Processing Summary
      </h3>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {metrics.map((metric) => {
          const value = summary[metric.key as keyof ProcessSummaryType];
          return (
            <div
              key={metric.key}
              className="flex flex-col items-center text-center gap-2 p-3 rounded-xl bg-surface"
            >
              <span className="text-foreground/40">{metric.icon}</span>
              <span className="text-2xl font-bold text-foreground">
                {metric.format(value as never)}
              </span>
              <span className="text-xs text-foreground/50">{metric.label}</span>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}