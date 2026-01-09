"""
Tests for part generation service.
"""
import pytest
from pathlib import Path
from app.services.part_generator import PartGenerationService
from app.domain.models import CadPart, Dimensions, Hole, Fillet, Position


def test_generate_simple_part(tmp_path):
    """Test generating a simple part."""
    service = PartGenerationService(output_dir=str(tmp_path))
    
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=100, width=50, height=30)
    )
    
    result = service.generate_part(part)
    
    assert result.status == "success"
    assert result.step_file_path != ""
    assert Path(result.step_file_path).exists()


def test_generate_part_with_features(tmp_path):
    """Test generating a part with holes and fillets."""
    service = PartGenerationService(output_dir=str(tmp_path))
    
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=100, width=100, height=50),
        holes=[
            Hole(diameter=10, depth=25, position=Position(x=20, y=20, z=0))
        ],
        fillets=[
            Fillet(radius=5, edges="all")
        ]
    )
    
    result = service.generate_part(part)
    
    assert result.status == "success"
    assert result.step_file_path != ""
    assert Path(result.step_file_path).exists()


def test_generate_part_with_custom_name(tmp_path):
    """Test generating a part with a custom filename."""
    service = PartGenerationService(output_dir=str(tmp_path))
    
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=75, width=75, height=40)
    )
    
    result = service.generate_part_with_name(part, "custom_part")
    
    assert result.status == "success"
    assert "custom_part.step" in result.step_file_path
    assert Path(result.step_file_path).exists()


def test_generate_invalid_part(tmp_path):
    """Test that invalid parts are rejected."""
    service = PartGenerationService(output_dir=str(tmp_path))
    
    # Create part with holes too close together
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=50, width=50, height=25),
        holes=[
            Hole(diameter=15, depth=20, position=Position(x=0, y=0, z=0)),
            Hole(diameter=15, depth=20, position=Position(x=5, y=0, z=0))
        ]
    )
    
    result = service.generate_part(part)
    
    assert result.status == "error"
    assert "too close" in result.message.lower()


def test_generate_part_with_warnings(tmp_path):
    """Test generating a part that produces warnings."""
    service = PartGenerationService(output_dir=str(tmp_path))
    
    # Create part with deep hole that causes depth-to-diameter warning
    # Depth/diameter = 60/5 = 12, which exceeds MAX_HOLE_DEPTH_RATIO of 10
    part = CadPart(
        shape="box",
        dimensions=Dimensions(length=100, width=100, height=70),
        holes=[
            Hole(diameter=5, depth=60, position=Position(x=0, y=0, z=0))
        ]
    )
    
    result = service.generate_part(part)
    
    assert result.status == "success"
    assert result.message is not None
    assert "warning" in result.message.lower()


def test_output_directory_creation(tmp_path):
    """Test that output directory is created if it doesn't exist."""
    test_dir = tmp_path / "test_mechanical_output"
    service = PartGenerationService(output_dir=str(test_dir))
    
    assert service.output_dir.exists()
    assert service.output_dir.is_dir()
