"""API endpoints for SIS."""
from fastapi import APIRouter, Depends, HTTPException
from sis.api.schemas import ScanRequest, ScanResponse

router = APIRouter(prefix="/v1", tags=["scan"])

@router.post("/scan", response_model=ScanResponse)
async def scan_endpoint(request: ScanRequest):
    """Scan files endpoint."""
    from sis.main import scan_files
    return await scan_files(request)