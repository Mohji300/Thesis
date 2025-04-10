// services/bartService.ts
import { huggingFaceAPI } from '../utils/apiClient';

export async function summarizeText(text: string): Promise<string> {
  const response = await huggingFaceAPI.post('facebook/bart-large-cnn', { inputs: text });
  return response.data[0].summary_text;
}