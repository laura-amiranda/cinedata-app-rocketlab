import { clearToken, getToken } from './auth';
import type { MovieDetail, MoviePage, Review } from './types';

const BASE_URL = 'http://127.0.0.1:8000/api/v1';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const token = getToken();
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    ...options,
  });

  if (!response.ok) {
    if (response.status === 401) {
      clearToken();
    }
    const body = await response.json().catch(() => null);
    const message = body?.detail ? JSON.stringify(body.detail) : `Erro ${response.status}`;
    throw new Error(message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export interface MovieFilters {
  genero?: string;
  ano?: number;
  notaMinima?: number;
}

export function listMovies(
  page: number,
  pageSize: number,
  search: string,
  filters: MovieFilters = {}
): Promise<MoviePage> {
  const params = new URLSearchParams({ page: String(page), page_size: String(pageSize) });
  if (search.trim()) {
    params.set('search', search.trim());
  }
  if (filters.genero) {
    params.set('genero', filters.genero);
  }
  if (filters.ano) {
    params.set('ano', String(filters.ano));
  }
  if (filters.notaMinima !== undefined) {
    params.set('nota_minima', String(filters.notaMinima));
  }
  return request<MoviePage>(`/movies?${params.toString()}`);
}

export function listGenres(): Promise<string[]> {
  return request<string[]>('/movies/genres');
}

export interface LoginPayload {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export function login(payload: LoginPayload): Promise<LoginResponse> {
  return request<LoginResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function getMovie(skMovieId: string): Promise<MovieDetail> {
  return request<MovieDetail>(`/movies/${skMovieId}`);
}

export interface MoviePayload {
  titulo: string;
  diretor: string | null;
  ano_lancamento: number | null;
  genero: string | null;
  sinopse: string | null;
}

export function createMovie(payload: MoviePayload): Promise<MovieDetail> {
  return request<MovieDetail>('/movies', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function updateMovie(skMovieId: string, payload: MoviePayload): Promise<MovieDetail> {
  return request<MovieDetail>(`/movies/${skMovieId}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });
}

export function deleteMovie(skMovieId: string): Promise<void> {
  return request<void>(`/movies/${skMovieId}`, { method: 'DELETE' });
}

export interface ReviewPayload {
  nome: string;
  nota: number;
  comentario: string;
}

export function addReview(skMovieId: string, payload: ReviewPayload): Promise<Review> {
  return request<Review>(`/movies/${skMovieId}/reviews`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}