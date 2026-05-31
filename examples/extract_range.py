from pdf_page_manipulator import PdfPageManipulator

def main():
    manipulator = PdfPageManipulator("PPMTest.pdf", "./")
    manipulator.load_pdf()
    manipulator.extract_range(page_list=[5,10])
    manipulator.save(prefix_name="ExteractRange.test")

if __name__ == "__main__":
    main()
