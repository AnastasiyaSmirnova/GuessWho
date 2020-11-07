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

  isFirstTime = true;
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
        this.round = data;
        this.isFirstTime = false;
        this.loading = false;
        console.log(data);
      },
      error => {
        console.log(error);
        this.loading = false;
      }
    );
  }

  showAnswer(): void {
    this.answer = !this.answer;
  }

  getBackgroundColor(name: string): string {
    return name === this.round.correctName ? '#3D9970' : '#FF4136';
  }

  setCurrentAnswer(name: string): void {
    this.currentAnswer = name;
  }

  /**
   * todo()
   * play again()
   * check answers doesn't work!
   */
}
