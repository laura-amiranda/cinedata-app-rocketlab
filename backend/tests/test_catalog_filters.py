async def _create(client, **overrides):
    payload = {"titulo": "Filme", "genero": None, "ano_lancamento": None}
    payload.update(overrides)
    response = await client.post("/api/v1/movies", json=payload)
    assert response.status_code == 201
    return response.json()


async def test_search_filters_by_title(client):
    await _create(client, titulo="Matrix Reloaded")
    await _create(client, titulo="Outro filme qualquer")

    response = await client.get("/api/v1/movies", params={"search": "matrix"})
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["titulo"] == "Matrix Reloaded"


async def test_filter_by_genero(client):
    await _create(client, titulo="Filme de terror", genero="Terror")
    await _create(client, titulo="Filme de drama", genero="Drama")

    response = await client.get("/api/v1/movies", params={"genero": "Terror"})
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["titulo"] == "Filme de terror"


async def test_filter_by_ano(client):
    await _create(client, titulo="Filme 2020", ano_lancamento=2020)
    await _create(client, titulo="Filme 2021", ano_lancamento=2021)

    response = await client.get("/api/v1/movies", params={"ano": 2020})
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["titulo"] == "Filme 2020"


async def test_filter_by_nota_minima(client):
    alto = await _create(client, titulo="Nota alta")
    baixo = await _create(client, titulo="Nota baixa")

    await client.post(
        f"/api/v1/movies/{alto['sk_movie_id']}/reviews",
        json={"nome": "A", "nota": 9, "comentario": "..."},
    )
    await client.post(
        f"/api/v1/movies/{baixo['sk_movie_id']}/reviews",
        json={"nome": "B", "nota": 3, "comentario": "..."},
    )

    response = await client.get("/api/v1/movies", params={"nota_minima": 8})
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["titulo"] == "Nota alta"


async def test_pagination(client):
    for i in range(3):
        await _create(client, titulo=f"Filme {i}")

    response = await client.get("/api/v1/movies", params={"page": 1, "page_size": 2})
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 3

    response_p2 = await client.get("/api/v1/movies", params={"page": 2, "page_size": 2})
    assert len(response_p2.json()["items"]) == 1


async def test_genres_route_is_not_shadowed_by_dynamic_route(client):
    await _create(client, titulo="Filme com genero", genero="Ficção científica")

    response = await client.get("/api/v1/movies/genres")
    assert response.status_code == 200
    assert response.json() == ["Ficção científica"]