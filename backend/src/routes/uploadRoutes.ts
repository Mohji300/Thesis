import { Router } from 'express';
import multer from 'multer';
import { handleFileUploadRequest } from '../controllers/uploadController';

const router = Router();
const upload = multer({ dest: 'uploads/' });

router.post('/upload', upload.single('file'), handleFileUploadRequest);

export default router;
