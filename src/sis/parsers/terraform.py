"""Terraform parser for SIS."""
from typing import List, Dict, Any
import io
import json
import hcl2


def _load_terraform(content: str) -> Dict[str, Any]:
    content = content.strip()
    if not content:
        return {}

    # Terraform JSON configuration is valid JSON.
    if content.startswith("{") or content.startswith("["):
        return json.loads(content)

    return hcl2.load(io.StringIO(content))


def _iter_resource_blocks(resource_block: Any):
    if isinstance(resource_block, dict):
        yield resource_block
    elif isinstance(resource_block, list):
        for item in resource_block:
            if isinstance(item, dict):
                yield item


def _normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _normalize(val) for key, val in value.items()}
    if isinstance(value, list):
        if len(value) == 1 and isinstance(value[0], dict):
            return _normalize(value[0])
        return [_normalize(item) for item in value]
    return value


ALLOWED_KINDS = {
    "google_service_account",
    "aws_iam_access_key",
    "aws_instance",
    "google_compute_instance",
    "aws_cloudtrail",
    "aws_autoscaling_group",
}


def parse_terraform(content: str) -> List[Dict[str, Any]]:
    """Parse Terraform HCL/JSON into resource list (demo scope)."""
    data = _load_terraform(content)
    resources: List[Dict[str, Any]] = []

    for block in _iter_resource_blocks(data.get("resource", {})):
        for resource_type, resource_defs in block.items():
            if resource_type not in ALLOWED_KINDS:
                continue
            if not isinstance(resource_defs, dict):
                continue
            for name, attrs in resource_defs.items():
                if not isinstance(attrs, dict):
                    continue
                resource = {"kind": resource_type, "name": name}
                resource.update(_normalize(attrs))
                resources.append(resource)

    return resources
