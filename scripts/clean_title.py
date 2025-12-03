#!/usr/bin/env python3

def clean_title(raw_title: str) -> str:
    """cleans the painting title by removing unwanted characters."""

    # Check if the title is empty or None
    if not raw_title:
        return ""

    # Remove leading/trailing whitespace and unwanted characters
    title = str(raw_title).strip()
    title = title.replace('"', "").replace("'", "")
    title = " ".join(title.split())

    # Normalize the title by converting to title case
    return title.title()
