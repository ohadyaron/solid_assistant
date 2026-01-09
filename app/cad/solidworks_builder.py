"""
SolidWorks builder for generating SLDPRT files.
Uses SolidWorks COM API via pywin32 to create native SolidWorks parts.
"""
from pathlib import Path
from datetime import datetime
from typing import Optional

from app.domain.intent import PartIntent
from app.cad.builder_interface import CADBuilderInterface


class SolidWorksBuilder(CADBuilderInterface):
    """
    SolidWorks implementation of CAD builder.
    
    Generates SLDPRT files using the SolidWorks COM API via pywin32.
    Requires Windows and SolidWorks installation.
    """
    
    def validate(self, part: PartIntent) -> None:
        """
        Validate the PartIntent specification.
        
        Args:
            part: PartIntent specification to validate
            
        Raises:
            ValueError: If validation fails
        """
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
    
    def build(self, part: PartIntent, output_dir: Path) -> Path:
        """
        Build a SLDPRT file from PartIntent using SolidWorks COM API.
        
        This method creates a parametric CAD model in SolidWorks using the COM API
        and saves it as a native .sldprt file. Requires Windows and SolidWorks installation.
        
        Args:
            part: PartIntent specification containing shape, dimensions, holes, and fillets
            output_dir: Directory where the SLDPRT file will be saved
            
        Returns:
            Path: Full path to the generated SLDPRT file
            
        Raises:
            ImportError: If pywin32 is not installed
            RuntimeError: If SolidWorks is not available or generation fails
            ValueError: If required dimensions are missing or invalid
        """
        # Import COM API (Windows only)
        try:
            import win32com.client
            import pythoncom
        except ImportError as e:
            raise ImportError(
                "pywin32 is required for SolidWorks COM API. "
                "Install it with: pip install pywin32"
            ) from e
        
        # Validate the part specification
        self.validate(part)
        
        # Initialize COM
        pythoncom.CoInitialize()
        
        sw_app = None
        sw_model = None
        
        try:
            # Connect to SolidWorks
            sw_app = win32com.client.Dispatch("SldWorks.Application")
            sw_app.Visible = True  # Make SolidWorks visible for debugging
            
            # Create new part document
            sw_model = sw_app.NewDocument(
                sw_app.GetUserPreferenceStringValue(0),  # Default part template
                0,  # Paper size (not applicable)
                0,  # Width (not applicable)
                0   # Height (not applicable)
            )
            
            if not sw_model:
                raise RuntimeError("Failed to create new SolidWorks part document")
            
            # Create base shape
            if part.shape == "box":
                self._create_box_solidworks(sw_model, part.dimensions)
            else:
                raise ValueError(f"Unsupported shape: {part.shape}")
            
            # Apply holes
            for hole in part.holes:
                self._add_hole_solidworks(sw_model, hole)
            
            # Apply fillets
            for fillet in part.fillets:
                self._add_fillet_solidworks(sw_model, fillet)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"part_{timestamp}.sldprt"
            filepath = output_dir / filename
            
            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save the part
            save_success = sw_model.SaveAs(str(filepath.resolve()))
            
            if not save_success:
                raise RuntimeError(f"Failed to save SolidWorks part to {filepath}")
            
            return filepath
            
        except Exception as e:
            raise RuntimeError(f"Failed to build SLDPRT file: {str(e)}") from e
        
        finally:
            # Clean up: close document and COM
            if sw_model:
                try:
                    sw_app.CloseDoc(sw_model.GetTitle())
                except Exception:
                    pass  # Best effort cleanup
            
            pythoncom.CoUninitialize()
    
    def _create_box_solidworks(self, sw_model, dimensions) -> None:
        """
        Create a box shape in SolidWorks using sketch and extrude.
        
        Args:
            sw_model: SolidWorks model document object
            dimensions: DimensionIntent with length, width, height
        """
        
        # Select front plane for sketch
        front_plane = sw_model.Extension.SelectByID2(
            "Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0
        )
        
        if not front_plane:
            raise RuntimeError("Failed to select Front Plane")
        
        # Create sketch on front plane
        sw_model.InsertSketch2(True)
        sw_model_ext = sw_model.Extension
        
        # Draw rectangle centered at origin
        # Convert from center-based to corner-based coordinates
        x1 = -dimensions.length / 2.0 / 1000.0  # Convert mm to meters
        y1 = -dimensions.height / 2.0 / 1000.0
        x2 = dimensions.length / 2.0 / 1000.0
        y2 = dimensions.height / 2.0 / 1000.0
        
        # Create rectangle
        sw_model.CreateCenterRectangle(0, 0, 0, x2, y2, 0)
        
        # Exit sketch
        sw_model.InsertSketch2(True)
        
        # Extrude the sketch
        extrude_depth = dimensions.width / 1000.0  # Convert mm to meters
        
        sw_model.Extension.SelectByID2(
            "Sketch1", "SKETCH", 0, 0, 0, False, 0, None, 0
        )
        
        sw_model.FeatureExtrusion2(
            True,           # SD (single direction)
            False,          # Flip (don't flip direction)
            False,          # Dir (direction)
            0,              # T1 (end condition type: blind)
            0,              # T2 (end condition type for dir2)
            extrude_depth,  # D1 (depth)
            0,              # D2 (depth for dir2)
            False,          # Dchk1 (draft check)
            False,          # Dchk2 (draft check dir2)
            False,          # Ddir1 (draft direction)
            False,          # Ddir2 (draft direction dir2)
            0,              # Dang1 (draft angle)
            0,              # Dang2 (draft angle dir2)
            False,          # OffsetReverse1
            False,          # OffsetReverse2
            0,              # Offset1
            0,              # Offset2
            False,          # FlipStartCap
            False,          # FlipEndCap
            False           # Merge
        )
    
    def _add_hole_solidworks(self, sw_model, hole) -> None:
        """
        Add a hole to the SolidWorks model.
        
        Args:
            sw_model: SolidWorks model document object
            hole: HoleIntent with diameter, depth, and optional location
        """
        if not hole.diameter or not hole.depth:
            return  # Skip holes without required dimensions
        
        # Parse location - default to center (0, 0)
        x, y = 0.0, 0.0
        if hole.location and hole.location.lower() == "center":
            x, y = 0.0, 0.0
        
        # Convert to meters
        x_m = x / 1000.0
        y_m = y / 1000.0
        diameter_m = hole.diameter / 1000.0
        depth_m = hole.depth / 1000.0
        
        # Select top face for hole sketch
        sw_model.Extension.SelectByID2(
            "Face1", "FACE", 0, 0, 0, False, 0, None, 0
        )
        
        # Create sketch for hole
        sw_model.InsertSketch2(True)
        
        # Draw circle at location
        sw_model.CreateCircle(x_m, y_m, 0, x_m, y_m + diameter_m / 2.0, 0)
        
        # Exit sketch
        sw_model.InsertSketch2(True)
        
        # Create cut extrude for hole
        sw_model.Extension.SelectByID2(
            "Sketch2", "SKETCH", 0, 0, 0, False, 0, None, 0
        )
        
        sw_model.FeatureCut3(
            True,       # SD (single direction)
            False,      # Flip
            False,      # Dir
            0,          # T1 (blind)
            0,          # T2
            depth_m,    # D1
            0,          # D2
            False,      # Dchk1
            False,      # Dchk2
            False,      # Ddir1
            False,      # Ddir2
            0,          # Dang1
            0,          # Dang2
            False,      # OffsetReverse1
            False,      # OffsetReverse2
            0,          # Offset1
            0,          # Offset2
            False       # UseFeatScope
        )
    
    def _add_fillet_solidworks(self, sw_model, fillet) -> None:
        """
        Add fillets to edges in SolidWorks.
        
        Args:
            sw_model: SolidWorks model document object
            fillet: FilletIntent with radius and optional location
        """
        if not fillet.radius:
            return  # Skip fillets without radius
        
        radius_m = fillet.radius / 1000.0  # Convert mm to meters
        
        # Parse location for which edges to fillet
        # This is a simplified implementation that fillets specific edges
        # In a full implementation, would need more sophisticated edge selection
        
        if not fillet.location or fillet.location.lower() in ["all", "all edges"]:
            # Select all edges (simplified - select first few edges)
            # In practice, would iterate through all edges
            edge_count = 4  # For a box, selecting representative edges
            for i in range(1, edge_count + 1):
                sw_model.Extension.SelectByID2(
                    f"Edge{i}", "EDGE", 0, 0, 0, True, 0, None, 0
                )
        elif "top" in fillet.location.lower():
            # Select top edges only
            sw_model.Extension.SelectByID2(
                "Edge1", "EDGE", 0, 0, 0, False, 0, None, 0
            )
            sw_model.Extension.SelectByID2(
                "Edge2", "EDGE", 0, 0, 0, True, 0, None, 0
            )
        
        # Create fillet feature
        sw_model.FeatureFillet(
            2,          # Type (constant radius)
            radius_m,   # Radius
            0,          # Vertex fillet type
            0,          # Override default radius
            0,          # Overflow type
            0,          # Preview display
            False,      # Keep edge/face
            False,      # Rolling ball where applicable
            False,      # For construction
            False,      # No smooth
            False,      # Optimize geometry
            False,      # Internal faces only
            False       # Stop at pin/tangent
        )
