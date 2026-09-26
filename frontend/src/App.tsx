import { Route, Routes } from 'react-router-dom';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { CatalogPage } from './pages/CatalogPage';
import { MovieDetailPage } from './pages/MovieDetailPage';
import { MovieFormPage } from './pages/MovieFormPage';
import './App.css';

function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<CatalogPage />} />
        <Route path="/movies/new" element={<MovieFormPage />} />
        <Route path="/movies/:id" element={<MovieDetailPage />} />
        <Route path="/movies/:id/edit" element={<MovieFormPage />} />
      </Routes>
      <Footer />
    </>
  );
}

export default App;