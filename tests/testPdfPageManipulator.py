import unittest

# Todo: check this part
from PdfPageManipulator_vheidari import PdfPageManipulator

def testPdfPageManipulator():
     pass


if __name__ == "main" :
     # Todo : Check this part
     test = PdfPageManipulator("PPMTest.pdf", "./")
     test.load_pdf()
     unittest.main()