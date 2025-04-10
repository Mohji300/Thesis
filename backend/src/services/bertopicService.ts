// services/bertopicService.ts
import { pythonMicroserviceAPI } from '../utils/apiClient';

export async function getTopics(embeddings: number[][]): Promise<number[]> {
  const response = await pythonMicroserviceAPI.post('/topics/', { embeddings });
  return response.data.topics;
}