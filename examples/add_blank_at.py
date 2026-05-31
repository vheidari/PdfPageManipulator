from pdf_page_manipulator import PdfPageManipulator

def main():
    manipulator = PdfPageManipulator("PPMTest.pdf", "./")
    manipulator.load_pdf()
    manipulator.add_blank_at(page_number=7)
    manipulator.save(prefix_name="AddBlankAt.test")

if __name__ == "__main__":
    main()
