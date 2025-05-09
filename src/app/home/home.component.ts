// home.component.ts
import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common'; 
import { BackendApiService } from '../backend-api.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit, OnDestroy {
  currentDateTime: string = '';
  private timeInterval: any;
  searchQuery: string = '';
  isLoading: boolean = false; // Loading state for API calls
  errorMessage: string = ''; // Error message for API failures

  constructor(private router: Router, private backendApiService: BackendApiService) {}

  ngOnInit() {
    // Initialize the time immediately
    this.updateCurrentTime();
    // Update time every second
    this.timeInterval = setInterval(() => {
      this.updateCurrentTime();
    }, 1000);
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

  //logic for testing direkta pupunta sa content page alisin lang yung comment
/*   handleSearch() {
    if (this.searchQuery.trim()) {
      // Navigate to the ContentComponent with the search query as a query parameter
      this.router.navigate(['/content'], { queryParams: { query: this.searchQuery } });
    } else {
      // Show an alert or a field pop-up indicating the search field is empty
      alert('The search field is empty. Please enter a search query.');
    }
  } */

      //actuall logic for searching, i comment lang if need mag test
      handleSearch() {
        if (this.searchQuery.trim()) {
          this.isLoading = true;
          this.errorMessage = '';
      
          // Call the backend to validate the query
          this.backendApiService.searchDocuments(this.searchQuery, 10).subscribe(
            (response) => {
              if (response.documents && response.documents.length > 0) {
                // Navigate to the ContentComponent if documents are found
                this.router.navigate(['/content'], { queryParams: { query: this.searchQuery } });
              } else {
                // Show an alert if no documents are found
                alert('No documents found for the given query. Please try a different search term.');
              }
              this.isLoading = false;
            },
            (error) => {
              console.error('Error validating search query:', error);
              this.errorMessage = 'Failed to validate the search query. Please try again.';
              this.isLoading = false;
            }
          );
        } else {
          // Show an alert if the search field is empty
          alert('The search field is empty. Please enter a search query.');
        }
      }
    }