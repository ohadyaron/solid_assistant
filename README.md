# Mechanical Assistant

A FastAPI-based mechanical assistant that generates CAD parts from natural language descriptions, with a modern React + TypeScript frontend.

## Features

- **Natural Language to CAD**: Converts natural language descriptions into validated CAD part specifications
- **Deterministic CAD Generation**: Creates precise STEP files using CadQuery
- **Rule-Based Validation**: Enforces CNC manufacturing constraints
- **LLM-Powered Interpretation**: Uses LangChain and OpenAI to extract structured intent from user input
- **Fully Async Architecture**: All API endpoints are async with non-blocking I/O and thread pool execution for CPU-intensive CAD operations
- **Modern React Frontend**: Production-ready frontend with TypeScript, React Router, React Query, and comprehensive testing

## Project Structure

```
mechanical-assistant/
├── app/                           # Backend API (Python/FastAPI)
│   ├── api/
│   │   └── v1/
│   │       ├── parts.py          # STEP file generation endpoint
│   │       └── interpret.py      # Natural language interpretation endpoint
│   ├── cad/                      # CAD builder using CadQuery
│   ├── domain/
│   │   ├── models.py             # CAD Part schemas
│   │   └── intent.py             # LLM input/output schemas
│   ├── llm/                      # LangChain + LLM interpreter
│   ├── rules/                    # Validation rules engine
│   ├── services/                 # Part generation logic
│   └── main.py                   # FastAPI entry point
├── frontend/                      # Frontend application (React/TypeScript)
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   ├── pages/                # Page components
│   │   ├── hooks/                # Custom React hooks
│   │   ├── services/             # API client
│   │   └── types/                # TypeScript types (auto-generated from OpenAPI)
│   ├── package.json              # Node dependencies
│   └── README.md                 # Frontend documentation
├── tests/                         # Backend tests
├── pyproject.toml                # Poetry dependencies
└── README.md                     # This file
```

## Quick Start

### Backend Setup

#### Prerequisites

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

### Frontend Setup

#### Prerequisites

- Node.js 18+ and npm

#### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment (optional):
```bash
cp .env.example .env
# Edit .env if your backend is not running on http://localhost:8000
```

#### Running the Frontend

Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

#### Building for Production

```bash
npm run build
```

The production build will be in the `frontend/dist/` directory.

## Full Stack Development

To run both backend and frontend together:

1. **Terminal 1 - Backend**:
```bash
cd solid_assistant
poetry run uvicorn app.main:app --reload
```

2. **Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

3. Open `http://localhost:5173` in your browser

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

### Backend Tests

Run tests with pytest:
=======
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

### Frontend Tests

Run frontend tests:
```bash
cd frontend
npm test
```

Run tests with UI:
```bash
npm run test:ui
```

## Frontend Features

The React frontend provides a user-friendly interface for the API:

### Pages
- **Home Page** (`/`) - Overview and quick navigation
- **Interpreter Page** (`/interpret`) - Natural language input form with real-time interpretation
- **Generator Page** (`/parts`) - CAD part specification form with dynamic fields

### Technology Stack
- **React 19** with functional components and hooks
- **TypeScript** for type safety
- **React Router v6** for client-side routing
- **React Query** for data fetching and caching
- **React Hook Form** for form handling and validation
- **Axios** for API communication
- **Vitest + React Testing Library** for testing
- **ESLint + Prettier** for code quality

### Key Features
- Type-safe API client auto-generated from OpenAPI spec
- Loading and error states for all API calls
- Form validation with user-friendly error messages
- Responsive design for mobile and desktop
- Comprehensive test coverage
=======
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