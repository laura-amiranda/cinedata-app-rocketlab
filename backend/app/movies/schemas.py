"""Schemas Pydantic (request/response) do domínio de filmes."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class GenreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome_genero: str


class CompanyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome_produtora: str


class PersonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome_pessoa: str
    tipo_pessoa: str


class PerformanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    orcamento_usd: float | None = None
    receita_usd: float | None = None
    lucro_usd: float
    popularidade: float | None = None
    nota_tmdb: float | None = None
    nota_imdb: float | None = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sk_movie_review_id: str
    nome: str
    nota: float
    comentario: str
    created_at: datetime


class ReviewCreate(BaseModel):
    """Nova avaliação de um filme.

    A nota segue a escala de 0 a 10 já usada pelas avaliações importadas
    (dado histórico do dataset). O frontend, que exibe estrelas de 1 a 5,
    é responsável por converter (nota_exibida * 2 = nota enviada aqui).
    """

    nome: str = Field(min_length=1, max_length=120)
    nota: float = Field(ge=0, le=10)
    comentario: str = Field(min_length=1, max_length=4000)


class MovieListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sk_movie_id: str
    titulo: str
    ano_lancamento: int | None
    url_poster: str | None
    nota_media: float | None
    qtd_avaliacoes: int


class MoviePage(BaseModel):
    items: list[MovieListItem]
    total: int
    page: int
    page_size: int


class MovieDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sk_movie_id: str
    titulo: str
    data_lancamento: date | None
    ano_lancamento: int | None
    duracao_minutos: int | None
    status_filme: str | None
    sinopse: str | None
    url_poster: str | None
    url_backdrop: str | None
    generos: list[str]
    produtoras: list[str]
    diretores: list[str]
    atores: list[str]
    roteiristas: list[str]
    performance: PerformanceOut | None
    nota_media: float | None
    qtd_avaliacoes: int
    reviews: list[ReviewOut]


class MovieCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=500)
    diretor: str | None = Field(default=None, max_length=255)
    ano_lancamento: int | None = None
    genero: str | None = Field(default=None, max_length=50)
    sinopse: str | None = Field(default=None, max_length=4000)


class MovieUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=500)
    diretor: str | None = Field(default=None, max_length=255)
    ano_lancamento: int | None = None
    genero: str | None = Field(default=None, max_length=50)
    sinopse: str | None = Field(default=None, max_length=4000)