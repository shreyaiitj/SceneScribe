import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  HiOutlineDocumentText,
  HiOutlineEmojiHappy,
  HiOutlineChip,
  HiOutlineSparkles,
} from 'react-icons/hi';
import { HiCheck } from 'react-icons/hi2';
import type { CaptionResult } from '../types';
import ConfidenceBar from './ConfidenceBar';

interface CaptionCardProps {
  caption: CaptionResult;
  index: number;
}

const iconMap: Record<string, React.ReactNode> = {
  formal: <HiOutlineDocumentText className="w-5 h-5" />,
  sarcastic: <HiOutlineEmojiHappy className="w-5 h-5" />,
  humorous_tech: <HiOutlineChip className="w-5 h-5" />,
  humorous_non_tech: <HiOutlineSparkles className="w-5 h-5" />,
};

const badgeColors: Record<string, string> = {
  formal: 'bg-primary/20 text-primary',
  sarcastic: 'bg-secondary/20 text-secondary',
  humorous_tech: 'bg-cyan/20 text-cyan',
  humorous_non_tech: 'bg-purple/20 text-purple',
};

const toneFonts: Record<string, string> = {
  formal: 'font-sans',
  sarcastic: 'font-sans italic',
  humorous_tech: 'font-mono',
  humorous_non_tech: 'font-sans',
};

export default function CaptionCard({ caption, index }: CaptionCardProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(caption.text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      const textarea = document.createElement('textarea');
      textarea.value = caption.text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.15, ease: 'easeOut' }}
      className="glass rounded-2xl p-5 flex flex-col gap-4 group"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <span className="w-9 h-9 rounded-xl bg-surface flex items-center justify-center text-foreground/70">
            {iconMap[caption.style]}
          </span>
          <span
            className={`text-xs font-semibold px-2.5 py-1 rounded-full ${badgeColors[caption.style]}`}
          >
            {caption.label}
          </span>
        </div>
      </div>

      <p
        className={`text-sm leading-relaxed text-foreground/80 flex-1 ${toneFonts[caption.style]}`}
      >
        {caption.text}
      </p>

      <ConfidenceBar score={caption.confidence} />

      <button
        onClick={handleCopy}
        className={`
          flex items-center justify-center gap-2 w-full py-2.5 rounded-xl text-sm font-medium
          transition-all duration-200 cursor-pointer
          focus-visible:outline-2 focus-visible:outline-ring focus-visible:outline-offset-2
          ${copied
            ? 'bg-success/20 text-success'
            : 'bg-surface text-foreground/70 hover:bg-white/10 hover:text-foreground'
          }
        `}
        aria-label={copied ? 'Caption copied' : `Copy ${caption.label} caption`}
      >
        {copied ? (
          <>
            <HiCheck className="w-4 h-4" />
            Copied!
          </>
        ) : (
          <>
            <svg
              className="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
              <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />
            </svg>
            Copy
          </>
        )}
      </button>
    </motion.div>
  );
}