/**
 * Viewer Page Component
 * 
 * Demonstrates the StepViewer component with example STEP files.
 * Allows users to select from predefined models or use generated STEP files from the API.
 */
import { useState } from 'react';
import { StepViewer } from '../components/StepViewer';
import './ViewerPage.css';

// Predefined sample models
const sampleModels = [
  {
    name: 'Sample Cube',
    url: '/models/sample-cube.step',
    description: 'A simple cube model for testing',
  },
];

export function ViewerPage() {
  const [selectedUrl, setSelectedUrl] = useState<string>(sampleModels[0].url);
  const [customUrl, setCustomUrl] = useState<string>('');
  const [useCustomUrl, setUseCustomUrl] = useState<boolean>(false);

  const handleModelSelect = (url: string) => {
    setSelectedUrl(url);
    setUseCustomUrl(false);
  };

  const handleCustomUrlSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (customUrl.trim()) {
      setSelectedUrl(customUrl.trim());
      setUseCustomUrl(true);
    }
  };

  const displayUrl = useCustomUrl ? customUrl : selectedUrl;

  return (
    <div className="viewer-page">
      <div className="viewer-header">
        <h1>STEP File Viewer</h1>
        <p className="viewer-description">
          View and interact with 3D STEP files directly in your browser. Use orbit controls to
          rotate, zoom, and pan around the model.
        </p>
      </div>

      <div className="viewer-content">
        <div className="viewer-sidebar">
          <div className="viewer-section">
            <h3>Sample Models</h3>
            <div className="model-list">
              {sampleModels.map((model) => (
                <button
                  key={model.url}
                  className={`model-button ${!useCustomUrl && selectedUrl === model.url ? 'active' : ''}`}
                  onClick={() => handleModelSelect(model.url)}
                >
                  <div className="model-name">{model.name}</div>
                  <div className="model-description">{model.description}</div>
                </button>
              ))}
            </div>
          </div>

          <div className="viewer-section">
            <h3>Custom URL</h3>
            <form onSubmit={handleCustomUrlSubmit} className="custom-url-form">
              <input
                type="text"
                value={customUrl}
                onChange={(e) => setCustomUrl(e.target.value)}
                placeholder="Enter STEP file URL..."
                className="custom-url-input"
              />
              <button type="submit" className="custom-url-button">
                Load
              </button>
            </form>
            <p className="helper-text">
              You can also load STEP files generated from the{' '}
              <a href="/parts">Parts Generator</a> by using the full URL to the generated file.
            </p>
          </div>

          <div className="viewer-section">
            <h3>Controls</h3>
            <ul className="controls-list">
              <li>
                <strong>Rotate:</strong> Left click + drag
              </li>
              <li>
                <strong>Zoom:</strong> Mouse wheel
              </li>
              <li>
                <strong>Pan:</strong> Right click + drag
              </li>
            </ul>
          </div>

          <div className="viewer-section">
            <h3>Features</h3>
            <ul className="features-list">
              <li>✓ Real-time 3D rendering</li>
              <li>✓ WebAssembly-powered STEP parsing</li>
              <li>✓ Interactive orbit controls</li>
              <li>✓ Automatic camera positioning</li>
              <li>✓ Responsive design</li>
              <li>✓ Multi-part support</li>
            </ul>
          </div>
        </div>

        <div className="viewer-main">
          <div className="viewer-toolbar">
            <span className="current-model">
              {useCustomUrl ? 'Custom URL' : sampleModels.find((m) => m.url === selectedUrl)?.name || 'Unknown'}
            </span>
            {displayUrl && (
              <span className="model-url" title={displayUrl}>
                {displayUrl}
              </span>
            )}
          </div>
          <StepViewer fileUrl={displayUrl} />
        </div>
      </div>

      <div className="viewer-info-section">
        <h2>About STEP Files</h2>
        <p>
          STEP (Standard for the Exchange of Product Data) is an ISO standard for representing
          3D product data. It's widely used in CAD/CAM/CAE systems for exchanging geometric and
          manufacturing information.
        </p>
        <p>
          This viewer uses <strong>OpenCascade.js</strong> (via occt-import-js) compiled to
          WebAssembly for parsing STEP files, and <strong>Three.js</strong> with{' '}
          <strong>React Three Fiber</strong> for rendering the 3D geometry in your browser.
        </p>
      </div>
    </div>
  );
}
