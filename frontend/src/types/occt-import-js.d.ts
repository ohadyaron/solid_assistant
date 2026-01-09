/**
 * Type definitions for occt-import-js
 * This library doesn't provide TypeScript types, so we define them here
 */

declare module 'occt-import-js' {
  export interface OcctMesh {
    name: string;
    color: [number, number, number];
    brep_faces: Array<{
      first: number;
      last: number;
    }>;
    attributes: {
      position: {
        array: Float32Array;
      };
      normal: {
        array: Float32Array;
      };
      index: {
        array: Uint32Array;
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
    ReadStepFile: (content: Uint8Array, params: null) => OcctResult;
    ReadBrepFile: (content: Uint8Array, params: null) => OcctResult;
    ReadIgesFile: (content: Uint8Array, params: null) => OcctResult;
  }

  function occtimportjs(): Promise<OcctImportJS>;
  export default occtimportjs;
}
