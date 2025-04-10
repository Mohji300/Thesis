// services/nerService.ts
import { huggingFaceAPI } from '../utils/apiClient';

export async function getEntities(text: string): Promise<any[]> {
  const response = await huggingFaceAPI.post('dslim/bert-base-NER', { inputs: text });
  return response.data;
}