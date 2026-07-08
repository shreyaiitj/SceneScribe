import { useState, useCallback } from 'react';
import { AnimatePresence } from 'framer-motion';
import HeroSection from './components/HeroSection';
import UploadSection from './components/UploadSection';
import ResultsGrid from './components/ResultsGrid';
import HowItWorks from './components/HowItWorks';
import Footer from './components/Footer';
import type { CaptionResult, ProcessSummary } from './types';

export default function App() {
  const [captions, setCaptions] = useState<CaptionResult[] | null>(null);
  const [summary, setSummary] = useState<ProcessSummary | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleResults = useCallback(
    (results: CaptionResult[], processingSummary: ProcessSummary) => {
      setCaptions(results);
      setSummary(processingSummary);
    },
    []
  );

  const handleProcessingStart = useCallback(() => {
    setIsProcessing(true);
  }, []);

  const handleProcessingEnd = useCallback(() => {
    setIsProcessing(false);
  }, []);

  const handleNewUpload = useCallback(() => {
    setCaptions(null);
    setSummary(null);
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground font-sans">
      <HeroSection />

      <UploadSection
        onResults={handleResults}
        onProcessingStart={handleProcessingStart}
        onProcessingEnd={handleProcessingEnd}
      />

      <AnimatePresence mode="wait">
        {captions && summary && (
          <ResultsGrid
            key="results"
            captions={captions}
            summary={summary}
          />
        )}
      </AnimatePresence>

      {!captions && !isProcessing && <HowItWorks />}

      <Footer />
    </div>
  );
}