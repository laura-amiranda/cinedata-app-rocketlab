import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as api from '../api';
import { CatalogPage } from './CatalogPage';

vi.mock('../api');

const mockedListMovies = vi.mocked(api.listMovies);
const mockedListGenres = vi.mocked(api.listGenres);

const moviePageMock = {
  items: [
    { sk_movie_id: '1', titulo: 'Filme A', ano_lancamento: 2020, url_poster: null, nota_media: 8, qtd_avaliacoes: 2 },
    { sk_movie_id: '2', titulo: 'Filme B', ano_lancamento: 2021, url_poster: null, nota_media: null, qtd_avaliacoes: 0 },
  ],
  total: 2,
  page: 1,
  page_size: 20,
};

function renderCatalog(initialEntry = '/') {
  return render(
    <MemoryRouter initialEntries={[initialEntry]}>
      <CatalogPage />
    </MemoryRouter>
  );
}

beforeEach(() => {
  mockedListMovies.mockReset().mockResolvedValue(moviePageMock);
  mockedListGenres.mockReset().mockResolvedValue(['Drama', 'Comédia', 'Terror']);
});

describe('CatalogPage', () => {
  it('carrega e mostra os filmes retornados pela API', async () => {
    renderCatalog();

    expect(await screen.findByText('Filme A')).toBeInTheDocument();
    expect(screen.getByText('Filme B')).toBeInTheDocument();
    expect(screen.getByText('2 filme(s) encontrado(s)')).toBeInTheDocument();
  });

  it('renderiza um pill para cada gênero vindo da API', async () => {
    renderCatalog();

    expect(await screen.findByRole('button', { name: 'Drama' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Comédia' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Terror' })).toBeInTheDocument();
  });

  it('busca com o filtro de gênero ao clicar em um pill', async () => {
    const user = userEvent.setup();
    renderCatalog();

    await screen.findByText('Filme A');
    await user.click(await screen.findByRole('button', { name: 'Drama' }));

    await waitFor(() => {
      const ultimaChamada = mockedListMovies.mock.calls.at(-1);
      expect(ultimaChamada?.[3]).toMatchObject({ genero: 'Drama' });
    });
  });

  it('restaura os filtros a partir da URL (ex.: ao voltar do detalhe do filme)', async () => {
    renderCatalog('/?genero=Terror&nota=8');

    await waitFor(() => {
      expect(mockedListMovies).toHaveBeenCalledWith(
        1,
        20,
        '',
        expect.objectContaining({ genero: 'Terror', notaMinima: 8 })
      );
    });

    expect(await screen.findByRole('button', { name: 'Limpar filtros' })).toBeInTheDocument();
  });

  it('mostra mensagem de erro quando a API falha', async () => {
    mockedListMovies.mockReset().mockRejectedValue(new Error('Falha de rede'));
    renderCatalog();

    expect(await screen.findByText(/Erro ao carregar filmes/)).toBeInTheDocument();
  });
});