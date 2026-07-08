export type CaptionStyle = 'formal' | 'sarcastic' | 'humorous_tech' | 'humorous_non_tech';

export interface CaptionResult {
  style: CaptionStyle;
  label: string;
  text: string;
  icon: string;
  confidence: number;
}

export interface ApiResponse {
  task_id: string;
  captions: Record<CaptionStyle, string>;
}

export interface ProcessingState {
  status: 'idle' | 'uploading' | 'downloading' | 'analyzing' | 'generating' | 'complete' | 'error';
  message: string;
  progress: number;
}

export interface ProcessSummary {
  videoDuration: string;
  framesAnalyzed: number;
  stylesGenerated: number;
  apiCalls: number;
  processingTime: number;
}

export type UploadMethod = 'file' | 'url';