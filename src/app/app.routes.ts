// app.routes.ts
import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ContentComponent } from './content/content.component';
import { SummaryComponent } from './summary/summary.component';
import { UploadComponent } from './upload/upload.component';

export const routes: Routes = [
    { path: 'home', component: HomeComponent },
    { path: 'content', component: ContentComponent },
    { path: 'summary', component: SummaryComponent },
    { path:'upload', component: UploadComponent },
    { path: '', redirectTo: '/home', pathMatch: 'full' }
];