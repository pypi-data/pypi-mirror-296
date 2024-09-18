# omnimark/utils/config.py

from pathlib import Path
import logging

# Directory to save extracted images
IMAGE_OUTPUT_DIR = Path("extracted_images")

# Define CONFIG object
CONFIG = {
    # Your configuration settings here
    "example_setting": "value",
    'IMAGE_OUTPUT_DIR': 'D:/DocAI/OmniMark/Omnimark2/extracted_images',  # Added IMAGE_OUTPUT_DIR
}

# Configure logging to write to a specific file
logging.basicConfig(
    filename='D:/DocAI/OmniMark/Omnimark2/omnimark_conversion.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# Make sure to export CONFIG
__all__ = ["CONFIG"]

# Add other configurations as needed
