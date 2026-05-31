from pdf_page_manipulator import PdfPageManipulator

def main():
    manipulator = PdfPageManipulator("PPMTest.pdf", "./")
    manipulator.load_pdf()
    manipulator.insert_blank_last()
    manipulator.save(prefix_name="InserBlankLast.test")

if __name__ == "__main__":
    main()
