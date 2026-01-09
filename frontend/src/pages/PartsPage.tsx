/**
 * Parts Page - CAD Part Generation
 */
import { useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { useGeneratePart } from '../hooks/useGeneratePart';
import { Loading } from '../components/Loading';
import { ErrorDisplay } from '../components/ErrorDisplay';
import { StepViewer } from '../components/StepViewer';
import { getStepFileUrl } from '../services/api';
import type { CadPart, Hole, Fillet, PartGenerationResult } from '../services/api';
import './PartsPage.css';

interface PartFormData {
  length: number;
  width: number;
  height: number;
  material: string;
  holes: Array<{
    diameter: number;
    depth: number;
    x: number;
    y: number;
    z: number;
  }>;
  fillets: Array<{
    radius: number;
    edges: 'all' | 'top' | 'bottom';
  }>;
}

export function PartsPage() {
  const { register, control, handleSubmit, formState: { errors } } = useForm<PartFormData>({
    defaultValues: {
      length: 100,
      width: 100,
      height: 50,
      material: 'aluminum',
      holes: [],
      fillets: [],
    },
  });
  
  const { fields: holeFields, append: appendHole, remove: removeHole } = useFieldArray({
    control,
    name: 'holes',
  });
  
  const { fields: filletFields, append: appendFillet, remove: removeFillet } = useFieldArray({
    control,
    name: 'fillets',
  });

  const generatePartMutation = useGeneratePart();
  const [result, setResult] = useState<PartGenerationResult | null>(null);

  const onSubmit = async (data: PartFormData) => {
    setResult(null);
    
    const cadPart: CadPart = {
      shape: 'box',
      dimensions: {
        length: data.length,
        width: data.width,
        height: data.height,
      },
      holes: data.holes.map(hole => ({
        diameter: hole.diameter,
        depth: hole.depth,
        position: {
          x: hole.x,
          y: hole.y,
          z: hole.z,
        },
      })) as Hole[],
      fillets: data.fillets as Fillet[],
      material: data.material || 'aluminum',
    };

    try {
      const response = await generatePartMutation.mutateAsync(cadPart);
      setResult(response);
    } catch {
      // Error is handled by the mutation
    }
  };

  return (
    <div className="parts-page">
      <div className="page-header">
        <h1>CAD Part Generator</h1>
        <p>Create a STEP file from CAD specifications</p>
      </div>

      <div className="content-layout">
        <div className="form-container">
          <form onSubmit={handleSubmit(onSubmit)} className="parts-form">
            {/* Dimensions Section */}
            <div className="form-section">
              <h2>Part Dimensions</h2>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="length">Length (mm)</label>
                  <input
                    type="number"
                    id="length"
                    step="0.1"
                    {...register('length', { 
                      required: 'Length is required',
                      min: { value: 10, message: 'Minimum 10mm' },
                      max: { value: 1000, message: 'Maximum 1000mm' }
                    })}
                    className="form-input"
                  />
                  {errors.length && <span className="form-error">{errors.length.message}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="width">Width (mm)</label>
                  <input
                    type="number"
                    id="width"
                    step="0.1"
                    {...register('width', { 
                      required: 'Width is required',
                      min: { value: 10, message: 'Minimum 10mm' },
                      max: { value: 1000, message: 'Maximum 1000mm' }
                    })}
                    className="form-input"
                  />
                  {errors.width && <span className="form-error">{errors.width.message}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="height">Height (mm)</label>
                  <input
                    type="number"
                    id="height"
                    step="0.1"
                    {...register('height', { 
                      required: 'Height is required',
                      min: { value: 10, message: 'Minimum 10mm' },
                      max: { value: 1000, message: 'Maximum 1000mm' }
                    })}
                    className="form-input"
                  />
                  {errors.height && <span className="form-error">{errors.height.message}</span>}
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="material">Material</label>
                <input
                  type="text"
                  id="material"
                  {...register('material')}
                  className="form-input"
                  placeholder="e.g., aluminum, steel, plastic"
                />
              </div>
            </div>

            {/* Holes Section */}
            <div className="form-section">
              <div className="section-header">
                <h2>Holes</h2>
                <button
                  type="button"
                  onClick={() => appendHole({ diameter: 10, depth: 20, x: 0, y: 0, z: 0 })}
                  className="add-button"
                >
                  + Add Hole
                </button>
              </div>

              {holeFields.map((field, index) => (
                <div key={field.id} className="array-item">
                  <div className="array-item-header">
                    <h3>Hole {index + 1}</h3>
                    <button
                      type="button"
                      onClick={() => removeHole(index)}
                      className="remove-button"
                    >
                      Remove
                    </button>
                  </div>

                  <div className="form-row">
                    <div className="form-group">
                      <label>Diameter (mm)</label>
                      <input
                        type="number"
                        step="0.1"
                        {...register(`holes.${index}.diameter`, { 
                          required: 'Required',
                          min: { value: 1, message: 'Min 1mm' }
                        })}
                        className="form-input"
                      />
                      {errors.holes?.[index]?.diameter && (
                        <span className="form-error">{errors.holes[index]!.diameter!.message}</span>
                      )}
                    </div>

                    <div className="form-group">
                      <label>Depth (mm)</label>
                      <input
                        type="number"
                        step="0.1"
                        {...register(`holes.${index}.depth`, { 
                          required: 'Required',
                          min: { value: 1, message: 'Min 1mm' }
                        })}
                        className="form-input"
                      />
                      {errors.holes?.[index]?.depth && (
                        <span className="form-error">{errors.holes[index]!.depth!.message}</span>
                      )}
                    </div>
                  </div>

                  <div className="form-row">
                    <div className="form-group">
                      <label>X Position (mm)</label>
                      <input
                        type="number"
                        step="0.1"
                        {...register(`holes.${index}.x`, { required: 'Required' })}
                        className="form-input"
                      />
                    </div>

                    <div className="form-group">
                      <label>Y Position (mm)</label>
                      <input
                        type="number"
                        step="0.1"
                        {...register(`holes.${index}.y`, { required: 'Required' })}
                        className="form-input"
                      />
                    </div>

                    <div className="form-group">
                      <label>Z Position (mm)</label>
                      <input
                        type="number"
                        step="0.1"
                        {...register(`holes.${index}.z`, { required: 'Required' })}
                        className="form-input"
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Fillets Section */}
            <div className="form-section">
              <div className="section-header">
                <h2>Fillets</h2>
                <button
                  type="button"
                  onClick={() => appendFillet({ radius: 5, edges: 'all' })}
                  className="add-button"
                >
                  + Add Fillet
                </button>
              </div>

              {filletFields.map((field, index) => (
                <div key={field.id} className="array-item">
                  <div className="array-item-header">
                    <h3>Fillet {index + 1}</h3>
                    <button
                      type="button"
                      onClick={() => removeFillet(index)}
                      className="remove-button"
                    >
                      Remove
                    </button>
                  </div>

                  <div className="form-row">
                    <div className="form-group">
                      <label>Radius (mm)</label>
                      <input
                        type="number"
                        step="0.1"
                        {...register(`fillets.${index}.radius`, { 
                          required: 'Required',
                          min: { value: 0.5, message: 'Min 0.5mm' }
                        })}
                        className="form-input"
                      />
                      {errors.fillets?.[index]?.radius && (
                        <span className="form-error">{errors.fillets[index]!.radius!.message}</span>
                      )}
                    </div>

                    <div className="form-group">
                      <label>Edges</label>
                      <select
                        {...register(`fillets.${index}.edges`)}
                        className="form-select"
                      >
                        <option value="all">All edges</option>
                        <option value="top">Top edges</option>
                        <option value="bottom">Bottom edges</option>
                      </select>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <button 
              type="submit" 
              className="submit-button"
              disabled={generatePartMutation.isPending}
            >
              {generatePartMutation.isPending ? 'Generating...' : 'Generate STEP File'}
            </button>
          </form>
        </div>

        <div className="result-container">
          <h2>Generation Result</h2>

          {generatePartMutation.isPending && (
            <Loading message="Generating CAD part..." />
          )}

          {generatePartMutation.isError && (
            <ErrorDisplay
              title="Generation Failed"
              message={generatePartMutation.error.detail || generatePartMutation.error.message}
              onRetry={() => handleSubmit(onSubmit)()}
            />
          )}

          {result && result.status === 'success' && (
            <div className="success-result">
              <div className="success-icon">✅</div>
              <h3>Part Generated Successfully!</h3>
              <div className="result-details">
                <div className="result-item">
                  <span className="result-label">STEP File:</span>
                  <span className="result-value">{result.step_file_path}</span>
                </div>
                {result.message && (
                  <div className="result-item">
                    <span className="result-label">Message:</span>
                    <span className="result-value">{result.message}</span>
                  </div>
                )}
              </div>
              <button
                onClick={() => {
                  const filename = result.step_file_path.split('/').pop() || result.step_file_path.split('\\').pop();
                  const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
                  window.open(`${apiUrl}/api/v1/parts/download/${filename}`, '_blank');
                }}
                className="download-button"
              >
                📥 Download STEP File
              </button>
              
              <div className="step-viewer-wrapper" style={{ marginTop: '20px', height: '500px', width: '100%', border: '1px solid #ddd', borderRadius: '8px', overflow: 'hidden' }}>
                <StepViewer fileUrl={getStepFileUrl(result.step_file_path)} />
              </div>
              
              <p className="result-note" style={{ marginTop: '10px' }}>
                The STEP file has been generated and saved on the server.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
