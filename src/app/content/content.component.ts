// content.component.ts
import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router, RouterModule, ActivatedRoute } from '@angular/router';
import { BackendApiService } from '../backend-api.service';

@Component({
  selector: 'app-content',
  standalone: true,
  imports: [FormsModule, RouterModule, CommonModule],
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.css']
})
export class ContentComponent implements OnInit, OnDestroy {
  currentDateTime: string = '';
  private timeInterval: any;
  documents: { title: string; abstract: string; id: number }[] = []; // Holds the list of documents
  isLoading: boolean = false; // Loading state for API calls
  errorMessage: string = ''; // Error message for API failures
  searchQuery: string = ''; // Holds the search query

  constructor(private backendApiService: BackendApiService, private router: Router, private route: ActivatedRoute) {}

  ngOnInit() {
    // Initialize the time immediately
    this.updateCurrentTime();
    // Update time every second
    this.timeInterval = setInterval(() => {
      this.updateCurrentTime();
    }, 1000);

    // Get the search query from the route parameters
    this.route.queryParams.subscribe((params) => {
      this.searchQuery = params['query'] || '';
      this.fetchDocuments();
    });
  }

  ngOnDestroy() {
    // Clean up interval when component is destroyed
    if (this.timeInterval) {
      clearInterval(this.timeInterval);
    }
  }

  private updateCurrentTime() {
    this.currentDateTime = new Date().toLocaleString();
  }

  /**
   * Fetches the list of documents based on the search query.
   */
  fetchDocuments() {
    this.isLoading = true;
    this.errorMessage = '';
    this.backendApiService.searchDocuments(this.searchQuery, 10).subscribe(
      (response) => {
        if (response.documents && response.documents.length > 0) {
          this.documents = response.documents;
          console.log('Fetched documents:', this.documents);
        } else {
          // Show a "Query not found" message if no documents are returned
          alert('Query not found. Please try a different search term.');
        }
        this.isLoading = false;
      },
      (error) => {
        console.error('Error fetching documents:', error);
        this.errorMessage = 'Failed to fetch documents. Please try again.';
        this.isLoading = false;
      }
    );
  }

  /**
   * Navigates to the summary page for the selected document.
   */
  navigateToSummary(documentId: number) {
    this.router.navigate(['/summary', documentId]);
  }
}