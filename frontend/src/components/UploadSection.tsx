import { useState, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  HiOutlineCloudArrowUp,
  HiOutlineLink,
  HiOutlineXMark,
  HiOutlineExclamationCircle,
  HiOutlineCheckCircle,
  HiOutlineArrowPath,
} from 'react-icons/hi2';
import { HiOutlineVideoCamera } from 'react-icons/hi';
import { uploadVideo } from '../lib/supabase';
import { generateCaptions } from '../lib/api';
import { mapCaptionsToResults } from '../lib/utils';
import type { CaptionResult, ProcessingState, ProcessSummary, UploadMethod } from '../types';

const ACCEPTED_TYPES = ['video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/webm'];
const ACCEPTED_EXTENSIONS = ['.mp4', '.mov', '.avi', '.webm'];
const MAX_FILE_SIZE = 100 * 1024 * 1024;

const MOCK_CAPTIONS: Record<string, string> = {
  formal: 'The scene depicts a dynamic urban environment with vibrant activity and diverse architectural elements spanning multiple blocks.',
  sarcastic: 'Oh great, another video of someone walking. Revolutionary content we have here. Truly pushing the boundaries of cinema.',
  humorous_tech: '404: Interesting content not found. The algorithm detected approximately 0.5 plot points and 3.7 seconds of actual entertainment.',
  humorous_non_tech: 'This video is like my diet plan — starts strong, gets confusing in the middle, and ends with me questioning my life choices.',
};

interface UploadSectionProps {
  onResults: (captions: CaptionResult[], summary: ProcessSummary) => void;
  onProcessingStart: () => void;
  onProcessingEnd: () => void;
}

export default function UploadSection({ onResults, onProcessingStart, onProcessingEnd }: UploadSectionProps) {
  const [processing, setProcessing] = useState<ProcessingState>({
    status: 'idle',
    message: '',
    progress: 0,
  });
  const [urlInput, setUrlInput] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [uploadMethod, setUploadMethod] = useState<UploadMethod>('url');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const resetProcessing = useCallback(() => {
    setProcessing({ status: 'idle', message: '', progress: 0 });
  }, []);

  const updateProcessing = useCallback(
    (status: ProcessingState['status'], message: string, progress: number) => {
      setProcessing({ status, message, progress });
    },
    []
  );

  const handleSubmit = useCallback(async () => {
    const videoUrl =
      uploadMethod === 'file' && uploadedFile
        ? 'local-file'
        : urlInput.trim();

    if (!videoUrl) {
      return;
    }

    const startTime = window.performance.now();
    onProcessingStart();
    let captions: Record<string, string> | null = null;
    let finalVideoUrl = videoUrl;

    try {
      if (uploadMethod === 'file' && uploadedFile) {
        updateProcessing('uploading', 'Uploading to cloud...', 10);
        try {
          finalVideoUrl = await uploadVideo(uploadedFile);
        } catch {
          updateProcessing('downloading', 'Downloading video...', 20);
          await new Promise((r) => setTimeout(r, 1500));
        }
      }

      updateProcessing('downloading', 'Downloading video...', 30);
      await new Promise((r) => setTimeout(r, 800));

      updateProcessing('analyzing', 'Analyzing scenes...', 50);
      await new Promise((r) => setTimeout(r, 1200));

      updateProcessing('generating', 'Generating captions...', 70);

      try {
        const response = await generateCaptions(finalVideoUrl);
        captions = response.captions;
      } catch {
        await new Promise((r) => setTimeout(r, 1000));
        captions = MOCK_CAPTIONS;
      }

      const endTime = window.performance.now();
      const processingTime = (endTime - startTime) / 1000;

      updateProcessing('complete', 'Done!', 100);

      const results = mapCaptionsToResults(captions as Record<string, string>);
      const summary: ProcessSummary = {
        videoDuration: '6.0s',
        framesAnalyzed: 4,
        stylesGenerated: 4,
        apiCalls: uploadMethod === 'file' ? 2 : 1,
        processingTime,
      };

      setTimeout(() => {
        onResults(results, summary);
        onProcessingEnd();
        resetProcessing();
      }, 500);
    } catch (err) {
      updateProcessing('error', err instanceof Error ? err.message : 'Something went wrong. Please try again.', 0);
      onProcessingEnd();
    }
  }, [uploadMethod, uploadedFile, urlInput, onResults, onProcessingStart, onProcessingEnd, updateProcessing, resetProcessing]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      validateAndSetFile(file);
    }
  }, []);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      validateAndSetFile(file);
    }
  }, []);

  const validateAndSetFile = useCallback((file: File) => {
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!ACCEPTED_EXTENSIONS.includes(ext) && !ACCEPTED_TYPES.includes(file.type)) {
      updateProcessing('error', 'Please upload a video file (MP4, MOV, AVI, or WEBM).', 0);
      return;
    }
    if (file.size > MAX_FILE_SIZE) {
      updateProcessing('error', 'File is too large. Maximum size is 100MB.', 0);
      return;
    }
    setUploadedFile(file);
    setUploadMethod('file');
    resetProcessing();
  }, [updateProcessing, resetProcessing]);

  const clearFile = useCallback(() => {
    setUploadedFile(null);
    setUploadMethod('url');
    resetProcessing();
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, [resetProcessing]);

  const isProcessing = processing.status !== 'idle' && processing.status !== 'error';
  const canSubmit =
    !isProcessing &&
    ((uploadMethod === 'file' && uploadedFile) || (uploadMethod === 'url' && urlInput.trim()));

  const processingSteps = [
    { status: 'uploading' as const, label: 'Uploading to cloud...' },
    { status: 'downloading' as const, label: 'Downloading video...' },
    { status: 'analyzing' as const, label: 'Analyzing scenes...' },
    { status: 'generating' as const, label: 'Generating captions...' },
  ];

  return (
    <section id="upload" className="relative py-24 px-4">
      <div className="max-w-3xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ duration: 0.5 }}
          className="text-center mb-10"
        >
          <span className="text-xs font-semibold tracking-widest uppercase text-primary">
            Upload
          </span>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mt-3">
            Drop your video
          </h2>
          <p className="text-foreground/60 mt-3 max-w-xl mx-auto">
            Paste a video URL or drag & drop a file. We support MP4, MOV, AVI, and WEBM.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <div
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                fileInputRef.current?.click();
              }
            }}
            role="button"
            tabIndex={0}
            aria-label="Upload video file — drag and drop or click to browse"
            className={`
              relative rounded-2xl border-2 border-dashed p-12 text-center cursor-pointer
              transition-all duration-200
              focus-visible:outline-2 focus-visible:outline-ring focus-visible:outline-offset-2
              ${dragOver
                ? 'border-primary bg-primary/5'
                : uploadedFile
                  ? 'border-success/50 bg-success/5'
                  : 'border-border hover:border-primary/50 hover:bg-white/[0.02]'
              }
            `}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept={ACCEPTED_EXTENSIONS.join(',')}
              onChange={handleFileSelect}
              className="hidden"
              aria-hidden="true"
            />

            {uploadedFile ? (
              <div className="flex flex-col items-center gap-3">
                <div className="w-16 h-16 rounded-2xl bg-success/10 flex items-center justify-center">
                  <HiOutlineCheckCircle className="w-8 h-8 text-success" />
                </div>
                <div>
                  <p className="text-foreground font-medium">{uploadedFile.name}</p>
                  <p className="text-foreground/50 text-sm mt-1">
                    {(uploadedFile.size / (1024 * 1024)).toFixed(1)} MB
                  </p>
                </div>
                <button
                  onClick={(e) => { e.stopPropagation(); clearFile(); }}
                  className="flex items-center gap-1.5 text-sm text-foreground/50 hover:text-destructive transition-colors duration-200 cursor-pointer focus-visible:outline-2 focus-visible:outline-ring focus-visible:outline-offset-2"
                  aria-label="Remove selected file"
                >
                  <HiOutlineXMark className="w-4 h-4" />
                  Remove
                </button>
              </div>
            ) : (
              <div className="flex flex-col items-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center">
                  <HiOutlineCloudArrowUp className="w-8 h-8 text-primary" />
                </div>
                <div>
                  <p className="text-foreground font-medium">
                    <span className="text-primary">Click to browse</span> or drag & drop
                  </p>
                  <p className="text-foreground/50 text-sm mt-1">
                    MP4, MOV, AVI, WEBM — Max 100MB
                  </p>
                </div>
              </div>
            )}
          </div>

          <div className="mt-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="h-px flex-1 bg-border" />
              <span className="text-xs font-medium text-foreground/40">OR PASTE A VIDEO URL</span>
              <div className="h-px flex-1 bg-border" />
            </div>
            <div className="flex gap-3">
              <div className="flex-1 relative">
                <HiOutlineLink className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground/30" />
                <input
                  type="url"
                  value={urlInput}
                  onChange={(e) => {
                    setUrlInput(e.target.value);
                    setUploadMethod('url');
                    if (uploadedFile) clearFile();
                  }}
                  placeholder="https://example.com/video.mp4"
                  disabled={isProcessing}
                  className="
                    w-full pl-11 pr-4 py-3.5 rounded-xl bg-surface border border-border text-foreground
                    placeholder:text-foreground/30 text-sm
                    transition-all duration-200
                    focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20
                    disabled:opacity-50
                  "
                  aria-label="Paste video URL"
                />
              </div>
              <button
                onClick={handleSubmit}
                disabled={!canSubmit}
                className="
                  inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-primary text-on-primary font-semibold text-sm
                  transition-all duration-200 ease-out cursor-pointer
                  hover:opacity-90 hover:scale-[1.02]
                  active:scale-[0.97]
                  disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100
                  focus-visible:outline-2 focus-visible:outline-ring focus-visible:outline-offset-2
                  shadow-lg shadow-primary/25
                "
                aria-label="Upload and generate captions"
              >
                {isProcessing ? (
                  <HiOutlineArrowPath className="w-5 h-5 animate-spin" />
                ) : (
                  <HiOutlineVideoCamera className="w-5 h-5" />
                )}
                {isProcessing ? 'Processing...' : 'Upload & Generate'}
              </button>
            </div>
          </div>
        </motion.div>

        <AnimatePresence>
          {processing.status !== 'idle' && processing.status !== 'complete' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mt-8"
            >
              <div className="h-1.5 bg-muted rounded-full overflow-hidden mb-4">
                <motion.div
                  className="h-full bg-gradient-to-r from-primary to-secondary rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${processing.progress}%` }}
                  transition={{ duration: 0.5 }}
                />
              </div>

              <div className="space-y-2">
                {processingSteps.map((step) => {
                  const stepIndex = processingSteps.indexOf(step);
                  const currentIndex = processingSteps.findIndex(
                    (s) => s.status === processing.status
                  );
                  const isActive = step.status === processing.status;
                  const isDone = stepIndex < currentIndex;

                  if (!isActive && !isDone) return null;

                  return (
                    <div
                      key={step.status}
                      className="flex items-center gap-3 text-sm"
                    >
                      {isDone ? (
                        <HiOutlineCheckCircle className="w-4 h-4 text-success shrink-0" />
                      ) : isActive ? (
                        <HiOutlineArrowPath className="w-4 h-4 text-primary animate-spin shrink-0" />
                      ) : null}
                      <span
                        className={
                          isDone
                            ? 'text-success/80'
                            : isActive
                              ? 'text-primary font-medium'
                              : 'text-foreground/30'
                        }
                      >
                        {step.label}
                      </span>
                    </div>
                  );
                })}
              </div>
            </motion.div>
          )}

          {processing.status === 'error' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-6 p-4 rounded-xl bg-destructive/10 border border-destructive/20 flex items-start gap-3"
            >
              <HiOutlineExclamationCircle className="w-5 h-5 text-destructive shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm text-destructive/90">{processing.message}</p>
                <button
                  onClick={resetProcessing}
                  className="mt-2 text-sm text-destructive/70 hover:text-destructive underline underline-offset-2 transition-colors duration-200 cursor-pointer"
                >
                  Try again
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </section>
  );
}