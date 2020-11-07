import { TestBed } from '@angular/core/testing';

import { GuessWhoService } from './guess-who.service';

describe('GuessWhoService', () => {
  let service: GuessWhoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GuessWhoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
