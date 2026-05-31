#!/bin/bash

# copyright (c) 2024-2025. All rights reserved.
# Author: 
#    Vahid Heidari
# Date: 
#    2024-06-01
# Discription:
#    This script is used to run the example scripts in the examples directory after setting up the virtual environment
#    and installing the required dependencies using the install.sh script. It activates the virtual
#    environment named "ppm_env" and then executes each of the example scripts sequentially. This allows you to
#    test the functionality of the PdfPageManipulator library and see how it works with different PDF
#    manipulation tasks such as inserting blank pages, extracting pages, and removing pages from PDF files.



ENVNAME=ppm_env

echo "✅ Activate ${ENVNAME} virtual environment ..."
source ./${ENVNAME}/bin/activate

echo "✅ Running example scripts ..."
echo "-------------------------------"

echo "✅ Insert a blank page at the beginning of a PDF file ..."
python3 ./insert_blank_first.py

echo "✅ Insert a blank page at the end of a PDF file ..."
python3 ./insert_blank_last.py

echo "✅ Insert a blank page after the 2nd page of a PDF file ..."
python3 ./add_blank_after.py

echo "✅ insert a blank page at spacific page numbers of a PDF file ..."
python3 ./add_blank_at.py

echo "✅ Extract list of page numbers from a PDF file ..."
python3 ./extract_pages.py

echo "✅ Extract a range of pages from a PDF file ..."
python3 ./extract_range.py

echo "✅ Extract even page numbers from a PDF file ..."
python3 ./extract_evens.py

echo "✅ Extract odd page numbers from a PDF file ..."
python3 ./extract_odds.py

echo "✅ Remove the first page of a PDF file ..."
python3 ./remove_first_page.py

echo "✅ Remove the last page of a PDF file ..."
python3 ./remove_last_page.py

echo "-------------------------------"

echo "🥳 Done. :)"