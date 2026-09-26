"""Funções de acesso a dados (queries e regras de persistência) do domínio de filmes."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.movies.models import (
    DimGenre,
    DimMovie,
    DimPerson,
    MovieReview,
)


async def get_or_create_genre(session: AsyncSession, nome_genero: str) -> DimGenre:
    result = await session.execute(select(DimGenre).where(DimGenre.nome_genero == nome_genero))
    genre = result.scalar_one_or_none()
    if genre is None:
        genre = DimGenre(nome_genero=nome_genero)
        session.add(genre)
        await session.flush()
    return genre


async def get_or_create_person(session: AsyncSession, nome_pessoa: str, tipo_pessoa: str) -> DimPerson:
    result = await session.execute(
        select(DimPerson).where(
            DimPerson.nome_pessoa == nome_pessoa, DimPerson.tipo_pessoa == tipo_pessoa
        )
    )
    person = result.scalar_one_or_none()
    if person is None:
        person = DimPerson(nome_pessoa=nome_pessoa, tipo_pessoa=tipo_pessoa)
        session.add(person)
        await session.flush()
    return person


def _rating_stats(reviews: list[MovieReview]) -> tuple[float | None, int]:
    if not reviews:
        return None, 0
    media = sum(r.nota for r in reviews) / len(reviews)
    return round(media, 2), len(reviews)


async def list_movies(
    session: AsyncSession,
    page: int,
    page_size: int,
    search: str | None,
    genero: str | None = None,
    ano: int | None = None,
    nota_minima: float | None = None,
) -> tuple[list[dict], int]:
    base_stmt = select(DimMovie)
    if search:
        base_stmt = base_stmt.where(DimMovie.titulo.ilike(f"%{search}%"))
    if genero:
        base_stmt = base_stmt.join(DimMovie.genres).where(DimGenre.nome_genero == genero).distinct()
    if ano:
        base_stmt = base_stmt.where(DimMovie.ano_lancamento == ano)
    if nota_minima is not None:
        avg_subq = (
            select(MovieReview.sk_movie_id)
            .group_by(MovieReview.sk_movie_id)
            .having(func.avg(MovieReview.nota) >= nota_minima)
        )
        base_stmt = base_stmt.where(DimMovie.sk_movie_id.in_(avg_subq))

    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = (await session.execute(count_stmt)).scalar_one()

    stmt = (
        base_stmt.options(selectinload(DimMovie.reviews))
        .order_by(DimMovie.titulo)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    movies = (await session.execute(stmt)).scalars().all()

    items = []
    for movie in movies:
        nota_media, qtd = _rating_stats(movie.reviews)
        items.append(
            {
                "sk_movie_id": movie.sk_movie_id,
                "titulo": movie.titulo,
                "ano_lancamento": movie.ano_lancamento,
                "url_poster": movie.url_poster,
                "nota_media": nota_media,
                "qtd_avaliacoes": qtd,
            }
        )
    return items, total


async def get_movie_detail(session: AsyncSession, sk_movie_id: str) -> DimMovie | None:
    stmt = (
        select(DimMovie)
        .where(DimMovie.sk_movie_id == sk_movie_id)
        .options(
            selectinload(DimMovie.genres),
            selectinload(DimMovie.companies),
            selectinload(DimMovie.people),
            selectinload(DimMovie.performance),
            selectinload(DimMovie.reviews),
        )
    )
    return (await session.execute(stmt)).scalar_one_or_none()


def build_movie_detail_dict(movie: DimMovie) -> dict:
    nota_media, qtd = _rating_stats(movie.reviews)
    return {
        "sk_movie_id": movie.sk_movie_id,
        "titulo": movie.titulo,
        "data_lancamento": movie.data_lancamento,
        "ano_lancamento": movie.ano_lancamento,
        "duracao_minutos": movie.duracao_minutos,
        "status_filme": movie.status_filme,
        "sinopse": movie.sinopse,
        "url_poster": movie.url_poster,
        "url_backdrop": movie.url_backdrop,
        "generos": [g.nome_genero for g in movie.genres],
        "produtoras": [c.nome_produtora for c in movie.companies],
        "diretores": [p.nome_pessoa for p in movie.people if p.tipo_pessoa == "Diretor"],
        "atores": [p.nome_pessoa for p in movie.people if p.tipo_pessoa == "Ator"],
        "roteiristas": [p.nome_pessoa for p in movie.people if p.tipo_pessoa == "Roteirista"],
        "performance": movie.performance,
        "nota_media": nota_media,
        "qtd_avaliacoes": qtd,
        "reviews": movie.reviews,
    }


async def create_movie(
    session: AsyncSession,
    titulo: str,
    diretor: str | None,
    ano_lancamento: int | None,
    genero: str | None,
    sinopse: str | None,
) -> DimMovie:
    from uuid import uuid4

    movie = DimMovie(
        id_filme=f"manual-{uuid4().hex}",
        titulo=titulo,
        ano_lancamento=ano_lancamento,
        sinopse=sinopse,
        status_filme="Lançado",
    )
    if genero:
        movie.genres.append(await get_or_create_genre(session, genero))
    if diretor:
        movie.people.append(await get_or_create_person(session, diretor, "Diretor"))

    session.add(movie)
    await session.flush()
    return movie


async def update_movie(
    session: AsyncSession,
    movie: DimMovie,
    titulo: str | None,
    diretor: str | None,
    ano_lancamento: int | None,
    genero: str | None,
    sinopse: str | None,
) -> DimMovie:
    if titulo is not None:
        movie.titulo = titulo
    if ano_lancamento is not None:
        movie.ano_lancamento = ano_lancamento
    if sinopse is not None:
        movie.sinopse = sinopse
    if genero is not None:
        movie.genres = [await get_or_create_genre(session, genero)]
    if diretor is not None:
        outros = [p for p in movie.people if p.tipo_pessoa != "Diretor"]
        movie.people = [*outros, await get_or_create_person(session, diretor, "Diretor")]

    await session.flush()
    return movie


async def delete_movie(session: AsyncSession, movie: DimMovie) -> None:
    await session.delete(movie)
    await session.flush()


async def add_review(
    session: AsyncSession, sk_movie_id: str, nome: str, nota: float, comentario: str
) -> MovieReview:
    review = MovieReview(sk_movie_id=sk_movie_id, nome=nome, nota=nota, comentario=comentario)
    session.add(review)
    await session.flush()
    await session.refresh(review)
    return review


async def list_genres(session: AsyncSession) -> list[str]:
    result = await session.execute(select(DimGenre.nome_genero).order_by(DimGenre.nome_genero))
    return [row[0] for row in result.all()]