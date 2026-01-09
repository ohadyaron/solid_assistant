/**
 * Custom React hook for loading and processing STEP files
 * Manages loading state, errors, and mesh data
 */
import { useState, useEffect, useCallback } from 'react';
import * as THREE from 'three';
import {
  loadStepFile,
  convertOcctResultToMeshes,
  calculateCameraPosition,
} from '../utils/stepLoader';

interface MeshData {
  geometry: THREE.BufferGeometry;
  color: THREE.Color;
  name: string;
}

interface UseStepLoaderResult {
  meshes: MeshData[];
  loading: boolean;
  error: string | null;
  cameraPosition: THREE.Vector3 | null;
  reload: () => void;
}

/**
 * Hook to load and process STEP files
 * @param fileUrl - URL to the STEP file to load
 * @returns Loading state, error state, mesh data, and optimal camera position
 */
export function useStepLoader(fileUrl: string | null): UseStepLoaderResult {
  const [meshes, setMeshes] = useState<MeshData[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [cameraPosition, setCameraPosition] = useState<THREE.Vector3 | null>(null);

  const loadFile = useCallback(async () => {
    if (!fileUrl) {
      setMeshes([]);
      setCameraPosition(null);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Load and parse the STEP file
      const result = await loadStepFile(fileUrl);

      // Convert OCCT result to Three.js meshes
      const meshData = convertOcctResultToMeshes(result);
      setMeshes(meshData);

      // Calculate overall bounding box for camera positioning
      if (meshData.length > 0) {
        const boundingBox = new THREE.Box3();
        meshData.forEach((mesh) => {
          if (mesh.geometry.boundingBox) {
            boundingBox.union(mesh.geometry.boundingBox);
          }
        });

        const optimalPosition = calculateCameraPosition(boundingBox);
        setCameraPosition(optimalPosition);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load STEP file';
      setError(errorMessage);
      setMeshes([]);
      setCameraPosition(null);
    } finally {
      setLoading(false);
    }
  }, [fileUrl]);

  // Load file when URL changes
  useEffect(() => {
    loadFile();
  }, [loadFile]);

  return {
    meshes,
    loading,
    error,
    cameraPosition,
    reload: loadFile,
  };
}
