/**
 * Utility functions for loading and processing STEP files
 * Uses occt-import-js to parse STEP files and convert them to Three.js compatible geometry
 */
import * as THREE from 'three';
import type { OcctImportJS, OcctResult, OcctMesh } from 'occt-import-js';

// Lazy load occt-import-js module
let occtInstance: OcctImportJS | null = null;
let occtLoadPromise: Promise<OcctImportJS> | null = null;

/**
 * Load the OCCT script dynamically via script tag
 * This is necessary because occt-import-js is a UMD module
 */
function loadOcctScript(): Promise<any> {
  return new Promise((resolve, reject) => {
    // Check if already loaded
    if ((window as any).occtimportjs) {
      resolve((window as any).occtimportjs);
      return;
    }

    // Create script element
    const script = document.createElement('script');
    script.src = '/node_modules/occt-import-js/dist/occt-import-js.js';
    script.async = true;
    
    script.onload = () => {
      // The UMD module should now be available on window
      if ((window as any).occtimportjs) {
        resolve((window as any).occtimportjs);
      } else {
        reject(new Error('occt-import-js script loaded but occtimportjs not found on window'));
      }
    };
    
    script.onerror = () => {
      reject(new Error('Failed to load occt-import-js script'));
    };
    
    document.head.appendChild(script);
  });
}

/**
 * Initialize and load the OCCT WebAssembly module
 * This is done once and cached for subsequent uses
 */
async function loadOcct(): Promise<OcctImportJS> {
  if (occtInstance) {
    return occtInstance;
  }

  // If already loading, return the same promise
  if (occtLoadPromise) {
    return occtLoadPromise;
  }

  occtLoadPromise = (async () => {
    try {
      console.log('Loading OCCT module via script tag...');
      
      // Load the UMD module via script tag
      const occtFactory = await loadOcctScript();
      console.log('OCCT factory loaded:', typeof occtFactory);
      
      if (typeof occtFactory !== 'function') {
        throw new Error('occt-import-js did not export a function. Type: ' + typeof occtFactory);
      }
      
      console.log('Initializing OCCT WebAssembly...');
      // Call the factory function to initialize the OCCT WebAssembly instance
      const instance = await occtFactory();
      console.log('OCCT instance created successfully');
      occtInstance = instance;
      return instance;
    } catch (error) {
      console.error('Failed to load OCCT module:', error);
      occtLoadPromise = null; // Reset so we can try again
      throw new Error(`Failed to initialize OCCT WebAssembly module: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  })();

  return occtLoadPromise;
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
  const result = occt.ReadStepFile(fileBuffer, {
    linearDeflection: 0.001,
    angularDeflection: 0.1,
    quality: 1.0,
    edgeLength: 0.001
  });

  if (!result.success) {
    throw new Error('Failed to parse STEP file');
  }

  if (!result.meshes || result.meshes.length === 0) {
    throw new Error('No meshes found in STEP file');
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
    const positions = mesh.attributes.position.array;
    const positionArray = positions instanceof Float32Array ? positions : new Float32Array(positions);
    geometry.setAttribute(
      'position',
      new THREE.BufferAttribute(positionArray, 3)
    );
  }

  // Set index attribute - check both attributes.index and root level index
  const indexData = mesh.attributes.index || (mesh as any).index;
  if (indexData && indexData.array) {
    const indices = indexData.array;
    const indexArray = indices instanceof Uint32Array || indices instanceof Uint16Array 
      ? indices 
      : new Uint32Array(indices);
    geometry.setIndex(new THREE.BufferAttribute(indexArray, 1));
  }

  // Set normal attribute for lighting
  if (mesh.attributes.normal) {
    const normals = mesh.attributes.normal.array;
    const normalArray = normals instanceof Float32Array ? normals : new Float32Array(normals);
    geometry.setAttribute(
      'normal',
      new THREE.BufferAttribute(normalArray, 3)
    );
  } else {
    // Compute vertex normals if not provided
    geometry.computeVertexNormals();
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
    
    // Default to gray if color is undefined
    const color = mesh.color && mesh.color.length >= 3
      ? new THREE.Color(
          mesh.color[0] / 255,
          mesh.color[1] / 255,
          mesh.color[2] / 255
        )
      : new THREE.Color(0.7, 0.7, 0.7);

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
