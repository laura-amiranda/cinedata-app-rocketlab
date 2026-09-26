"""Rotas HTTP do domínio de filmes: catálogo, detalhes, CRUD e avaliações."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_admin
from app.core.cache import (
    GENRES_CACHE_KEY,
    cache_clear,
    cache_get,
    cache_set,
    movies_list_cache_key,
)
from app.db.session import get_db
from app.movies import service
from app.movies.schemas import (
    MovieCreate,
    MovieDetail,
    MoviePage,
    MovieUpdate,
    ReviewCreate,
    ReviewOut,
)

router = APIRouter()


async def _get_movie_or_404(session: AsyncSession, sk_movie_id: str):
    movie = await service.get_movie_detail(session, sk_movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Filme não encontrado")
    return movie


@router.get("", response_model=MoviePage)
async def list_movies(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None, min_length=1, max_length=200),
    genero: str | None = Query(default=None, min_length=1, max_length=100),
    ano: int | None = Query(default=None, ge=1800, le=2100),
    nota_minima: float | None = Query(default=None, ge=0, le=10),
    session: AsyncSession = Depends(get_db),
) -> MoviePage:
    cache_key = movies_list_cache_key(page, page_size, search, genero, ano, nota_minima)
    cached = cache_get(cache_key)
    if cached is not None:
        return cached

    items, total = await service.list_movies(
        session, page, page_size, search, genero, ano, nota_minima
    )
    result = MoviePage(items=items, total=total, page=page, page_size=page_size)
    cache_set(cache_key, result)
    return result


@router.get("/genres", response_model=list[str])
async def list_genres(session: AsyncSession = Depends(get_db)) -> list[str]:
    cached = cache_get(GENRES_CACHE_KEY)
    if cached is not None:
        return cached

    genres = await service.list_genres(session)
    cache_set(GENRES_CACHE_KEY, genres)
    return genres


@router.get("/{sk_movie_id}", response_model=MovieDetail)
async def get_movie(sk_movie_id: str, session: AsyncSession = Depends(get_db)) -> MovieDetail:
    movie = await _get_movie_or_404(session, sk_movie_id)
    return service.build_movie_detail_dict(movie)


@router.post("", response_model=MovieDetail, status_code=status.HTTP_201_CREATED)
async def create_movie(
    payload: MovieCreate,
    session: AsyncSession = Depends(get_db),
    _admin: str = Depends(require_admin),
) -> MovieDetail:
    movie = await service.create_movie(
        session,
        titulo=payload.titulo,
        diretor=payload.diretor,
        ano_lancamento=payload.ano_lancamento,
        genero=payload.genero,
        sinopse=payload.sinopse,
    )
    await session.commit()
    movie = await _get_movie_or_404(session, movie.sk_movie_id)
    cache_clear()
    return service.build_movie_detail_dict(movie)


@router.patch("/{sk_movie_id}", response_model=MovieDetail)
async def update_movie(
    sk_movie_id: str,
    payload: MovieUpdate,
    session: AsyncSession = Depends(get_db),
    _admin: str = Depends(require_admin),
) -> MovieDetail:
    movie = await _get_movie_or_404(session, sk_movie_id)
    movie = await service.update_movie(
        session,
        movie,
        titulo=payload.titulo,
        diretor=payload.diretor,
        ano_lancamento=payload.ano_lancamento,
        genero=payload.genero,
        sinopse=payload.sinopse,
    )
    await session.commit()
    movie = await _get_movie_or_404(session, sk_movie_id)
    cache_clear()
    return service.build_movie_detail_dict(movie)


@router.delete("/{sk_movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    sk_movie_id: str,
    session: AsyncSession = Depends(get_db),
    _admin: str = Depends(require_admin),
) -> None:
    movie = await _get_movie_or_404(session, sk_movie_id)
    await service.delete_movie(session, movie)
    await session.commit()
    cache_clear()


@router.post(
    "/{sk_movie_id}/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED
)
async def create_review(
    sk_movie_id: str, payload: ReviewCreate, session: AsyncSession = Depends(get_db)
) -> ReviewOut:
    await _get_movie_or_404(session, sk_movie_id)
    review = await service.add_review(
        session,
        sk_movie_id=sk_movie_id,
        nome=payload.nome,
        nota=payload.nota,
        comentario=payload.comentario,
    )
    await session.commit()
    cache_clear()
    return review