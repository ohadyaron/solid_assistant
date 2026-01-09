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

#### Running the Backend

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

## Testing

### Backend Tests

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