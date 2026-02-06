"""Parsers for supported IaC formats."""
from typing import List, Dict, Any

from .terraform import parse_terraform
from .cloudformation import parse_cloudformation
from .kubernetes import parse_kubernetes
from .docker_compose import parse_docker_compose
from .arm import parse_arm


def parse_file(file_type: str, content: str) -> List[Dict[str, Any]]:
    """Dispatch to the correct parser based on file type."""
    if file_type == "terraform":
        return parse_terraform(content)
    if file_type == "cloudformation":
        return parse_cloudformation(content)
    if file_type == "kubernetes":
        return parse_kubernetes(content)
    if file_type == "docker_compose":
        return parse_docker_compose(content)
    if file_type == "arm":
        return parse_arm(content)

    raise ValueError(f"Unsupported file type: {file_type}")


__all__ = ["parse_file"]
