/**
 * Navigation Component
 */
import { Link, useLocation } from 'react-router-dom';
import './Navigation.css';

export function Navigation() {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="navigation">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          <span className="nav-logo-icon">🔧</span>
          <span className="nav-logo-text">Mechanical Assistant</span>
        </Link>

        <div className="nav-links">
          <Link 
            to="/" 
            className={`nav-link ${isActive('/') ? 'active' : ''}`}
          >
            Home
          </Link>
          <Link 
            to="/interpret" 
            className={`nav-link ${isActive('/interpret') ? 'active' : ''}`}
          >
            Interpreter
          </Link>
          <Link 
            to="/parts" 
            className={`nav-link ${isActive('/parts') ? 'active' : ''}`}
          >
            Generator
          </Link>
        </div>
      </div>
    </nav>
  );
}
