"""Azure ARM template parser for SIS."""
from typing import List, Dict, Any
import json


def parse_arm(content: str) -> List[Dict[str, Any]]:
    """Parse ARM JSON template into resource list (demo stub)."""
    _ = json.loads(content) if content.strip() else {}
    return []
