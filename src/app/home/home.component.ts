// home.component.ts
import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router'; // Import Router

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit, OnDestroy {
  currentDateTime: string = '';
  private timeInterval: any;
  searchQuery: string = '';

  constructor(private router: Router) {} // Inject Router

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
    // Navigate to the ContentComponent without any query parameters
    this.router.navigate(['/content']);
  }
}