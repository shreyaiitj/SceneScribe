import { motion } from 'framer-motion';
import { HiOutlineSparkles } from 'react-icons/hi2';
import type { CaptionResult, ProcessSummary as ProcessSummaryType } from '../types';
import CaptionCard from './CaptionCard';
import ProcessSummary from './ProcessSummary';

interface ResultsGridProps {
  captions: CaptionResult[];
  summary: ProcessSummaryType;
}

export default function ResultsGrid({ captions, summary }: ResultsGridProps) {
  return (
    <section className="relative py-24 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <span className="inline-flex items-center gap-2 text-xs font-semibold tracking-widest uppercase text-primary">
            <HiOutlineSparkles className="w-4 h-4" />
            Results
          </span>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mt-3">
            Your AI-generated captions
          </h2>
          <p className="text-foreground/60 mt-3 max-w-xl mx-auto">
            Each caption is scored by confidence. Click Copy to grab any caption for your content.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {captions.map((caption, i) => (
            <CaptionCard key={caption.style} caption={caption} index={i} />
          ))}
        </div>

        <div className="mt-8">
          <ProcessSummary summary={summary} />
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 1.5 }}
          className="text-center mt-10"
        >
          <button
            onClick={() => {
              document.getElementById('upload')?.scrollIntoView({ behavior: 'smooth' });
            }}
            className="inline-flex items-center gap-2 text-sm text-foreground/50 hover:text-primary transition-colors duration-200 cursor-pointer focus-visible:outline-2 focus-visible:outline-ring focus-visible:outline-offset-2"
          >
            Want to caption another video?
          </button>
        </motion.div>
      </div>
    </section>
  );
}