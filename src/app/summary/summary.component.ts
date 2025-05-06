import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { BackendApiService } from '../backend-api.service'; // Import the BackendApiService

@Component({
  selector: 'app-summary',
  standalone: true,
  imports: [FormsModule, RouterModule, CommonModule],
  templateUrl: './summary.component.html',
  styleUrl: './summary.component.css'
})
export class SummaryComponent implements OnInit, OnDestroy {
  currentDateTime: string = '';
  private timeInterval: any;
  summary: string = ''; // Holds the summarized body of the document
  sections: string[] = []; // Holds the extracted sections
  isLoading: boolean = false; // Loading state for API calls
  errorMessage: string = ''; // Error message for API failures

  constructor(private backendApiService: BackendApiService) {} // Inject BackendApiService

  ngOnInit() {
    // Initialize the time immediately
    this.updateCurrentTime();
    // Update time every second
    this.timeInterval = setInterval(() => {
      this.updateCurrentTime();
    }, 1000);

    // Fetch the initial summary and sections (stubbed for now)
    this.fetchSummary();
    this.fetchSections();
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
   * Fetches the summarized body of the document.
   */
  fetchSummary() {
    this.isLoading = true;
    this.errorMessage = '';
    this.backendApiService.generateSummary('Sample text for summary').subscribe(
      (response) => {
        this.summary = response.summary;
        console.log('Fetched summary:', this.summary);
        this.isLoading = false;
      },
      (error) => {
        console.error('Error fetching summary:', error);
        this.errorMessage = 'Failed to fetch summary. Please try again.';
        this.isLoading = false;
      }
    );
  }

  /**
   * Fetches the sections of the document.
   */
  fetchSections() {
    this.isLoading = true;
    this.errorMessage = '';
    this.backendApiService.extractSections('Sample text for sections').subscribe(
      (response) => {
        this.sections = response.sections;
        console.log('Fetched sections:', this.sections);
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
   * Handles the extraction of a specific section.
   */
  extractSection(section: string) {
    console.log(`Extracting section: ${section}`);
    // Add logic to extract the specific section
  }

  /**
   * Handles summarizing a specific section.
   */
  summarizeSection(section: string) {
    console.log(`Summarizing section: ${section}`);
    // Add logic to summarize the specific section
  }
}
