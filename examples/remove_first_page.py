from pdf_page_manipulator import PdfPageManipulator

def main():
    manipulator = PdfPageManipulator("PPMTest.pdf", "./")
    manipulator.load_pdf()
    manipulator.remove_first_page()
    manipulator.save(prefix_name="RemoveFirstPage.test")

if __name__ == "__main__":
    main()
