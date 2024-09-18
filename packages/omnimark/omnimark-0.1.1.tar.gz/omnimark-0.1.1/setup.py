from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="omnimark",
    version="0.1.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    author="Roy Abes",
    author_email="roy.abes@gmail.com",
    description="A PDF to Markdown converter with support for native, scanned, and hybrid PDFs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/royabes/omnimark",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pytesseract>=0.3.0",
        "Pillow>=8.0.0",
        "PyPDF2==2.12.1",
        "camelot-py[cv]>=0.10.0",
        "opencv-python>=4.0.0",
        "pdf2image>=1.16.0",
        "pypdf>=3.0.0",
        "filetype>=1.0.0",
        "pdfplumber>=0.7.0",
        "pdfminer.six>=20200726",  # Added this line
    ],
    entry_points={
        "console_scripts": [
            "omnimark=omnimark.__main__:main",
        ],
    },
    include_package_data=True,
    extras_require={
        'dev': [
            'pytest>=6.0',
            'flake8>=3.9',
            'mypy>=0.800',
        ],
    },
)