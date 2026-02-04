#!/bin/bash
FILE="Swami ni vato 1 to 9.pdf"
OUTPUT="output.txt"

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    echo "Please copy it to: $(pwd)"
    exit 1
fi

echo "Attempting to extract text from $FILE using local Tesseract OCR..."
echo "This handles scanned Gujurati text."

# Source venv if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# detailed check
if python3 extract_tesseract_local.py; then
    echo "Success! Extraction complete."
    if [ -f "extracted_gujarati.txt" ]; then
        mv extracted_gujarati.txt "$OUTPUT"
        echo "Text saved to $OUTPUT"
        echo "Preview:"
        head -n 20 "$OUTPUT"
    fi
else
    echo "Extraction script failed."
fi
