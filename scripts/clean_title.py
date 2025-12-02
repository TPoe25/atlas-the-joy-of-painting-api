#!/usr/bin/env python3

def clean_title(title: str) -> str:
    """cleans the painting title by removing unwanted characters."""
    if not title:
        return ""
    t = title.strip().replace('"', '').replace("'", "").title()
    t = " ".join(t.split()) # remove extra spaces
    return t.title()  # capitalize the first letter of each word
