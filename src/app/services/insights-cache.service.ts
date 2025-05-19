import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class InsightsCacheService {
  public documents: any[] = [];
  public insights: { [id: string]: string } = {};
  public lastQuery: string = '';
}