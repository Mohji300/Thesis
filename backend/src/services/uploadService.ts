// services/uploadService.ts
import { saveFile } from '../utils/fileStorage';
import { parsePdf } from '../utils/pdfParser';
import { processDocument } from './document.service';

export async function handleFileUpload(file: Express.Multer.File, title: string, metadata: any) {
  const filePath = await saveFile(file);
  const text = await parsePdf(filePath);
  return processDocument(text, title, metadata);
}