import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { BackendApiService } from '../backend-api.service';

@Component({
  selector: 'app-summary',
  standalone: true,
  templateUrl: './summary.component.html',
  styleUrl: './summary.component.css',
  imports: [CommonModule],
})
export class SummaryComponent implements OnInit, OnDestroy {
  currentDateTime: string = '';
  private timeInterval: any;
  sections: string[] = []; // Holds the extracted section names
  sectionContent: { [key: string]: string } = {}; // Holds the content of each section
  selectedSection: string = ''; // Holds the currently selected section for summarization
  summarizedContent: string = ''; // Holds the summarized content of the selected section
  isLoading: boolean = false; // Loading state for API calls
  errorMessage: string = ''; // Error message for API failures

  // New properties for title, authors, and abstract
  title: string = '';
  author: string = '';
  abstract: string = '';

  constructor(private backendApiService: BackendApiService, private route: ActivatedRoute) {}

  ngOnInit() {
    this.updateCurrentTime();
    this.timeInterval = setInterval(() => {
      this.updateCurrentTime();
    }, 1000);

    // Fetch the document ID from the route parameters
    this.route.params.subscribe((params) => {
      const documentId = params['id'];
      if (documentId) {
        this.fetchDocumentDetails(documentId); // Fetch document details (title, authors, abstract)
        this.fetchSections(documentId); // Fetch sections and their content
      }
    });
  }

  ngOnDestroy() {
    if (this.timeInterval) {
      clearInterval(this.timeInterval);
    }
  }

  private updateCurrentTime() {
    this.currentDateTime = new Date().toLocaleString();
  }

  /**
   * Fetches the document details (title, authors, abstract) from the backend.
   */
  fetchDocumentDetails(documentId: number) {
    this.backendApiService.getDocumentDetails(documentId).subscribe(
      (response) => {
        this.title = response.title;
        this.author = response.author;
        this.abstract = response.abstract;
        console.log('Fetched document details:', response);
      },
      (error) => {
        console.error('Error fetching document details:', error);
        this.errorMessage = 'Failed to fetch document details. Please try again.';
      }
    );
  }

  /**
   * Fetches the sections and their content from the backend.
   */
  fetchSections(documentId: number) {
    this.isLoading = true;
    this.errorMessage = '';
    this.backendApiService.getDocumentSections(documentId).subscribe(
      (response) => {
        this.sections = Object.keys(response.sections); // Extract section names
        this.sectionContent = response.sections; // Store section content
        console.log('Fetched sections:', this.sections);
        console.log('Fetched section content:', this.sectionContent);
        this.isLoading = false;
      },
      (error) => {
        console.error('Error fetching sections:', error);
        this.errorMessage = 'Failed to fetch sections. Please try again.';
        this.isLoading = false;
      }
    );
  }

  /**
   * Handles summarizing a specific section.
   */
  summarizeSection(section: string) {
    this.selectedSection = section;
    const sectionText = this.sectionContent[section]; // Get the content of the selected section
    if (!sectionText) {
      console.error('No content found for the selected section.');
      this.errorMessage = 'No content found for the selected section.';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.backendApiService.generateSummary(sectionText).subscribe(
      (response) => {
        this.summarizedContent = response.summary; // Store the summarized content
        console.log(`Summarized section (${section}):`, this.summarizedContent);
        this.isLoading = false;
      },
      (error) => {
        console.error('Error summarizing section:', error);
        this.errorMessage = 'Failed to summarize the section. Please try again.';
        this.isLoading = false;
      }
    );
  }
}