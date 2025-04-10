// utils/pdfParser.ts
import fs from 'fs/promises';
import pdfParse from 'pdf-parse';

export async function parsePdf(filePath: string): Promise<string> {
  const dataBuffer = await fs.readFile(filePath);
  const data = await pdfParse(dataBuffer);
  return data.text;
}