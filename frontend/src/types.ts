export interface MovieListItem {
  sk_movie_id: string;
  titulo: string;
  ano_lancamento: number | null;
  url_poster: string | null;
  nota_media: number | null;
  qtd_avaliacoes: number;
}

export interface MoviePage {
  items: MovieListItem[];
  total: number;
  page: number;
  page_size: number;
}

export interface Performance {
  orcamento_usd: number | null;
  receita_usd: number | null;
  lucro_usd: number;
  popularidade: number | null;
  nota_tmdb: number | null;
  nota_imdb: number | null;
}

export interface Review {
  sk_movie_review_id: string;
  nome: string;
  nota: number;
  comentario: string;
  created_at: string;
}

export interface MovieDetail {
  sk_movie_id: string;
  titulo: string;
  data_lancamento: string | null;
  ano_lancamento: number | null;
  duracao_minutos: number | null;
  status_filme: string | null;
  sinopse: string | null;
  url_poster: string | null;
  url_backdrop: string | null;
  generos: string[];
  produtoras: string[];
  diretores: string[];
  atores: string[];
  roteiristas: string[];
  performance: Performance | null;
  nota_media: number | null;
  qtd_avaliacoes: number;
  reviews: Review[];
}

export interface MovieFormData {
  titulo: string;
  diretor: string;
  ano_lancamento: string;
  genero: string;
  sinopse: string;
}