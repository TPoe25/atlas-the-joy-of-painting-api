#!/usr/bin/env python3

from typing import Any

def safe_int(value: Any) -> int:
    """Converts a string to an integer safely. Returns 0 if conversion fails."""
    try:
        return int(value)
    except Exception:
        return 0
