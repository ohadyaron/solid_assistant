/**
 * Error Display Component
 */
import './ErrorDisplay.css';

interface ErrorDisplayProps {
  title?: string;
  message: string;
  onRetry?: () => void;
}

export function ErrorDisplay({ 
  title = 'Error', 
  message, 
  onRetry 
}: ErrorDisplayProps) {
  return (
    <div className="error-container">
      <div className="error-icon">⚠️</div>
      <h3 className="error-title">{title}</h3>
      <p className="error-message">{message}</p>
      {onRetry && (
        <button onClick={onRetry} className="error-retry-button">
          Try Again
        </button>
      )}
    </div>
  );
}
