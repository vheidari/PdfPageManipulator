from pdf_page_manipulator import PdfPageManipulator

def main():
    manipulator = PdfPageManipulator("PPMTest.pdf", "./")
    manipulator.load_pdf()
    manipulator.extract_evens()
    manipulator.save(prefix_name="ExtractEven.test")

if __name__ == "__main__":
    main()
