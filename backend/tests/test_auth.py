async def test_login_with_valid_credentials_returns_token(anon_client):
    response = await anon_client.post(
        "/api/v1/auth/login", json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


async def test_login_with_invalid_credentials_is_rejected(anon_client):
    response = await anon_client.post(
        "/api/v1/auth/login", json={"username": "admin", "password": "senha-errada"}
    )
    assert response.status_code == 401


async def test_create_movie_without_token_is_rejected(anon_client):
    response = await anon_client.post("/api/v1/movies", json={"titulo": "Sem token"})
    assert response.status_code == 401


async def test_update_movie_without_token_is_rejected(anon_client, client):
    create = await client.post("/api/v1/movies", json={"titulo": "Original"})
    sk_id = create.json()["sk_movie_id"]

    response = await anon_client.patch(f"/api/v1/movies/{sk_id}", json={"titulo": "Hackeado"})
    assert response.status_code == 401


async def test_delete_movie_without_token_is_rejected(anon_client, client):
    create = await client.post("/api/v1/movies", json={"titulo": "Protegido"})
    sk_id = create.json()["sk_movie_id"]

    response = await anon_client.delete(f"/api/v1/movies/{sk_id}")
    assert response.status_code == 401


async def test_create_movie_with_invalid_token_is_rejected(anon_client):
    anon_client.headers["Authorization"] = "Bearer token-invalido"
    response = await anon_client.post("/api/v1/movies", json={"titulo": "Token ruim"})
    assert response.status_code == 401


async def test_reviews_do_not_require_authentication(anon_client, client):
    create = await client.post("/api/v1/movies", json={"titulo": "Filme aberto para avaliação"})
    sk_id = create.json()["sk_movie_id"]

    response = await anon_client.post(
        f"/api/v1/movies/{sk_id}/reviews",
        json={"nome": "Visitante", "nota": 7, "comentario": "Gostei"},
    )
    assert response.status_code == 201