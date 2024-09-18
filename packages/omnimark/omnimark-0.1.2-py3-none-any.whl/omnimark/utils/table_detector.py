# omnimark/utils/table_detector.py

import camelot
import logging
from typing import List, Dict, Any
import PyPDF2

logger = logging.getLogger(__name__)

def detect_tables(doc_path: str, page_limit: int = None) -> List[Dict[str, Any]]:
    try:
        tables = []
        
        with open(doc_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
        
        logger.info(f"Total pages in document: {total_pages}")

        pages = f"1-{page_limit}" if page_limit else f"1-{total_pages}"
        
        # Choose 'lattice' or 'stream' based on your PDF's structure
        flavor = 'lattice'
        
        extracted_tables = camelot.read_pdf(
            doc_path,
            pages=pages,
            flavor=flavor,
            suppress_stdout=True,
            line_scale=40,  # Adjust this as needed
            shift_text=['']  # Use if necessary to adjust text alignment
        )
        
        logger.info(f"Found {len(extracted_tables)} tables using {flavor} method.")
        
        for table in extracted_tables:
            df = clean_table_data(table.df)
            if is_valid_table(df):
                tables.append({
                    'page_num': table.page,
                    'data': df,
                    'flavor': flavor
                })
        
        logger.info(f"Detected a total of {len(tables)} tables across all pages using Camelot.")
        return tables
    except Exception as e:
        logger.exception(f"Error detecting tables with Camelot: {str(e)}")
        return []

def clean_table_data(df):
    # Remove empty rows/columns or other unwanted data
    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    return df

def is_valid_table(df):
    # Check minimum number of rows and columns
    return df.shape[0] > 2 and df.shape[1] > 1


def is_valid_table(df):
    return df.shape[0] > 2 and df.shape[1] > 1

def table_to_markdown(table: Dict[str, Any], page_num: int) -> str:
    try:
        df = table['data']
        df = df.fillna('')
        
        if df.empty or not is_valid_table(df):
            return '' 
        
        markdown = f"### Table on page {page_num}\n\n"
        
        col_widths = [max(df[col].astype(str).map(len).max(), len(str(col))) for col in df.columns]
        
        header = "| " + " | ".join(str(col).ljust(width) for col, width in zip(df.columns, col_widths)) + " |"
        separator = "|" + "|".join("-" * (width + 2) for width in col_widths) + "|"
        
        markdown += header + "\n" + separator + "\n"
        
        for _, row in df.iterrows():
            row_str = "| " + " | ".join(str(cell).replace("\n", " ").ljust(width) for cell, width in zip(row, col_widths)) + " |"
            markdown += row_str + "\n"
        
        markdown += "\n"
        logger.info(f"Generated markdown table for page {page_num} with {len(df)} rows and {len(df.columns)} columns")
        return markdown
    except Exception as e:
        logger.exception(f"Error converting Camelot table to Markdown on page {page_num}: {str(e)}")
        return f"Error processing table on page {page_num}\n\n"

__all__ = ['detect_tables', 'table_to_markdown']