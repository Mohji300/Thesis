import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  username = '';
  password = '';
  errorMessage = '';
  successMessage = '';

  constructor(private router: Router, private http: HttpClient) {}

  register() {
    this.http.post<any>('http://127.0.0.1:5000/register', {
      username: this.username,
      password: this.password
    }).subscribe({
      next: () => {
        this.successMessage = 'Account created! Redirecting to login...';
        this.errorMessage = '';
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 3000); //3 seconds delay for user feedback
      },
      error: (err) => {
        this.errorMessage = err.error?.error || 'Registration failed';
        this.successMessage = '';
      }
    });
  }

  goToLogin() {
    this.router.navigate(['/login']);
  }

  goToHome() {
  this.router.navigate(['/']);
}
}
