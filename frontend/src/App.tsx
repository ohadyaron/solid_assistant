/**
 * Main App Component
 * Sets up React Router and React Query
 */
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from './lib/queryClient';
import { Navigation } from './components/Navigation';
import { HomePage } from './pages/HomePage';
import { InterpretPage } from './pages/InterpretPage';
import { PartsPage } from './pages/PartsPage';
import { ViewerPage } from './pages/ViewerPage';
import './App.css';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="app">
          <Navigation />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/interpret" element={<InterpretPage />} />
              <Route path="/parts" element={<PartsPage />} />
              <Route path="/viewer" element={<ViewerPage />} />
            </Routes>
          </main>
          <footer className="footer">
            <p>Mechanical Assistant API v0.1.0</p>
          </footer>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
