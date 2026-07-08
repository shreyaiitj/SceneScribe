import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface GenerateCaptionsResponse {
  task_id: string;
  captions: {
    formal: string;
    sarcastic: string;
    humorous_tech: string;
    humorous_non_tech: string;
  };
}

export async function generateCaptions(
  videoUrl: string
): Promise<GenerateCaptionsResponse> {
  const { data } = await api.post<GenerateCaptionsResponse>(
    '/api/generate-captions',
    { video_url: videoUrl }
  );
  return data;
}

export async function healthCheck(): Promise<boolean> {
  try {
    const { status } = await api.get('/health');
    return status === 200;
  } catch {
    return false;
  }
}

export default api;