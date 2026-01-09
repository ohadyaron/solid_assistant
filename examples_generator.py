"""
Example usage of the CAD Generator module.

This script demonstrates how to use the generic CAD generator to create
CAD files using different engines (CadQuery and SolidWorks).
"""
import tempfile
from pathlib import Path
from app.cad.generator import CADGenerator
from app.domain.intent import PartIntent, DimensionIntent, HoleIntent, FilletIntent


# Use cross-platform temporary directory
EXAMPLES_OUTPUT_DIR = Path(tempfile.gettempdir()) / "cad_examples"


def example_simple_box():
    """Example: Generate a simple box using CadQuery."""
    print("\n=== Example 1: Simple Box ===")
    
    generator = CADGenerator(output_dir=str(EXAMPLES_OUTPUT_DIR))
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0)
    )
    
    result = generator.generate(part, engine="cadquery")
    
    if result["status"] == "ok":
        print(f"✓ Success! File created at: {result['file_path']}")
    else:
        print(f"✗ Error: {result['errors']}")


def example_box_with_hole():
    """Example: Generate a box with a hole in the center."""
    print("\n=== Example 2: Box with Center Hole ===")
    
    generator = CADGenerator(output_dir=str(EXAMPLES_OUTPUT_DIR))
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=100.0, height=50.0),
        holes=[
            HoleIntent(diameter=20.0, depth=30.0, location="center")
        ]
    )
    
    result = generator.generate(part, engine="cadquery")
    
    if result["status"] == "ok":
        print(f"✓ Success! File created at: {result['file_path']}")
    else:
        print(f"✗ Error: {result['errors']}")


def example_box_with_fillets():
    """Example: Generate a box with rounded edges (fillets)."""
    print("\n=== Example 3: Box with Fillets ===")
    
    generator = CADGenerator(output_dir=str(EXAMPLES_OUTPUT_DIR))
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=80.0, width=60.0, height=40.0),
        fillets=[
            FilletIntent(radius=5.0, location="all edges")
        ]
    )
    
    result = generator.generate(part, engine="cadquery")
    
    if result["status"] == "ok":
        print(f"✓ Success! File created at: {result['file_path']}")
    else:
        print(f"✗ Error: {result['errors']}")


def example_complex_part():
    """Example: Generate a complex part with multiple features."""
    print("\n=== Example 4: Complex Part with Holes and Fillets ===")
    
    generator = CADGenerator(output_dir=str(EXAMPLES_OUTPUT_DIR))
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=150.0, width=100.0, height=50.0),
        holes=[
            HoleIntent(diameter=10.0, depth=25.0, location="center"),
            HoleIntent(diameter=15.0, depth=30.0, location="center")
        ],
        fillets=[
            FilletIntent(radius=3.0, location="top"),
            FilletIntent(radius=2.0, location="all edges")
        ],
        material="aluminum"
    )
    
    result = generator.generate(part, engine="cadquery")
    
    if result["status"] == "ok":
        print(f"✓ Success! File created at: {result['file_path']}")
        print(f"  Material: {part.material}")
    else:
        print(f"✗ Error: {result['errors']}")


def example_solidworks():
    """Example: Generate a part using SolidWorks engine (Windows only)."""
    print("\n=== Example 5: SolidWorks Engine (Windows only) ===")
    
    generator = CADGenerator(output_dir=str(EXAMPLES_OUTPUT_DIR))
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0)
    )
    
    result = generator.generate(part, engine="solidworks")
    
    if result["status"] == "ok":
        print(f"✓ Success! File created at: {result['file_path']}")
    else:
        print(f"✗ Error (expected on non-Windows): {result['errors'][0]}")


def example_error_handling():
    """Example: Error handling for unsupported engines and invalid data."""
    print("\n=== Example 6: Error Handling ===")
    
    generator = CADGenerator(output_dir=str(EXAMPLES_OUTPUT_DIR))
    
    # Test 1: Unsupported engine
    print("\nTest 1: Unsupported engine")
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0)
    )
    result = generator.generate(part, engine="invalid_engine")
    print(f"Result: {result['status']}")
    print(f"Error: {result['errors'][0]}")
    
    # Test 2: Missing dimensions
    print("\nTest 2: Missing dimensions")
    part = PartIntent(shape="box", dimensions=None)
    result = generator.generate(part, engine="cadquery")
    print(f"Result: {result['status']}")
    print(f"Error: {result['errors'][0]}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("CAD Generator Module Examples")
    print("=" * 60)
    
    example_simple_box()
    example_box_with_hole()
    example_box_with_fillets()
    example_complex_part()
    example_solidworks()
    example_error_handling()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print(f"Check {EXAMPLES_OUTPUT_DIR} for generated STEP files")
    print("=" * 60)


if __name__ == "__main__":
    main()
