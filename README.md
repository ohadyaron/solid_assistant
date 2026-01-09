# Mechanical Assistant

A FastAPI-based mechanical assistant that generates CAD parts from natural language descriptions.

## Features

- **Natural Language to CAD**: Converts natural language descriptions into validated CAD part specifications
- **Deterministic CAD Generation**: Creates precise STEP files using CadQuery
- **Rule-Based Validation**: Enforces CNC manufacturing constraints
- **LLM-Powered Interpretation**: Uses LangChain and OpenAI to extract structured intent from user input
- **Fully Async Architecture**: All API endpoints are async with non-blocking I/O and thread pool execution for CPU-intensive CAD operations

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

- **Python 3.10, 3.11, or 3.12** (NOT 3.13 - see [DEPENDENCIES.md](DEPENDENCIES.md))
- **Poetry** for dependency management

### Installation

#### 1. Clone the repository:
```bash
git clone <repository-url>
cd solid_assistant
```

#### 2. Set up Python virtual environment with Poetry:

**Important:** Use Python 3.12 (or 3.10/3.11) to avoid compatibility issues:

```bash
# Check if you have Python 3.12
python3.12 --version

# Configure Poetry to use Python 3.12
poetry env use python3.12

# Verify the environment
poetry env info
```

#### 3. Install dependencies:

Poetry will create a virtual environment and install all locked dependencies:

```bash
poetry install --no-root
```

This installs all dependencies from the locked `poetry.lock` file, ensuring reproducible builds.

#### 4. Set up environment variables:

For the `/api/v1/interpret` endpoint (optional if you only use `/api/v1/parts`):

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

Or create a `.env` file:
```bash
echo "OPENAI_API_KEY=your-openai-api-key" > .env
```

### Running Tests

Run all tests (39 tests, takes ~2 seconds):

```bash
poetry run pytest tests/ -v
```

Run specific test file:
```bash
poetry run pytest tests/test_generator.py -v
```

Run with short tracebacks:
```bash
poetry run pytest tests/ -v --tb=short
```

Run specific test:
```bash
poetry run pytest tests/test_generator.py::test_generator_initialization -v
```

**Expected output:**
```
===== test session starts =====
collected 39 items

tests/test_async_endpoints.py::test_concurrent_part_generation PASSED [  2%]
tests/test_async_endpoints.py::test_health_endpoints_async PASSED     [  5%]
...
===== 39 passed in 2.06s =====
```

### Running the Server

#### Development Mode (with auto-reload):

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### Production Mode:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Accessing the Server:

- **API Root:** http://localhost:8000/
- **Interactive API Docs (Swagger UI):** http://localhost:8000/docs
- **Alternative API Docs (ReDoc):** http://localhost:8000/redoc
- **OpenAPI Spec:** http://localhost:8000/openapi.json
- **Health Check:** http://localhost:8000/health

#### Quick Server Test:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test root endpoint
curl http://localhost:8000/

# Generate a simple part
curl -X POST http://localhost:8000/api/v1/parts \
  -H "Content-Type: application/json" \
  -d '{
    "shape": "box",
    "dimensions": {"length": 100, "width": 50, "height": 30},
    "material": "aluminum"
  }'
```

### Virtual Environment Management

#### Check current environment:
```bash
poetry env info
```

#### List all Poetry environments:
```bash
poetry env list
```

#### Remove environment:
```bash
poetry env remove python3.12
```

#### Activate environment manually (if needed):
```bash
source $(poetry env info --path)/bin/activate
```

#### Deactivate:
```bash
deactivate
```

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

## Troubleshooting

### Tests are slow or stuck
- **Problem:** Tests hang during collection or take >30 seconds
- **Solution:** Ensure numpy < 2.0 is installed. See [DEPENDENCIES.md](DEPENDENCIES.md) for details.
```bash
poetry run pip install 'numpy>=1.20.0,<2.0'
```

### Python version mismatch
- **Problem:** `Current Python version (3.13.x) is not allowed by the project`
- **Solution:** Use Python 3.10-3.12
```bash
poetry env use python3.12
poetry install --no-root
```

### CadQuery import errors
- **Problem:** `ImportError: cannot import name 'IVtkOCC_Shape'`
- **Solution:** Ensure correct cadquery-ocp version:
```bash
poetry run pip install cadquery==2.4.0 'cadquery-ocp>=7.7.0,<7.8'
```

### OpenAI API errors
- **Problem:** 500 error on `/api/v1/interpret`
- **Solution:** Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-key-here"
```

For complete dependency information, see [DEPENDENCIES.md](DEPENDENCIES.md).

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