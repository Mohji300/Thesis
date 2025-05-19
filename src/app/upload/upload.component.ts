import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BackendApiService } from '../backend-api.service';
@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent {
  title: string = ''; // Holds the document title
  metadata: string = ''; // Holds the metadata as a JSON string
  selectedFile: File | null = null; // Holds the selected file
  isLoading: boolean = false; // Loading state for API calls
  successMessage: string = ''; // Success message
  errorMessage: string = ''; // Error message

  constructor(
    private backendApiService: BackendApiService,
    private http: HttpClient,
    private router: Router
  ) {}

  /**
   * Handles file selection.
   */
  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.errorMessage = ''; // Clear any previous error
    }
  }

  /**
   * Uploads the document to the backend.
   */
  uploadDocument() {
    if (!this.selectedFile) {
      this.errorMessage = 'Please select a file to upload.';
      return;
    }
  
    if (!this.title.trim()) {
      alert('Please provide a title for the document.');
      return;
    }
  
    if (!this.metadata.trim()) {
      alert('Please provide metadata for the document.');
      return;
    }
  
    this.isLoading = true;
    this.successMessage = '';
    this.errorMessage = '';
  
    const formData = new FormData();
    formData.append('file', this.selectedFile);
    formData.append('title', this.title || 'Untitled');
    formData.append('metadata', this.metadata || '{}');
  
    // Correctly call getApiUrl()
    this.http.post(`${this.backendApiService.getApiUrl()}/upload/document`, formData).subscribe(
      (response: any) => {
        this.successMessage = `Document uploaded successfully! Document ID: ${response.document_id}`;
        this.isLoading = false;
        this.resetForm();
      },
      (error) => {
        console.error('Error uploading document:', error);
        this.errorMessage = 'Failed to upload document. Please try again.';
        this.isLoading = false;
      }
    );
  }

goToHome() {
  localStorage.removeItem('auth_token');
  this.router.navigate(['/']);
}

logout() {
  localStorage.removeItem('auth_token');
  this.router.navigate(['/login']);
}

  /**
   * Resets the form after a successful upload.
   */
  resetForm() {
    this.title = '';
    this.metadata = '';
    this.selectedFile = null;
  }
}
