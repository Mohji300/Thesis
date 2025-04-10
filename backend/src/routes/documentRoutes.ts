// routes/documentRoutes.ts
import express from 'express';
import multer from 'multer';
import { handleFileUploadRequest } from '../controllers/uploadController';

const router = express.Router();
const upload = multer(); // For handling file uploads

router.post('/upload', upload.single('file'), handleFileUploadRequest);

export default router;