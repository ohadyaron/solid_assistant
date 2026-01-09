"""
CAD builder using CadQuery.
Deterministic CAD generation with no LLM involvement.
"""
from typing import List
import cadquery as cq
from app.domain.models import CadPart, Hole, Fillet


class CadBuilder:
    """Builds CAD models deterministically using CadQuery."""
    
    def __init__(self):
        """Initialize the CAD builder."""
        self.result: cq.Workplane = None
    
    def build_part(self, part: CadPart) -> cq.Workplane:
        """
        Build a complete CAD part from specification.
        
        Args:
            part: CadPart specification
            
        Returns:
            CadQuery Workplane with the built part
        """
        # Validate holes are within bounds
        part.validate_holes_within_bounds()
        
        # Create base shape
        if part.shape == "box":
            self.result = self._create_box(
                part.dimensions.length,
                part.dimensions.width,
                part.dimensions.height
            )
        else:
            raise ValueError(f"Unsupported shape: {part.shape}")
        
        # Apply holes
        for hole in part.holes:
            self._add_hole(hole)
        
        # Apply fillets
        for fillet in part.fillets:
            self._add_fillet(fillet, part)
        
        return self.result
    
    def _create_box(self, length: float, width: float, height: float) -> cq.Workplane:
        """
        Create a box shape.
        
        Args:
            length: Box length in mm
            width: Box width in mm
            height: Box height in mm
            
        Returns:
            CadQuery Workplane with box
        """
        return cq.Workplane("XY").box(length, width, height)
    
    def _add_hole(self, hole: Hole) -> None:
        """
        Add a hole to the current part.
        
        Args:
            hole: Hole specification
        """
        if self.result is None:
            raise ValueError("No base shape created yet")
        
        # Position the workplane at the hole location
        # CadQuery uses center-based positioning
        self.result = (
            self.result
            .faces(">Z")  # Select top face
            .workplane()
            .center(hole.position.x, hole.position.y)
            .hole(hole.diameter, hole.depth)
        )
    
    def _add_fillet(self, fillet: Fillet, part: CadPart) -> None:
        """
        Add fillets to edges.
        
        Args:
            fillet: Fillet specification
            part: Complete part specification for context
        """
        if self.result is None:
            raise ValueError("No base shape created yet")
        
        if fillet.edges == "all":
            # Fillet all edges
            self.result = self.result.edges().fillet(fillet.radius)
        elif fillet.edges == "top":
            # Fillet only top edges
            self.result = (
                self.result
                .faces(">Z")
                .edges()
                .fillet(fillet.radius)
            )
        elif fillet.edges == "bottom":
            # Fillet only bottom edges
            self.result = (
                self.result
                .faces("<Z")
                .edges()
                .fillet(fillet.radius)
            )
    
    def export_step(self, filepath: str) -> None:
        """
        Export the current part to STEP format.
        
        Args:
            filepath: Output STEP file path
        """
        if self.result is None:
            raise ValueError("No part to export")
        
        cq.exporters.export(self.result, filepath)
    
    @staticmethod
    def create_and_export(part: CadPart, filepath: str) -> None:
        """
        Convenience method to build and export in one step.
        
        Args:
            part: CadPart specification
            filepath: Output STEP file path
        """
        builder = CadBuilder()
        builder.build_part(part)
        builder.export_step(filepath)
