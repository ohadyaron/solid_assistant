/**
 * Home Page Component
 */
import { Link } from 'react-router-dom';
import './HomePage.css';

export function HomePage() {
  return (
    <div className="home-page">
      <div className="hero-section">
        <h1 className="hero-title">Mechanical Assistant</h1>
        <p className="hero-description">
          Generate CAD parts from natural language descriptions
        </p>
      </div>

      <div className="features-grid">
        <div className="feature-card">
          <div className="feature-icon">💬</div>
          <h3>Natural Language Processing</h3>
          <p>Describe your CAD part in plain English and let AI interpret it</p>
          <Link to="/interpret" className="feature-link">
            Try Interpreter →
          </Link>
        </div>

        <div className="feature-card">
          <div className="feature-icon">🔧</div>
          <h3>CAD Part Generation</h3>
          <p>Create precise STEP files from validated specifications</p>
          <Link to="/parts" className="feature-link">
            Generate Part →
          </Link>
        </div>
      </div>

      <div className="info-section">
        <h2>How it works</h2>
        <ol className="steps-list">
          <li>
            <strong>Interpret:</strong> Describe your part in natural language
          </li>
          <li>
            <strong>Review:</strong> Check the structured intent and complete missing information
          </li>
          <li>
            <strong>Generate:</strong> Create a manufacturable STEP file
          </li>
        </ol>
      </div>

      <div className="api-info">
        <h3>API Endpoints</h3>
        <div className="endpoint-list">
          <div className="endpoint">
            <code>POST /api/v1/interpret</code>
            <span>Convert natural language to structured intent</span>
          </div>
          <div className="endpoint">
            <code>POST /api/v1/parts</code>
            <span>Generate STEP files from CAD specifications</span>
          </div>
        </div>
      </div>
    </div>
  );
}
