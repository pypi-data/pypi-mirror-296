# OmniMark

OmniMark is a powerful PDF to Markdown converter with support for native, scanned, and hybrid PDFs. It's designed to handle various types of PDFs and extract text, tables, and images, converting them into well-formatted Markdown.

## Features

- Supports native (text-based), scanned (image-based), and hybrid PDFs
- Extracts text content using OCR for scanned documents
- Detects and converts tables to Markdown format
- Handles images and converts them to Markdown image links
- Analyzes PDF structure to maintain document hierarchy
- Configurable page limit for processing large documents

## Installation

Since this is currently a private repository, installation is limited to those with access. Here are the steps for authorized users:

1. Clone the repository (you'll need to authenticate with GitHub):
   ```bash
   git clone https://github.com/royabes/omnimark.git
   cd omnimark
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

## Usage for Authorized Users

After installation, you can use OmniMark as a command-line tool:

```
omnimark <page_limit> <input_file> <output_md>


- `<page_limit>`: Number of pages to process (use 'A' for all pages)
- `<input_file>`: Path to the input PDF file
- `<output_md>`: Path for the output Markdown file

Example:
omnimark A input.pdf output.md

## Requirements

- Python 3.7+
- Dependencies:
  - pytesseract
  - Pillow
  - PyPDF2 (version 2.12.1)
  - camelot-py[cv]
  - opencv-python
  - pdf2image
  - pypdf
  - filetype
  - pdfplumber

## Project Structure

```bash
omnimark/
├── src/
│ └── omnimark/
│ ├── init.py
│ ├── processors/
│ │ └── pdf_page_processor.py
│ └── utils/
│ ├── utils.py
│ ├── table_detector.py
│ ├── pdf_utils.py
│ ├── markdown_converter.py
│ └── config.py
├── setup.py
├── README.md
├── LICENSE
└── .gitignore

   ```
## Development

To set up the development environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/royabes/omnimark.git
   cd omnimark
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the development dependencies:
   ```bash
   pip install -e .
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## For Collaborators

If you're a collaborator on this project:

1. Ensure you have the necessary permissions to access the repository.
2. Follow the installation instructions above.
3. Make your changes in a new branch:
   ```
   git checkout -b feature/your-feature-name
   ```
4. Commit your changes and push to the repository:
   ```
   git add .
   git commit -m "Description of your changes"
   git push origin feature/your-feature-name
   ```
5. Create a pull request on GitHub for review.

## For Other Users

If you're not a collaborator but need to use this package:

1. Contact the repository owner (Roy Abes - roy.abes@gmail.com) to request access.
2. Once granted access, follow the installation instructions above.

Alternatively, if you need to use this in another project without direct access:

1. The repository owner can add the project as a submodule to your project.
2. Or, the owner can build and provide you with a wheel file for installation.

For more detailed instructions on using private repositories, please refer to the `git_instruct.md` file in this repository.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact:
Your Name - your.email@example.com

Project Link: https://github.com/royabes/omnimark
