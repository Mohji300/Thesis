import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { BackendApiService } from '../backend-api.service';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent {
  title: string = '';
  authors: string = ''; // Single text field for authors
  selectedFile: File | null = null;
  isLoading: boolean = false;
  successMessage: string = '';
  errorMessage: string = '';

  constructor(private backendApiService: BackendApiService, private http: HttpClient) {}

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.errorMessage = '';
    }
  }

  uploadDocument() {
    if (!this.selectedFile) {
      this.errorMessage = 'Please select a file to upload.';
      return;
    }

    if (!this.title.trim()) {
      alert('Please provide a title for the document.');
      return;
    }

    const authorsArray = this.authors
      .split(',')
      .map((author) => author.trim())
      .filter((author) => author.length > 0);

    if (authorsArray.length === 0) {
      alert('Please provide at least one author.');
      return;
    }

    if (authorsArray.length > 5) {
      alert('You can only provide up to 5 authors.');
      return;
    }

    const metadataJson = JSON.stringify({ authors: authorsArray });

    this.isLoading = true;
    this.successMessage = '';
    this.errorMessage = '';

    const formData = new FormData();
    formData.append('file', this.selectedFile);
    formData.append('title', this.title);
    formData.append('metadata', metadataJson);

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

  resetForm() {
    this.title = '';
    this.authors = '';
    this.selectedFile = null;
  }
}
