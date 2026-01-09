"""
Part generation service.
Orchestrates CAD building, validation, and export.
"""
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple

from app.domain.models import CadPart, PartGenerationResult
from app.cad import CadBuilder
from app.rules import validate_part, ValidationError


class PartGenerationService:
    """Service for generating CAD parts."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the part generation service.
        
        Args:
            output_dir: Directory for output STEP files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_part(self, part: CadPart) -> PartGenerationResult:
        """
        Generate a STEP file from a CAD part specification.
        
        Args:
            part: CadPart specification
            
        Returns:
            PartGenerationResult with file path and status
        """
        try:
            # Validate the part
            is_valid, errors, warnings = validate_part(part)
            
            if not is_valid:
                error_msg = "Validation failed: " + "; ".join(errors)
                return PartGenerationResult(
                    step_file_path="",
                    status="error",
                    message=error_msg
                )
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"part_{timestamp}.step"
            filepath = self.output_dir / filename
            
            # Build and export CAD model
            builder = CadBuilder()
            builder.build_part(part)
            builder.export_step(str(filepath))
            
            # Prepare result message
            message = "Part generated successfully"
            if warnings:
                message += f". Warnings: {'; '.join(warnings)}"
            
            return PartGenerationResult(
                step_file_path=str(filepath),
                status="success",
                message=message
            )
            
        except Exception as e:
            return PartGenerationResult(
                step_file_path="",
                status="error",
                message=f"Error generating part: {str(e)}"
            )
    
    def generate_part_with_name(
        self,
        part: CadPart,
        filename: str
    ) -> PartGenerationResult:
        """
        Generate a STEP file with a specific filename.
        
        Args:
            part: CadPart specification
            filename: Desired filename (without extension)
            
        Returns:
            PartGenerationResult with file path and status
        """
        try:
            # Validate the part
            is_valid, errors, warnings = validate_part(part)
            
            if not is_valid:
                error_msg = "Validation failed: " + "; ".join(errors)
                return PartGenerationResult(
                    step_file_path="",
                    status="error",
                    message=error_msg
                )
            
            # Ensure .step extension
            if not filename.endswith('.step'):
                filename = f"{filename}.step"
            
            filepath = self.output_dir / filename
            
            # Build and export CAD model
            builder = CadBuilder()
            builder.build_part(part)
            builder.export_step(str(filepath))
            
            # Prepare result message
            message = "Part generated successfully"
            if warnings:
                message += f". Warnings: {'; '.join(warnings)}"
            
            return PartGenerationResult(
                step_file_path=str(filepath),
                status="success",
                message=message
            )
            
        except Exception as e:
            return PartGenerationResult(
                step_file_path="",
                status="error",
                message=f"Error generating part: {str(e)}"
            )
