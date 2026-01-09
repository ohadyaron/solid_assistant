"""
Base interface for CAD builders.
Defines the contract that all CAD builder implementations must follow.
"""
from abc import ABC, abstractmethod
from pathlib import Path

from app.domain.intent import PartIntent


class CADBuilderInterface(ABC):
    """
    Abstract base class for CAD builders.
    
    All CAD builder implementations (CadQuery, SolidWorks, etc.) must inherit
    from this class and implement the required methods.
    """
    
    @abstractmethod
    def build(self, part: PartIntent, output_dir: Path) -> Path:
        """
        Build a CAD file from PartIntent specification.
        
        This method must be implemented by all concrete builder classes to
        generate a CAD file based on the provided part specification.
        
        Args:
            part: PartIntent specification containing shape, dimensions, holes, and fillets
            output_dir: Directory where the CAD file will be saved
            
        Returns:
            Path: Full path to the generated CAD file
            
        Raises:
            ValueError: If required dimensions are missing or invalid
            RuntimeError: If CAD generation or export fails
        """
        pass
    
    @abstractmethod
    def validate(self, part: PartIntent) -> None:
        """
        Validate the PartIntent specification before building.
        
        This method should check that all required fields are present and valid
        before attempting to build the CAD model.
        
        Args:
            part: PartIntent specification to validate
            
        Raises:
            ValueError: If validation fails
        """
        pass
