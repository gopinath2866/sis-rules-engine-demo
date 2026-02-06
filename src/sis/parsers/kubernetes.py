"""Kubernetes manifest parser for SIS."""
from typing import List, Dict, Any
import yaml


ALLOWED_KINDS = {"ServiceAccount", "ClusterRoleBinding"}


def parse_kubernetes(content: str) -> List[Dict[str, Any]]:
    """Parse Kubernetes YAML into resource list (demo scope)."""
    resources: List[Dict[str, Any]] = []

    for doc in yaml.safe_load_all(content):
        if not isinstance(doc, dict):
            continue
        kind = doc.get("kind")
        if kind not in ALLOWED_KINDS:
            continue
        metadata = doc.get("metadata", {}) or {}
        name = metadata.get("name", "") if isinstance(metadata, dict) else ""
        entry = dict(doc)
        entry["name"] = name
        resources.append(entry)

    return resources
