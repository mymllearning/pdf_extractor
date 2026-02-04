# PDF Extractor & Converter

This project is a specialized tool designed to extract, clean, and structure Gujarati text from PDF documents. It utilizes OCR (Optical Character Recognition) to convert scanned PDF pages into editable text and subsequently transforms it into a structured JSON format for use in applications.

## 🚀 Features

- **OCR Extraction**: Converts scanned Gujarati PDF pages into raw text using a local Tesseract binary.
- **Text Cleaning**: Post-processes raw OCR output to fix line breaks, remove page artifacts, and normalize formatting.
- **Structured JSON**: Parses the cleaned text to identify Chapters ("Prakaran") and numbered items ("Vatos"), exporting them into a clean JSON structure.  
- **Batch Processing**: Handles large PDFs by processing pages in batches to manage memory usage.

## 📂 Project Structure

- **`extract_tesseract_local.py`**: The core script that converts PDF pages to images and runs Tesseract OCR on them.
- **`clean_text.py`**: Cleans the raw extracted text, merging broken lines and handling headers.
- **`convert_to_json.py`**: Parses the cleaned text file and converts it into a structured JSON file with metadata, chapters, and items.
- **`extract.sh`**: A shell script to automate the extraction process.
- **`web_app/`**: Directory for the frontend web application (currently in development).
- **`tesseract/`** & **`tessdata/`**: Local binaries and data files for Tesseract OCR.

## 🛠️ Prerequisites

- **Python 3.x**
- **Poppler**: Required for `pdf2image`.
  - Ubuntu/Debian: `sudo apt-get install poppler-utils`
  - macOS: `brew install poppler`
- **Linux Environment**: The included Tesseract binary is compiled for Linux.

## 📦 Installation

1. **Clone the repository** (if applicable).
2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Python dependencies**:
   ```bash
   pip install pdf2image
   ```
   *(Note: Ensure other dependencies like `Pillow` are installed if not included with `pdf2image`)*

## 📖 Usage

### Automated Extraction
You can use the provided shell script to run the extraction:
```bash
./extract.sh
```

### Manual Step-by-Step

1. **Extract Text from PDF**:
   Modify `extract_tesseract_local.py` to point to your target PDF file, then run:
   ```bash
   python extract_tesseract_local.py
   ```
   This generates `extracted_gujarati.txt`.

2. **Clean the Text**:
   Run the cleaning script to format the raw output:
   ```bash
   python clean_text.py
   ```
   This generates `cleaned_gujarati.txt`.

3. **Convert to JSON**:
   Parse the text into a structured JSON file:
   ```bash
   python convert_to_json.py
   ```
   This generates `swami_ni_vato1.json`.

## 📄 Output Format

The final JSON output follows this structure:

```json
{
  "title": "Swami Ni Vato",
  "metadata": "...",
  "chapters": [
    {
      "chapter_number": 1,
      "chapter_title": "...",
      "intro_text": "...",
      "items": [
        {
          "id": 1,
          "text": "..."
        }
      ]
    }
  ]
}
```

## 📝 Notes

- The project relies on a local `tesseract` binary located in the root directory. Ensure it has execution permissions (`chmod +x tesseract`).
- The OCR is specifically tuned for Gujarati language (`-l guj`).
