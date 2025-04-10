// controllers/uploadController.ts
import { Request, Response } from 'express';
import { handleFileUpload } from '../services/uploadService';

export async function handleFileUploadRequest(req: Request, res: Response) {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }
    const title = req.body.title;
    const metadata = req.body.metadata;
    const documentId = await handleFileUpload(req.file, title, metadata);
    res.json({ documentId });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}