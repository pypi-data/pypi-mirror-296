# omnimark/utils/__init__.py

from .config import CONFIG
from .markdown_converter import text_to_markdown
from .table_detector import detect_tables, table_to_markdown
from .utils import setup_logging, log_error, notify_user

__all__ = [
    'CONFIG',
    'text_to_markdown',
    'detect_tables',
    'table_to_markdown',
    'setup_logging',
    'log_error',
    'notify_user'
]
