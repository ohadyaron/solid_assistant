# Mechanical Assistant

A FastAPI-based mechanical assistant that generates CAD parts from natural language descriptions.

## Features

- **Natural Language to CAD**: Converts natural language descriptions into validated CAD part specifications
- **Deterministic CAD Generation**: Creates precise STEP files using CadQuery
- **Rule-Based Validation**: Enforces CNC manufacturing constraints
- **LLM-Powered Interpretation**: Uses LangChain and OpenAI to extract structured intent from user input

## Project Structure

```
mechanical-assistant/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── parts.py        # STEP file generation endpoint
│   │       └── interpret.py    # Natural language interpretation endpoint
│   ├── cad/                    # CAD builder using CadQuery
│   ├── domain/
│   │   ├── models.py           # CAD Part schemas
│   │   └── intent.py           # LLM input/output schemas
│   ├── llm/                    # LangChain + LLM interpreter
│   ├── rules/                  # Validation rules engine
│   ├── services/               # Part generation logic
│   └── main.py                 # FastAPI entry point
├── tests/                      # Pytest tests
├── pyproject.toml              # Poetry dependencies
├── .gitignore
└── README.md
```

## Setup

### Prerequisites

- Python 3.10+
- Poetry (recommended) or pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd solid_assistant
```

2. Install dependencies with Poetry:
```bash
poetry install
```

Or with pip:
```bash
pip install -e .
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### Running the Application

Start the FastAPI development server:

```bash
poetry run uvicorn app.main:app --reload
```

Or:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

## API Endpoints

### POST /api/v1/interpret

Interprets natural language input and returns structured intent.

**Request:**
```json
{
  "text": "Create a 100mm cube with a 20mm hole in the center and 5mm fillets"
}
```

**Response:**
```json
{
  "intent": {
    "shape": "box",
    "dimensions": {"length": 100, "width": 100, "height": 100},
    "features": [
      {"type": "hole", "diameter": 20},
      {"type": "fillet", "radius": 5}
    ]
  }
}
```

### POST /api/v1/parts

Generates a STEP file from validated CAD part specification.

**Request:**
```json
{
  "shape": "box",
  "dimensions": {"length": 100, "width": 100, "height": 100},
  "holes": [{"diameter": 20, "depth": 50, "position": {"x": 0, "y": 0, "z": 0}}],
  "fillets": [{"radius": 5, "edges": "all"}]
}
```

**Response:**
```json
{
  "step_file_path": "output/part_20240109_123456.step",
  "status": "success"
}
```

## Testing

Run tests with pytest:

```bash
poetry run pytest
```

Or:
```bash
pytest
```

Run with coverage:
```bash
poetry run pytest --cov=app tests/
```

## Development

This project uses:
- **FastAPI** for the REST API
- **Pydantic v2** for data validation
- **CadQuery** for deterministic CAD generation
- **LangChain** for LLM orchestration
- **OpenAI** for natural language understanding

## Phase 1 Constraints

- Deterministic CAD generation only (no LLM-generated geometry)
- No assemblies
- No optimizations
- LLM only translates natural language → structured intent

## License

MIT License