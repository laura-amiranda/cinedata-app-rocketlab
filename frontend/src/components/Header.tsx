import { Link, useNavigate } from 'react-router-dom';
import { clearToken, useIsAuthenticated } from '../auth';

export function Header() {
  const authenticated = useIsAuthenticated();
  const navigate = useNavigate();

  function handleLogout() {
    clearToken();
    navigate('/');
  }

  return (
    <header className="site-header">
      <div className="site-header-inner">
        <Link to="/" className="brand">
          Notaflix
        </Link>
        <div className="header-actions">
          {authenticated ? (
            <>
              <Link to="/movies/new" className="button-new">
                <span aria-hidden="true">+</span> Novo filme
              </Link>
              <button type="button" className="button-logout" onClick={handleLogout}>
                Sair
              </button>
            </>
          ) : (
            <Link to="/login" className="button-login">
              Entrar
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}