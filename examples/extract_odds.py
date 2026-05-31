from pdf_page_manipulator import PdfPageManipulator

def main():
    manipulator = PdfPageManipulator("PPMTest.pdf", "./")
    manipulator.load_pdf()
    manipulator.extract_odds()
    manipulator.save(prefix_name="ExteractOdds.test")

if __name__ == "__main__":
    main()
