#!/bin/bash

# copyright (c) 2024-2025. All rights reserved.
# Author: 
#    Vahid Heidari
# Date: 
#    2024-06-01
# Discription:
#    This script is used to clean up the generated PDF files in the examples directory after running 
#    the example scripts. It removes all PDF files that have been generated with the suffix "_PPMTest.pdf".
#    This helps to keep the examples directory clean and organized after testing the functionality 
#    of the PdfPageManipulator library.

echo "✅ Cleaning up generated PDF files ..."
rm ./*_PPMTest.pdf
echo "🥳 Done. :)"
