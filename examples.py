#!/usr/bin/env python3
"""
Example usage of the Mechanical Assistant API.
Demonstrates both direct usage and API endpoints.
"""
from app.domain.models import CadPart, Dimensions, Hole, Fillet, Position
from app.services.part_generator import PartGenerationService
from app.cad import CadBuilder


def example_1_simple_box():
    """Example 1: Create a simple box."""
    print("Example 1: Simple Box")
    print("-" * 50)
    
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=100, width=50, height=30)
    )
    
    service = PartGenerationService()
    result = service.generate_part_with_name(part, "simple_box")
    
    print(f"Status: {result.status}")
    print(f"File: {result.step_file_path}")
    print(f"Message: {result.message}")
    print()


def example_2_box_with_hole():
    """Example 2: Create a box with a centered hole."""
    print("Example 2: Box with Centered Hole")
    print("-" * 50)
    
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=100, width=100, height=50),
        holes=[
            Hole(
                diameter=20,
                depth=30,
                position=Position(x=0, y=0, z=0)
            )
        ]
    )
    
    service = PartGenerationService()
    result = service.generate_part_with_name(part, "box_with_hole")
    
    print(f"Status: {result.status}")
    print(f"File: {result.step_file_path}")
    print(f"Message: {result.message}")
    print()


def example_3_box_with_fillets():
    """Example 3: Create a box with rounded edges."""
    print("Example 3: Box with Fillets")
    print("-" * 50)
    
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=80, width=60, height=40),
        fillets=[
            Fillet(radius=5, edges="all")
        ]
    )
    
    service = PartGenerationService()
    result = service.generate_part_with_name(part, "box_with_fillets")
    
    print(f"Status: {result.status}")
    print(f"File: {result.step_file_path}")
    print(f"Message: {result.message}")
    print()


def example_4_complex_part():
    """Example 4: Create a complex part with multiple features."""
    print("Example 4: Complex Part")
    print("-" * 50)
    
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=150, width=100, height=50),
        holes=[
            Hole(diameter=10, depth=25, position=Position(x=30, y=20, z=0)),
            Hole(diameter=15, depth=30, position=Position(x=-30, y=-20, z=0)),
            Hole(diameter=8, depth=20, position=Position(x=0, y=0, z=0))
        ],
        fillets=[
            Fillet(radius=3, edges="top")
        ],
        material="aluminum"
    )
    
    service = PartGenerationService()
    result = service.generate_part_with_name(part, "complex_part")
    
    print(f"Status: {result.status}")
    print(f"File: {result.step_file_path}")
    print(f"Message: {result.message}")
    print()


def example_5_direct_cad_builder():
    """Example 5: Use CAD builder directly."""
    print("Example 5: Direct CAD Builder Usage")
    print("-" * 50)
    
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=60, width=60, height=25),
        holes=[
            Hole(diameter=12, depth=20, position=Position(x=15, y=15, z=0))
        ]
    )
    
    # Use the convenience method
    CadBuilder.create_and_export(part, "output/direct_builder_example.step")
    
    print("Status: success")
    print("File: output/direct_builder_example.step")
    print("Message: Created using CadBuilder directly")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Mechanical Assistant - Usage Examples")
    print("=" * 50 + "\n")
    
    example_1_simple_box()
    example_2_box_with_hole()
    example_3_box_with_fillets()
    example_4_complex_part()
    example_5_direct_cad_builder()
    
    print("=" * 50)
    print("All examples completed successfully!")
    print("Check the 'output/' directory for generated STEP files.")
    print("=" * 50)
