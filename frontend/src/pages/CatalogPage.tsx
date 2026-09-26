import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { listGenres, listMovies } from '../api';
import type { MovieListItem } from '../types';
import { limparTitulo } from '../utils/text';

const PAGE_SIZE = 20;
const NOTA_OPTIONS = ['9', '8', '7', '6', '5'];

export function CatalogPage() {
  const [searchParams, setSearchParams] = useSearchParams();

  const page = Number(searchParams.get('page') ?? '1') || 1;
  const search = searchParams.get('q') ?? '';
  const genero = searchParams.get('genero') ?? '';
  const ano = searchParams.get('ano') ?? '';
  const notaMinima = searchParams.get('nota') ?? '';

  const [items, setItems] = useState<MovieListItem[]>([]);
  const [total, setTotal] = useState(0);
  const [searchInput, setSearchInput] = useState(search);
  const [anoInput, setAnoInput] = useState(ano);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [genres, setGenres] = useState<string[]>([]);

  useEffect(() => {
    listGenres()
      .then(setGenres)
      .catch(() => setGenres([]));
  }, []);

  useEffect(() => {
    setLoading(true);
    setError(null);
    listMovies(page, PAGE_SIZE, search, {
      genero: genero || undefined,
      ano: ano ? Number(ano) : undefined,
      notaMinima: notaMinima ? Number(notaMinima) : undefined,
    })
      .then((data) => {
        setItems(data.items);
        setTotal(data.total);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [page, search, genero, ano, notaMinima]);

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  const filtrosAtivos = Boolean(genero || ano || notaMinima);

  function updateParams(updates: Record<string, string | null>) {
    const next = new URLSearchParams(searchParams);
    for (const [key, value] of Object.entries(updates)) {
      if (value) {
        next.set(key, value);
      } else {
        next.delete(key);
      }
    }
    setSearchParams(next, { replace: true });
  }

  function handleSearchSubmit(event: React.FormEvent) {
    event.preventDefault();
    updateParams({ q: searchInput || null, page: null });
  }

  function handleGeneroClick(value: string) {
    updateParams({ genero: value || null, page: null });
  }

  function commitAno() {
    const trimmed = anoInput.trim();
    if (trimmed && !/^\d{4}$/.test(trimmed)) {
      return;
    }
    updateParams({ ano: trimmed || null, page: null });
  }

  function handleAnoKeyDown(event: React.KeyboardEvent<HTMLInputElement>) {
    if (event.key === 'Enter') {
      event.preventDefault();
      commitAno();
    }
  }

  function handleNotaChange(event: React.ChangeEvent<HTMLSelectElement>) {
    updateParams({ nota: event.target.value || null, page: null });
  }

  function handleLimparFiltros() {
    setAnoInput('');
    updateParams({ genero: null, ano: null, nota: null, page: null });
  }

  function goToPage(nextPage: number) {
    updateParams({ page: nextPage > 1 ? String(nextPage) : null });
  }

  return (
    <div className="page">
      <div className="catalog-intro">
        <span className="catalog-kicker">
          <span className="dot" /> Catálogo
        </span>
        <h1>Catálogo de filmes</h1>
      </div>

      <form onSubmit={handleSearchSubmit} className="search-form">
        <input
          type="text"
          placeholder="Buscar por título, diretor ou ano..."
          value={searchInput}
          onChange={(event) => setSearchInput(event.target.value)}
        />
        <button type="submit">Buscar</button>
      </form>

      <div className="filters-bar">
        <div className="genre-pills">
          <button
            type="button"
            className={`pill ${genero === '' ? 'pill-active' : ''}`}
            onClick={() => handleGeneroClick('')}
          >
            Todos
          </button>
          {genres.map((g) => (
            <button
              key={g}
              type="button"
              className={`pill ${genero === g ? 'pill-active' : ''}`}
              onClick={() => handleGeneroClick(g)}
            >
              {g}
            </button>
          ))}
        </div>

        <div className="filters-extra">
          <label className="filter-field">
            <span>Ano</span>
            <input
              type="text"
              inputMode="numeric"
              placeholder="Ex: 2020"
              value={anoInput}
              onChange={(event) => setAnoInput(event.target.value)}
              onKeyDown={handleAnoKeyDown}
              onBlur={commitAno}
            />
          </label>

          <label className="filter-field">
            <span>Nota mínima</span>
            <select value={notaMinima} onChange={handleNotaChange}>
              <option value="">Qualquer nota</option>
              {NOTA_OPTIONS.map((n) => (
                <option key={n} value={n}>
                  {n}+
                </option>
              ))}
            </select>
          </label>

          {filtrosAtivos && (
            <button type="button" className="filter-clear" onClick={handleLimparFiltros}>
              Limpar filtros
            </button>
          )}
        </div>
      </div>

      {loading && <p className="results-count">Carregando...</p>}
      {error && <p className="error">Erro ao carregar filmes: {error}</p>}

      {!loading && !error && (
        <>
          <p className="results-count">{total} filme(s) encontrado(s)</p>

          <div className="movie-grid">
            {items.map((movie) => (
              <Link key={movie.sk_movie_id} to={`/movies/${movie.sk_movie_id}`} className="movie-card">
                <div className="poster-wrap">
                  {movie.url_poster ? (
                    <img src={movie.url_poster} alt={movie.titulo} />
                  ) : (
                    <div className="poster-placeholder">Sem imagem</div>
                  )}
                  {movie.nota_media !== null && (
                    <span className="rating-badge">
                      <span className="star">★</span> {movie.nota_media.toFixed(1)}
                    </span>
                  )}
                </div>
                <h3>{limparTitulo(movie.titulo)}</h3>
                <p className="meta">{movie.ano_lancamento ?? 'Ano desconhecido'}</p>
              </Link>
            ))}
          </div>

          <div className="pagination">
            <button disabled={page <= 1} onClick={() => goToPage(page - 1)}>
              Anterior
            </button>
            <span>
              Página {page} de {totalPages}
            </span>
            <button disabled={page >= totalPages} onClick={() => goToPage(page + 1)}>
              Próxima
            </button>
          </div>
        </>
      )}
    </div>
  );
}