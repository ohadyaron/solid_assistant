"""
Parts API endpoint.
Receives validated CAD Part JSON and generates STEP file.
"""
from fastapi import APIRouter, HTTPException, status
from app.domain.models import CadPart, PartGenerationResult
from app.services.part_generator import PartGenerationService

router = APIRouter(prefix="/api/v1", tags=["parts"])

# Service instance
part_service = PartGenerationService()


@router.post("/parts", response_model=PartGenerationResult)
async def generate_part(part: CadPart) -> PartGenerationResult:
    """
    Generate a STEP file from a validated CAD part specification.
    
    This endpoint:
    1. Validates the part against CNC manufacturing rules
    2. Builds the CAD model deterministically using CadQuery
    3. Exports the result as a STEP file
    
    Args:
        part: Validated CAD part specification
        
    Returns:
        PartGenerationResult with STEP file path and status
        
    Raises:
        HTTPException: If generation fails
    """
    result = await part_service.generate_part_async(part)
    
    if result.status == "error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.message
        )
    
    return result


@router.get("/parts/health")
async def health_check():
    """
    Health check endpoint for the parts service.
    
    Returns:
        Status information
    """
    return {
        "status": "healthy",
        "service": "parts-generation",
        "output_directory": str(part_service.output_dir)
    }
