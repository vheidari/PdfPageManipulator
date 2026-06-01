#!/bin/bash

ENVNAME=PdfPageManipulatorEnv

# This script sets up the virtual environment and installs the required dependencies for the PdfPageManipulator project.

echo "🔧 Setting up virtual environment and installing dependencies..."

python3 -m venv $ENVNAME

echo "✅ Virtual environment '$ENVNAME' created."

echo "🔧 Activating virtual environment..."
source ./$ENVNAME/bin/activate

echo "🔧 Installing dependencies..."

python3 -m pip install --upgrade PyPDF2
python3 -m pip install --upgrade pytest
python3 -m pip install --upgrade pytest-cov
python3 -m pip install --upgrade pytest-mock
python3 -m pip install --upgrade pytest-html
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine

echo "✅ Virtual environment '$ENVNAME' created and dependencies installed."
