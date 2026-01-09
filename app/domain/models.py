"""
Domain models for CAD parts.
Deterministic schemas for representing mechanical parts.
"""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


class Position(BaseModel):
    """3D position coordinates."""
    x: float = Field(default=0.0, description="X coordinate in mm")
    y: float = Field(default=0.0, description="Y coordinate in mm")
    z: float = Field(default=0.0, description="Z coordinate in mm")


class Dimensions(BaseModel):
    """Part dimensions."""
    length: float = Field(gt=0, description="Length in mm")
    width: float = Field(gt=0, description="Width in mm")
    height: float = Field(gt=0, description="Height in mm")


class Hole(BaseModel):
    """Hole feature specification."""
    diameter: float = Field(gt=0, description="Hole diameter in mm")
    depth: float = Field(gt=0, description="Hole depth in mm")
    position: Position = Field(default_factory=Position, description="Hole position")
    
    @field_validator('diameter')
    @classmethod
    def validate_diameter(cls, v: float) -> float:
        """Validate hole diameter meets minimum manufacturing requirements."""
        if v < 1.0:
            raise ValueError("Hole diameter must be at least 1mm for CNC machining")
        return v


class Fillet(BaseModel):
    """Fillet feature specification."""
    radius: float = Field(gt=0, description="Fillet radius in mm")
    edges: Literal["all", "top", "bottom"] = Field(
        default="all",
        description="Which edges to apply fillet to"
    )
    
    @field_validator('radius')
    @classmethod
    def validate_radius(cls, v: float) -> float:
        """Validate fillet radius meets minimum manufacturing requirements."""
        if v < 0.5:
            raise ValueError("Fillet radius must be at least 0.5mm for CNC machining")
        return v


class CadPart(BaseModel):
    """
    Complete CAD part specification.
    Represents a deterministic, manufacturable part.
    """
    shape: Literal["box"] = Field(
        default="box",
        description="Base shape type (currently only box supported)"
    )
    dimensions: Dimensions = Field(description="Part dimensions")
    holes: List[Hole] = Field(
        default_factory=list,
        description="List of holes to create"
    )
    fillets: List[Fillet] = Field(
        default_factory=list,
        description="List of fillets to apply"
    )
    material: Optional[str] = Field(
        default="aluminum",
        description="Material for manufacturing context"
    )
    
    @field_validator('dimensions')
    @classmethod
    def validate_dimensions(cls, v: Dimensions) -> Dimensions:
        """Validate dimensions meet minimum manufacturing requirements."""
        min_size = 10.0
        if v.length < min_size or v.width < min_size or v.height < min_size:
            raise ValueError(f"All dimensions must be at least {min_size}mm")
        
        max_size = 1000.0
        if v.length > max_size or v.width > max_size or v.height > max_size:
            raise ValueError(f"All dimensions must be at most {max_size}mm")
        
        return v
    
    def validate_holes_within_bounds(self) -> None:
        """Validate that all holes are within part bounds."""
        for hole in self.holes:
            if abs(hole.position.x) > self.dimensions.length / 2:
                raise ValueError(f"Hole position x={hole.position.x} exceeds part length bounds")
            if abs(hole.position.y) > self.dimensions.width / 2:
                raise ValueError(f"Hole position y={hole.position.y} exceeds part width bounds")
            if hole.depth > self.dimensions.height:
                raise ValueError(f"Hole depth {hole.depth} exceeds part height {self.dimensions.height}")


class PartGenerationResult(BaseModel):
    """Result of part generation."""
    step_file_path: str = Field(description="Path to generated STEP file")
    status: Literal["success", "error"] = Field(description="Generation status")
    message: Optional[str] = Field(default=None, description="Optional status message")
