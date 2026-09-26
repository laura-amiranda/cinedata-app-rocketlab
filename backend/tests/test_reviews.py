async def test_add_review_updates_average(client):
    create = await client.post("/api/v1/movies", json={"titulo": "Avaliado"})
    sk_id = create.json()["sk_movie_id"]

    await client.post(
        f"/api/v1/movies/{sk_id}/reviews",
        json={"nome": "Ana", "nota": 8, "comentario": "Muito bom"},
    )
    await client.post(
        f"/api/v1/movies/{sk_id}/reviews",
        json={"nome": "Bruno", "nota": 6, "comentario": "Ok"},
    )

    response = await client.get(f"/api/v1/movies/{sk_id}")
    data = response.json()
    assert data["qtd_avaliacoes"] == 2
    assert data["nota_media"] == 7.0


async def test_review_nota_out_of_range_is_rejected(client):
    create = await client.post("/api/v1/movies", json={"titulo": "Nota invalida"})
    sk_id = create.json()["sk_movie_id"]

    response = await client.post(
        f"/api/v1/movies/{sk_id}/reviews",
        json={"nome": "Ana", "nota": 15, "comentario": "..."},
    )
    assert response.status_code == 422


async def test_review_for_unknown_movie_returns_404(client):
    response = await client.post(
        "/api/v1/movies/nao-existe/reviews",
        json={"nome": "Ana", "nota": 5, "comentario": "..."},
    )
    assert response.status_code == 404