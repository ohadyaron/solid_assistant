"""
Validation rules engine for CNC manufacturing constraints.
Enforces manufacturability rules on CAD parts.
"""
from typing import List, Tuple
from app.domain.models import CadPart


class ValidationError(Exception):
    """Raised when a part fails validation."""
    pass


class RulesEngine:
    """Validates parts against CNC manufacturing rules."""
    
    # Manufacturing constraints
    MIN_WALL_THICKNESS = 2.0  # mm
    MIN_HOLE_DIAMETER = 1.0  # mm
    MAX_HOLE_DEPTH_RATIO = 10.0  # depth/diameter ratio
    MIN_FILLET_RADIUS = 0.5  # mm
    MAX_FILLET_RADIUS_RATIO = 0.5  # fillet/smallest dimension ratio
    
    def __init__(self):
        """Initialize the rules engine."""
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self, part: CadPart) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a part against all rules.
        
        Args:
            part: CadPart to validate
            
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        self._validate_dimensions(part)
        self._validate_holes(part)
        self._validate_fillets(part)
        self._validate_hole_positions(part)
        self._validate_wall_thickness(part)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_dimensions(self, part: CadPart) -> None:
        """Validate part dimensions."""
        dims = part.dimensions
        
        # Check minimum dimensions (already validated by Pydantic, but double-check)
        if dims.length < 10 or dims.width < 10 or dims.height < 10:
            self.errors.append(
                f"Part dimensions too small: {dims.length}x{dims.width}x{dims.height}mm. "
                f"Minimum 10mm required for stable CNC machining."
            )
        
        # Check aspect ratios
        aspect_ratios = [
            dims.length / dims.width,
            dims.width / dims.length,
            dims.length / dims.height,
            dims.height / dims.length,
            dims.width / dims.height,
            dims.height / dims.width
        ]
        max_aspect_ratio = max(aspect_ratios)
        if max_aspect_ratio > 20:
            self.warnings.append(
                f"High aspect ratio ({max_aspect_ratio:.1f}:1) may cause stability issues during machining."
            )
    
    def _validate_holes(self, part: CadPart) -> None:
        """Validate hole specifications."""
        for i, hole in enumerate(part.holes):
            # Check diameter
            if hole.diameter < self.MIN_HOLE_DIAMETER:
                self.errors.append(
                    f"Hole {i}: Diameter {hole.diameter}mm is below minimum {self.MIN_HOLE_DIAMETER}mm"
                )
            
            # Check depth-to-diameter ratio
            depth_ratio = hole.depth / hole.diameter
            if depth_ratio > self.MAX_HOLE_DEPTH_RATIO:
                self.warnings.append(
                    f"Hole {i}: Depth-to-diameter ratio {depth_ratio:.1f} exceeds "
                    f"recommended maximum {self.MAX_HOLE_DEPTH_RATIO}. May require special tooling."
                )
            
            # Check if hole is too close to edge
            edge_distance_x = (part.dimensions.length / 2) - abs(hole.position.x)
            edge_distance_y = (part.dimensions.width / 2) - abs(hole.position.y)
            min_edge_distance = max(hole.diameter, self.MIN_WALL_THICKNESS)
            
            if edge_distance_x < min_edge_distance:
                self.warnings.append(
                    f"Hole {i}: Too close to edge (x-axis). Minimum {min_edge_distance}mm recommended."
                )
            if edge_distance_y < min_edge_distance:
                self.warnings.append(
                    f"Hole {i}: Too close to edge (y-axis). Minimum {min_edge_distance}mm recommended."
                )
    
    def _validate_fillets(self, part: CadPart) -> None:
        """Validate fillet specifications."""
        smallest_dim = min(
            part.dimensions.length,
            part.dimensions.width,
            part.dimensions.height
        )
        
        for i, fillet in enumerate(part.fillets):
            # Check minimum radius
            if fillet.radius < self.MIN_FILLET_RADIUS:
                self.errors.append(
                    f"Fillet {i}: Radius {fillet.radius}mm is below minimum {self.MIN_FILLET_RADIUS}mm"
                )
            
            # Check maximum radius relative to part size
            max_fillet = smallest_dim * self.MAX_FILLET_RADIUS_RATIO
            if fillet.radius > max_fillet:
                self.errors.append(
                    f"Fillet {i}: Radius {fillet.radius}mm exceeds maximum {max_fillet:.1f}mm "
                    f"(50% of smallest dimension {smallest_dim}mm)"
                )
    
    def _validate_hole_positions(self, part: CadPart) -> None:
        """Validate that holes don't interfere with each other."""
        for i, hole1 in enumerate(part.holes):
            for j, hole2 in enumerate(part.holes[i+1:], start=i+1):
                # Calculate distance between hole centers
                dx = hole1.position.x - hole2.position.x
                dy = hole1.position.y - hole2.position.y
                distance = (dx**2 + dy**2)**0.5
                
                # Minimum distance is sum of radii plus wall thickness
                min_distance = (hole1.diameter + hole2.diameter) / 2 + self.MIN_WALL_THICKNESS
                
                if distance < min_distance:
                    self.errors.append(
                        f"Holes {i} and {j} are too close ({distance:.1f}mm). "
                        f"Minimum separation {min_distance:.1f}mm required."
                    )
    
    def _validate_wall_thickness(self, part: CadPart) -> None:
        """Validate wall thickness around holes."""
        for i, hole in enumerate(part.holes):
            # Check remaining material thickness
            remaining_height = part.dimensions.height - hole.depth
            if remaining_height < self.MIN_WALL_THICKNESS:
                self.warnings.append(
                    f"Hole {i}: Remaining material thickness {remaining_height:.1f}mm "
                    f"is below recommended {self.MIN_WALL_THICKNESS}mm"
                )


def validate_part(part: CadPart) -> Tuple[bool, List[str], List[str]]:
    """
    Convenience function to validate a part.
    
    Args:
        part: CadPart to validate
        
    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    engine = RulesEngine()
    return engine.validate(part)
