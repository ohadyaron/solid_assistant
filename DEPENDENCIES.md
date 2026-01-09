# Locked Dependency Configuration

This document records the tested and working dependency versions for this project.

## Critical Version Constraints

### Python Version
- **Python 3.10, 3.11, or 3.12** (NOT 3.13)
- Currently tested with: **Python 3.12.11**

### Core Dependencies (DO NOT UPGRADE without testing)

#### CadQuery Stack
```
cadquery==2.4.0
cadquery-ocp>=7.7.0,<7.8
numpy>=1.20.0,<2.0        # numpy 2.x breaks nptyping compatibility!
nptyping==2.0.1
nlopt>=2.7.0              # Required for cadquery, must support arm64
```

**⚠️ Critical Notes:**
- CadQuery 2.4.0 requires specific versions of cadquery-ocp and numpy
- numpy 2.x is incompatible with nptyping 2.0.1 (causes `AttributeError: 'bool8'`)
- nlopt must have arm64 wheels available on macOS

#### LangChain Stack
```
langchain==1.2.3
langchain-core==1.2.6
langchain-openai==1.1.7
langgraph==1.0.5
openai==1.109.1
tiktoken==0.12.0
```

#### FastAPI Stack
```
fastapi==0.128.0
uvicorn[standard]==0.40.0
pydantic==2.12.5
```

#### Testing
```
pytest==9.0.2
pytest-asyncio==1.3.0
httpx==0.26.0
```

## Installation

### Fresh Install
```bash
# Use Python 3.12
poetry env use python3.12

# Install dependencies
poetry install --no-root

# Verify
poetry run pytest tests/ -v
```

### Lock File
The `poetry.lock` file contains the complete dependency tree with exact versions.
Do not delete this file - it ensures reproducible builds.

## Known Issues

### Numpy 2.x Incompatibility
- **Problem:** numpy 2.4.0 removes `np.bool8`, breaking nptyping
- **Solution:** Locked to numpy<2.0

### CadQuery Import Speed
- CadQuery loads 166MB of C++ bindings (OpenCascade)
- First import takes several seconds - this is normal

### Python 3.13 Incompatibility
- Project requires Python <3.13 due to dependency constraints
- Use Python 3.10, 3.11, or 3.12

## Test Results
Last successful test run: 39/39 tests passed in 23.70 seconds

## Updating Dependencies

⚠️ **Before updating any CadQuery-related packages:**
1. Create a backup of the working environment
2. Test thoroughly with all 39 tests
3. Verify STEP file generation works correctly
4. Check numpy compatibility with nptyping

The CadQuery stack is particularly fragile and version-sensitive.
