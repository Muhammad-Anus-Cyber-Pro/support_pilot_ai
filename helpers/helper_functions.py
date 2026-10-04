def escape_dollars(text: str) -> str:
    """Prevents Streamlit from misinterpreting $ as LaTeX math delimiters."""
    return text.replace("$", "\\$")