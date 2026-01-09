/**
 * Type definitions for occt-import-js
 * This library doesn't provide TypeScript types, so we define them here
 */

declare module 'occt-import-js' {
  export interface TessellationParams {
    linearDeflection?: number;
    angularDeflection?: number;
  }

  export interface OcctMesh {
    name: string;
    color: [number, number, number];
    brep_faces: Array<{
      first: number;
      last: number;
    }>;
    attributes: {
      position: {
        array: Float32Array | number[];
      };
      normal: {
        array: Float32Array | number[];
      };
      index?: {
        array: Uint32Array | number[];
      };
    };
  }

  export interface OcctResult {
    success: boolean;
    root: {
      name: string;
      meshes: number[];
      children: number[];
    };
    meshes: OcctMesh[];
  }

  export interface OcctImportJS {
    ReadStepFile: (content: Uint8Array, params: TessellationParams | null) => OcctResult;
    ReadBrepFile: (content: Uint8Array, params: TessellationParams | null) => OcctResult;
    ReadIgesFile: (content: Uint8Array, params: TessellationParams | null) => OcctResult;
  }

  function occtimportjs(): Promise<OcctImportJS>;
  export default occtimportjs;
}
