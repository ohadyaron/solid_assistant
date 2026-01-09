"""
Test async endpoints with concurrent requests.
"""
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.domain.models import CadPart, Dimensions


@pytest.mark.asyncio
async def test_concurrent_part_generation():
    """Test that multiple parts can be generated concurrently."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create multiple part generation requests
        tasks = []
        for i in range(3):
            part_data = {
                "shape": "box",
                "dimensions": {
                    "length": 50 + i * 10,
                    "width": 50 + i * 10,
                    "height": 30 + i * 5
                },
                "holes": [],
                "fillets": []
            }
            task = client.post("/api/v1/parts", json=part_data)
            tasks.append(task)
        
        # Execute all requests concurrently
        responses = await asyncio.gather(*tasks)
        
        # Verify all succeeded
        for i, response in enumerate(responses):
            assert response.status_code == 200
            result = response.json()
            assert result["status"] == "success"
            assert result["step_file_path"] != ""
            print(f"Request {i+1} completed: {result['step_file_path']}")


@pytest.mark.asyncio
async def test_health_endpoints_async():
    """Test health check endpoints are async."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Test both health endpoints concurrently
        parts_health_task = client.get("/api/v1/parts/health")
        interpret_health_task = client.get("/api/v1/interpret/health")
        
        parts_response, interpret_response = await asyncio.gather(
            parts_health_task,
            interpret_health_task
        )
        
        assert parts_response.status_code == 200
        assert interpret_response.status_code == 200
        
        parts_data = parts_response.json()
        interpret_data = interpret_response.json()
        
        assert parts_data["status"] == "healthy"
        assert interpret_data["service"] == "natural-language-interpretation"
