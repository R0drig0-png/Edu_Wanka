import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { FooterComponente } from './components/footer-componente/footer-componente';
import { HeaderComponente } from './components/header-componente/header-componente';

@Component({
  imports: [RouterOutlet, HeaderComponente, FooterComponente],
  selector: 'app-root',
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App {}
