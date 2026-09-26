import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api';
import { setToken } from '../auth';

export function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const data = await login({ username, password });
      setToken(data.access_token);
      navigate('/');
    } catch {
      setError('Usuário ou senha inválidos.');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="page">
      <div className="catalog-intro">
        <span className="catalog-kicker">
          <span className="dot" /> Acesso restrito
        </span>
        <h1>Entrar como administrador</h1>
      </div>

      <form onSubmit={handleSubmit} className="review-form login-form">
        <label>
          Usuário
          <input
            type="text"
            required
            autoFocus
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
        </label>
        <label>
          Senha
          <input
            type="password"
            required
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>
        {error && <p className="error">{error}</p>}
        <button type="submit" className="button-primary" disabled={submitting}>
          {submitting ? 'Entrando...' : 'Entrar'}
        </button>
      </form>
    </div>
  );
}