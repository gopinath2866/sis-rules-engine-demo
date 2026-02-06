"""CloudFormation parser for SIS."""
from typing import List, Dict, Any
import json
import yaml
import re


TYPE_MAP = {
    "AWS::AutoScaling::AutoScalingGroup": "aws_autoscaling_group",
}


def _load_json_or_yaml(content: str) -> Dict[str, Any]:
    content = content.strip()
    if not content:
        return {}

    if content.startswith("{") or content.startswith("["):
        return json.loads(content)

    return yaml.safe_load(content) or {}


def _to_snake(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "_", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\\1_\\2", value)
    return value.lower().strip("_")


def _normalize_keys(value: Any) -> Any:
    if isinstance(value, dict):
        return {_to_snake(str(k)): _normalize_keys(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize_keys(item) for item in value]
    return value


def parse_cloudformation(content: str) -> List[Dict[str, Any]]:
    """Parse CloudFormation template into resource list."""
    data = _load_json_or_yaml(content)
    resources: List[Dict[str, Any]] = []

    for name, resource in (data.get("Resources", {}) or {}).items():
        if not isinstance(resource, dict):
            continue
        raw_type = resource.get("Type", "")
        kind = TYPE_MAP.get(raw_type)
        if not kind:
            continue
        props = resource.get("Properties", {}) or {}
        if not isinstance(props, dict):
            props = {}
        props = _normalize_keys(props)
        entry = {"kind": kind, "name": name}
        entry.update(props)
        resources.append(entry)

    return resources
