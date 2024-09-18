# omnimark/utils/markdown_converter.py

import logging
import os

logger = logging.getLogger(__name__)

def text_to_markdown(elem):
    """
    Converts a text element with styling into Markdown.
    """
    if isinstance(elem, str):
        return elem

    if not isinstance(elem, dict):
        logger.warning(f"Unexpected element type: {type(elem)}. Returning as is.")
        return str(elem)

    text = elem.get("text", "")
    font_size = elem.get("font_size", 0)
    is_bold = "bold" in elem.get("font_styles", [])
    is_italic = "italic" in elem.get("font_styles", [])

    # Determine if it's a heading based on font size
    if font_size > 14:  # Adjust this threshold as needed
        heading_level = "#" if font_size > 18 else "##"
        text = f"{heading_level} {text}"
    
    if is_bold:
        text = f"**{text}**"
    if is_italic:
        text = f"*{text}*"

    return text

def image_to_markdown(image_path: str) -> str:
    """
    Convert an image file to a Markdown image link.
    """
    try:
        if not os.path.exists(image_path):
            logger.error(f"Image file does not exist: {image_path}")
            return ""
        
        # Assuming images are in a relative path from the Markdown file
        relative_path = os.path.relpath(image_path)
        filename = os.path.basename(image_path)
        markdown = f"![{filename}]({relative_path})"
        logger.debug(f"Converted {image_path} to Markdown: {markdown}")
        return markdown
    except Exception as e:
        logger.exception(f"Failed to convert image to Markdown: {e}")
        raise
