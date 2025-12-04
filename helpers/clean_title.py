#!/usr/bin/env python3
from typing import Any

def clean_title(raw_title: Any) -> str:
    """cleans the painting title by removing unwanted characters."""

    # Check if the title is empty or None
    if not raw_title:
        return ""

    # Remove leading/trailing whitespace and unwanted characters
    text = str(clean_title).strip()
    text = text.replace('"', "").replace("'", "")
    text = " ".join(text.split())

    # Normalize the title by converting to title case
    return text.title()
