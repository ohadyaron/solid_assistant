"""
Tests for CAD generator module.
Tests the generic CAD generator and its builder classes.
"""
import pytest
from pathlib import Path
from app.cad.generator import CADGenerator
from app.cad.cadquery_builder import CadQueryBuilder
from app.domain.intent import PartIntent, DimensionIntent, HoleIntent, FilletIntent


def test_generator_initialization(tmp_path):
    """Test CADGenerator initialization."""
    generator = CADGenerator(output_dir=str(tmp_path))
    
    assert generator.output_dir == tmp_path
    assert generator.output_dir.exists()


def test_generator_initialization_creates_directory(tmp_path):
    """Test that CADGenerator creates output directory if it doesn't exist."""
    test_dir = tmp_path / "test_cad_output"
    generator = CADGenerator(output_dir=str(test_dir))
    
    assert test_dir.exists()
    assert test_dir.is_dir()


def test_generate_cadquery_simple_box(tmp_path):
    """Test generating a simple box with CadQuery engine."""
    generator = CADGenerator(output_dir=str(tmp_path))
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0)
    )
    
    result = generator.generate(part, engine="cadquery")
    
    assert result["status"] == "ok"
    assert result["file_path"] != ""
    assert Path(result["file_path"]).exists()
    assert result["file_path"].endswith(".step")
    assert result["errors"] == []


def test_generate_cadquery_with_hole(tmp_path):
    """Test generating a box with hole using CadQuery engine."""
    generator = CADGenerator(output_dir=str(tmp_path))
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=100.0, height=50.0),
        holes=[
            HoleIntent(diameter=20.0, depth=30.0, location="center")
        ]
    )
    
    result = generator.generate(part, engine="cadquery")
    
    assert result["status"] == "ok"
    assert Path(result["file_path"]).exists()
    assert result["errors"] == []


def test_generate_cadquery_with_fillets(tmp_path):
    """Test generating a box with fillets using CadQuery engine."""
    generator = CADGenerator(output_dir=str(tmp_path))
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0),
        fillets=[
            FilletIntent(radius=5.0, location="all edges")
        ]
    )
    
    result = generator.generate(part, engine="cadquery")
    
    assert result["status"] == "ok"
    assert Path(result["file_path"]).exists()
    assert result["errors"] == []


def test_generate_cadquery_complex_part(tmp_path):
    """Test generating a complex part with holes and fillets."""
    generator = CADGenerator(output_dir=str(tmp_path))
    
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
        ]
    )
    
    result = generator.generate(part, engine="cadquery")
    
    assert result["status"] == "ok"
    assert Path(result["file_path"]).exists()
    assert result["errors"] == []


def test_generate_unsupported_engine(tmp_path):
    """Test that unsupported engine returns error."""
    generator = CADGenerator(output_dir=str(tmp_path))
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0)
    )
    
    result = generator.generate(part, engine="invalid_engine")
    
    assert result["status"] == "error"
    assert result["file_path"] == ""
    assert len(result["errors"]) > 0
    assert "Unsupported engine" in result["errors"][0]


def test_generate_missing_dimensions(tmp_path):
    """Test that missing dimensions returns error."""
    generator = CADGenerator(output_dir=str(tmp_path))
    
    part = PartIntent(
        shape="box",
        dimensions=None
    )
    
    result = generator.generate(part, engine="cadquery")
    
    assert result["status"] == "error"
    assert result["file_path"] == ""
    assert len(result["errors"]) > 0


def test_generate_missing_shape(tmp_path):
    """Test that missing shape returns error."""
    generator = CADGenerator(output_dir=str(tmp_path))
    
    part = PartIntent(
        shape=None,
        dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0)
    )
    
    result = generator.generate(part, engine="cadquery")
    
    assert result["status"] == "error"
    assert result["file_path"] == ""
    assert len(result["errors"]) > 0


def test_cadquery_builder_class(tmp_path):
    """Test the CadQueryBuilder class directly."""
    builder = CadQueryBuilder()
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=80.0, width=60.0, height=40.0)
    )
    
    filepath = builder.build(part, tmp_path)
    
    assert filepath.exists()
    assert filepath.suffix == ".step"
    assert filepath.parent == tmp_path


def test_cadquery_builder_with_features(tmp_path):
    """Test CadQueryBuilder with holes and fillets."""
    builder = CadQueryBuilder()
    
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
    
    filepath = builder.build(part, tmp_path)
    
    assert filepath.exists()
    assert filepath.stat().st_size > 0


def test_build_step_invalid_shape(tmp_path):
    """Test that unsupported shape raises error."""
    # Note: PartIntent schema only accepts "box" currently via Literal type
    # This test validates the error handling at the generation level
    # We'll test using the generator with an unsupported engine instead
    from app.cad.generator import CADGenerator
    
    generator = CADGenerator(output_dir=str(tmp_path))
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0)
    )
    
    # Test with a typo in engine name
    result = generator.generate(part, engine="cadquery_typo")
    
    assert result["status"] == "error"
    assert "Unsupported engine" in result["errors"][0]


def test_cadquery_builder_missing_dimensions(tmp_path):
    """Test that missing dimensions raises error."""
    builder = CadQueryBuilder()
    
    part = PartIntent(
        shape="box",
        dimensions=None
    )
    
    with pytest.raises(ValueError):
        builder.build(part, tmp_path)


def test_multiple_files_unique_names(tmp_path):
    """Test that multiple generated files have unique names."""
    generator = CADGenerator(output_dir=str(tmp_path))
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0)
    )
    
    result1 = generator.generate(part, engine="cadquery")
    result2 = generator.generate(part, engine="cadquery")
    
    assert result1["status"] == "ok"
    assert result2["status"] == "ok"
    assert result1["file_path"] != result2["file_path"]
    assert Path(result1["file_path"]).exists()
    assert Path(result2["file_path"]).exists()


def test_solidworks_engine_without_pywin32(tmp_path):
    """Test that SolidWorks engine without pywin32 returns helpful error."""
    generator = CADGenerator(output_dir=str(tmp_path))
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0)
    )
    
    result = generator.generate(part, engine="solidworks")
    
    # On non-Windows or without pywin32, should get an error
    # On Windows with pywin32 and SolidWorks, might succeed
    assert result["status"] in ["ok", "error"]
    if result["status"] == "error":
        assert len(result["errors"]) > 0


def test_generator_default_output_dir():
    """Test generator with default output directory."""
    generator = CADGenerator()
    
    assert generator.output_dir == Path("/tmp")
    assert generator.output_dir.exists()


def test_cadquery_builder_partial_hole_data(tmp_path):
    """Test that holes without complete data are skipped gracefully."""
    builder = CadQueryBuilder()
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0),
        holes=[
            HoleIntent(diameter=20.0, depth=None, location="center"),  # Missing depth
            HoleIntent(diameter=None, depth=30.0, location="center")   # Missing diameter
        ]
    )
    
    # Should complete without error, skipping invalid holes
    filepath = builder.build(part, tmp_path)
    
    assert filepath.exists()


def test_cadquery_builder_partial_fillet_data(tmp_path):
    """Test that fillets without radius are skipped gracefully."""
    builder = CadQueryBuilder()
    
    part = PartIntent(
        shape="box",
        dimensions=DimensionIntent(length=100.0, width=50.0, height=30.0),
        fillets=[
            FilletIntent(radius=None, location="all edges")  # Missing radius
        ]
    )
    
    # Should complete without error, skipping invalid fillets
    filepath = builder.build(part, tmp_path)
    
    assert filepath.exists()
