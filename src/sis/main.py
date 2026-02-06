"""SIS FastAPI application."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
from datetime import datetime
from typing import List
import time
from collections import defaultdict

from sis.api.schemas import ScanRequest, ScanResponse, ErrorResponse
from sis.engine import RuleEngine
from sis.parsers import parse_file

app = FastAPI(
    title="Static Irreversibility Scanner (SIS)",
    version="1.0.0",
    description="Deterministic pattern scanner for irreversible infrastructure decisions"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Rate limiting cache
rate_limit_cache = defaultdict(list)

# Rule engine (singleton)
engine = RuleEngine()

def check_rate_limit(api_key: str, max_per_hour: int = 100) -> bool:
    """Simple rate limiting."""
    now = time.time()
    window = 3600
    
    rate_limit_cache[api_key] = [
        timestamp for timestamp in rate_limit_cache[api_key]
        if now - timestamp < window
    ]
    
    if len(rate_limit_cache[api_key]) >= max_per_hour:
        return False
    
    rate_limit_cache[api_key].append(now)
    return True

@app.post("/v1/scan", response_model=ScanResponse)
async def scan_files(request: ScanRequest, api_request: Request):
    """Scan files for irreversible patterns."""
    
    api_key = api_request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    if not check_rate_limit(api_key):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": "3600"}
        )
    
    total_size = sum(len(f.content) for f in request.files)
    if total_size > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Payload too large")
    
    if len(request.files) > 100:
        raise HTTPException(status_code=400, detail="Too many files")
    
    all_findings = []
    errors = []
    
    for file in request.files:
        try:
            resources = parse_file(file.type, file.content)
            
            for resource in resources:
                findings = engine.scan_resource(
                    file_type=file.type,
                    resource_kind=resource.get("kind", ""),
                    resource=resource
                )
                
                for finding in findings:
                    finding.update({
                        "file": file.name,
                        "line": resource.get("line", 1)
                    })
                
                all_findings.extend(findings)
                
        except Exception as e:
            errors.append({
                "file": file.name,
                "error": "PARSE_ERROR",
                "message": str(e)
            })
    
    summary = {
        "total_files": len(request.files),
        "total_findings": len(all_findings),
        "by_type": {
            "IRREVERSIBLE_IDENTITY_BINDING": 0,
            "IRREVERSIBLE_DECISION": 0,
            "ADMIN_OVERRIDE_DEPENDENCY": 0
        }
    }
    
    for finding in all_findings:
        summary["by_type"][finding["rule_type"]] += 1
    
    return ScanResponse(
        scan_id=request.scan_id or str(uuid.uuid4()),
        timestamp=datetime.utcnow().isoformat() + "Z",
        scanner_version="1.0.0",
        findings=all_findings,
        summary=summary,
        errors=errors
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.status_code,
            message=exc.detail
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


def run():
    """Entry point for running the API server."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
