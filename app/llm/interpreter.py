"""
LLM-based natural language interpreter.
Uses LangChain and OpenAI to extract structured intent from text.
"""
import os
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

from app.domain.intent import PartIntent


class NaturalLanguageInterpreter:
    """Interprets natural language descriptions into structured part intent."""
    
    SYSTEM_PROMPT = """You are a precise mechanical engineering assistant that extracts part specifications from natural language.

Your role is to:
1. Extract ONLY the parameters explicitly mentioned in the user's description
2. Do NOT invent or assume geometry, dimensions, or features not stated
3. List any missing critical information needed to manufacture the part
4. Be conservative - if unsure, mark information as missing

Guidelines:
- Extract dimensions in millimeters (convert if units given)
- Extract hole specifications (diameter, depth, position description)
- Extract fillet specifications (radius, location description)
- Identify the base shape (currently only "box" is supported)
- Note any material mentions
- List missing information clearly

{format_instructions}

Examples of what to extract:
✓ "100mm cube" → dimensions: length=100, width=100, height=100
✓ "20mm diameter hole" → hole with diameter=20
✓ "5mm fillet on all edges" → fillet with radius=5, location="all edges"

Examples of what NOT to do:
✗ Do not guess dimensions if not provided
✗ Do not invent hole positions if not specified
✗ Do not assume standard features
✗ Do not add features not mentioned

If critical information is missing, add it to the missing_information list."""
    
    def __init__(self, api_key: Optional[str] = None, temperature: float = 0):
        """
        Initialize the interpreter.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            temperature: LLM temperature (0 for deterministic)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required (set OPENAI_API_KEY env var)")
        
        # Initialize LLM with temperature=0 for deterministic output
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=temperature,
            api_key=self.api_key
        )
        
        # Setup output parser
        self.parser = PydanticOutputParser(pydantic_object=PartIntent)
        
        # Create prompt template
        self.prompt = PromptTemplate(
            template=self.SYSTEM_PROMPT + "\n\nUser description: {text}\n\nExtracted intent:",
            input_variables=["text"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            }
        )
    
    def interpret(self, text: str) -> PartIntent:
        """
        Interpret natural language text into structured intent.
        
        Args:
            text: Natural language description of the part
            
        Returns:
            PartIntent with extracted parameters
        """
        # Create the chain
        chain = self.prompt | self.llm | self.parser
        
        # Execute the chain
        try:
            result = chain.invoke({"text": text})
            return result
        except Exception as e:
            # If parsing fails, return minimal intent with error in missing info
            return PartIntent(
                missing_information=[
                    f"Failed to parse description: {str(e)}",
                    "Please provide a clearer description"
                ]
            )
    
    async def interpret_async(self, text: str) -> PartIntent:
        """
        Async version of interpret.
        
        Args:
            text: Natural language description of the part
            
        Returns:
            PartIntent with extracted parameters
        """
        # Create the chain
        chain = self.prompt | self.llm | self.parser
        
        # Execute the chain asynchronously
        try:
            result = await chain.ainvoke({"text": text})
            return result
        except Exception as e:
            # If parsing fails, return minimal intent with error in missing info
            return PartIntent(
                missing_information=[
                    f"Failed to parse description: {str(e)}",
                    "Please provide a clearer description"
                ]
            )


# Singleton instance
_interpreter_instance: Optional[NaturalLanguageInterpreter] = None


def get_interpreter() -> NaturalLanguageInterpreter:
    """
    Get or create the interpreter singleton.
    
    Returns:
        NaturalLanguageInterpreter instance
    """
    global _interpreter_instance
    if _interpreter_instance is None:
        _interpreter_instance = NaturalLanguageInterpreter()
    return _interpreter_instance
