// utils/fileStorage.ts
import fs from 'fs/promises';
import path from 'path';

const UPLOAD_DIR = path.join(__dirname, '../uploads'); // Create an 'uploads' directory

export async function saveFile(file: Express.Multer.File): Promise<string> {
  const filePath = path.join(UPLOAD_DIR, file.originalname);
  await fs.writeFile(filePath, file.buffer);
  return filePath;
}