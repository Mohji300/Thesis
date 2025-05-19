// content.component.ts
import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router, RouterModule, ActivatedRoute } from '@angular/router';
import { BackendApiService } from '../backend-api.service';
import { InsightsCacheService } from '../services/insights-cache.service';

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
  documents: { title: string; abstract: string; id: number; similarity: number }[] = []; // Holds the list of documents
  isLoading: boolean = false; // Loading state for API calls
  errorMessage: string = ''; // Error message for API failures
  searchQuery: string = ''; // Holds the search query
  expandedAbstracts: { [id: number]: boolean } = {}; // Track expanded abstracts
  abstractPreviewLimit: number = 150; // Number of chars to show in preview
  insights: { [id: number]: string } = {};
  page: number = 1;
  pageSize: number = 10;

  constructor(private backendApiService: BackendApiService, private router: Router, private route: ActivatedRoute, private cache: InsightsCacheService) {}

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
      this.loadDocumentsAndInsights();
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

  get totalPages(): number {
  return Math.ceil(this.documents.length / this.pageSize);
}

get paginatedDocuments() {
  const start = (this.page - 1) * this.pageSize;
  return this.documents.slice(start, start + this.pageSize);
}

goToPage(page: number) {
  if (page >= 1 && page <= this.totalPages) {
    this.page = page;
  }
}

    /**
   * Loads documents and insights, using cache if available.
   */
  async loadDocumentsAndInsights() {
    // Use cache if query matches and data exists
    if (
      this.cache.lastQuery === this.searchQuery &&
      this.cache.documents.length > 0 &&
      Object.keys(this.cache.insights).length > 0
    ) {
      this.documents = this.cache.documents;
      this.insights = this.cache.insights;
      this.isLoading = false;
      this.errorMessage = '';
      return;
    }
    // Otherwise, fetch and generate
    await this.fetchDocuments();
  }

  /**
   * Fetches the list of documents based on the search query.
   */
  async fetchDocuments() {
    this.isLoading = true;
    this.errorMessage = '';

    this.backendApiService.searchDocuments(this.searchQuery, 10).subscribe(
      async (response) => {
        if (response.documents && response.documents.length > 0) {
          // Cosine similarity is already in [-1, 1], scale to [0, 1] for percentage
            this.documents = response.documents.map((doc: any) => ({
              ...doc,
              // similarity is already in [-1, 1], but backend now ensures it's >= 0.2
              similarity: doc.similarity !== undefined ? Math.pow(((doc.similarity + 1) / 2), 0.6) : 0
            }));
          this.expandedAbstracts = {};
          this.insights = {};
          for (const doc of this.documents) {
            await this.generateInsightFromBackendAsync(doc, this.searchQuery);
          }
                    // Cache results
          this.cache.documents = this.documents;
          this.cache.insights = this.insights;
          this.cache.lastQuery = this.searchQuery;
        } else {
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

  // Generate insight using backend summarizer
  // Helper to wrap the observable in a promise for sequential execution
  generateInsightFromBackendAsync(document: any, query: string): Promise<void> {
    const prompt = `
Given the following document abstract and the user's search query, generate a concise insight explaining how this document is relevant to the query.

Document Abstract: ${document.abstract}
User Query: ${query}
Insight:
    `;
    this.insights[document.id] = 'Generating insight...';
    return new Promise((resolve) => {
      this.backendApiService.generateSummary(prompt).subscribe(
        (response) => {
          this.insights[document.id] = response.summary;
          resolve();
        },
        (error) => {
          this.insights[document.id] = 'Failed to generate insight.';
          resolve();
        }
      );
    });
  }

  /**
   * Navigates to the summary page for the selected document.
   */
  navigateToSummary(documentId: number) {
    this.router.navigate(['/summary', documentId]);
  }

  toggleAbstract(id: number) {
    this.expandedAbstracts[id] = !this.expandedAbstracts[id];
  }
}