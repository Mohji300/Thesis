// controllers/queryController.ts
import { Request, Response } from 'express';
import { performSemanticSearch } from '../services/queryService';

export async function handleQuery(req: Request, res: Response) {
  try {
    const query = req.body.query;
    const results = await performSemanticSearch(query);
    res.json(results);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}