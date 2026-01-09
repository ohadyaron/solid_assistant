"""
Generic CAD generator module.
Provides a unified interface for generating CAD files using different engines.
"""
from pathlib import Path
from typing import Dict, Literal

from app.domain.intent import PartIntent
from app.cad.builder_interface import CADBuilderInterface
from app.cad.cadquery_builder import CadQueryBuilder
from app.cad.solidworks_builder import SolidWorksBuilder


class CADGenerator:
    """
    Generic CAD generator that supports multiple CAD engines.
    
    This class provides a unified interface for generating CAD files using
    different engines (CadQuery for STEP files, SolidWorks for SLDPRT files).
    All engines implement the same CADBuilderInterface and work with the same
    PartIntent schema.
    
    Attributes:
        output_dir: Directory where generated CAD files will be saved
        _builders: Dictionary mapping engine names to builder instances
    """
    
    def __init__(self, output_dir: str = "/tmp"):
        """
        Initialize the CAD generator.
        
        Args:
            output_dir: Directory for output CAD files (default: /tmp)
        """
        self.output_dir = Path(output_dir)
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize builders - both inherit from CADBuilderInterface
        self._builders: Dict[str, CADBuilderInterface] = {
            "cadquery": CadQueryBuilder(),
            "solidworks": SolidWorksBuilder()
        }
    
    def generate(
        self,
        part: PartIntent,
        engine: Literal["cadquery", "solidworks"]
    ) -> Dict[str, any]:
        """
        Generate a CAD file from PartIntent using the specified engine.
        
        This method routes to the appropriate builder implementation based on the
        engine parameter. All builders inherit from CADBuilderInterface and use
        the same PartIntent schema, ensuring consistency across engines.
        
        Args:
            part: PartIntent specification containing shape, dimensions, holes, and fillets
            engine: CAD engine to use - either "cadquery" (STEP) or "solidworks" (SLDPRT)
            
        Returns:
            Dictionary with the following structure:
            {
                "status": "ok" | "error",
                "file_path": "path/to/generated/file",
                "errors": ["optional error messages"]
            }
            
        Examples:
            >>> generator = CADGenerator(output_dir="/tmp/cad")
            >>> part = PartIntent(
            ...     shape="box",
            ...     dimensions=DimensionIntent(length=100, width=50, height=30)
            ... )
            >>> result = generator.generate(part, engine="cadquery")
            >>> print(result["status"])
            ok
            >>> print(result["file_path"])
            /tmp/cad/part_20240109_123456.step
        """
        # Validate engine parameter
        if engine not in self._builders:
            return {
                "status": "error",
                "file_path": "",
                "errors": [
                    f"Unsupported engine: '{engine}'. "
                    f"Supported engines are: {', '.join(self._builders.keys())}"
                ]
            }
        
        try:
            # Get the appropriate builder (all implement CADBuilderInterface)
            builder = self._builders[engine]
            
            # Use the common interface method
            file_path = builder.build(part, self.output_dir)
            
            # Return success response
            return {
                "status": "ok",
                "file_path": str(file_path),
                "errors": []
            }
            
        except ImportError as e:
            # Handle missing dependencies
            error_msg = str(e)
            if "pywin32" in error_msg:
                error_msg = (
                    "SolidWorks engine requires pywin32. "
                    "Install it with: pip install pywin32"
                )
            
            return {
                "status": "error",
                "file_path": "",
                "errors": [error_msg]
            }
            
        except ValueError as e:
            # Handle validation errors
            return {
                "status": "error",
                "file_path": "",
                "errors": [f"Validation error: {str(e)}"]
            }
            
        except RuntimeError as e:
            # Handle generation errors
            return {
                "status": "error",
                "file_path": "",
                "errors": [f"Generation error: {str(e)}"]
            }
            
        except Exception as e:
            # Handle unexpected errors
            return {
                "status": "error",
                "file_path": "",
                "errors": [f"Unexpected error: {str(e)}"]
            }
