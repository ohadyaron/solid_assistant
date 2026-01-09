"""
Tests for CAD builder.
"""
import pytest
from app.cad import CadBuilder
from app.domain.models import CadPart, Dimensions, Hole, Fillet, Position


def test_build_simple_box():
    """Test building a simple box."""
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=100, width=50, height=30)
    )
    
    builder = CadBuilder()
    result = builder.build_part(part)
    
    assert result is not None
    # CadQuery Workplane should have a valid shape
    assert result.val() is not None


def test_build_box_with_hole():
    """Test building a box with a hole."""
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
    
    builder = CadBuilder()
    result = builder.build_part(part)
    
    assert result is not None
    assert result.val() is not None


def test_build_box_with_fillets():
    """Test building a box with fillets."""
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=100, width=50, height=30),
        fillets=[
            Fillet(radius=5, edges="all")
        ]
    )
    
    builder = CadBuilder()
    result = builder.build_part(part)
    
    assert result is not None
    assert result.val() is not None


def test_build_complex_part():
    """Test building a complex part with holes and fillets."""
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=150, width=100, height=50),
        holes=[
            Hole(diameter=10, depth=25, position=Position(x=30, y=20, z=0)),
            Hole(diameter=15, depth=30, position=Position(x=-30, y=-20, z=0))
        ],
        fillets=[
            Fillet(radius=3, edges="top")
        ]
    )
    
    builder = CadBuilder()
    result = builder.build_part(part)
    
    assert result is not None
    assert result.val() is not None


def test_export_step(tmp_path):
    """Test exporting a part to STEP file."""
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=50, width=50, height=25)
    )
    
    output_file = tmp_path / "test_part.step"
    
    builder = CadBuilder()
    builder.build_part(part)
    builder.export_step(str(output_file))
    
    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_hole_out_of_bounds():
    """Test that hole validation catches out-of-bounds positions."""
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=50, width=50, height=25),
        holes=[
            Hole(diameter=10, depth=20, position=Position(x=100, y=0, z=0))
        ]
    )
    
    builder = CadBuilder()
    
    with pytest.raises(ValueError):
        builder.build_part(part)


def test_create_and_export_convenience(tmp_path):
    """Test the convenience method for creating and exporting."""
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=60, width=40, height=20)
    )
    
    output_file = tmp_path / "convenience_test.step"
    
    CadBuilder.create_and_export(part, str(output_file))
    
    assert output_file.exists()
    assert output_file.stat().st_size > 0
