import { DOCUMENT } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  imports: [RouterLink, RouterLinkActive],
  selector: 'app-header-componente',
  styleUrl: './header-componente.css',
  templateUrl: './header-componente.html',
})
export class HeaderComponente {
  private readonly document = inject(DOCUMENT);

  protected cambiarTamanoLetra(tamanoPixeles: number): void {
    this.document.body.style.fontSize = `${tamanoPixeles}px`;
  }
}
