import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { StarRatingDisplay } from './StarRating';

describe('StarRatingDisplay', () => {
  it('mostra "Sem avaliações" quando a nota é null', () => {
    render(<StarRatingDisplay notaSobreDez={null} />);
    expect(screen.getByText('Sem avaliações')).toBeInTheDocument();
  });

  it('converte a nota de 0-10 para 5 estrelas corretamente', () => {
    render(<StarRatingDisplay notaSobreDez={10} />);
    expect(screen.getByTitle('10.0 / 10')).toHaveTextContent('★★★★★');
  });

  it('arredonda nota intermediária para a estrela mais próxima', () => {
    // 6 / 2 = 3 estrelas cheias, 2 vazias
    render(<StarRatingDisplay notaSobreDez={6} />);
    expect(screen.getByTitle('6.0 / 10')).toHaveTextContent('★★★☆☆');
  });

  it('mostra 0 estrelas cheias para a nota mais baixa', () => {
    render(<StarRatingDisplay notaSobreDez={0} />);
    expect(screen.getByTitle('0.0 / 10')).toHaveTextContent('☆☆☆☆☆');
  });
});