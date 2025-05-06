import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {
  private apiUrl = 'http://127.0.0.1:5000'; // Flask backend base URL

  constructor(private http: HttpClient) {}

  getApiUrl(): string {
    return this.apiUrl;
  }

  /**
   * Upload a PDF document to the backend.
   */
  uploadPdf(file: File, title: string, metadata: any = {}): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    formData.append('metadata', JSON.stringify(metadata));
    return this.http.post(`${this.apiUrl}/upload/document`, formData);
  }

  /*
   * Search documents in the database.
   */
  searchDocuments(query: string, top_k: number = 10): Observable<any> {
    return this.http.post(`${this.apiUrl}/query/search`, { query, top_k });
  }

  /*
   * Generate a summary for a given text.
   */
  generateSummary(text: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/summary/generate`, { text });
  }

  /*
   * Extract sections from a given text.
   */
  extractSections(text: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/extract/sections`, { text });
  }

  /*
   * Assign a cluster (topic) to the input text.
   */
  assignCluster(text: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/cluster/assign`, { text });
  }
}
