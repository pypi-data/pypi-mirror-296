# omnimark/__init__.py


try:
    from .processors.pdf_page_processor import PDFPageProcessor, process_pdf

    __all__ = ['PDFPageProcessor', 'process_pdf']
except ImportError as e:
    print(f"Error importing processors: {e}")
    print("Current directory structure:")
    import os
    for root, dirs, files in os.walk("."):
        level = root.replace(".", "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")
    __all__ = []