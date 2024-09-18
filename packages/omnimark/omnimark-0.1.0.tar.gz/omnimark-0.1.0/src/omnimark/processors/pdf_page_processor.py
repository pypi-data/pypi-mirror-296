# omnimark/pdf_page_processor.py

import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LAParams, LTImage, LTFigure
from omnimark.utils.markdown_converter import text_to_markdown
from omnimark.utils.table_detector import detect_tables, table_to_markdown
from omnimark.utils.config import CONFIG
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

logger = logging.getLogger(__name__)

class PDFPageProcessor:
    def __init__(self):
        self.config = CONFIG

    def process(self, file_path: str, output_path: str, page_limit: int = None) -> str:
        try:
            logger.info(f"Starting to process PDF: {file_path}")
            logger.info(f"Output will be written to: {output_path}")

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Input PDF file not found: {file_path}")

            markdown_content = self.process_pdf_pages(file_path, page_limit)
            logger.info(f"Generated markdown content. Length: {len(markdown_content)}")

            self._write_markdown(markdown_content, output_path)

            logger.info(f"Successfully processed PDF: {file_path}")
            return markdown_content
        except Exception as e:
            logger.exception(f"Error in PDF processor: {str(e)}")
            raise

    def process_pdf_pages(self, file_path: str, page_limit: int = None) -> str:
        markdown_content = []
        laparams = LAParams()
        pages = extract_pages(file_path, laparams=laparams)

        for page_num, page_layout in enumerate(pages, start=1):
            if page_limit and page_num > page_limit:
                break

            logger.info(f"Processing page {page_num}")
            page_elements = self.extract_page_elements(page_layout, page_num)
            page_tables = detect_tables(file_path, page_num)
            page_images = self.extract_and_ocr_images(page_layout, file_path, page_num)

            page_markdown = self.convert_page_to_markdown(page_elements, page_tables, page_images, page_num)
            markdown_content.append(page_markdown)

        return "\n\n---\n\n".join(markdown_content)

    def extract_page_elements(self, page_layout, page_num: int) -> List[Dict[str, Any]]:
        elements = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    text = text_line.get_text().strip()
                    if text:
                        font_size = self.get_font_size(text_line)
                        font_styles = self.get_font_styles(text_line)
                        elements.append({
                            'type': 'text',
                            'text': text,
                            'font_size': font_size,
                            'font_styles': font_styles,
                            'x0': text_line.x0,
                            'y0': text_line.y0,
                            'x1': text_line.x1,
                            'y1': text_line.y1,
                            'page_number': page_num
                        })
        return elements

    def extract_and_ocr_images(self, page_layout, file_path: str, page_num: int) -> List[str]:
        image_texts = []
        for element in page_layout:
            if isinstance(element, (LTImage, LTFigure)):
                image = self.extract_image(element, file_path, page_num)
                if image is not None and self.might_contain_text(image):
                    text = pytesseract.image_to_string(image)
                    if text.strip():
                        image_texts.append(text)
        return image_texts

    def extract_image(self, lt_image, file_path: str, page_num: int) -> Image.Image:
        try:
            images = convert_from_path(file_path, first_page=page_num, last_page=page_num)
            if images:
                return images[0].crop(self.get_bbox(lt_image))
        except Exception as e:
            logger.error(f"Error extracting image from page {page_num}: {str(e)}")
        return None

    def get_bbox(self, element) -> Tuple[float, float, float, float]:
        x0, y0, x1, y1 = element.bbox
        return (x0, y0, x1, y1)

    def might_contain_text(self, image: Image.Image) -> bool:
        img_array = np.array(image)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        text_pixel_ratio = np.sum(thresh == 255) / thresh.size
        return text_pixel_ratio > 0.01

    def convert_page_to_markdown(self, elements: List[Dict[str, Any]], tables: List[Dict[str, Any]], image_texts: List[str], page_num: int) -> str:
        markdown_content = [f"## Page {page_num}\n"]

        # Convert text elements to markdown
        for element in elements:
            if element['type'] == 'text':
                md_text = text_to_markdown(element)
                markdown_content.append(md_text)

        # Add tables
        for table in tables:
            table_md = table_to_markdown(table, page_num)
            markdown_content.append(f"\n\n{table_md}\n\n")

        # Add OCR'd text from images
        if image_texts:
            markdown_content.append("\n### Text extracted from images:\n")
            for text in image_texts:
                markdown_content.append(f"\n{text}\n")

        return "\n".join(markdown_content)

    def get_font_size(self, text_line) -> float:
        for char in text_line:
            if isinstance(char, LTChar):
                return char.size
        return 0  # Default size if no characters found

    def get_font_styles(self, text_line) -> List[str]:
        styles = set()
        for char in text_line:
            if isinstance(char, LTChar):
                font_name = char.fontname.lower()
                if 'bold' in font_name:
                    styles.add('bold')
                if 'italic' in font_name or 'oblique' in font_name:
                    styles.add('italic')
        return list(styles)

    def _write_markdown(self, content: str, output_path: str) -> None:
        output_file = Path(output_path)
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Attempting to write output to: {output_file}")
            output_file.write_text(content, encoding='utf-8')
            logger.info(f"Markdown file written: {output_file}")
            logger.info(f"File size: {output_file.stat().st_size} bytes")
        except Exception as e:
            logger.exception(f"Error writing markdown file: {output_file}")
            raise

def process_pdf(input_pdf: str, output_md: str, page_limit: int = None) -> str:
    """
    Process a PDF by extracting text, tables, and OCR'ing images, then converting to Markdown.
    """
    processor = PDFPageProcessor()
    return processor.process(input_pdf, output_md, page_limit)