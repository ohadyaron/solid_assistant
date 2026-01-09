/**
 * StepViewer Component
 * 
 * A reusable React component for displaying 3D STEP files (.step/.stp) in the browser.
 * Uses Three.js and React Three Fiber for 3D rendering, with occt-import-js for STEP parsing.
 * 
 * Features:
 * - Interactive orbit controls (rotate, zoom, pan)
 * - Loading and error states
 * - Automatic camera positioning
 * - Responsive canvas sizing
 * - Material with proper lighting
 * 
 * @example
 * <StepViewer fileUrl="/path/to/model.step" />
 */
import { useEffect, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';
import { useStepLoader } from '../hooks/useStepLoader';
import { Loading } from './Loading';
import { ErrorDisplay } from './ErrorDisplay';
import './StepViewer.css';

interface StepViewerProps {
  fileUrl: string;
  className?: string;
}

/**
 * Component to render individual meshes from the STEP file
 */
function StepMesh({ geometry, color, name }: {
  geometry: THREE.BufferGeometry;
  color: THREE.Color;
  name: string;
}) {
  return (
    <mesh geometry={geometry} name={name}>
      <meshStandardMaterial
        color={color}
        side={THREE.DoubleSide}
        metalness={0.3}
        roughness={0.7}
      />
    </mesh>
  );
}

/**
 * Scene component containing all meshes and lighting
 */
function StepScene({ meshes, cameraPosition }: {
  meshes: Array<{ geometry: THREE.BufferGeometry; color: THREE.Color; name: string }>;
  cameraPosition: THREE.Vector3 | null;
}) {
  const cameraRef = useRef<THREE.PerspectiveCamera>(null);

  // Update camera position when model loads
  useEffect(() => {
    if (cameraRef.current && cameraPosition) {
      cameraRef.current.position.copy(cameraPosition);
      cameraRef.current.lookAt(0, 0, 0);
    }
  }, [cameraPosition]);

  return (
    <>
      {/* Camera setup with initial position */}
      <PerspectiveCamera
        ref={cameraRef}
        makeDefault
        fov={50}
        position={cameraPosition ? [cameraPosition.x, cameraPosition.y, cameraPosition.z] : [100, 100, 100]}
      />

      {/* Orbit controls for user interaction */}
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        rotateSpeed={0.5}
        zoomSpeed={1}
        panSpeed={0.5}
      />

      {/* Lighting setup */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} castShadow />
      <directionalLight position={[-10, -10, -5]} intensity={0.5} />
      <hemisphereLight intensity={0.3} />

      {/* Grid helper for visual reference */}
      <Grid
        args={[100, 100]}
        cellColor="#888888"
        sectionColor="#444444"
        fadeDistance={200}
        fadeStrength={1}
      />

      {/* Render all meshes from the STEP file */}
      {meshes.map((mesh, index) => (
        <StepMesh
          key={`${mesh.name}-${index}`}
          geometry={mesh.geometry}
          color={mesh.color}
          name={mesh.name}
        />
      ))}
    </>
  );
}

/**
 * Main StepViewer component
 * 
 * Loads and displays a STEP file with interactive 3D controls.
 * Handles loading and error states automatically.
 * 
 * @param fileUrl - URL to the STEP file (.step or .stp)
 * @param className - Optional CSS class for styling
 */
export function StepViewer({ fileUrl, className }: StepViewerProps) {
  const { meshes, loading, error, cameraPosition } = useStepLoader(fileUrl);

  // Show loading state while parsing STEP file
  if (loading) {
    return (
      <div className={`step-viewer-container ${className || ''}`}>
        <Loading message="Loading STEP file..." size="large" />
      </div>
    );
  }

  // Show error state if loading failed
  if (error) {
    return (
      <div className={`step-viewer-container ${className || ''}`}>
        <ErrorDisplay message={error} />
      </div>
    );
  }

  // Show message if no meshes were loaded
  if (meshes.length === 0) {
    return (
      <div className={`step-viewer-container ${className || ''}`}>
        <div className="step-viewer-empty">
          <p>No geometry found in STEP file</p>
        </div>
      </div>
    );
  }

  // Render the 3D scene
  return (
    <div className={`step-viewer-container ${className || ''}`}>
      <Canvas
        className="step-viewer-canvas"
        gl={{
          antialias: true,
          alpha: true,
          preserveDrawingBuffer: true,
        }}
        shadows
      >
        <StepScene meshes={meshes} cameraPosition={cameraPosition} />
      </Canvas>
      <div className="step-viewer-info">
        <span>{meshes.length} mesh{meshes.length !== 1 ? 'es' : ''} loaded</span>
      </div>
    </div>
  );
}
