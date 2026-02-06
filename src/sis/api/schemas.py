"""Pydantic schemas for SIS API."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class FileType(str, Enum):
    TERRAFORM = "terraform"
    CLOUDFORMATION = "cloudformation"
    KUBERNETES = "kubernetes"
    DOCKER_COMPOSE = "docker_compose"
    ARM = "arm"

class RuleType(str, Enum):
    IDENTITY_BINDING = "IRREVERSIBLE_IDENTITY_BINDING"
    DECISION = "IRREVERSIBLE_DECISION"
    ADMIN_OVERRIDE = "ADMIN_OVERRIDE_DEPENDENCY"

class ScanFile(BaseModel):
    name: str = Field(..., max_length=255, regex=r'^[a-zA-Z0-9_\-\.]+$')
    type: FileType
    content: str = Field(..., max_length=1048576)

class ScanRequest(BaseModel):
    scan_id: Optional[str] = Field(None, regex=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    files: List[ScanFile] = Field(..., max_items=100)

class Finding(BaseModel):
    rule_id: str
    rule_type: RuleType
    file: str
    line: int
    resource_kind: str
    resource_name: str
    message: str

class Summary(BaseModel):
    total_files: int
    total_findings: int
    by_type: Dict[RuleType, int]

class FileError(BaseModel):
    file: str
    error: str

class ScanResponse(BaseModel):
    scan_id: str
    timestamp: str
    scanner_version: str
    findings: List[Finding]
    summary: Summary
    errors: List[FileError]

class ErrorResponse(BaseModel):
    error: str
    message: str
    retry_after: Optional[int] = None