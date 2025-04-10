// utils/embedding.ts
import { pythonMicroserviceAPI } from './apiClient';

export async function getEmbedding(text: string): Promise<number[]> {
  const response = await pythonMicroserviceAPI.post('/embed/', { text });
  return response.data.embedding;
}