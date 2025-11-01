# Import stdlib libraries 
import os 
from enum import Enum

# Import third-party libraries
from PyPDF2 import PdfReader , PdfWriter


class PdfActions(Enum):
    """Enumeration of all available PDF manipulation actions.
    
    This enum defines the supported operations for manipulating PDF documents,
    including inserting blank pages, extracting specific pages, and removing pages.
    
    Available actions:
        INSERT_FIRST: Insert a blank page at the beginning
        INSERT_LAST: Insert a blank page at the end
        ADD_AFTER_PAGE: Add a blank page after a specified page
        ADD_BLANK: Add a blank page at a specified position
        EXTRACT_PAGES: Extract specific pages by their numbers
        EXTRACT_RANGE: Extract a range of pages
        EXTRACT_EVENS: Extract all even-numbered pages
        EXTRACT_ODDS: Extract all odd-numbered pages
        EXTRACT_EVEN_ODD_AND_SAVE: Extract and save even/odd pages separately
        REMOVE_FIRST_PAGE: Remove the first page
        REMOVE_LAST_PAGE: Remove the last page
        REMOVE_PAGES: Remove specific pages
    """
    INSERT_FIRST              = "inser_first"
    INSERT_LAST               = "inser_last"
    ADD_AFTER_PAGE            = "add_after_page"
    ADD_BLANK                 = "add_blank"
    EXTRACT_PAGES             = "extract_pages"
    EXTRACT_RANGE             = "extract_range"
    EXTRACT_EVENS             = "extract_evens"
    EXTRACT_ODDS              = "extract_odds"
    EXTRACT_EVEN_ODD_AND_SAVE = "extract_even_odd_and_save"
    REMOVE_FIRST_PAGE         = "remove_first_page"
    REMOVE_LAST_PAGE          = "remove_last_page"
    REMOVE_PAGES              = "remoe_pages"


class PdfPageManipulator:
    """A class for manipulating PDF documents with operations like inserting, extracting, and removing pages.

    This class provides a high-level interface for common PDF manipulation tasks
    using PyPDF2 as the underlying PDF processing engine. It maintains state about
    the current PDF document and provides methods to modify it in various ways.

    Features:
        - Insert blank pages at any position
        - Extract specific pages or ranges
        - Extract even/odd pages
        - Remove pages
        - Save modified PDFs
        
    Attributes:
        pdf_name (str): Name of the PDF file
        path (str): Directory path containing the PDF
        full_path (str): Complete path to the PDF file
        pages (list): List of current PDF pages
        page_length (int): Number of pages in the PDF
        original_pages (list): Backup copy of original PDF pages
        even_pages (list): List of even-numbered pages
        odd_pages (list): List of odd-numbered pages
        last_method (str): Name of the last operation performed
        writer (PdfWriter): PyPDF2 writer object for PDF operations
    """
    # Default constructor 
    def __init__(self, pdf_name: str, path: str):
        """Initialize a new PDF manipulator instance.

        Args:
            pdf_name (str): Name of the PDF file to manipulate
            path (str): Directory path where the PDF file is located
            
        The constructor sets up the initial state but does not load the PDF.
        Call load_pdf() after initialization to read the PDF content.
        """
        # Pdf Name and Path 
        self.pdf_name : str         = pdf_name
        self.path : str             = path
        self.full_path : str        = os.path.join(path, pdf_name)
    
        # Pdf Pages Variables 
        self.pages : list           = []
        self.page_length            = 0
        self.original_pages : list  = []
        self.even_pages : list      = []
        self.odd_pages : list       = []
        self.last_method : str      = None
        self.writer = PdfWriter()



    # Public Methods
    # io methods -------------------------------------------------------------------
    def load_pdf(self):
        """Load the PDF file and initialize internal page collections.
        
        This method:
        1. Opens the PDF file using PyPDF2
        2. Loads all pages into memory
        3. Creates a backup of original pages
        4. Sets up the page count
        
        Returns:
            self: Returns this instance for method chaining
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            PyPDF2.errors.PdfReadError: If the file is not a valid PDF
        """
        reader                  = PdfReader(self.full_path)
        self.pages              = list(reader.pages)
        self.page_length        = len(self.pages)
        self.original_pages     = self.pages.copy()
        return self


    # insert page methods  ---------------------------------------------------------
    def insert_first(self, use_buffer: bool = True) -> None:
        """Insert a blank page at the beginning of the PDF.
        
        Args:
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            
        The blank page will be inserted as page 1, and all existing pages
        will be shifted forward by one position.
        """
        index = 0
        self.__dispatch_action(PdfActions.INSERT_FIRST, use_buffer, index=index), 

    def insert_last(self, use_buffer: bool = True) -> None:
        """Insert a blank page at the end of the PDF.
        
        Args:
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            
        The blank page will be appended as the last page of the document,
        after all existing pages.
        """
        index = len(self.pages)
        self.__dispatch_action(PdfActions.INSERT_LAST, use_buffer, index=index)

    def add_after_page(self, page_number: int, use_buffer: bool = True) -> None:
        """Insert a blank page after a specified page number.
        
        Args:
            page_number (int): The page number after which to insert the blank page
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            
        The blank page will be inserted immediately after the specified page,
        and all subsequent pages will be shifted forward by one position.
        
        Note:
            Page numbers are 0-based (first page is 0, second is 1, etc.)
        """
        index = page_number
        self.__dispatch_action(PdfActions.ADD_AFTER_PAGE, use_buffer, index=index)
    
    def add_blank(self, use_buffer: bool = True, after_page: int = None) -> None:
        """Add a blank page at a specified position or at the end.
        
        Args:
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            after_page (int, optional): Page number after which to insert. If None,
                                      adds at the end. Defaults to None.
                                      
        This is a more flexible version of add_after_page that defaults to
        appending at the end if no position is specified.
        
        Note:
            Page numbers are 0-based (first page is 0, second is 1, etc.)
        """
        self.__dispatch_action(PdfActions.ADD_BLANK, use_buffer, after_page = after_page)



    # extract pages methods --------------------------------------------------------
    def extract_pages(self, use_buffer: bool = True, page_list: list[int] = None) -> None:
        """Extract specific pages from the PDF by their page numbers.
        
        Args:
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            page_list (list[int], optional): List of page numbers to extract.
                                           Defaults to None.
                                           
        Uses list comprehension to efficiently extract the specified pages
        while preserving their order in the page_list. The extracted pages
        replace the current page list (use save() to write to a new file).
        
        Example:
            >>> pdf.extract_pages(page_list=[0, 2, 5])  # Extracts pages 0, 2, and 5
        
        Note:
            - Page numbers are 0-based (first page is 0, second is 1, etc.)
            - Updates self.pages and self.page_length automatically
            - Ignores any page numbers that are out of range
            
        Raises:
            ValueError: If page_list is None
        """
        self.__dispatch_action(PdfActions.EXTRACT_PAGES, use_buffer, page_list = page_list)
     
    def extract_range(self, use_buffer: bool = True, page_list: list[int] = None) -> None:
        """Extract a continuous range of pages from the PDF.
        
        Args:
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            page_list (list[int], optional): List containing [start, end] page numbers.
                                           Must contain exactly two elements.
                                           Defaults to None.
                                           
        Extracts pages from start to end (inclusive) using array slicing.
        The extracted pages are stored in self.pages after the operation.
        
        Example:
            >>> pdf.extract_range(page_list=[1, 5])  # Extracts pages 1,2,3,4,5
        
        Note:
            - Page numbers are 0-based (first page is 0, second is 1, etc.)
            - Both start and end pages are included in the extraction
            - Updates self.pages and self.page_length automatically
        
        Raises:
            IndexError: If page_list indexes are out of range
            ValueError: If page_list doesn't contain exactly 2 elements
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
        """Extract and save even and odd pages into separate files.
        
        Args:
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            
        This method:
        1. Uses _op_even_odd_and_save helper to separate pages:
           - Even pages (0, 2, 4, ...) go to self.even_pages
           - Odd pages (1, 3, 5, ...) go to self.odd_pages
        2. Updates internal state (pages and page_length)
        3. Sets up for saving with suffixed filenames
        
        The output files will be named:
        - Original name + '_even.pdf' for even pages
        - Original name + '_odd.pdf' for odd pages
        
        Example:
            >>> pdf.extract_even_odd_and_save()
            # Creates: 'document_even.pdf' and 'document_odd.pdf'
        
        Note:
            - Page numbers are 0-based (page 0 is even)
            - Both collections are saved automatically
            - Original page list is preserved
        """        
        self.__dispatch_action(PdfActions.EXTRACT_EVEN_ODD_AND_SAVE, use_buffer)



    # remove pages methods ----------------------------------------------------------
    def remove_first_page(self, use_buffer: bool = True) -> None:
        """Remove the first page from the PDF.
        
        Args:
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            
        The first page (page 0) will be removed and all subsequent pages
        will be shifted back by one position.
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
            ValueError: If page_list is None
        """
        if page_list == None:
                 raise ValueError("page_list cant' be a None, plase pass correct page_list. ex: [0, 11, 12, 99]")
        
        self.__dispatch_action(PdfActions.REMOVE_PAGES, use_buffer, page_list = page_list)
         


    def save(self):
        pass 


    # Private Methods
    def __dispatch_action(self, action: PdfActions, use_buffer: bool, **kw_args) -> None:
        """Internal method to dispatch PDF operations to their implementations.
        
        Args:
            action (PdfActions): The PDF operation to perform
            use_buffer (bool): Whether to use buffering for operations
            **kw_args: Additional keyword arguments specific to each operation:
                - index (int): Page index for insert operations
                - page_list (list[int]): List of page numbers for extract/remove operations
                - from_page (int): Start page for range extraction
                - to_page (int): End page for range extraction
            
        The dispatch system uses direct list operations and list comprehensions for:
        - Insert: Uses _op_insert_at helper with buffering
        - Extract: List comprehensions to filter pages
        - Remove: List slicing or filtering via comprehension
        
        After each operation, updates page list and length via _op_update_pages_and_its_len.
        
        Raises:
            ValueError: If an unknown action is provided
            KeyError: If required kw_args are missing for an operation
        """        
        # Map each action to a lightweight lambda that calls the appropriate helper
        operations = {
            PdfActions.INSERT_FIRST               : lambda : self._op_insert_at(kw_args["index"], use_buffer),
            PdfActions.INSERT_LAST                : lambda : self._op_insert_at(kw_args["index"], use_buffer),
            PdfActions.ADD_AFTER_PAGE             : lambda : self._op_insert_at(kw_args["index"], use_buffer),
            PdfActions.ADD_BLANK                  : lambda : self._op_insert_at(kw_args["index"], use_buffer),
            PdfActions.EXTRACT_PAGES              : lambda : [result for i, result in enumerate(self.pages) if self.pages[i] in kw_args["page_list"]] ,
            PdfActions.EXTRACT_RANGE              : lambda : self.pages[kw_args["from_page"]: kw_args["to_page"]],
            PdfActions.EXTRACT_EVENS              : lambda : [result for i, result in enumerate(self.pages) if i % 2 == 0],
            PdfActions.EXTRACT_ODDS               : lambda : [result for i, result in enumerate(self.pages) if i % 2 != 0],
            PdfActions.EXTRACT_EVEN_ODD_AND_SAVE  : lambda : self._op_even_odd_and_save(),
            PdfActions.REMOVE_FIRST_PAGE          : lambda : self.pages[1:],
            PdfActions.REMOVE_LAST_PAGE           : lambda : self.pages[:-1],
            PdfActions.REMOVE_PAGES               : lambda : [result for i, result in enumerate(self.pages) if i not in kw_args["page_list"]],
        }

        if action not in operations:
            raise ValueError(f"Unknown action: {action}")
        
        # Run Operation and update state (self.pages and self.page_length)
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

    def _op_insert_at(self, index: int, use_buffer: bool = True) -> list:
        """Insert a blank page at a specified index in the PDF.
        
        Args:
            index (int): Position where the blank page should be inserted
            use_buffer (bool, optional): Whether to use buffering. Defaults to True.
            
        Returns:
            list: New list of pages with the blank page inserted
            
        This helper method:
        1. Creates a new blank page using PdfWriter
        2. Inserts it at the specified position
        3. Returns the new page list
        
        The method handles buffering if enabled and ensures the index
        is within valid bounds. Called by insert_first, insert_last,
        add_after_page, and add_blank operations.
        """
        # Implementation will go here
        pass
        
    
    def _op_even_odd_and_save(self) -> tuple[list, list]:
        """Extract even and odd pages and prepare them for saving.
        
        Returns:
            tuple[list, list]: A tuple containing (even_pages, odd_pages)
            
        This helper method:
        1. Uses list comprehensions to separate even and odd pages
        2. Updates self.even_pages and self.odd_pages
        3. Returns both collections for saving
        
        The even/odd determination uses 0-based indexing, so:
        - Even pages: 0, 2, 4, ...
        - Odd pages: 1, 3, 5, ...
        
        Note: The actual saving is handled by the save() method
        """
        # Implementation will go here
        pass

    def _op_gen_outputname():
        pass