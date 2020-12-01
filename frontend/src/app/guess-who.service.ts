import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Response } from './model/Responce';

@Injectable({
  providedIn: 'root'
})
export class GuessWhoService {

  constructor(private http: HttpClient) {
  }

  getData(level: number): Observable<Response> {
    const headers = new HttpHeaders();
    headers.set('Access-Control-Request-Headers', 'Content-Type');
    headers.set('Access-Control-Allow-Origin', '*');
    headers.set('Access-Control-Request-Method', 'GET');
    return this.http.get<Response>(`http://localhost:8080?level=${level}`, {headers});
  }
}
