import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username = '';
  password = '';
  errorMessage = '';

  constructor(private router: Router, private http: HttpClient) {}

  login() {
    this.errorMessage = '';
    this.http.post<any>('http://127.0.0.1:5000/login', {
      username: this.username,
      password_hash: this.password
    }).subscribe({
      next: (res) => {
        localStorage.setItem('auth_token', res.token);
        this.errorMessage = 'Login successful! Redirecting to upload...';
        setTimeout(() => {
          this.router.navigate(['/upload'], { replaceUrl: true });
        }, 3000); // 3 seconds delay
      },
      error: (err) => {
        this.errorMessage = err.error?.error || 'Login failed';
      }
    });
  }

  goToRegister() {
    this.router.navigate(['/register']);
  }

  goToHome() {
  this.router.navigate(['/']);
}
}