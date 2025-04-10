// routes/queryRoutes.ts
import express from 'express';
import { handleQuery } from '../controllers/queryController';

const router = express.Router();

router.post('/query', handleQuery);

export default router;