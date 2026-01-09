# CAD Generator Module

A generic CAD generator module for the Mechanical Assistant FastAPI backend that supports multiple CAD engines.

## Overview

The CAD Generator module provides a unified interface for generating CAD files using different engines:
- **CadQuery**: Generates STEP files (cross-platform)
- **SolidWorks**: Generates native SLDPRT files via COM API (Windows only)

## Architecture

### Components

1. **`app/cad/generator.py`** - Main interface
   - `CADGenerator` class: Generic generator with engine abstraction
   - Supports multiple engines through a single API
   - Standardized response format

2. **`app/cad/cadquery_builder.py`** - CadQuery implementation
   - `build_step()` function: Generates deterministic STEP files
   - Uses CadQuery library for cross-platform CAD generation
   - Supports boxes, holes, and fillets

3. **`app/cad/solidworks_builder.py`** - SolidWorks implementation
   - `build_sldprt()` function: Generates native SolidWorks parts
   - Uses SolidWorks COM API via pywin32
   - Creates parametric features (extrusions, holes, fillets)
   - Requires Windows and SolidWorks installation

## Usage

### Basic Example

```python
from app.cad.generator import CADGenerator
from app.domain.intent import PartIntent, DimensionIntent

# Create generator
generator = CADGenerator(output_dir="/tmp/cad_output")

# Define part
part = PartIntent(
    shape="box",
    dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0)
)

# Generate STEP file using CadQuery
result = generator.generate(part, engine="cadquery")

if result["status"] == "ok":
    print(f"File created: {result['file_path']}")
else:
    print(f"Errors: {result['errors']}")
```

### With Features (Holes and Fillets)

```python
from app.domain.intent import HoleIntent, FilletIntent

part = PartIntent(
    shape="box",
    dimensions=DimensionIntent(length=100.0, width=100.0, height=50.0),
    holes=[
        HoleIntent(diameter=20.0, depth=30.0, location="center")
    ],
    fillets=[
        FilletIntent(radius=5.0, location="all edges")
    ]
)

result = generator.generate(part, engine="cadquery")
```

### Using SolidWorks Engine (Windows only)

```python
# Requires Windows and SolidWorks installation
result = generator.generate(part, engine="solidworks")
```

## API Reference

### CADGenerator

```python
class CADGenerator:
    def __init__(self, output_dir: str = "/tmp")
    def generate(self, part: PartIntent, engine: str) -> Dict[str, any]
```

**Parameters:**
- `output_dir`: Directory for generated CAD files (default: `/tmp`)

**`generate()` Method:**
- `part`: PartIntent specification
- `engine`: `"cadquery"` or `"solidworks"`
- Returns: Dictionary with `status`, `file_path`, and `errors`

**Response Format:**

```python
{
    "status": "ok" | "error",
    "file_path": "path/to/file.step",
    "errors": []  # List of error messages if status is "error"
}
```

### build_step()

```python
def build_step(part: PartIntent, output_dir: Path) -> Path
```

Generates a STEP file using CadQuery.

**Parameters:**
- `part`: PartIntent with shape, dimensions, holes, fillets
- `output_dir`: Output directory path

**Returns:** Path to generated STEP file

**Raises:**
- `ValueError`: Invalid or missing dimensions
- `RuntimeError`: Generation or export failure

### build_sldprt()

```python
def build_sldprt(part: PartIntent, output_dir: Path) -> Path
```

Generates a SLDPRT file using SolidWorks COM API.

**Parameters:**
- `part`: PartIntent with shape, dimensions, holes, fillets
- `output_dir`: Output directory path

**Returns:** Path to generated SLDPRT file

**Raises:**
- `ImportError`: pywin32 not installed
- `RuntimeError`: SolidWorks not available or generation failure
- `ValueError`: Invalid or missing dimensions

## Input Schema (PartIntent)

```python
PartIntent(
    shape: Literal["box"],              # Currently only "box" supported
    dimensions: DimensionIntent,         # Required
    holes: List[HoleIntent],             # Optional
    fillets: List[FilletIntent],         # Optional
    material: Optional[str],             # Optional metadata
    missing_information: List[str]       # Optional validation info
)

DimensionIntent(
    length: float,   # in mm
    width: float,    # in mm
    height: float    # in mm
)

HoleIntent(
    diameter: float,         # in mm
    depth: float,            # in mm
    location: Optional[str]  # e.g., "center", "top"
)

FilletIntent(
    radius: float,           # in mm
    location: Optional[str]  # e.g., "all edges", "top", "bottom"
)
```

## Examples

See `examples_generator.py` for comprehensive usage examples including:
- Simple box generation
- Parts with holes and fillets
- Complex parts with multiple features
- Error handling
- SolidWorks engine usage

Run examples:
```bash
python examples_generator.py
```

## Testing

Comprehensive test suite with 18 tests covering:
- Generator initialization and directory creation
- CadQuery engine with various features
- Error handling for invalid inputs
- File generation and uniqueness
- SolidWorks engine (graceful degradation)

Run tests:
```bash
pytest tests/test_generator.py -v
```

## Dependencies

### Required for CadQuery
- `cadquery >= 2.4.0`
- `pydantic >= 2.5.0`

### Required for SolidWorks (Windows only)
- `pywin32`
- SolidWorks installation

## Supported Features (Phase 1)

### Shapes
- ✅ Box (rectangular prism)
- ❌ Cylinder (future)
- ❌ Sphere (future)

### Features
- ✅ Extrusion (box creation)
- ✅ Holes (with diameter, depth, location)
- ✅ Fillets (with radius, edge selection)
- ❌ Chamfers (future)
- ❌ Patterns (future)

### Engines
- ✅ CadQuery (STEP files)
- ✅ SolidWorks (SLDPRT files)
- ❌ FreeCAD (future)
- ❌ OpenSCAD (future)

## Error Handling

The generator handles various error conditions gracefully:

1. **Unsupported Engine**: Returns error with list of supported engines
2. **Missing Dependencies**: Clear error messages for missing libraries (e.g., pywin32)
3. **Invalid Input**: Validation errors for missing or invalid dimensions
4. **Generation Failures**: Runtime errors with descriptive messages
5. **Partial Data**: Gracefully skips invalid holes or fillets

## Design Principles

1. **Engine Agnostic**: Same input schema works with all engines
2. **Modular**: Each builder is independent and focused
3. **Typed**: Full type hints for all functions and classes
4. **Documented**: Comprehensive docstrings and examples
5. **Testable**: Extensive test coverage with clear assertions
6. **Deterministic**: Same input produces consistent output

## Future Enhancements

- Support for additional shapes (cylinder, sphere, cone)
- More feature types (chamfers, patterns, shells)
- Additional engines (FreeCAD, OpenSCAD)
- Parametric dimensions with constraints
- Assembly support
- Material properties in output files
- Optimization and validation improvements

## License

MIT License - Part of the Mechanical Assistant project
