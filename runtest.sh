#!/bin/bash

ENVNAME=PdfPageManipulatorEnv

# This script runs the tests for the PdfPageManipulator class using pytest.
# PYTHONPATH is set to src to ensure that the tests can import the PdfPageManipulator module correctly.
export PYTHONPATH=src

# Activate the virtual environment
echo "🔧 Activating virtual environment..."
source ./$ENVNAME/bin/activate

# Run the cleanup script to remove old test files
bash ./cleanuptest.sh

echo "✅ Running tests for PdfPageManipulator..."

python3 -m pytest --verbose tests/test_PdfPageManipulator.py

echo "🥳 Tests completed."