// utils/apiClient.ts
import axios from 'axios';

const HUGGING_FACE_API_TOKEN = 'YOUR_HUGGING_FACE_API_TOKEN'; // Replace with your token

export const huggingFaceAPI = axios.create({
  baseURL: 'https://api-inference.huggingface.co/models/',
  headers: { Authorization: `Bearer ${HUGGING_FACE_API_TOKEN}` },
});

export const pythonMicroserviceAPI = axios.create({
  baseURL: 'http://localhost:8000', // Assuming your Python microservice runs on port 8000
});