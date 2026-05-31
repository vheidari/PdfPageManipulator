from pdf_page_manipulator import PdfPageManipulator

def main():
    manipulator = PdfPageManipulator("PPMTest.pdf", "./")
    manipulator.load_pdf()
    manipulator.extract_pages(page_list=[10,12,1,5,15])
    manipulator.save("ExtractPages.test")

if __name__ == "__main__":
    main()
