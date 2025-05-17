// app.routes.ts
import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ContentComponent } from './content/content.component';
import { SummaryComponent } from './summary/summary.component';
import { UploadComponent } from './upload/upload.component';
import { AuthGuard } from './auth/auth.guard';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';

export const routes: Routes = [
    { path: 'home', component: HomeComponent },
    { path: 'content', component: ContentComponent },
    { path: 'summary/:id', component: SummaryComponent },
    { path:'upload', component: UploadComponent, canActivate: [AuthGuard] },
    {path : 'register', component: RegisterComponent, /* canActivate: [AuthGuard] */},
    { path: 'login', component: LoginComponent },
    { path: '', redirectTo: '/home', pathMatch: 'full' }
];