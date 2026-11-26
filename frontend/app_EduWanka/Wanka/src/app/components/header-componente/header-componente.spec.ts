import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

import { HeaderComponente } from './header-componente';

describe('HeaderComponente', () => {
  let component: HeaderComponente;
  let fixture: ComponentFixture<HeaderComponente>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HeaderComponente],
      providers: [provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(HeaderComponente);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('debería crear el componente', () => {
    expect(component).toBeTruthy();
  });
});
