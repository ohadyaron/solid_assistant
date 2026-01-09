"""
Intent schemas for LLM interpretation.
These models represent the input/output of natural language processing.
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class DimensionIntent(BaseModel):
    """Extracted dimension intent from natural language."""
    length: Optional[float] = Field(default=None, description="Length in mm")
    width: Optional[float] = Field(default=None, description="Width in mm")
    height: Optional[float] = Field(default=None, description="Height in mm")


class HoleIntent(BaseModel):
    """Extracted hole intent from natural language."""
    diameter: Optional[float] = Field(default=None, description="Hole diameter in mm")
    depth: Optional[float] = Field(default=None, description="Hole depth in mm")
    location: Optional[str] = Field(default=None, description="Hole location description")


class FilletIntent(BaseModel):
    """Extracted fillet intent from natural language."""
    radius: Optional[float] = Field(default=None, description="Fillet radius in mm")
    location: Optional[str] = Field(default=None, description="Fillet location description")


class PartIntent(BaseModel):
    """
    Structured intent extracted from natural language.
    This schema is enforced by LangChain PydanticOutputParser.
    """
    shape: Optional[Literal["box"]] = Field(
        default=None,
        description="Base shape type extracted from text"
    )
    dimensions: Optional[DimensionIntent] = Field(
        default=None,
        description="Extracted dimensions"
    )
    holes: List[HoleIntent] = Field(
        default_factory=list,
        description="List of holes mentioned in text"
    )
    fillets: List[FilletIntent] = Field(
        default_factory=list,
        description="List of fillets mentioned in text"
    )
    material: Optional[str] = Field(
        default=None,
        description="Material mentioned in text"
    )
    missing_information: List[str] = Field(
        default_factory=list,
        description="List of missing critical information"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "shape": "box",
                "dimensions": {
                    "length": 100.0,
                    "width": 50.0,
                    "height": 30.0
                },
                "holes": [
                    {
                        "diameter": 10.0,
                        "depth": 20.0,
                        "location": "center"
                    }
                ],
                "fillets": [
                    {
                        "radius": 5.0,
                        "location": "all edges"
                    }
                ],
                "material": "aluminum",
                "missing_information": []
            }
        }
    }


class InterpretRequest(BaseModel):
    """Request for natural language interpretation."""
    text: str = Field(description="Natural language description of the part")


class InterpretResponse(BaseModel):
    """Response from natural language interpretation."""
    intent: PartIntent = Field(description="Structured intent extracted from text")
