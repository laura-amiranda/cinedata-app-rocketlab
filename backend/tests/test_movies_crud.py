async def test_create_movie_returns_full_detail(client):
    payload = {
        "titulo": "Filme Teste",
        "diretor": "Diretora Exemplo",
        "ano_lancamento": 2022,
        "genero": "Drama",
        "sinopse": "Uma sinopse de teste.",
    }
    response = await client.post("/api/v1/movies", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Filme Teste"
    assert data["generos"] == ["Drama"]
    assert data["diretores"] == ["Diretora Exemplo"]
    assert data["nota_media"] is None
    assert data["qtd_avaliacoes"] == 0


async def test_create_movie_requires_titulo(client):
    response = await client.post("/api/v1/movies", json={"titulo": ""})
    assert response.status_code == 422


async def test_get_movie_not_found(client):
    response = await client.get("/api/v1/movies/nao-existe")
    assert response.status_code == 404


async def test_update_movie_changes_fields(client):
    create = await client.post("/api/v1/movies", json={"titulo": "Original", "genero": "Ação"})
    sk_id = create.json()["sk_movie_id"]

    response = await client.patch(
        f"/api/v1/movies/{sk_id}", json={"titulo": "Atualizado", "genero": "Comédia"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Atualizado"
    assert data["generos"] == ["Comédia"]


async def test_delete_movie_removes_it(client):
    create = await client.post("/api/v1/movies", json={"titulo": "Para deletar"})
    sk_id = create.json()["sk_movie_id"]

    delete_response = await client.delete(f"/api/v1/movies/{sk_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/v1/movies/{sk_id}")
    assert get_response.status_code == 404