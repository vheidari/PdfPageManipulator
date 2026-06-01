# PdfPageManipulator

`PdfPageManipulator` is a simple Python package built on `PyPDF2` for programmatically manipulating PDF pages. It provides a clean object-oriented API for loading, inserting, extracting, removing, and saving PDF pages with optional page-size control.

The source code lives in `src/pdf_page_manipulator/`, and package metadata is defined in `pyproject.toml`.

## Features

- Load and cache PDF pages in memory
- Insert blank pages:
  - at the beginning
  - at the end
  - after a specific page
  - at a specific page index
- Extract pages by explicit index list or inclusive range
- Extract even and odd pages separately
- Write even/odd page split files directly to disk
- Remove pages:
  - first page
  - last page
  - multiple specified pages
- Save modified PDFs with optional filename prefixes
- Inspect current document state with helper getters
- Use standard page sizes via `PageSize`

## Installation

Install the project dependency in a Python environment that supports Python 3 (**ensure your virtual environment is active**):

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

# Insert a blank page after page 1
manipulator.add_blank_after(1, page_size=PageSize().set_to_A4())

# Insert a blank page before page 2
manipulator.add_blank_at(page_number=2, page_size=PageSize().set_to_A4())

# Extract specific pages using zero-based indexes
manipulator.extract_pages(page_list=[0, 2, 4])

# Extract an inclusive page range: pages 0 through 2
manipulator.extract_range(page_list=[0, 2])

# Remove the first page and save the result
manipulator.remove_first_page()
manipulator.save(prefix_name="edited")
```

### Save even and odd pages separately

```python
manipulator = PdfPageManipulator("example.pdf", ".")
manipulator.load_pdf()
manipulator.extract_even_odd_and_save()
```

This writes two files to the same directory as the original PDF:
- `evens_pages_<original_filename>.pdf`
- `odds_pages_<original_filename>.pdf`

## API Summary

- `PdfPageManipulator(pdf_name: str, path: str)`
- `load_pdf()`
- `get_page_length() -> int`
- `get_full_path() -> str`
- `get_save_path() -> str`
- `set_full_path() -> None`
- `set_save_path() -> None`
- `insert_blank_first(use_buffer: bool = True, page_size: PageSize = None)`
- `insert_blank_last(use_buffer: bool = True, page_size: PageSize = None)`
- `add_blank_after(page_number: int, use_buffer: bool = True, page_size: PageSize = None)`
- `add_blank_at(use_buffer: bool = True, page_number: int = None, page_size: PageSize = None)`
- `extract_pages(use_buffer: bool = True, page_list: list[int] = None)`
- `extract_range(use_buffer: bool = True, page_list: list[int] = None)`
- `extract_evens(use_buffer: bool = True)`
- `extract_odds(use_buffer: bool = True)`
- `extract_even_odd_and_save(use_buffer: bool = True)`
- `remove_first_page(use_buffer: bool = True)`
- `remove_last_page(use_buffer: bool = True)`
- `remove_pages(page_list: list[int] = None, use_buffer: bool = True)`
- `save(save_original = False, prefix_name: str = "")`

## Notes

- `page_list` values are zero-based indexes.
- `extract_range` accepts `[start, end]` and includes both endpoints.
- `extract_even_odd_and_save()` writes split files directly and does not modify the in-memory page list.
- `PageSize` provides convenient standard sizes such as `set_to_A4()`.

## Utility Scripts

This repository includes helper scripts to simplify setup, testing, and cleanup.

- `install_toolchain.sh`
  - Creates a Python virtual environment named `PdfPageManipulatorEnv`.
  - Installs required dependencies: `PyPDF2`, `pytest`, `pytest-cov`, `pytest-mock`, `pytest-html`, `build`, and `twine`.
  - Use before running tests or working with the project for the first time.

- `run_tests.sh`
  - Activates the `PdfPageManipulatorEnv` virtual environment.
  - Runs `cleanup_tests.sh` to remove stale generated test files.
  - Executes `pytest` against `tests/test_PdfPageManipulator.py` with verbose output.
  - Use this script to run the project test suite quickly.

- `cleanup_tests.sh`
  - Removes generated PDF test artifacts matching `*_PPMTest.pdf` from the `tests/` directory.
  - Use this script to clean the test workspace before or after running tests.

## Package Structure

- `src/pdf_page_manipulator/PdfPageManipulator.py` — main implementation
- `tests/test_PdfPageManipulator.py` — test module
- `pyproject.toml` — package metadata and dependencies

## License

This project is licensed under the MIT License.
