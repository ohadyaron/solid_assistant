"""
CadQuery builder for generating STEP files.
Generates deterministic STEP files based on PartIntent specifications.
"""
from pathlib import Path
from datetime import datetime
import cadquery as cq

from app.domain.intent import PartIntent


def build_step(part: PartIntent, output_dir: Path) -> Path:
    """
    Build a STEP file from PartIntent using CadQuery.
    
    This function creates a deterministic CAD model from the provided
    PartIntent specification and exports it as a STEP file.
    
    Args:
        part: PartIntent specification containing shape, dimensions, holes, and fillets
        output_dir: Directory where the STEP file will be saved
        
    Returns:
        Path: Full path to the generated STEP file
        
    Raises:
        ValueError: If required dimensions are missing or invalid
        RuntimeError: If CAD generation or export fails
    """
    # Validate required fields
    if not part.shape:
        raise ValueError("Part shape is required")
    
    if not part.dimensions:
        raise ValueError("Part dimensions are required")
    
    if not all([
        part.dimensions.length,
        part.dimensions.width,
        part.dimensions.height
    ]):
        raise ValueError("All dimensions (length, width, height) are required")
    
    try:
        # Create base shape
        if part.shape == "box":
            result = _create_box(
                part.dimensions.length,
                part.dimensions.width,
                part.dimensions.height
            )
        else:
            raise ValueError(f"Unsupported shape: {part.shape}")
        
        # Apply holes if any
        for hole in part.holes:
            result = _add_hole(result, hole)
        
        # Apply fillets if any
        for fillet in part.fillets:
            result = _add_fillet(result, fillet)
        
        # Generate filename with timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"part_{timestamp}.step"
        filepath = output_dir / filename
        
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Export to STEP format
        cq.exporters.export(result, str(filepath))
        
        return filepath
        
    except Exception as e:
        raise RuntimeError(f"Failed to build STEP file: {str(e)}") from e


def _create_box(length: float, width: float, height: float) -> cq.Workplane:
    """
    Create a box shape using CadQuery.
    
    Args:
        length: Box length in mm
        width: Box width in mm
        height: Box height in mm
        
    Returns:
        CadQuery Workplane with box shape
    """
    return cq.Workplane("XY").box(length, width, height)


def _add_hole(workplane: cq.Workplane, hole) -> cq.Workplane:
    """
    Add a hole to the workplane.
    
    Args:
        workplane: Current CadQuery workplane
        hole: HoleIntent with diameter, depth, and optional location
        
    Returns:
        Updated CadQuery Workplane with hole added
    """
    if not hole.diameter or not hole.depth:
        # Skip holes without required dimensions
        return workplane
    
    # Parse location - default to center (0, 0)
    x, y = 0.0, 0.0
    if hole.location:
        # Simple location parsing: "center" -> (0, 0)
        # For more complex locations, would need additional parsing logic
        if hole.location.lower() == "center":
            x, y = 0.0, 0.0
        # Could extend to parse coordinates like "x:10,y:20"
    
    # Add hole to top face
    return (
        workplane
        .faces(">Z")  # Select top face
        .workplane()
        .center(x, y)
        .hole(hole.diameter, hole.depth)
    )


def _add_fillet(workplane: cq.Workplane, fillet) -> cq.Workplane:
    """
    Add fillets to edges.
    
    Args:
        workplane: Current CadQuery workplane
        fillet: FilletIntent with radius and optional location
        
    Returns:
        Updated CadQuery Workplane with fillets added
    """
    if not fillet.radius:
        # Skip fillets without radius
        return workplane
    
    # Parse location for which edges to fillet
    if not fillet.location or fillet.location.lower() in ["all", "all edges"]:
        # Fillet all edges
        return workplane.edges().fillet(fillet.radius)
    elif "top" in fillet.location.lower():
        # Fillet only top edges
        return workplane.faces(">Z").edges().fillet(fillet.radius)
    elif "bottom" in fillet.location.lower():
        # Fillet only bottom edges
        return workplane.faces("<Z").edges().fillet(fillet.radius)
    else:
        # Default to all edges if location not recognized
        return workplane.edges().fillet(fillet.radius)
