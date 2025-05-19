import { TestBed } from '@angular/core/testing';

import { InsightsCacheService } from './insights-cache.service';

describe('InsightsCacheService', () => {
  let service: InsightsCacheService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InsightsCacheService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
