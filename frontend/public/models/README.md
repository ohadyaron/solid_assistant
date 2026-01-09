# Sample Models Directory

This directory contains sample STEP files for testing the 3D viewer.

## Adding Sample Files

You can add your own STEP files (.step or .stp) to this directory to test the viewer.

### Option 1: Use Generated Files

Generate STEP files using the [Parts Generator](/parts) page and save them to this directory.

### Option 2: Use Test Files

Copy test files from the occt-import-js package:

```bash
cp node_modules/occt-import-js/test/testfiles/cube-fcstd/cube.step public/models/sample-cube.step
```

### Option 3: Download Sample STEP Files

You can download sample STEP files from various sources:
- [GrabCAD](https://grabcad.com/library)
- [Thingiverse](https://www.thingiverse.com/)
- [Free CAD Files](https://www.freecadfiles.com/)

## Recommended Test Files

The following test files from occt-import-js work well with the viewer:
- `testfiles/cube-fcstd/cube.step` - Simple cube
- `testfiles/cube-10x10mm/Cube 10x10.stp` - 10mm cube
- `testfiles/conical-surface/conical-surface.step` - Conical surface

## Note

STEP files (*.step, *.stp) are ignored by Git by default. This is intentional to keep the repository size manageable.
