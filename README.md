# PdfPageManipulator

`PdfPageManipulator` is a small, simple, fast, and straightforward Python package designed to manipulate PDF pages programmatically. It is built around `PyPDF2` and provides a clear, object-oriented API for inserting blank pages, extracting page ranges, removing pages, and saving modified PDF documents.

The source code lives in `src/pdf_page_manipulator/`, and the package metadata is defined in `pyproject.toml`.

## Features

- Load a PDF file and cache its pages in memory
- Insert blank pages:
  - at the beginning
  - at the end
  - after a specific page
  - at a specific page index
- Extract pages by index, range, or parity:
  - even pages
  - odd pages
  - save even/odd pages to separate files
- Remove pages:
  - first page
  - last page
  - multiple specified pages
- Save changes to a new PDF file with optional filename prefixes
- Manage standard page sizes via `PageSize`

## Installation

Install the project dependencies in a Python environment that supports Python 3 (**Ensure your virtual environment is active.**):

```bash
python3 -m pip install PyPDF2>=3.0.0
```

If you are installing from source, use (**Ensure your virtual environment is active.**):

```bash
python3 -m pip install .
```

## Usage

```python
from pdf_page_manipulator.PdfPageManipulator import PdfPageManipulator, PageSize

manipulator = PdfPageManipulator("example.pdf", ".")
manipulator.load_pdf()

# Insert a blank A4 page at the beginning
manipulator.insert_blank_first(page_size=PageSize().set_to_A4())

# Remove the last page
manipulator.remove_last_page()

# Extract a range of pages
manipulator.extract_range(page_list=[0, 2])

# Save the modified document
manipulator.save(prefix_name="edited")
```

### Extract even/odd pages and save separately

```python
manipulator = PdfPageManipulator("example.pdf", ".")
manipulator.load_pdf()
manipulator.extract_even_odd_and_save()
```

## API Summary

- `PdfPageManipulator(pdf_name, path)`
- `load_pdf()`
- `insert_blank_first(use_buffer=True, page_size=None)`
- `insert_blank_last(use_buffer=True, page_size=None)`
- `add_blank_after(page_number, use_buffer=True, page_size=None)`
- `add_blank_at(use_buffer=True, after_page=None, page_size=None)`
- `extract_pages(use_buffer=True, page_list=None)`
- `extract_range(use_buffer=True, page_list=None)`
- `extract_evens(use_buffer=True)`
- `extract_odds(use_buffer=True)`
- `extract_even_odd_and_save(use_buffer=True)`
- `remove_first_page(use_buffer=True)`
- `remove_last_page(use_buffer=True)`
- `remove_pages(page_list=None, use_buffer=True)`
- `save(save_original=False, prefix_name="")`

## Package Structure

- `src/pdf_page_manipulator/PdfPageManipulator.py` — main implementation
- `tests/testPdfPageManipulator.py` — starting point for tests
- `pyproject.toml` — package metadata and dependencies

## License

This project is licensed under the MIT License.
