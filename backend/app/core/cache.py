"""Cache simples em memória para consultas de leitura (GET) do catálogo.

Não é um cache "de verdade" tipo Redis — é um dicionário com TTL, suficiente
pro escopo da atividade. Qualquer escrita (criar, editar, remover filme ou
avaliação) limpa o cache inteiro via `cache_clear()`, então nunca fica dado
desatualizado depois de uma mudança.
"""

import time
from typing import Any

_TTL_SECONDS = 30
_store: dict[str, tuple[float, Any]] = {}


def cache_get(key: str) -> Any | None:
    entry = _store.get(key)
    if entry is None:
        return None
    expires_at, value = entry
    if time.monotonic() > expires_at:
        _store.pop(key, None)
        return None
    return value


def cache_set(key: str, value: Any, ttl: float = _TTL_SECONDS) -> None:
    _store[key] = (time.monotonic() + ttl, value)


def cache_clear() -> None:
    _store.clear()


def movies_list_cache_key(
    page: int,
    page_size: int,
    search: str | None,
    genero: str | None,
    ano: int | None,
    nota_minima: float | None,
) -> str:
    return (
        f"movies:list:page={page}:page_size={page_size}:search={search or ''}:"
        f"genero={genero or ''}:ano={ano or ''}:"
        f"nota_minima={nota_minima if nota_minima is not None else ''}"
    )


GENRES_CACHE_KEY = "movies:genres"