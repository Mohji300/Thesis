import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http'; // Import provideHttpClient
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, {
  ...appConfig,
  providers: [
    provideHttpClient(), // Add HttpClient globally
    ...(appConfig.providers || [])
  ]
}).catch((err) => console.error(err));
