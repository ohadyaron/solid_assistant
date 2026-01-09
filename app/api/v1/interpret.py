"""
Interpret API endpoint.
Receives natural language and outputs JSON intent schema.
"""
from fastapi import APIRouter, HTTPException, status
from app.domain.intent import InterpretRequest, InterpretResponse, PartIntent
from app.llm.interpreter import get_interpreter

router = APIRouter(prefix="/api/v1", tags=["interpret"])


@router.post("/interpret", response_model=InterpretResponse)
async def interpret_text(request: InterpretRequest) -> InterpretResponse:
    """
    Interpret natural language description into structured part intent.
    
    This endpoint uses LangChain and OpenAI to:
    1. Extract parameters explicitly mentioned in the text
    2. Identify missing critical information
    3. Enforce output matches PartIntent schema
    4. Never invent or assume geometry not stated
    
    Args:
        request: Natural language description
        
    Returns:
        InterpretResponse with structured PartIntent
        
    Raises:
        HTTPException: If interpretation fails or API key is missing
    """
    try:
        interpreter = get_interpreter()
        intent = await interpreter.interpret_async(request.text)
        
        return InterpretResponse(intent=intent)
        
    except ValueError as e:
        # API key or configuration error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        # Other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Interpretation error: {str(e)}"
        )


@router.get("/interpret/health")
async def health_check():
    """
    Health check endpoint for the interpret service.
    
    Returns:
        Status information
    """
    try:
        # Check if interpreter can be initialized
        interpreter = get_interpreter()
        return {
            "status": "healthy",
            "service": "natural-language-interpretation",
            "llm_configured": True
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "natural-language-interpretation",
            "llm_configured": False,
            "error": str(e)
        }
