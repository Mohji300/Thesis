import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';

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
  searchDocuments(query: string, limit: number): Observable<any> {
    const payload = { query, limit };
    return this.http.post(`${this.getApiUrl()}/query/search`, payload);
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

  /**
   * Fetch the summary of a document by its ID.
   * Updated to include the `/query` prefix.
   */
  getDocumentSummary(documentId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/query/documents/${documentId}/summary`).pipe(
      catchError((error) => {
        console.error('Error fetching document summary:', error);
        return throwError(() => new Error('Failed to fetch document summary.'));
      })
    );
  }

  /**
   * Fetch the sections of a document by its ID.
   * Updated to include the `/query` prefix.
   */
  getDocumentSections(documentId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/query/documents/${documentId}/sections`).pipe(
      catchError((error) => {
        console.error('Error fetching document sections:', error);
        return throwError(() => new Error('Failed to fetch document sections.'));
      })
    );
  }

  /**
   * Fetch the details (title, authors, abstract) of a document by its ID.
   * Updated to include the `/query` prefix.
   */
  getDocumentDetails(documentId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/query/documents/${documentId}/details`).pipe(
      catchError((error) => {
        console.error('Error fetching document details:', error);
        return throwError(() => new Error('Failed to fetch document details.'));
      })
    );
  }
}