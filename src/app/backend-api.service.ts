import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {
  private apiUrl = 'http://127.0.0.1:5000'; // Flask backend base URL

  constructor(private http: HttpClient) {}

  //Matches: POST /upload/document
  uploadPdf(file: File, title: string, metadata: any = {}): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    formData.append('metadata', JSON.stringify(metadata));
    return this.http.post(`${this.apiUrl}/upload/document`, formData);
  }

  //POST /query/search
  searchDocuments(query: string, top_k: number = 10): Observable<any> {
    return this.http.post(`${this.apiUrl}/query/search`, { query, top_k });
  }

  //POST /summary
  summarizeSection(text: string, section: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/summary`, { text, section });
  }

  //POST /extract
  extractSections(text: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/extract`, { text });
  }

  //POST /cluster
  clusterTopics(texts: string[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/cluster`, { texts });
  }
}
