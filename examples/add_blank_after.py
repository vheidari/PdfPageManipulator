from pdf_page_manipulator import PdfPageManipulator

def main():
    manipulator = PdfPageManipulator("PPMTest.pdf", "./")
    manipulator.load_pdf()
    manipulator.add_blank_after(page_number=20)
    manipulator.save(prefix_name="AddBlankAfter.test")

if __name__ == "__main__":
    main()
