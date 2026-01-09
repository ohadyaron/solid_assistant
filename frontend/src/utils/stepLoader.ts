/**
 * Utility functions for loading and processing STEP files
 * Uses occt-import-js to parse STEP files and convert them to Three.js compatible geometry
 */
import * as THREE from 'three';
import type { OcctImportJS, OcctResult, OcctMesh } from 'occt-import-js';

// Lazy load occt-import-js module
let occtInstance: OcctImportJS | null = null;

/**
 * Initialize and load the OCCT WebAssembly module
 * This is done once and cached for subsequent uses
 */
async function loadOcct(): Promise<OcctImportJS> {
  if (occtInstance) {
    return occtInstance;
  }

  try {
    // Dynamically import occt-import-js
    // The module exports a function that returns a promise
    const module = await import('occt-import-js');
    
    // Handle both CommonJS and ES module exports
    let occtimportjs;
    if (typeof module.default === 'function') {
      occtimportjs = module.default;
    } else if (typeof module === 'function') {
      occtimportjs = module;
    } else {
      throw new Error('Unexpected module format');
    }
    
    // Call the function to initialize OCCT
    const instance = await occtimportjs();
    occtInstance = instance;
    return instance;
  } catch (error) {
    console.error('Failed to load OCCT module:', error);
    throw new Error(`Failed to initialize OCCT WebAssembly module: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Load a STEP file from a URL and parse it using OCCT
 * @param url - URL to the STEP file
 * @returns Parsed OCCT result containing mesh data
 */
export async function loadStepFile(url: string): Promise<OcctResult> {
  // Load the OCCT WebAssembly module
  const occt = await loadOcct();

  // Fetch the STEP file
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch STEP file: ${response.statusText}`);
  }

  // Convert to Uint8Array for OCCT processing
  const buffer = await response.arrayBuffer();
  const fileBuffer = new Uint8Array(buffer);

  // Parse the STEP file with OCCT
  const result = occt.ReadStepFile(fileBuffer, null);

  if (!result.success) {
    throw new Error('Failed to parse STEP file');
  }

  return result;
}

/**
 * Convert OCCT mesh data to Three.js BufferGeometry
 * @param mesh - OCCT mesh object containing vertices, normals, and indices
 * @returns Three.js BufferGeometry ready for rendering
 */
export function createGeometryFromOcctMesh(mesh: OcctMesh): THREE.BufferGeometry {
  const geometry = new THREE.BufferGeometry();

  // Set position attribute (vertices)
  if (mesh.attributes.position) {
    geometry.setAttribute(
      'position',
      new THREE.BufferAttribute(mesh.attributes.position.array, 3)
    );
  }

  // Set normal attribute for lighting
  if (mesh.attributes.normal) {
    geometry.setAttribute(
      'normal',
      new THREE.BufferAttribute(mesh.attributes.normal.array, 3)
    );
  }

  // Set index attribute for efficient rendering
  if (mesh.attributes.index) {
    geometry.setIndex(new THREE.BufferAttribute(mesh.attributes.index.array, 1));
  }

  // Compute bounding box and sphere for camera fitting
  geometry.computeBoundingBox();
  geometry.computeBoundingSphere();

  return geometry;
}

/**
 * Convert OCCT result to an array of Three.js mesh objects
 * @param result - Parsed OCCT result
 * @returns Array of objects containing geometry, color, and name
 */
export function convertOcctResultToMeshes(result: OcctResult) {
  return result.meshes.map((mesh) => {
    const geometry = createGeometryFromOcctMesh(mesh);
    const color = new THREE.Color(
      mesh.color[0] / 255,
      mesh.color[1] / 255,
      mesh.color[2] / 255
    );

    return {
      geometry,
      color,
      name: mesh.name,
    };
  });
}

/**
 * Calculate optimal camera position based on bounding box
 * @param boundingBox - Three.js bounding box of the model
 * @returns Optimal camera position
 */
export function calculateCameraPosition(boundingBox: THREE.Box3): THREE.Vector3 {
  const center = new THREE.Vector3();
  boundingBox.getCenter(center);

  const size = new THREE.Vector3();
  boundingBox.getSize(size);

  // Position camera at a distance proportional to model size
  const maxDim = Math.max(size.x, size.y, size.z);
  const distance = maxDim * 2;

  return new THREE.Vector3(
    center.x + distance * 0.7,
    center.y + distance * 0.7,
    center.z + distance * 0.7
  );
}
