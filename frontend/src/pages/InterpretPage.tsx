/**
 * Interpret Page - Natural Language to Structured Intent
 */
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useInterpret } from '../hooks/useInterpret';
import { Loading } from '../components/Loading';
import { ErrorDisplay } from '../components/ErrorDisplay';
import type { PartIntent } from '../services/api';
import './InterpretPage.css';

interface InterpretFormData {
  text: string;
}

export function InterpretPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<InterpretFormData>();
  const interpretMutation = useInterpret();
  const [result, setResult] = useState<PartIntent | null>(null);

  const onSubmit = async (data: InterpretFormData) => {
    setResult(null);
    try {
      const response = await interpretMutation.mutateAsync(data.text);
      setResult(response.intent);
    } catch {
      // Error is handled by the mutation
    }
  };

  return (
    <div className="interpret-page">
      <div className="page-header">
        <h1>Natural Language Interpreter</h1>
        <p>Describe your CAD part in plain English</p>
      </div>

      <div className="content-grid">
        <div className="form-section">
          <form onSubmit={handleSubmit(onSubmit)} className="interpret-form">
            <div className="form-group">
              <label htmlFor="text">Part Description</label>
              <textarea
                id="text"
                {...register('text', { 
                  required: 'Please enter a description',
                  minLength: {
                    value: 10,
                    message: 'Description must be at least 10 characters'
                  }
                })}
                className="form-textarea"
                placeholder="Example: Create a 100mm cube with a 20mm hole in the center and 5mm fillets on all edges"
                rows={6}
              />
              {errors.text && (
                <span className="form-error">{errors.text.message}</span>
              )}
            </div>

            <button 
              type="submit" 
              className="submit-button"
              disabled={interpretMutation.isPending}
            >
              {interpretMutation.isPending ? 'Interpreting...' : 'Interpret'}
            </button>
          </form>

          <div className="examples-section">
            <h3>Example Descriptions:</h3>
            <ul>
              <li>"A 50x50x25mm aluminum box"</li>
              <li>"100mm cube with a 10mm hole through the center"</li>
              <li>"Create a 200x100x30mm box with 2mm fillets on all edges"</li>
              <li>"Make a rectangular part 150mm long, 75mm wide, and 40mm tall"</li>
            </ul>
          </div>
        </div>

        <div className="result-section">
          <h2>Structured Intent</h2>
          
          {interpretMutation.isPending && (
            <Loading message="Interpreting your description..." />
          )}

          {interpretMutation.isError && (
            <ErrorDisplay
              title="Interpretation Failed"
              message={interpretMutation.error.detail || interpretMutation.error.message}
              onRetry={() => handleSubmit(onSubmit)()}
            />
          )}

          {result && (
            <div className="result-container">
              <div className="result-card">
                <h3>Basic Information</h3>
                <div className="result-item">
                  <span className="result-label">Shape:</span>
                  <span className="result-value">{result.shape || 'Not specified'}</span>
                </div>
                {result.material && (
                  <div className="result-item">
                    <span className="result-label">Material:</span>
                    <span className="result-value">{result.material}</span>
                  </div>
                )}
              </div>

              {result.dimensions && (
                <div className="result-card">
                  <h3>Dimensions</h3>
                  <div className="result-item">
                    <span className="result-label">Length:</span>
                    <span className="result-value">{result.dimensions.length ? `${result.dimensions.length}mm` : 'Not specified'}</span>
                  </div>
                  <div className="result-item">
                    <span className="result-label">Width:</span>
                    <span className="result-value">{result.dimensions.width ? `${result.dimensions.width}mm` : 'Not specified'}</span>
                  </div>
                  <div className="result-item">
                    <span className="result-label">Height:</span>
                    <span className="result-value">{result.dimensions.height ? `${result.dimensions.height}mm` : 'Not specified'}</span>
                  </div>
                </div>
              )}

              {result.holes && result.holes.length > 0 && (
                <div className="result-card">
                  <h3>Holes ({result.holes.length})</h3>
                  {result.holes.map((hole, index) => (
                    <div key={index} className="feature-item">
                      <strong>Hole {index + 1}:</strong>
                      <div className="result-item">
                        <span className="result-label">Diameter:</span>
                        <span className="result-value">{hole.diameter ? `${hole.diameter}mm` : 'Not specified'}</span>
                      </div>
                      <div className="result-item">
                        <span className="result-label">Depth:</span>
                        <span className="result-value">{hole.depth ? `${hole.depth}mm` : 'Not specified'}</span>
                      </div>
                      {hole.location && (
                        <div className="result-item">
                          <span className="result-label">Location:</span>
                          <span className="result-value">{hole.location}</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {result.fillets && result.fillets.length > 0 && (
                <div className="result-card">
                  <h3>Fillets ({result.fillets.length})</h3>
                  {result.fillets.map((fillet, index) => (
                    <div key={index} className="feature-item">
                      <strong>Fillet {index + 1}:</strong>
                      <div className="result-item">
                        <span className="result-label">Radius:</span>
                        <span className="result-value">{fillet.radius ? `${fillet.radius}mm` : 'Not specified'}</span>
                      </div>
                      {fillet.location && (
                        <div className="result-item">
                          <span className="result-label">Location:</span>
                          <span className="result-value">{fillet.location}</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {result.missing_information && result.missing_information.length > 0 && (
                <div className="result-card warning-card">
                  <h3>⚠️ Missing Information</h3>
                  <ul>
                    {result.missing_information.map((info, index) => (
                      <li key={index}>{info}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="json-section">
                <h3>JSON Output</h3>
                <pre className="json-output">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
