import { Component } from '@angular/core';
import { GuessWhoService } from './guess-who.service';
import { Response } from './model/Responce';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Guess who???';

  loading = false;
  round: Response = null;
  answer = false;
  currentAnswer: string;

  questionMarkURL = 'https://cdn.psychologytoday.com/sites/default/files/styles/amp_metadata_content_image_min_1200px_wide/public/field_blog_entry_teaser_image/2019-12/question_aisa-144x144-88_0-400_400.jpg?itok=LRzyp_qj';

  constructor(private service: GuessWhoService) {
  }

  play(): void {
    this.loading = true;
    this.service.getData().subscribe(
      data => {
        this.loading = false;
        this.answer = false;
        this.round = data;
        this.currentAnswer = undefined;
        console.log(this.round);
      },
      error => {
        this.loading = false;
        console.log(error);
      }
    );
  }

  getBackgroundColor(name: string): string {
    return name === this.round.correctName ? '#8FBC8F' : '#F08080';
  }

  setCurrentAnswer(name: string): void {
    this.currentAnswer = name;
  }
}
