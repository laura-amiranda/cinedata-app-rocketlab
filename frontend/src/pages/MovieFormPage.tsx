import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { createMovie, getMovie, updateMovie } from '../api';
import type { MovieFormData } from '../types';

const EMPTY_FORM: MovieFormData = {
  titulo: '',
  diretor: '',
  ano_lancamento: '',
  genero: '',
  sinopse: '',
};

export function MovieFormPage() {
  const { id } = useParams<{ id: string }>();
  const isEditing = Boolean(id);
  const navigate = useNavigate();

  const [form, setForm] = useState<MovieFormData>(EMPTY_FORM);
  const [loading, setLoading] = useState(isEditing);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    getMovie(id)
      .then((movie) => {
        setForm({
          titulo: movie.titulo,
          diretor: movie.diretores[0] ?? '',
          ano_lancamento: movie.ano_lancamento ? String(movie.ano_lancamento) : '',
          genero: movie.generos[0] ?? '',
          sinopse: movie.sinopse ?? '',
        });
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  function handleChange(field: keyof MovieFormData, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);

    const payload = {
      titulo: form.titulo,
      diretor: form.diretor || null,
      ano_lancamento: form.ano_lancamento ? Number(form.ano_lancamento) : null,
      genero: form.genero || null,
      sinopse: form.sinopse || null,
    };

    try {
      const movie = isEditing && id ? await updateMovie(id, payload) : await createMovie(payload);
      navigate(`/movies/${movie.sk_movie_id}`);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <div className="page">Carregando...</div>;

  return (
    <div className="page">
      <Link to="/" className="back-link">
        &larr; Voltar ao catálogo
      </Link>
      <div className="catalog-intro">
        <span className="catalog-kicker">
          <span className="dot" /> {isEditing ? 'Edição' : 'Novo título'}
        </span>
        <h1>{isEditing ? 'Editar filme' : 'Novo filme'}</h1>
      </div>

      <form onSubmit={handleSubmit} className="movie-form">
        <label className="field-full">
          Título *
          <input
            type="text"
            required
            value={form.titulo}
            onChange={(event) => handleChange('titulo', event.target.value)}
          />
        </label>
        <label>
          Diretor
          <input
            type="text"
            value={form.diretor}
            onChange={(event) => handleChange('diretor', event.target.value)}
          />
        </label>
        <label>
          Ano de lançamento
          <input
            type="number"
            value={form.ano_lancamento}
            onChange={(event) => handleChange('ano_lancamento', event.target.value)}
          />
        </label>
        <label className="field-full">
          Gênero
          <input
            type="text"
            value={form.genero}
            onChange={(event) => handleChange('genero', event.target.value)}
          />
        </label>
        <label className="field-full">
          Sinopse
          <textarea
            value={form.sinopse}
            onChange={(event) => handleChange('sinopse', event.target.value)}
          />
        </label>

        {error && <p className="error field-full">{error}</p>}

        <button type="submit" className="button-primary field-full" disabled={submitting}>
          {submitting ? 'Salvando...' : isEditing ? 'Salvar alterações' : 'Criar filme'}
        </button>
      </form>
    </div>
  );
}