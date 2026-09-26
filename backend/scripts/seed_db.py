"""Popula o banco SQLite com os dados iniciais de filmes fornecidos na atividade.

Uso:
    python scripts/seed_db.py

Espera encontrar os CSVs extraídos em:
    backend/seed_data/bases_atv_dev1/   (dim_movies, dim_genres, dim_companies,
                                          dim_people, dim_reviews)
    backend/seed_data/bases_atv_dev_2/  (bridges, fact_movies_performance,
                                          movies_reviews)
"""

import csv
import sqlite3
import sys
from pathlib import Path

csv.field_size_limit(sys.maxsize)

BACKEND_DIR = Path(__file__).resolve().parent.parent
DATA_DIR_1 = BACKEND_DIR / "seed_data" / "bases_atv_dev1"
DATA_DIR_2 = BACKEND_DIR / "seed_data" / "bases_atv_dev_2"
DB_PATH = BACKEND_DIR / "rocketlab.db"


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def none_if_empty(value: str):
    """Converte string vazia (campo nulo no CSV) para None."""
    return value if value.strip() != "" else None


def seed_dim_movies(cur: sqlite3.Cursor) -> None:
    rows = read_csv(DATA_DIR_1 / "dim_movies.csv")
    data = [
        (
            row["sk_movie_id"],
            row["id_filme"],
            row["titulo"],
            none_if_empty(row["data_lancamento"]),
            none_if_empty(row["ano_lancamento"]),
            none_if_empty(row["duracao_minutos"]),
            none_if_empty(row["status_filme"]),
            none_if_empty(row["sinopse"]),
            none_if_empty(row["url_poster"]),
            none_if_empty(row["url_backdrop"]),
        )
        for row in rows
    ]
    cur.executemany(
        """
        INSERT INTO dim_movies (
            sk_movie_id, id_filme, titulo, data_lancamento, ano_lancamento,
            duracao_minutos, status_filme, sinopse, url_poster, url_backdrop
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        data,
    )
    print(f"dim_movies: {len(data)} linhas inseridas")


def seed_dim_genres(cur: sqlite3.Cursor) -> None:
    rows = read_csv(DATA_DIR_1 / "dim_genres.csv")
    data = [(row["sk_genre_id"], row["nome_genero"]) for row in rows]
    cur.executemany(
        "INSERT INTO dim_genres (sk_genre_id, nome_genero) VALUES (?, ?)", data
    )
    print(f"dim_genres: {len(data)} linhas inseridas")


def seed_dim_companies(cur: sqlite3.Cursor) -> None:
    rows = read_csv(DATA_DIR_1 / "dim_companies.csv")
    data = [(row["sk_company_id"], row["nome_produtora"]) for row in rows]
    cur.executemany(
        "INSERT INTO dim_companies (sk_company_id, nome_produtora) VALUES (?, ?)", data
    )
    print(f"dim_companies: {len(data)} linhas inseridas")


def seed_dim_people(cur: sqlite3.Cursor) -> None:
    rows = read_csv(DATA_DIR_1 / "dim_people.csv")
    data = [(row["sk_person_id"], row["nome_pessoa"], row["tipo_pessoa"]) for row in rows]
    cur.executemany(
        "INSERT INTO dim_people (sk_person_id, nome_pessoa, tipo_pessoa) VALUES (?, ?, ?)",
        data,
    )
    print(f"dim_people: {len(data)} linhas inseridas")


def seed_bridge_movie_genre(cur: sqlite3.Cursor) -> None:
    rows = read_csv(DATA_DIR_2 / "bridge_movie_genre.csv")
    data = [(row["sk_movie_id"], row["sk_genre_id"]) for row in rows]
    cur.executemany(
        "INSERT INTO bridge_movie_genre (sk_movie_id, sk_genre_id) VALUES (?, ?)", data
    )
    print(f"bridge_movie_genre: {len(data)} linhas inseridas")


def seed_bridge_movie_company(cur: sqlite3.Cursor) -> None:
    rows = read_csv(DATA_DIR_2 / "bridge_movie_company.csv")
    data = [(row["sk_movie_id"], row["sk_company_id"]) for row in rows]
    cur.executemany(
        "INSERT INTO bridge_movie_company (sk_movie_id, sk_company_id) VALUES (?, ?)", data
    )
    print(f"bridge_movie_company: {len(data)} linhas inseridas")


def seed_bridge_movie_person(cur: sqlite3.Cursor) -> None:
    rows = read_csv(DATA_DIR_2 / "bridge_movie_person.csv")
    data = [(row["sk_movie_id"], row["sk_person_id"]) for row in rows]
    cur.executemany(
        "INSERT INTO bridge_movie_person (sk_movie_id, sk_person_id) VALUES (?, ?)", data
    )
    print(f"bridge_movie_person: {len(data)} linhas inseridas")


def seed_fact_movies_performance(cur: sqlite3.Cursor) -> None:
    rows = read_csv(DATA_DIR_2 / "fact_movies_performance.csv")
    data = [
        (
            row["sk_movie_id"],
            none_if_empty(row["orcamento_usd"]),
            none_if_empty(row["receita_usd"]),
            row["lucro_usd"],
            none_if_empty(row["orcamento_brl"]),
            none_if_empty(row["receita_brl"]),
            row["lucro_brl"],
            none_if_empty(row["popularidade"]),
            none_if_empty(row["nota_tmdb"]),
            none_if_empty(row["qtd_tmdb"]),
            none_if_empty(row["nota_imdb"]),
            none_if_empty(row["qtd_imdb"]),
        )
        for row in rows
    ]
    cur.executemany(
        """
        INSERT INTO fact_movies_performance (
            sk_movie_id, orcamento_usd, receita_usd, lucro_usd,
            orcamento_brl, receita_brl, lucro_brl, popularidade,
            nota_tmdb, qtd_tmdb, nota_imdb, qtd_imdb
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        data,
    )
    print(f"fact_movies_performance: {len(data)} linhas inseridas")


def seed_movie_reviews(cur: sqlite3.Cursor) -> None:
    rows = read_csv(DATA_DIR_2 / "movies_reviews.csv")
    data = [
        (row["sk_movie_review_id"], row["sk_movie_id"], row["nome"], row["nota"], row["comentario"])
        for row in rows
    ]
    cur.executemany(
        """
        INSERT INTO movie_reviews (sk_movie_review_id, sk_movie_id, nome, nota, comentario)
        VALUES (?, ?, ?, ?, ?)
        """,
        data,
    )
    print(f"movie_reviews: {len(data)} linhas inseridas")


def seed_dim_reviews(cur: sqlite3.Cursor) -> None:
    rows = read_csv(DATA_DIR_1 / "dim_reviews.csv")
    data = [
        (
            row["sk_review_id"],
            row["sk_movie_id"],
            row["qtd_avaliacoes_usuarios"],
            none_if_empty(row["nota_media_usuarios"]),
        )
        for row in rows
    ]
    cur.executemany(
        """
        INSERT INTO dim_reviews (sk_review_id, sk_movie_id, qtd_avaliacoes_usuarios, nota_media_usuarios)
        VALUES (?, ?, ?, ?)
        """,
        data,
    )
    print(f"dim_reviews: {len(data)} linhas inseridas")


def main() -> None:
    if not DATA_DIR_1.exists() or not DATA_DIR_2.exists():
        print(
            "ERRO: pastas de dados não encontradas. Extraia bases-1.zip e bases-2.zip "
            f"dentro de {BACKEND_DIR / 'seed_data'} antes de rodar este script."
        )
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    # Confere se o banco já tem dados, pra evitar duplicar ao rodar 2x.
    cur.execute("SELECT COUNT(*) FROM dim_movies")
    if cur.fetchone()[0] > 0:
        print("O banco já contém dados em dim_movies. Abortando para não duplicar.")
        print("Se quiser recomeçar do zero, apague o arquivo rocketlab.db e rode a migration de novo.")
        conn.close()
        sys.exit(1)

    try:
        seed_dim_movies(cur)
        seed_dim_genres(cur)
        seed_dim_companies(cur)
        seed_dim_people(cur)
        seed_bridge_movie_genre(cur)
        seed_bridge_movie_company(cur)
        seed_bridge_movie_person(cur)
        seed_fact_movies_performance(cur)
        seed_movie_reviews(cur)
        seed_dim_reviews(cur)
        conn.commit()
        print("Seed concluído com sucesso!")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()