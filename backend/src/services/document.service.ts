// services/documentService.ts
import { summarizeText } from './bartService';
import { getEntities } from './nerService';
import { getEmbedding } from '../utils/embedding';
import { getTopics } from './bertopicService';
import pool from '../utils/db';

export async function processDocument(text: string, title: string, metadata: any) {
  const summary = await summarizeText(text);
  const entities = await getEntities(text);
  const embedding = await getEmbedding(text);
  const topics = await getTopics([embedding]);

  const connection = await pool.getConnection();
  try {
    const [result] = await connection.execute<any>(
      'INSERT INTO documents (title, text, metadata, summary, entities, embeddings, topics) VALUES (?, ?, ?, ?, ?, ?, ?)',
      [title, text, JSON.stringify(metadata), summary, JSON.stringify(entities), JSON.stringify(embedding), JSON.stringify(topics)]
    );
    return result.insertId;
  } finally {
    connection.release();
  }
}