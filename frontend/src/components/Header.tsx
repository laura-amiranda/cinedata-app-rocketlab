import { Link } from 'react-router-dom';

export function Header() {
  return (
    <header className="site-header">
      <div className="site-header-inner">
        <Link to="/" className="brand">
          Notaflix
        </Link>
        <Link to="/movies/new" className="button-new">
          <span aria-hidden="true">+</span> Novo filme
        </Link>
      </div>
    </header>
  );
}