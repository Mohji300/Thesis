import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { BackendApiService } from '../backend-api.service';
import { ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-summary',
  standalone: true,
  templateUrl: './summary.component.html',
  styleUrl: './summary.component.css',
  imports: [CommonModule, FormsModule],
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
  summaryPreviewLimit = 350;
  showFullSummary = false;
  abstractPreviewLimit = 1250;
  showFullAbstract = false;
  summaryStartTime: number = 0;
  summaryLatency: number = 0; // in milliseconds
  leftSelectedSection: string = 'abstract';

  // New properties for title, authors, and abstract
  title: string = '';
  author: string = '';
  abstract: string = '';

  constructor(private backendApiService: BackendApiService, private route: ActivatedRoute) {}

  @ViewChild('abstractContainer') abstractContainer!: ElementRef<HTMLDivElement>;
isAbstractOverflowing = false;

ngAfterViewInit() {
  setTimeout(() => this.checkAbstractOverflow(), 0);
}

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

  ngOnChanges() {
  this.checkAbstractOverflow();
}

checkAbstractOverflow() {
  if (this.abstractContainer) {
    const el = this.abstractContainer.nativeElement;
    this.isAbstractOverflowing = el.scrollHeight > el.clientHeight;
  }
}

  ngOnDestroy() {
    if (this.timeInterval) {
      clearInterval(this.timeInterval);
    }
  }

  private updateCurrentTime() {
    this.currentDateTime = new Date().toLocaleString();
  }

  onLeftSectionChange() {
  this.showFullAbstract = false;
  setTimeout(() => this.checkAbstractOverflow(), 0);
}

getLeftSectionContent(): string {
  if (this.leftSelectedSection === 'abstract') {
    return this.abstract;
  }
  return this.sectionContent[this.leftSelectedSection] || '';
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
      setTimeout(() => this.checkAbstractOverflow(), 0); // Wait for DOM update
    },
    (error) => {
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
// handles read more button
  getSummaryPreview(): string {
  if (!this.summarizedContent) return '';
  if (this.showFullSummary || this.summarizedContent.length <= this.summaryPreviewLimit) {
    return this.summarizedContent;
  }
  return this.summarizedContent.slice(0, this.summaryPreviewLimit) + '...';
}

selectSection(section: string) {
    if (section === 'abstract' || section === 'review of related literature') {
    return;
  }
  this.selectedSection = section;
  if (section === 'whole_paper') {
    this.summarizeWholePaper();
  } else {
    this.summarizeSection(section);
  }
}


  /**
   * Handles summarizing a specific section.
   */
summarizeSection(section: string) {
  if (section === 'abstract' || section === 'review of related literature') {
    return;
  }
  this.selectedSection = section;
  this.isLoading = true;
  this.showFullSummary = false;
  this.summaryLatency = 0;
  this.summaryStartTime = Date.now(); // Start timer

  const sectionText = this.sectionContent[section];
  if (!sectionText) {
    console.error('No content found for the selected section.');
    this.errorMessage = 'No content found for the selected section.';
    this.isLoading = false;
    return;
  }

  this.errorMessage = '';
  this.backendApiService.generateSummary(sectionText).subscribe(
    (response) => {
      this.summarizedContent = response.summary;
      this.isLoading = false;
      this.summaryLatency = Date.now() - this.summaryStartTime; // End timer
      console.log(`Summary latency: ${this.summaryLatency} ms`);
    },
    (error) => {
      console.error('Error summarizing section:', error);
      this.errorMessage = 'Failed to summarize the section. Please try again.';
      this.isLoading = false;
      this.summaryLatency = Date.now() - this.summaryStartTime; // End timer even on error
    }
  );
}
summarizeWholePaper() {
  this.isLoading = true;
  this.showFullSummary = false;
  this.summaryLatency = 0;
  this.summaryStartTime = Date.now();

  // Combine all section contents except abstract and review of related literature
  const combinedText = this.sections
    .filter(
      (sec) =>
        sec !== 'abstract' && sec !== 'review of related literature'
    )
    .map((sec) => this.sectionContent[sec])
    .join('\n\n');

  if (!combinedText) {
    this.errorMessage = 'No content found for the whole paper.';
    this.isLoading = false;
    return;
  }

  this.errorMessage = '';
  this.backendApiService.generateSummary(combinedText).subscribe(
    (response) => {
      this.summarizedContent = response.summary;
      this.isLoading = false;
      this.summaryLatency = Date.now() - this.summaryStartTime;
    },
    (error) => {
      this.errorMessage = 'Failed to summarize the whole paper. Please try again.';
      this.isLoading = false;
      this.summaryLatency = Date.now() - this.summaryStartTime;
    }
  );
}
}