# Import stdlib libraries 
import os 
from enum import Enum

# Import third-party libraries
from PyPDF2 import PdfReader, PdfWriter , PaperSize


class PdfActions(Enum):
    """Enumeration of PDF manipulation actions supported by the library.

    Each enum value represents one high-level operation that can be performed
    by `PdfPageManipulator.__dispatch_action`. The names reflect the current
    public API methods (for example `insert_blank_first` maps to
    `PdfActions.INSERT_BLANK_FIRST`).

    Use these values only internally; public callers should use the
    `PdfPageManipulator` convenience methods such as `insert_blank_first`.
    """
    
    INSERT_BLANK_FIRST        = "insert_blank_first"
    INSERT_BLANK_LAST         = "insert_blank_last"
    ADD_BLANK_AFTER           = "add_blank_after"
    ADD_BLANK_AT              = "add_blank_at"
    EXTRACT_PAGES             = "extract_pages"
    EXTRACT_RANGE             = "extract_range"
    EXTRACT_EVENS             = "extract_evens"
    EXTRACT_ODDS              = "extract_odds"
    EXTRACT_EVEN_ODD_AND_SAVE = "extract_even_odd_and_save"
    REMOVE_FIRST_PAGE         = "remove_first_page"
    REMOVE_LAST_PAGE          = "remove_last_page"
    REMOVE_PAGES              = "remove_pages"

class PageSize:
    """
    PageSize class for managing standard paper sizes.
    This class provides access to common international paper sizes (ISO 216 A-series
    and C-series formats) and offers methods to retrieve specific paper dimensions.
    Attributes:
        A0 (tuple): ISO A0 paper size dimensions (width, height) in points.
        A1 (tuple): ISO A1 paper size dimensions (width, height) in points.
        A2 (tuple): ISO A2 paper size dimensions (width, height) in points.
        A3 (tuple): ISO A3 paper size dimensions (width, height) in points.
        A4 (tuple): ISO A4 paper size dimensions (width, height) in points.
        A5 (tuple): ISO A5 paper size dimensions (width, height) in points.
        A6 (tuple): ISO A6 paper size dimensions (width, height) in points.
        A7 (tuple): ISO A7 paper size dimensions (width, height) in points.
        A8 (tuple): ISO A8 paper size dimensions (width, height) in points.
        C4 (tuple): ISO C4 paper size dimensions (width, height) in points.
    Methods:
        set_to_default() -> tuple: Returns the default paper size (A4).
        set_to_A0() -> tuple: Returns A0 paper size dimensions.
        set_to_A1() -> tuple: Returns A1 paper size dimensions.
        set_to_A2() -> tuple: Returns A2 paper size dimensions.
        set_to_A3() -> tuple: Returns A3 paper size dimensions.
        set_to_A4() -> tuple: Returns A4 paper size dimensions.
        set_to_A5() -> tuple: Returns A5 paper size dimensions.
        set_to_A6() -> tuple: Returns A6 paper size dimensions.
        set_to_A7() -> tuple: Returns A7 paper size dimensions.
        set_to_A8() -> tuple: Returns A8 paper size dimensions.
        set_to_C4() -> tuple: Returns C4 paper size dimensions.
    """
    
    def __init__(self):
        getPaperSize = PaperSize()
        self.A0 = getPaperSize.A0
        self.A1 = getPaperSize.A1
        self.A2 = getPaperSize.A2
        self.A3 = getPaperSize.A3
        self.A4 = getPaperSize.A4
        self.A5 = getPaperSize.A5
        self.A6 = getPaperSize.A6
        self.A7 = getPaperSize.A7
        self.A8 = getPaperSize.A8
        self.C4 = getPaperSize.C4

    def set_to_default(self) -> tuple:
        return self.A4
    
    def set_to_A0(self) -> tuple:
        return self.A0

    def set_to_A1(self) -> tuple:
        return self.A1
    
    def set_to_A2(self) -> tuple:
        return self.A2
    
    def set_to_A3(self) -> tuple:
        return self.A3
    
    def set_to_A4(self) -> tuple:
        return self.A4
    
    def set_to_A5(self) -> tuple:
        return self.A5
    
    def set_to_A6(self) -> tuple:
        return self.A6

    def set_to_A7(self) -> tuple:
        return self.A7
    
    def set_to_A8(self) -> tuple:
        return self.A8
    
    def set_to_C4(self) -> tuple:
        return self.C4
    

class PdfPageManipulator:
    """Manipulate PDF documents: insert, extract, remove pages and save results.

    This class wraps PyPDF2 primitives to provide a small, opinionated API
    for common PDF page operations. It keeps an in-memory list of pages
    (``self.pages``) and a :class:`PdfWriter` instance (``self.writer``)
    used when writing changes back to disk.

    Notes about internal state:
      - ``self.full_path`` is the path used by :meth:`load_pdf` and :meth:`save`;
        by default the filename is prefixed with ``"new_"`` when constructed.
      - ``self.pages`` is a Python list of page objects (as returned by
        :class:`PdfReader`). Many operations replace ``self.pages`` atomically
        via :meth:`_op_update_pages_and_its_len` so callers can rely on
        ``self.page_length``.

    Public methods call :meth:`__dispatch_action`, which maps actions to small
    helper functions. The helpers perform the page-level work (list
    comprehensions, rebuilding a writer, writing files) while dispatch keeps
    the mapping readable and unit-testable.
    """
    # Default constructor 
    def __init__(self, pdf_name: str, path: str):
        """Initialize a new PDF manipulator instance.

        Args:
            pdf_name (str): Name of the PDF file to manipulate
            path (str): Directory path where the PDF file is located

        Important:
            - The constructor does not read the file from disk. Call
              `load_pdf()` to populate `self.pages`.
            - By default the internal `full_path` uses the string
              "new_" + pdf_name so saving operations won't overwrite the
              original file unless you intentionally set `self.full_path`.
        """
        
        # Pdf Name and Path 
        self.pdf_name : str         = pdf_name
        self.path : str             = path
        self.full_path : str        = os.path.join(path, pdf_name)
        self.save_path              = os.path.join(path, "new_" + pdf_name)
    
        # Pdf Pages Variables 
        self.pages : list           = []
        self.page_length            = 0
        self.original_pages : list  = []
        self.even_pages : list      = []
        self.odd_pages : list       = []
        self.last_method : str      = None
        self.writer                 = PdfWriter()



    # Public Methods
    # io methods -------------------------------------------------------------------
    def load_pdf(self):
        """Load the PDF pointed to by `self.full_path` and cache pages.

        This method reads the file using `PdfReader` and stores the pages in
        `self.pages`. It also copies the loaded pages into
        `self.original_pages` as a lightweight backup. After calling this the
        instance is ready for modification operations.

        Returns:
            self: the same instance (useful for chaining)

        Raises:
            FileNotFoundError: if the file path does not exist
            PyPDF2.errors.PdfReadError: if the file is not a valid PDF
        """
        
        reader                  = PdfReader(self.full_path)
        self.pages              = list(reader.pages)
        self.page_length        = len(self.pages)
        self.original_pages     = self.pages.copy()
        return self


    def get_page_length(self) -> int:
        """Return the current number of pages in the PDF.

        This method provides a convenient way to access the current page count
        after any modifications have been made. It simply returns the value of
        `self.page_length`, which is updated by all operations that modify
        `self.pages`.

        Returns:
            int: The current number of pages in the PDF.
        """
        
        return self.page_length

    def get_full_path(self) -> str:
        """Return the full path to the PDF file being manipulated.

        This method provides access to the internal `full_path` variable, which
        is used for loading and saving the PDF. It returns the current value of
        `self.full_path`, allowing callers to verify or use the path as needed.

        Returns:
            str: The full file path to the PDF document.
        """
        
        return self.full_path

    def get_save_path(self) -> str:
        """Return the full path where the modified PDF will be saved.

        This method provides access to the internal `save_path` variable, which
        is used when writing the modified PDF to disk. It returns the current
        value of `self.save_path`, allowing callers to verify or use the save
        path as needed.

        Returns:
            str: The full file path where the modified PDF will be saved.
        """
        
        return self.save_path


    def set_full_path(self, new_full_path: str) -> None:
        """
        Set the full path for the PDF file by combining the provided directory path with the PDF name.
        Args:
            new_full_path (str): The directory path where the PDF file is located. Must not be an empty string.
        Raises:
            ValueError: If new_full_path is an empty string.
        Returns:
            None
        """

        if new_full_path == "" :
            raise ValueError("new_full_path can't be an empty string")
        
        self.full_path = os.path.join(new_full_path, self.pdf_name)

    def set_save_path(self, new_save_path: str, pdf_name : str = "") -> None:
        """
        Set the save path for the PDF file.
        Args:
            new_save_path (str): The directory path where the PDF will be saved.
                                Cannot be an empty string.
            pdf_name (str, optional): The name of the PDF file to save. If not provided,
                                     defaults to "new_{original_pdf_name}". Defaults to "".
        Raises:
            ValueError: If new_save_path is an empty string.
        Returns:
            None
        """

        if new_save_path == "" :
            raise ValueError("new_save_path can't be an empty string")
        
        if pdf_name == "":
            self.save_path = os.path.join(new_save_path, f"new_{self.pdf_name}")
        else:
            self.save_path = os.path.join(new_save_path, f"{pdf_name}")


    # insert page methods  ---------------------------------------------------------
    def insert_blank_first(self, use_buffer: bool = True, page_size : PageSize = None) -> None:
        """
        Insert a blank page at the beginning of the PDF document.

        Args:
            use_buffer (bool, optional): Whether to use buffer for the operation. Defaults to True.
            page_size (PageSize, optional): The size of the blank page to insert. If None, uses the default page size. Defaults to None.

        Returns:
            None
        """
        
        index = 0
        if page_size is None:
            get_page_size = PageSize()
            page_size = get_page_size.set_to_default()
        self.__dispatch_action(PdfActions.INSERT_BLANK_FIRST, use_buffer, index=index, page_size = page_size), 

    def insert_blank_last(self, use_buffer: bool = True, page_size: PageSize = None) -> None:
        """
        Insert a blank page at the end of the PDF document.

        Args:
            use_buffer (bool, optional): Whether to use the buffer for this operation. Defaults to True.
            page_size (PageSize, optional): The size of the blank page to be inserted. If None, the default page size will be used. Defaults to None.

        Returns:
            None
        """
        
        index = self.page_length
        if page_size is None:
            get_page_size = PageSize()
            page_size = get_page_size.set_to_default()
        self.__dispatch_action(PdfActions.INSERT_BLANK_LAST, use_buffer, index=index, page_size=page_size)

    def add_blank_after(self, page_number: int, use_buffer: bool = True, page_size: PageSize = None) -> None:
        """
        Add a blank page after the specified page number.
        Args:
            page_number (int): The page number after which to insert a blank page.
            use_buffer (bool, optional): Whether to use buffer for the operation. Defaults to True.
            page_size (PageSize, optional): The size of the blank page to add. If None, uses the default page size. Defaults to None.
        Returns:
            None
        """
        
        index = page_number - 1

        if page_size is None:
            get_page_size = PageSize()
            page_size = get_page_size.set_to_default()
        self.__dispatch_action(PdfActions.ADD_BLANK_AFTER, use_buffer, index=index, page_size = page_size)
    
    def add_blank_at(self, use_buffer: bool = True, page_number: int = None, page_size: PageSize = None) -> None:
        """
        Add a blank page at the specified position in the PDF.

        Args:
            use_buffer (bool, optional): Whether to use the buffer for undo/redo functionality. Defaults to True.
            page_number (int, optional): The page number where the blank page should be inserted. If None, defaults to the end of the document.
                                          - Values <= 0 insert at the beginning
                                          - Values >= total pages insert at the end
                                          - Otherwise, inserts before the specified page number
            page_size (PageSize, optional): The size of the blank page to be added. If None, defaults to the default page size.

        Returns:
            None

        Raises:
            None
        """

        index = page_number - 1 

        if page_size is None:
            get_page_size = PageSize()
            page_size = get_page_size.set_to_default()
        self.__dispatch_action(PdfActions.ADD_BLANK_AT, use_buffer, index=index, page_size = page_size)



    # extract pages methods --------------------------------------------------------
    def extract_pages(self, use_buffer: bool = True, page_list: list[int] = None) -> None:
        """Extract a set of pages specified by `page_list` and replace `self.pages`.

        The method uses the dispatch system which filters the current
        `self.pages` via a list comprehension. Invalid indexes are ignored.

        Args:
            page_list (list[int]): sequence of zero-based page indexes to keep

        Raises:
            ValueError: if `page_list` is None (method expects an explicit list)
        """
        
        self.__dispatch_action(PdfActions.EXTRACT_PAGES, use_buffer, page_list = page_list)
     
    def extract_range(self, use_buffer: bool = True, page_list: list[int] = None) -> None:
        """Extract a continuous inclusive range of pages and replace `self.pages`.

        Args:
            page_list (list[int]): must contain two integers: [start, end]

        Behavior:
            - Extracts pages from `start` to `end` inclusive using Python slicing
            - Replaces `self.pages` with the extracted range and updates
              `self.page_length` via the dispatch machinery

        Raises:
            ValueError: if `page_list` is None or does not contain two elements
            IndexError: if `start`/`end` are out of bounds
        """
        
        from_page   = page_list[0]
        to_page     = page_list[1]
        self.__dispatch_action(PdfActions.EXTRACT_RANGE, use_buffer, from_page = from_page, to_page = to_page)

    def extract_evens(self, use_buffer: bool = True) -> None:
        """Extract all even-numbered pages from the PDF.
        
        Args:
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            
        Extracts pages 0, 2, 4, etc. The extracted pages are stored in
        self.even_pages and can be saved to a new file using save().
        
        Note:
            Page numbers are 0-based, so page 0 is considered even.
        """        
        
        self.__dispatch_action(PdfActions.EXTRACT_EVENS, use_buffer)

    def extract_odds(self, use_buffer: bool = True) -> None:
        """Extract all odd-numbered pages from the PDF.
        
        Args:
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            
        Extracts pages 1, 3, 5, etc. The extracted pages are stored in
        self.odd_pages and can be saved to a new file using save().
        
        Note:
            Page numbers are 0-based, so page 1 is the second page.
        """        
        
        self.__dispatch_action(PdfActions.EXTRACT_ODDS, use_buffer)

    def extract_even_odd_and_save(self, use_buffer: bool = True) -> None:
        """Separate pages into even/odd sets and write two files to disk.

        This operation writes two output files directly to disk and therefore
        does not replace `self.pages`. The filenames are constructed by
        prefixing the original filename with `even_pages_` and `odd_pages_`.

        Side effects:
            - Updates `self.even_pages` and `self.odd_pages`
            - Writes two files to `self.path`
        """
        
        self.__dispatch_action(PdfActions.EXTRACT_EVEN_ODD_AND_SAVE, use_buffer)



    # remove pages methods ----------------------------------------------------------
    def remove_first_page(self, use_buffer: bool = True) -> None:
        """
        Remove the first page from the PDF document.
        Args:
            use_buffer (bool, optional): If True, the action is added to the undo buffer,
                allowing it to be undone. If False, the action is performed directly without
                buffering. Defaults to True.
        Returns:
            None
        """
        
        self.__dispatch_action(PdfActions.REMOVE_FIRST_PAGE, use_buffer)

    def remove_last_page(self, use_buffer: bool = True) -> None:
        """Remove the last page from the PDF.
        
        Args:
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            
        The final page will be removed. All other pages remain unchanged.
        """        
        
        self.__dispatch_action(PdfActions.REMOVE_LAST_PAGE, use_buffer)

    def remove_pages(self, page_list: list[int] = None, use_buffer: bool = True) -> None:
        """Remove multiple pages from the PDF by their page numbers.
        
        Args:
            page_list (list[int]): List of page numbers to remove
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            
        Uses list comprehension to create a new page list excluding the specified
        page numbers. Pages are removed in a single operation, and the remaining
        pages are reindexed automatically.
        
        Example:
            >>> pdf.remove_pages([1, 3, 5])  # Removes pages 1, 3, and 5
        
        Note:
            - Page numbers are 0-based (first page is 0, second is 1, etc.)
            - Pages can be removed in any order
            - Updates self.pages and self.page_length automatically
            
        Raises:
            ValueError: If page_list is None (the method expects an explicit list)
        """
        
        if page_list == None:
            raise ValueError("page_list cant' be a None, plase pass correct page_list. ex: [0, 11, 12, 99]")
        
        self.__dispatch_action(PdfActions.REMOVE_PAGES, use_buffer, page_list = page_list)
         

    # save pdfs methods ----------------------------------------------------------
    def save(self, save_original = False, prefix_name: str = ""):
        """
        Save the PDF document to disk with optional modifications.
        Args:
            save_original (bool, optional): If True, saves the original PDF without modifications. 
                Defaults to False.
            prefix_name (str, optional): A prefix to add to the output filename. If provided, 
                the file will be saved with a new path using this prefix. Defaults to "".
        Returns:
            None
        Raises:
            IOError: If the file cannot be written to the specified path.
        Notes:
            - Prepares the writer object before adding pages.
            - If prefix_name is provided, generates a new save path with the given prefix.
            - Writes the PDF to disk at self.save_path.
        """

        # Prepare self.writer for original page
        self._prepare_writer()

        # Prepare self.writer and add pages 
        for  page in self.pages:
            self.writer.add_page(page)
        
        if prefix_name != "":
            self.save_path = self._get_new_fullpath(prefix=prefix_name)
        
        # Writing Edited  Pdf to disk
        with open(self.save_path, "wb") as output_file:
            self.writer.write(output_file) 
    
    def _save_original(self, prefix_name: str = ""):
        """
        Save the original PDF to disk with an optional prefix to the filename.
        This method prepares a writer object, optionally generates a new file path
        based on the provided prefix, adds all original pages to the writer, and
        writes the PDF to disk.
        Args:
            prefix_name (str, optional): A prefix to add to the original filename.
                If an empty string (default), the original filepath is used.
                Otherwise, a new filepath is generated with the prefix applied.
        Returns:
            None
        Raises:
            IOError: If the file cannot be written to disk.
        """
        
        # Prepare self.writer for original page
        self._prepare_writer()

        # Get full_path 
        full_path = self.full_path

        # Check User request for new name 
        if prefix_name != "":
            full_path = self._get_new_fullpath(prefix=prefix_name)
        
        # Preapre Original PDF for writing to disk
        for page in self.original_pages:
            self.writer.add_page(page)
    
        # Wriring Original Pdf to disk
        with open(full_path, "wb") as output:
            self.writer.write(output)


    # Private Methods
    def __dispatch_action(self, action: PdfActions, use_buffer: bool, **kw_args) -> None:
        """
        Dispatches and executes a PDF action operation based on the specified action type.
        This method serves as a central router for various PDF page manipulation operations.
        It maps each action to a lightweight lambda function that calls the appropriate helper
        method, executes the operation, and updates the internal state if necessary.
        Args:
            action (PdfActions): The PDF action to be executed. Must be a valid PdfActions enum member.
            use_buffer (bool): Indicates whether to use buffering for the operation (currently unused in routing).
            **kw_args: Variable keyword arguments passed to the operation helpers. Expected keys vary by action:
                - For INSERT_BLANK_FIRST, INSERT_BLANK_LAST, ADD_BLANK_AFTER, ADD_BLANK_AT:
                    - index (int): The position where the blank page should be inserted.
                    - page_size (tuple): The size of the blank page to add.
                - For EXTRACT_PAGES: page_list (list): List of pages to extract.
                - For EXTRACT_RANGE: from_page (int), to_page (int): Range boundaries for extraction.
                - For REMOVE_PAGES: page_list (list): List of page indices to remove.
        Raises:
            ValueError: If the provided action is not a recognized PdfActions member.
        Side Effects:
            - Updates self.pages with the result of the operation (except for EXTRACT_EVEN_ODD_AND_SAVE).
            - Updates self.page_length to reflect the new number of pages.
            - Sets self.last_method to the current action for tracking purposes.
        Note:
            EXTRACT_EVEN_ODD_AND_SAVE is handled specially and does not update the internal pages state.
        """
        
        # Map each action to a lightweight lambda that calls the appropriate helper
        operations = {
            PdfActions.INSERT_BLANK_FIRST         : lambda : self._op_insert_at(kw_args["index"], PdfActions.INSERT_BLANK_FIRST, page_size = kw_args["page_size"]),
            PdfActions.INSERT_BLANK_LAST          : lambda : self._op_insert_at(kw_args["index"], PdfActions.INSERT_BLANK_LAST, page_size = kw_args["page_size"]),
            PdfActions.ADD_BLANK_AFTER            : lambda : self._op_insert_at(kw_args["index"], PdfActions.ADD_BLANK_AFTER, page_size = kw_args["page_size"]),
            PdfActions.ADD_BLANK_AT               : lambda : self._op_insert_at(kw_args["index"], PdfActions.ADD_BLANK_AT, page_size = kw_args["page_size"]),
            PdfActions.EXTRACT_PAGES              : lambda : [result for i, result in enumerate(self.pages) if i in kw_args["page_list"]] ,
            PdfActions.EXTRACT_RANGE              : lambda : self.pages[kw_args["from_page"]: kw_args["to_page"] + 1],
            PdfActions.EXTRACT_EVENS              : lambda : [result for i, result in enumerate(self.pages) if i % 2 != 0], # Note: 0-based indexing means even pages are at odd indices
            PdfActions.EXTRACT_ODDS               : lambda : [result for i, result in enumerate(self.pages) if i % 2 == 0], # Note: 0-based indexing means odd pages are at even indices
            PdfActions.EXTRACT_EVEN_ODD_AND_SAVE  : lambda : self._op_even_odd_and_save(),
            PdfActions.REMOVE_FIRST_PAGE          : lambda : self.pages[1:],
            PdfActions.REMOVE_LAST_PAGE           : lambda : self.pages[:-1],
            PdfActions.REMOVE_PAGES               : lambda : [result for i, result in enumerate(self.pages) if i not in kw_args["page_list"]],
        }

        if action not in operations:
            raise ValueError(f"Unknown action: {action}")
        
        # Handle the special case for EXTRACT_EVEN_ODD_AND_SAVE which does not update self.pages
        if action == PdfActions.EXTRACT_EVEN_ODD_AND_SAVE:
            operations[action]()


        # Run Operation and update state (self.pages and self.page_length)
        if action != PdfActions.EXTRACT_EVEN_ODD_AND_SAVE : 
            self._op_update_pages_and_its_len( operations[action]() )
        

        self.last_method = action

    def _op_update_pages_and_its_len(self, new_pages: list) -> None:
        """Update the page list and length after an operation.
        
        Args:
            new_pages (list): New list of pages to store
            
        Updates both self.pages and self.page_length to maintain consistency
        after operations that modify the page collection.
        
        This is called automatically by __dispatch_action after each operation
        to ensure the page count stays synchronized with the actual pages.
        """
        
        self.pages = new_pages
        self.page_length = len(self.pages)

    def _op_insert_at(self, index: int, op_name: PdfActions = None, **kw_args) -> list:
        """
        Insert blank pages at specified positions in the PDF document.
        This method modifies the internal PdfWriter by adding blank pages at various
        positions based on the operation type specified. The document is reconstructed
        with the blank page(s) inserted at the requested location(s).
        Args:
            index (int): The position index where the blank page(s) should be inserted.
                        Must be between 0 and the current page length (inclusive).
                        Used for ADD_BLANK_AT and ADD_BLANK_AFTER operations.
            op_name (PdfActions, optional): The operation type that determines where and how
                                           blank pages are inserted. Supported values:
                                           - PdfActions.ADD_BLANK_AT: Insert blank page at the specified index
                                           - PdfActions.INSERT_BLANK_FIRST: Insert blank page at the beginning
                                           - PdfActions.INSERT_BLANK_LAST: Insert blank page at the end
                                           - PdfActions.ADD_BLANK_AFTER: Insert blank page after the specified index
            **kw_args: Arbitrary keyword arguments. Expected to contain:
                       - page_size: Object with 'width' and 'height' attributes for the blank page dimensions
        Returns:
            list: A list of pages from the updated PdfWriter object after the blank page(s) have been inserted.
        Raises:
            ValueError: If the index is out of valid range (less than 0 or greater than current page length).
        """

        if index > self.page_length or index < 0:
            raise ValueError(f"Index should be between 0 and {self.page_length}")

        # Prepare writer - rebuild a fresh PdfWriter that we will populate
        self.writer = PdfWriter()

        # Set Page Size
        page_width = kw_args["page_size"].width;
        page_height = kw_args["page_size"].height;

        # Add a blank page by index (insert at `index`)
        if op_name == PdfActions.ADD_BLANK_AT:
            for i in range(self.page_length):
                if i == index:
                    self.writer.add_blank_page(page_width, page_height)
                    self.writer.add_page(self.pages[i])
                else:
                    self.writer.add_page(self.pages[i])

        # Add a blank page at the first
        elif op_name == PdfActions.INSERT_BLANK_FIRST:
            self.writer.add_blank_page(page_width, page_height)
            for page in self.pages:
                self.writer.add_page(page)

        # Add a blank page at the last page
        elif op_name == PdfActions.INSERT_BLANK_LAST:
            for page in self.pages:
                self.writer.add_page(page)
            self.writer.add_blank_page(page_width, page_height)

        # Add a blank page after a page index
        elif op_name == PdfActions.ADD_BLANK_AFTER:
            for i in range(self.page_length):
                if i == index:
                    self.writer.add_page(self.pages[i])
                    self.writer.add_blank_page(page_width, page_height)
                else:
                    self.writer.add_page(self.pages[i])

        # Return a concrete list of pages for the dispatcher to store
        return list(self.writer.pages)


    
    def _op_even_odd_and_save(self) -> None:
        """Separate pages into even and odd sets and write them to disk.

        Side effects:
            - Populates ``self.even_pages`` and ``self.odd_pages``
            - Writes two files to disk at paths constructed from ``self.path``
              and ``self.pdf_name`` (prefixes "even_pages_" and "odd_pages_")

        Returns:
            None
        """
        
        # Implementation will go here
        evens_writer, odds_writer   = PdfWriter() , PdfWriter()

        # Extract Evens Pages
        self.even_pages = [result for i, result in enumerate(self.pages) if i % 2 != 0] # Note: 0-based indexing means even pages are at odd indices
        
        # Extract Odd Pages
        self.odd_pages = [result for i, result in enumerate(self.pages) if i %  2 == 0] # Note: 0-based indexing means odd pages are at even indices

        # Prepare Evens and Odds Pages for Writing on the disk
        for page in self.even_pages :
            evens_writer.add_page(page)
        
        for page in self.odd_pages :
            odds_writer.add_page(page)

        # Create Even and Odd Paths
        even_fullpath = self._get_new_fullpath(prefix="evens_pages")
        odd_fullpath  = self._get_new_fullpath(prefix="odds_pages")

        # Write evens and odds pages on the disk
        with open(even_fullpath, "wb") as evens_output, open(odd_fullpath, "wb") as odds_output:
            evens_writer.write(evens_output)
            odds_writer.write(odds_output)

        
    def _prepare_writer(self):
        """
        Initialize and prepare a PdfWriter instance for PDF manipulation.
        
        Creates a new PdfWriter object and assigns it to the instance variable.
        This method should be called before performing any write operations on PDF files.
        """
        self.writer = None
        self.writer = PdfWriter()

    def _get_new_fullpath(self, new_path: str = "", prefix: str = "") -> str:
        """
        Generate a new file path with a prefix added to the PDF filename.
        Args:
            new_path (str, optional): The directory path where the new file should be located.
                If empty, uses the original PDF's directory. Defaults to "".
            prefix (str, optional): A prefix to add to the PDF filename. Cannot be empty.
                Defaults to "".
        Returns:
            str: The full path to the new file with the prefix prepended to the filename.
        Raises:
            KeyError: If prefix is None or an empty string.
        Examples:
            >>> manipulator._get_new_fullpath(new_path="/output", prefix="processed")
            "/output/processed_document.pdf"
            >>> manipulator._get_new_fullpath(prefix="backup")
            "/home/mintblack/Desktop/Projects/.../backup_document.pdf"
        """
        if prefix == "":
            raise KeyError("prefix could be None or an empty Str: {prefix}")
        
        if new_path != "":
            return os.path.join(new_path, f"{prefix}_{self.pdf_name}")
        else:
            return os.path.join(self.path, f"{prefix}_{self.pdf_name}")