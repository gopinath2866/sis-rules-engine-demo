"""Docker Compose parser for SIS."""
from typing import List, Dict, Any
import yaml


def parse_docker_compose(content: str) -> List[Dict[str, Any]]:
    """Parse Docker Compose YAML into service resources (demo stub)."""
    _ = yaml.safe_load(content) or {}
    return []
