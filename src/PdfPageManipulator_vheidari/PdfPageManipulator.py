# Import stdlib libraries 
import os 
from enum import Enum

# Import  third-party libraries
from PyPDF2 import PdfReader , PdfWriter


# Todo: compelete list of Actions 
class PdfActions(Enum):
    INSERT_FIRST    = "inser_first"
    INSERT_LAST     = "inser_last"
    ADD_AFTER_PAGE  = "add_after_page"
    ADD_BLANK =""
    

    #....

    

# We will going to adding  add page also to this. these  feature help us to create a pdf from multiple file



class PdfPageManipulator:
    # Default constructor 
    def __init__(self, pdf_name : str, path : str):

        # Pdf Name and Path 
        self.pdf_name : str         = pdf_name
        self.path : str             = path
        self.full_path : str = os.path.join(path, pdf_name)
    
        # Pdf Pages Variables 
        self.pages : list           = []
        self.original_pages : list  = []
        self.even_pages : list      = []
        self.odd_pages : list       = []
        self.last_method : str      = None
        self.writer = PdfWriter()



    # Public Methods
    # io methods -------------------------------------------------------------------
    def load_pdf(self):
        reader                  = PdfReader(self.full_path)
        self.pages              = list(reader.pages)
        self.original_pages     = self.pages.copy()
        return self


    # insert page methods  ---------------------------------------------------------
    def insert_first(self, use_buffer: bool = True) -> None:
        self.__dispatch_action("inser_first", use_buffer)

    def insert_last(self, use_buffer : bool = True) -> None:
        self.__dispatch_action("inser_last", use_buffer)

    def add_after_page(self, page_number : int, use_buffer : bool = True) -> None:
        self.__dispatch_action("add_fter_page", use_buffer, page_number)
    
    def add_blank(self, use_buffer : bool = True, after_page : int = None) -> None:
        self.__dispatch_action("add_blank", use_buffer, after_page)



    # extract pages methods --------------------------------------------------------
    def extract_pages(self, use_buffer : bool = True, page_list : list[int] = None) -> None:
        self.__dispatch_action("extract_pages", use_buffer, page_list)
     
    def extract_range(self, use_buffer : bool = True, page_list : list[int] = None ) -> None:
        self.__dispatch_action("extract_range", use_buffer, page_list)

    def extract_evens(self, use_buffer : bool = True) -> None:
        self.__dispatch_action("extract_evens", use_buffer)

    def extract_odds(self, use_buffer : bool = True) -> None:
        self.__dispatch_action("extract_odds", use_buffer)

    def extract_even_odd_and_save(self, use_buffer : bool = True) -> None:
        self.__dispatch_action("extract_even_and_odds", use_buffer)

    # remove pages methods ----------------------------------------------------------
    def remove_first_page(self, use_buffer : bool = True) -> None:
        self.__dispatch_action("remove_first_page", use_buffer)

    def remove_last_page(self, use_buffer : bool = True) -> None:
        self.__dispatch_action("remove_last_page", use_buffer)

    def remove_pages(self, page_number, use_buffer : bool = True) -> None:
        self.__dispatch_action("remove_pages", use_buffer)
         




    # Private Methods
    def __dispatch_action(self, action, use_buffer: bool, **kw_args):
        operations = {
            "remove_first" : lambda : self.pages[1:],
            "remove_last"  : lambda : self.pages[:-1],

        }