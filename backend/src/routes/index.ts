// routes/index.ts
import express from 'express';
import documentRoutes from './documentRoutes';
import queryRoutes from './queryRoutes';

const router = express.Router();

router.use('/documents', documentRoutes);
router.use('/queries', queryRoutes);

export default router;