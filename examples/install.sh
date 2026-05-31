#!/bin/bash

# copyright (c) 2024-2025. All rights reserved.
# Author: 
#    Vahid Heidari
# Date: 
#    2024-06-01
# Discription:
#    This script is used to prepare the virtual environment and install the required dependencies 
#    for running the example scripts in the examples directory. It creates a virtual environment 
#    named "ppm_env", activates it, and then installs the PyPDF2 library and the PdfPageModifier 
#    library from the local directory. This setup allows you to run the example scripts without 
#    affecting your global Python environment.


ENVNAME=ppm_env

echo "✅ Prepare ${ENVNAME} virtual environment ..."
python3 -m venv ${ENVNAME}

echo "✅ Activate ${ENVNAME} virtual environment ..."
source "./ppm_env/bin/activate"

echo "✅ Install PyPDF2 and PdfPageModifier ..."
python3 -m pip install --upgrade PyPDF2

echo "✅ Install PdfPageModifier from local directory ..."
python3 -m pip install --upgrade ../

echo "🥳 Done. :)"
