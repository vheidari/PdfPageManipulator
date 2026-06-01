import os
import pytest

from pdf_page_manipulator import PdfPageManipulator, PageSize
from pdf_page_manipulator.PdfPageManipulator import PdfActions



def test_get_page_length():
    # Given a PDF file, when I get the page length, then it should return the correct number of pages.
    expected_page_length = 20
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    manipulator.load_pdf()
    page_length = manipulator.get_page_length()

    assert page_length == expected_page_length, f"Expected page length to be 20, but got {page_length}"


def test_get_full_path():
    # Given a PDF file, when I get the full path, then it should return the correct full path of the PDF file.
    pdf_name = "PPMTest.pdf"
    path = "./tests/"

    expected_full_path = os.path.join(path, pdf_name)
    manipulator = PdfPageManipulator(pdf_name, path)
    manipulator.load_pdf()
    full_path = manipulator.get_full_path()

    assert full_path == expected_full_path, f"Expected full path to be {expected_full_path}, but got {full_path}"


def test_get_save_path():
    # Given a PDF file, when I get the save path, then it should return the correct save path of the PDF file.
    pdf_name = "PPMTest.pdf"
    path = "./tests/"

    expected_save_path = os.path.join(path, f"new_{pdf_name}")
    manipulator = PdfPageManipulator(pdf_name, path)
    manipulator.load_pdf()
    save_path = manipulator.get_save_path()

    assert save_path == expected_save_path, f"Expected save path to be {expected_save_path}, but got {save_path}"


def test_set_full_path():
    # Given a PDF file, when I set the full path, then it should update the full path of the PDF file.
    pdf_name = "PPMTest.pdf"
    path = "./tests/"
    new_path = "./new_tests/"
    expected_full_path = os.path.join(new_path, pdf_name)
    manipulator = PdfPageManipulator(pdf_name, path)
    manipulator.load_pdf()
    manipulator.set_full_path(new_path)
    full_path = manipulator.get_full_path()

    assert full_path == expected_full_path, f"Expected full path to be {expected_full_path}, but got {full_path}"


def test_set_save_path():
    # Given a PDF file, when I set the save path, then it should update the save path of the PDF file.
    pdf_name = "PPMTest.pdf"
    path = "./tests/"
    new_path = "./new_tests/"
    expected_save_path = os.path.join(new_path, f"new_{pdf_name}")
    manipulator = PdfPageManipulator(pdf_name, path)
    manipulator.load_pdf()
    manipulator.set_save_path(new_path)
    save_path = manipulator.get_save_path()

    assert save_path == expected_save_path, f"Expected save path to be {expected_save_path}, but got {save_path}"

def test_insert_first_page():
    # This test checks if the insert_blank_first method correctly inserts a blank page at the beginning of 
    # the PDF and increases the page length by 1. It also checks if the new file is created after saving.
    result_file_prefix = "test_insert_first_page"
    result_file_name = f"{result_file_prefix}_PPMTest.pdf"

    # Given a PDF file, when I insert a blank page at the beginning of the PDF, 
    # then the page length should increase by 1 and the new file should be created.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    page_size = PageSize()
    manipulator.load_pdf()
    original_page_length = manipulator.get_page_length()
    manipulator.insert_blank_first(page_size=page_size.set_to_A4())
    manipulator.save(prefix_name=result_file_prefix)
    
    # Load the new PDF and check the page length
    mp_test = PdfPageManipulator(result_file_name, "./tests/")
    mp_test.load_pdf()
    test_page_length = mp_test.get_page_length()

    compare_page_length =  test_page_length - original_page_length
    
    # The page length should be 1 less than the original page length because we inserted a blank page at the beginning of the PDF.
    assert compare_page_length == 1, f"Expected page length to be {original_page_length + 1}, but got {test_page_length}"

    
    # is the file created?
    assert os.path.exists(f"./tests/{result_file_name}"), f"Expected file {result_file_name} to be created, but it does not exist."
    


def test_insert_blank_last():
    # This test checks if the insert_blank_last method correctly inserts a blank page at the end of 
    # the PDF and increases the page length by 1. It also checks if the new file is created after saving.
    result_file_prefix = "test_insert_blank_last"
    result_file_name = f"{result_file_prefix}_PPMTest.pdf"

    # Given a PDF file, when I insert a blank page at the end of the PDF, 
    # then the page length should increase by 1 and the new file should be created.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    page_size = PageSize()
    manipulator.load_pdf()
    original_page_length = manipulator.get_page_length()
    manipulator.insert_blank_last(page_size=page_size.set_to_A4())
    manipulator.save(prefix_name=result_file_prefix)
    
    # Load the new PDF and check the page length
    mp_test = PdfPageManipulator(result_file_name, "./tests/")
    mp_test.load_pdf()
    test_page_length = mp_test.get_page_length()

    compare_page_length =  test_page_length - original_page_length
    
    # The page length should be 1 less than the original page length because we inserted a blank page at the end of the PDF.
    assert compare_page_length == 1, f"Expected page length to be {original_page_length + 1}, but got {test_page_length}"

    
    # is the file created?
    assert os.path.exists(f"./tests/{result_file_name}"), f"Expected file {result_file_name} to be created, but it does not exist."





def test_add_blank_after():
    # This test checks if the add_blank_after method correctly inserts a blank page after a specified page number in the PDF and increases the page length by 1. It also checks if the new file is created after saving.
    result_file_prefix = "test_add_blank_after"
    result_file_name = f"{result_file_prefix}_PPMTest.pdf"

    # Given a PDF file, when I insert a blank page after a specified page number in the PDF, 
    # then the page length should increase by 1 and the new file should be created.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    page_size = PageSize()
    manipulator.load_pdf()
    original_page_length = manipulator.get_page_length()
    manipulator.add_blank_after(page_number=5, page_size=page_size.set_to_A4())
    manipulator.add_blank_after(page_number=6, page_size=page_size.set_to_A4())

    manipulator.save(prefix_name=result_file_prefix)
    
    # Load the new PDF and check the page length
    mp_test = PdfPageManipulator(result_file_name, "./tests/")
    mp_test.load_pdf()
    test_page_length = mp_test.get_page_length()

    compare_page_length =  test_page_length - original_page_length
    
    # The page length should be 2 less than the original page length because we inserted a blank page after a specified page number in the PDF.
    assert compare_page_length == 2, f"Expected page length to be {original_page_length + 2}, but got {test_page_length}"

    
    # is the file created?
    assert os.path.exists(f"./tests/{result_file_name}"), f"Expected file {result_file_name} to be created, but it does not exist."



def test_add_blank_at():
    # This test checks if the add_blank_at method correctly inserts a blank page at a specified page number in the PDF and increases the page length by 1. It also checks if the new file is created after saving.
    result_file_prefix = "test_add_blank_at"
    result_file_name = f"{result_file_prefix}_PPMTest.pdf"

    # Given a PDF file, when I insert a blank page at a specified page number in the PDF, 
    # then the page length should increase by 1 and the new file should be created.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    page_size = PageSize()
    manipulator.load_pdf()
    original_page_length = manipulator.get_page_length()
    manipulator.add_blank_at(page_number=2, page_size=page_size.set_to_A4())
    manipulator.add_blank_at(page_number=9, page_size=page_size.set_to_A4())
    manipulator.add_blank_at(page_number=14, page_size=page_size.set_to_A4())

    manipulator.save(prefix_name=result_file_prefix)
    
    # Load the new PDF and check the page length
    mp_test = PdfPageManipulator(result_file_name, "./tests/")
    mp_test.load_pdf()
    test_page_length = mp_test.get_page_length()

    compare_page_length =  test_page_length - original_page_length
    
    # The page length should be 3 less than the original page length because we inserted a blank page at a specified page number in the PDF.
    assert compare_page_length == 3, f"Expected page length to be {original_page_length + 3}, but got {test_page_length}"

    
    # is the file created?
    assert os.path.exists(f"./tests/{result_file_name}"), f"Expected file {result_file_name} to be created, but it does not exist."


def test_extract_pages():
    # This test checks if the extract_pages method correctly extracts specified pages from the PDF and creates a new PDF file with the extracted pages. It also checks if the new file is created after saving.
    result_file_prefix = "test_extract_pages"
    result_file_name = f"{result_file_prefix}_PPMTest.pdf"

    # Given a PDF file, when I extract specified pages from the PDF, 
    # then a new PDF file should be created with the extracted pages.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    manipulator.load_pdf()
    manipulator.extract_pages(page_list=[2, 4, 6, 8]) # exteract even pages from the original PDF
    manipulator.save(prefix_name=result_file_prefix)
    
    # Load the new PDF and check the page length
    mp_test = PdfPageManipulator(result_file_name, "./tests/")
    mp_test.load_pdf()
    test_page_length = mp_test.get_page_length()

    expected_page_length = 4
    
    # The page length should be 4 because we extracted 4 pages from the original PDF.
    assert test_page_length == expected_page_length, f"Expected page length to be {expected_page_length}, but got {test_page_length}"

    
    # is the file created?
    assert os.path.exists(f"./tests/{result_file_name}"), f"Expected file {result_file_name} to be created, but it does not exist."



def test_extract_range():
    # This test checks if the extract_range method correctly extracts a range of pages from the PDF and creates a new PDF file with the extracted pages. It also checks if the new file is created after saving.
    result_file_prefix = "test_extract_range"
    result_file_name = f"{result_file_prefix}_PPMTest.pdf"

    # Given a PDF file, when I extract a range of pages from the PDF, 
    # then a new PDF file should be created with the extracted pages.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    manipulator.load_pdf()
    manipulator.extract_range(page_list=[5,10]) # exteract pages from 5 to 10 from the original PDF
    manipulator.save(prefix_name=result_file_prefix)
    
    # Load the new PDF and check the page length
    mp_test = PdfPageManipulator(result_file_name, "./tests/")
    mp_test.load_pdf()
    test_page_length = mp_test.get_page_length()

    expected_page_length = 6
    
    # The page length should be 6 because we extracted 6 pages from the original PDF.
    assert test_page_length == expected_page_length, f"Expected page length to be {expected_page_length}, but got {test_page_length}"

    
    # is the file created?
    assert os.path.exists(f"./tests/{result_file_name}"), f"Expected file {result_file_name} to be created, but it does not exist."


def test_extract_evens():
    # This test checks if the extract_even method correctly extracts all even pages from the PDF and creates a new PDF file with the extracted pages. It also checks if the new file is created after saving.
    result_file_prefix = "test_extract_even"
    result_file_name = f"{result_file_prefix}_PPMTest.pdf"

    # Given a PDF file, when I extract all even pages from the PDF, 
    # then a new PDF file should be created with the extracted pages.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    manipulator.load_pdf()
    manipulator.extract_evens() # exteract all even pages from the original PDF
    manipulator.save(prefix_name=result_file_prefix)
    
    # Load the new PDF and check the page length
    mp_test = PdfPageManipulator(result_file_name, "./tests/")
    mp_test.load_pdf()
    test_page_length = mp_test.get_page_length()

    expected_page_length = 10
    
    # The page length should be 10 because we extracted 10 even pages from the original PDF.
    assert test_page_length == expected_page_length, f"Expected page length to be {expected_page_length}, but got {test_page_length}"

    
    # is the file created?
    assert os.path.exists(f"./tests/{result_file_name}"), f"Expected file {result_file_name} to be created, but it does not exist."



def test_extract_odds():
    # This test checks if the extract_odd method correctly extracts all odd pages from the PDF and creates a new PDF file with the extracted pages. It also checks if the new file is created after saving.
    result_file_prefix = "test_extract_odd"
    result_file_name = f"{result_file_prefix}_PPMTest.pdf"

    # Given a PDF file, when I extract all odd pages from the PDF, 
    # then a new PDF file should be created with the extracted pages.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    manipulator.load_pdf()
    manipulator.extract_odds() # exteract all odd pages from the original PDF
    manipulator.save(prefix_name=result_file_prefix)
    
    # Load the new PDF and check the page length
    mp_test = PdfPageManipulator(result_file_name, "./tests/")
    mp_test.load_pdf()
    test_page_length = mp_test.get_page_length()

    expected_page_length = 10
    
    # The page length should be 10 because we extracted 10 odd pages from the original PDF.
    assert test_page_length == expected_page_length, f"Expected page length to be {expected_page_length}, but got {test_page_length}"

    
    # is the file created?
    assert os.path.exists(f"./tests/{result_file_name}"), f"Expected file {result_file_name} to be created, but it does not exist."



def test_extract_even_odd_and_save():
    # This test checks if the extract_evens_and_save and extract_odds_and_save methods correctly extract all even and odd pages from the PDF respectively and create new PDF files with the extracted pages. It also checks if the new files are created after saving.
    even_result_file_prefix = "evens_pages"
    even_result_file_name = f"{even_result_file_prefix}_PPMTest.pdf"

    odd_result_file_prefix = "odds_pages"
    odd_result_file_name = f"{odd_result_file_prefix}_PPMTest.pdf"

    # Given a PDF file, when I extract all even and odd pages from the PDF, 
    # then new PDF files should be created with the extracted pages.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    manipulator.load_pdf()
    manipulator.extract_even_odd_and_save() 
    
    # Load the new PDFs and check the page lengths
    mp_even_test = PdfPageManipulator(even_result_file_name, "./tests/")
    mp_even_test.load_pdf()
    even_test_page_length = mp_even_test.get_page_length()

    mp_odd_test = PdfPageManipulator(odd_result_file_name, "./tests/")
    mp_odd_test.load_pdf()
    odd_test_page_length = mp_odd_test.get_page_length()

    expected_page_length = 10
    
    # The page length of both even and odd PDFs should be 10 because we extracted 10 even and 10 odd pages from the original PDF.
    assert even_test_page_length == expected_page_length, f"Expected page length to be {expected_page_length}, but got {even_test_page_length}"
    assert odd_test_page_length == expected_page_length, f"Expected page length to be {expected_page_length}, but got {odd_test_page_length}"

    
    # are the files created?
    assert os.path.exists(f"./tests/{even_result_file_name}"), f"Expected file {even_result_file_name} to be created, but it does not exist."
    assert os.path.exists(f"./tests/{odd_result_file_name}"), f"Expected file {odd_result_file_name} to be created, but it does not"




def test_remove_first_page():
    # This test checks if the remove_first_page method correctly removes the first page from the PDF and decreases the page length by 1. It also checks if the new file is created after saving.
    result_file_prefix = "test_remove_first_page"
    result_file_name = f"{result_file_prefix}_PPMTest.pdf"

    # Given a PDF file, when I remove the first page from the PDF, 
    # then the page length should decrease by 1 and the new file should be created.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    manipulator.load_pdf()
    original_page_length = manipulator.get_page_length()
    manipulator.remove_first_page()
    manipulator.save(prefix_name=result_file_prefix)
    
    # Load the new PDF and check the page length
    mp_test = PdfPageManipulator(result_file_name, "./tests/")
    mp_test.load_pdf()
    test_page_length = mp_test.get_page_length()

    compare_page_length =  original_page_length - test_page_length
    
    # The page length should be 1 less than the original page length because we removed the first page from the PDF.
    assert compare_page_length == 1, f"Expected page length to be {original_page_length - 1}, but got {test_page_length}"

    
    # is the file created?
    assert os.path.exists(f"./tests/{result_file_name}"), f"Expected file {result_file_name} to be created, but it does not exist."


def test_remove_last_page():
    # This test checks if the remove_last_page method correctly removes the last page from the PDF and decreases the page length by 1. It also checks if the new file is created after saving.
    result_file_prefix = "test_remove_last_page"
    result_file_name = f"{result_file_prefix}_PPMTest.pdf"

    # Given a PDF file, when I remove the last page from the PDF, 
    # then the page length should decrease by 1 and the new file should be created.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    manipulator.load_pdf()
    original_page_length = manipulator.get_page_length()
    manipulator.remove_last_page()
    manipulator.save(prefix_name=result_file_prefix)
    
    # Load the new PDF and check the page length
    mp_test = PdfPageManipulator(result_file_name, "./tests/")
    mp_test.load_pdf()
    test_page_length = mp_test.get_page_length()

    compare_page_length =  original_page_length - test_page_length
    
    # The page length should be 1 less than the original page length because we removed the last page from the PDF.
    assert compare_page_length == 1, f"Expected page length to be {original_page_length - 1}, but got {test_page_length}"

    
    # is the file created?
    assert os.path.exists(f"./tests/{result_file_name}"), f"Expected file {result_file_name} to be created, but it does not exist."



def test_remove_pages():
    # This test checks if the remove_pages method correctly removes specified pages from the PDF and decreases the page length by the number of removed pages. It also checks if the new file is created after saving.
    result_file_prefix = "test_remove_pages"
    result_file_name = f"{result_file_prefix}_PPMTest.pdf"
    page_list=[3,4,5,6]

    # Given a PDF file, when I remove specified pages from the PDF, 
    # then the page length should decrease by the number of removed pages and the new file should be created.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    manipulator.load_pdf()
    original_page_length = manipulator.get_page_length()
    manipulator.remove_pages(page_list=page_list)
    manipulator.save(prefix_name=result_file_prefix)
    
    # Load the new PDF and check the page length
    mp_test = PdfPageManipulator(result_file_name, "./tests/")
    mp_test.load_pdf()
    test_page_length = mp_test.get_page_length()

    compare_page_length =  original_page_length - test_page_length
    
    # The page length should be 4 less than the original page length because we removed 4 pages from the PDF.
    assert compare_page_length == len(page_list), f"Expected page length to be {original_page_length - len(page_list)}, but got {test_page_length}"

    
    # is the file created?
    assert os.path.exists(f"./tests/{result_file_name}"), f"Expected file {result_file_name} to be created, but it does not exist."



def test_save():
    # This test checks if the save method correctly saves the PDF file with the specified prefix name and creates a new file. It also checks if the new file is created after saving.
    result_file_prefix = "test_save"
    result_file_name = f"{result_file_prefix}_PPMTest.pdf"

    # Given a PDF file, when I save the PDF file with a specified prefix name, 
    # then a new PDF file should be created with the specified prefix name.
    manipulator = PdfPageManipulator("PPMTest.pdf", "./tests/")
    manipulator.load_pdf()
    manipulator.save(prefix_name=result_file_prefix)
    
    # is the file created?
    assert os.path.exists(f"./tests/{result_file_name}"), f"Expected file {result_file_name} to be created, but it does not exist."

