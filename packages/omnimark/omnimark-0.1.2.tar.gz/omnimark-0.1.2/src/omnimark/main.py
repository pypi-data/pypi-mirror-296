from .processors.pdf_page_processor import process_pdf
import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: omnimark <page_limit> <input_file> <output_md>")
        sys.exit(1)
    
    page_limit = sys.argv[1]
    input_file = sys.argv[2]
    output_md = sys.argv[3]
    
    process_pdf(input_file, output_md, page_limit)

if __name__ == "__main__":
    main()