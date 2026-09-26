import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { addReview, deleteMovie, getMovie } from '../api';
import type { MovieDetail } from '../types';
import { StarRatingDisplay } from '../components/StarRating';
import { limparTitulo } from '../utils/text';
import { useIsAuthenticated } from '../auth';

export function MovieDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const authenticated = useIsAuthenticated();

  const [movie, setMovie] = useState<MovieDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [reviewNome, setReviewNome] = useState('');
  const [reviewNota, setReviewNota] = useState('10');
  const [reviewComentario, setReviewComentario] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [reviewError, setReviewError] = useState<string | null>(null);

  function loadMovie(skMovieId: string) {
    setLoading(true);
    setError(null);
    getMovie(skMovieId)
      .then(setMovie)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    if (id) loadMovie(id);
  }, [id]);

  async function handleDelete() {
    if (!id) return;
    if (!window.confirm('Tem certeza que deseja remover este filme?')) return;
    await deleteMovie(id);
    navigate('/');
  }

  async function handleReviewSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!id) return;
    setSubmitting(true);
    setReviewError(null);
    try {
      await addReview(id, {
        nome: reviewNome,
        nota: Number(reviewNota),
        comentario: reviewComentario,
      });
      setReviewNome('');
      setReviewNota('10');
      setReviewComentario('');
      loadMovie(id);
    } catch (err) {
      setReviewError((err as Error).message);
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <div className="page">Carregando...</div>;
  if (error) return <div className="page error">Erro: {error}</div>;
  if (!movie) return <div className="page">Filme não encontrado.</div>;

  return (
    <div className="page">
      <button type="button" className="back-link" onClick={() => navigate(-1)}>
        &larr; Voltar ao catálogo
      </button>

      <div className="movie-detail">
        {movie.url_poster ? (
          <img src={movie.url_poster} alt={movie.titulo} className="detail-poster" />
        ) : (
          <div className="detail-poster poster-placeholder">Sem imagem</div>
        )}
        <div className="detail-info">
          <h1>{limparTitulo(movie.titulo)}</h1>
          <p className="detail-meta">
            {movie.ano_lancamento ?? '—'} · {movie.duracao_minutos ? `${movie.duracao_minutos} min` : 'duração desconhecida'} ·{' '}
            {movie.status_filme ?? '—'}
          </p>
          <p className="detail-field">
            <strong>Gêneros:</strong> {movie.generos.length ? movie.generos.join(', ') : '—'}
          </p>
          <p className="detail-field">
            <strong>Diretor(es):</strong> {movie.diretores.length ? movie.diretores.join(', ') : '—'}
          </p>
          <p className="detail-field">
            <strong>Elenco:</strong> {movie.atores.length ? movie.atores.join(', ') : '—'}
          </p>
          <p className="detail-field">
            <strong>Produtora(s):</strong> {movie.produtoras.length ? movie.produtoras.join(', ') : '—'}
          </p>
          <p className="synopsis">{movie.sinopse ? limparTitulo(movie.sinopse) : 'Sem sinopse cadastrada.'}</p>

          <div className="rating-summary">
            {movie.nota_media !== null ? (
              <>
                <span className="rating-score">
                  {movie.nota_media.toFixed(1)}
                  <small>/10</small>
                </span>
                <div>
                  <StarRatingDisplay notaSobreDez={movie.nota_media} />
                  <div className="rating-detail">{movie.qtd_avaliacoes} avaliação(ões)</div>
                </div>
              </>
            ) : (
              <span className="stars-empty">Sem avaliações ainda</span>
            )}
          </div>

          {authenticated && (
            <div className="actions">
              <Link to={`/movies/${movie.sk_movie_id}/edit`} className="button-secondary">
                Editar
              </Link>
              <button className="button-danger" onClick={handleDelete}>
                Remover filme
              </button>
            </div>
          )}
        </div>
      </div>

      <section className="reviews-section">
        <h2>Avaliações</h2>
        {movie.reviews.length === 0 && <p className="results-count">Nenhuma avaliação ainda. Seja a primeira pessoa a avaliar!</p>}
        {movie.reviews.length > 0 && (
          <ul className="review-list">
            {movie.reviews.map((review) => (
              <li key={review.sk_movie_review_id}>
                <div className="review-head">
                  <strong>{review.nome}</strong>
                  <span className="review-score">{review.nota.toFixed(1)}/10</span>
                </div>
                <p>{review.comentario}</p>
              </li>
            ))}
          </ul>
        )}

        <form onSubmit={handleReviewSubmit} className="review-form">
          <h3>Nova avaliação</h3>
          <label>
            Seu nome
            <input
              type="text"
              required
              value={reviewNome}
              onChange={(event) => setReviewNome(event.target.value)}
            />
          </label>
          <label>
            Nota (0 a 10)
            <input
              type="number"
              min={0}
              max={10}
              step={0.5}
              required
              value={reviewNota}
              onChange={(event) => setReviewNota(event.target.value)}
            />
          </label>
          <label>
            Comentário
            <textarea
              required
              value={reviewComentario}
              onChange={(event) => setReviewComentario(event.target.value)}
            />
          </label>
          {reviewError && <p className="error">{reviewError}</p>}
          <button type="submit" className="button-primary" disabled={submitting}>
            {submitting ? 'Enviando...' : 'Enviar avaliação'}
          </button>
        </form>
      </section>
    </div>
  );
}