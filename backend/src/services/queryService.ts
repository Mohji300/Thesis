// services/queryService.ts
import { getEmbedding } from '../utils/embedding';
import pool from '../utils/db';

export async function performSemanticSearch(query: string, topK: number = 10) {
  const queryEmbedding = await getEmbedding(query);
  const connection = await pool.getConnection();
  try {
    const [rows] = await connection.execute(
      `SELECT *, SQRT(POW(?, embeddings[0] - ?) + POW(?, embeddings[1] - ?)) AS distance FROM documents ORDER BY distance LIMIT ?`,
      [queryEmbedding[0], queryEmbedding[0], queryEmbedding[1], queryEmbedding[1], topK] // Assuming 2D embeddings for simplicity
    );
    return rows;
  } finally {
    connection.release();
  }
}