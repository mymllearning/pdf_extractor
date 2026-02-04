
import easyocr
import sys
import os
import numpy as np
from pdf2image import convert_from_path

def extract_text(pdf_path, pages_to_process=3):
    print(f"Initializing EasyOCR (Language: Gujarati 'guj')...")
    try:
        reader = easyocr.Reader(['guj'], gpu=False)
    except Exception as e:
        print(f"Error initializing EasyOCR: {e}")
        return

    print(f"Converting PDF pages 1-{pages_to_process} to images...")
    try:
        images = convert_from_path(pdf_path, first_page=1, last_page=pages_to_process)
    except Exception as e:
        print(f"Error converting PDF: {e}")
        print("Ensure poppler-utils is installed (which seems true as pdftotext exists).")
        return

    full_text = ""
    for i, image in enumerate(images):
        print(f"Processing page {i+1}...")
        try:
            # detail=0 returns a list of strings
            results = reader.readtext(np.array(image), detail=0) 
            page_text = "\n".join(results)
            full_text += f"\n--- Page {i+1} ---\n{page_text}\n"
        except Exception as e:
            print(f"Error processing page {i+1}: {e}")
        
    print("\nExtraction Complete for first few pages.")
    return full_text

if __name__ == "__main__":
    pdf_file = "Swami ni vato 1 to 9.pdf"
    if not os.path.exists(pdf_file):
        print(f"File not found: {pdf_file}")
        sys.exit(1)
        
    text = extract_text(pdf_file)
    
    if text:
        output_file = "ocr_output_sample.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved extracted text to {output_file}")
        # Print a preview
        print("\n--- Preview ---\n")
        print(text[:500])
