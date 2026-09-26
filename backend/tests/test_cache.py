from app.core.cache import cache_get, movies_list_cache_key


async def test_movie_list_response_is_cached(client):
    await client.post("/api/v1/movies", json={"titulo": "Filme cacheado"})
    await client.get("/api/v1/movies")

    cache_key = movies_list_cache_key(1, 20, None, None, None, None)
    assert cache_get(cache_key) is not None


async def test_creating_a_movie_invalidates_the_list_cache(client):
    first = await client.get("/api/v1/movies")
    assert first.json()["total"] == 0

    await client.post("/api/v1/movies", json={"titulo": "Filme novo"})

    second = await client.get("/api/v1/movies")
    assert second.json()["total"] == 1


async def test_genres_list_is_cached_and_invalidated_on_create(client):
    first = await client.get("/api/v1/movies/genres")
    assert first.json() == []

    await client.post("/api/v1/movies", json={"titulo": "Com genero", "genero": "Aventura"})

    second = await client.get("/api/v1/movies/genres")
    assert second.json() == ["Aventura"]