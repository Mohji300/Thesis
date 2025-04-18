import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-summary',
  standalone: true,
  imports: [FormsModule, RouterModule],
  templateUrl: './summary.component.html',
  styleUrl: './summary.component.css'
})
export class SummaryComponent implements OnInit, OnDestroy {
  currentDateTime: string = '';
  private timeInterval: any;
  searchQuery: string = '';

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

  handleSearch() {
    if (this.searchQuery.trim()) {
      console.log('Searching for:', this.searchQuery);
      // Implement your search logic here
    }
  }
}
