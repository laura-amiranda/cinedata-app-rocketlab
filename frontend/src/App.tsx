import type { ReactElement } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { CatalogPage } from './pages/CatalogPage';
import { LoginPage } from './pages/LoginPage';
import { MovieDetailPage } from './pages/MovieDetailPage';
import { MovieFormPage } from './pages/MovieFormPage';
import { useIsAuthenticated } from './auth';
import './App.css';

function RequireAuth({ children }: { children: ReactElement }) {
  const authenticated = useIsAuthenticated();
  return authenticated ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<CatalogPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/movies/new"
          element={
            <RequireAuth>
              <MovieFormPage />
            </RequireAuth>
          }
        />
        <Route path="/movies/:id" element={<MovieDetailPage />} />
        <Route
          path="/movies/:id/edit"
          element={
            <RequireAuth>
              <MovieFormPage />
            </RequireAuth>
          }
        />
      </Routes>
      <Footer />
    </>
  );
}

export default App;