import os
import logging
from functools import lru_cache
from typing import List, Dict, Any

import filetype
from pypdf import PdfReader
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import camelot
import pandas as pd

# Configure logging
logger = logging.getLogger(__name__)

@lru_cache(maxsize=128)
def get_file_type(file_path: str) -> str:
    """Determine the MIME type of a file."""
    kind = filetype.guess(file_path)
    return kind.mime if kind else None

def load_file(file_path: str) -> str:
    """Determine if the file is a PDF or image."""
    mime = get_file_type(file_path)
    if mime is None:
        raise ValueError("Cannot determine the file type.")
    
    if mime == 'application/pdf':
        return 'pdf'
    elif mime.startswith('image/'):
        return 'image'
    else:
        raise ValueError("Unsupported file type: {}".format(mime))

def load_pdf(file_path: str) -> PdfReader:
    """Load a PDF file and handle potential issues."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    file_size = os.path.getsize(file_path)
    logger.info(f"File size: {file_size} bytes")
    
    if file_size == 0:
        raise ValueError(f"The file {file_path} is empty.")
    
    try:
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)
            if pdf.is_encrypted:
                logger.info("PDF is encrypted. Attempting to decrypt...")
                if not pdf.decrypt(''):
                    raise ValueError("Failed to decrypt PDF.")
                logger.info("Successfully decrypted PDF.")
            
            if len(pdf.pages) == 0:
                raise ValueError(f"The PDF file {file_path} has no pages.")
            
            logger.info(f"Successfully loaded PDF with {len(pdf.pages)} pages")
            return pdf
    except Exception as e:
        logger.error(f"Error reading PDF: {repr(e)}")
        raise ValueError(f"Error reading PDF: {repr(e)}")

def extract_text_content(pdf: PdfReader) -> str:
    """Extract text content from all pages of the PDF."""
    try:
        text_pages = []
        for page_number, page in enumerate(pdf.pages, 1):
            try:
                text = page.extract_text() or ""
                text_pages.append(text)
            except Exception as e:
                logger.error(f"Error extracting text from page {page_number}: {repr(e)}")
                text_pages.append("")
        return "\n".join(text_pages).strip()
    except Exception as e:
        logger.error(f"Error in extract_text_content: {repr(e)}")
        raise

def is_native_pdf(file_path: str) -> bool:
    """Determine if a PDF is native (text-based) or scanned (image-based)."""
    try:
        reader = PdfReader(file_path)
        return any(page.extract_text().strip() for page in reader.pages)
    except Exception as e:
        logger.error(f"Error processing PDF with pypdf: {repr(e)}")
        return False

def ocr_pdf(file_path: str) -> str:
    """Perform OCR on a PDF file."""
    try:
        images = convert_from_path(file_path)
        return '\n'.join(pytesseract.image_to_string(image) for image in images)
    except Exception as e:
        logger.error(f"Failed to perform OCR on PDF: {repr(e)}")
        return ''

def extract_tables(pdf_path: str) -> List[str]:
    """Extract tables from PDF and convert to Markdown."""
    try:
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')
        if not tables:
            tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
        
        return [table.df.replace('', ' ').to_markdown(index=False) for table in tables]
    except Exception as e:
        logger.error(f"Failed to extract tables from PDF: {repr(e)}")
        return []

def extract_tables_tabula(pdf_path: str) -> List[str]:
    """Extract tables from PDF using Tabula and convert to Markdown."""
    try:
        dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        return [df.replace('', ' ').to_markdown(index=False) for df in dfs]
    except Exception as e:
        logger.error(f"Failed to extract tables from PDF using Tabula: {repr(e)}")
        return []

def extract_html_content(pdf_path: str) -> str:
    """Extract HTML content from the PDF."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            html_content = ''
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    text = text.replace('\n', '<br>')
                    html_content += f'<p>{text}</p>'
            return html_content
    except Exception as e:
        logger.error(f"Failed to extract HTML content from PDF: {repr(e)}")
        return ''

def analyze_pdf_structure(pdf_path: str) -> List[Dict[str, Any]]:
    """Analyze the structure of a PDF file."""
    try:
        structure = []
        font_sizes = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                words = page.extract_words(
                    keep_blank_chars=True,
                    use_text_flow=True,
                    extra_attrs=['fontname', 'size', 'x0', 'top', 'width']
                )
                font_sizes.extend(word['size'] for word in words)
                structure.extend(extract_page_structure(words))

        if font_sizes:
            avg_font_size = sum(font_sizes) / len(font_sizes)
            logger.info(f"Average font size: {avg_font_size}")
        else:
            logger.warning("No font sizes extracted.")

        return structure
    except Exception as e:
        logger.error(f"Failed to analyze PDF structure: {repr(e)}")
        return []

def extract_page_structure(words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract the structure of a single page."""
    elements = []
    current_paragraph = ''
    previous_top = None
    previous_end_x = None
    line_spacing_threshold = 1.5

    for word in words:
        text = word['text'].strip()
        size = word['size']
        top = word['top']
        x0 = word['x0']
        width = word.get('width', 0)
        end_x = x0 + width

        new_line = previous_top is not None and (top - previous_top) > size * line_spacing_threshold
        add_space = not previous_end_x or (x0 - previous_end_x) >= size * 0.5

        if new_line and current_paragraph:
            elements.append({'type': 'paragraph', 'content': current_paragraph.strip()})
            current_paragraph = ''
        elif add_space and current_paragraph:
            current_paragraph += ' '

        current_paragraph += text
        previous_top, previous_end_x = top, end_x

    if current_paragraph:
        elements.append({'type': 'paragraph', 'content': current_paragraph.strip()})

    return elements

# Utility functions
def is_heading(size: float, fontname: str, threshold: float = 14) -> bool:
    return size >= threshold and 'Bold' in fontname

def is_list_item(text: str) -> bool:
    import re
    return bool(re.match(r'^([\-\*•●◦▪]|\d+\.)\s+', text))

def group_words_into_columns(words: List[Dict[str, Any]], tolerance: int = 50) -> List[List[Dict[str, Any]]]:
    columns = {}
    for word in words:
        column_key = round(word['x0'] / tolerance) * tolerance
        columns.setdefault(column_key, []).append(word)
    return [columns[key] for key in sorted(columns)]

# Main processing function
def process_pdf(file_path: str) -> Dict[str, Any]:
    """Process a PDF file and extract various information."""
    try:
        pdf = load_pdf(file_path)
        is_native = is_native_pdf(file_path)
        
        result = {
            'text_content': extract_text_content(pdf) if is_native else ocr_pdf(file_path),
            'tables': extract_tables(file_path),
            'html_content': extract_html_content(file_path),
            'structure': analyze_pdf_structure(file_path),
            'is_native': is_native,
        }
        
        return result
    except Exception as e:
        logger.error(f"Error processing PDF '{file_path}': {repr(e)}")
        raise