
import sys
from pypdf import PdfReader

file_path = "Swami ni vato 1 to 9.pdf"

try:
    reader = PdfReader(file_path)
    print(f"Number of pages: {len(reader.pages)}")
    
    page = reader.pages[0]
    text = page.extract_text()
    
    print(f"--- Page 1 Extraction Check ---")
    if text and text.strip():
        print("Text found:")
        print(text[:200]) # First 200 chars
    else:
        print("No text found on page 1.")
        
    print(f"\n--- Image Check ---")
    if len(page.images) > 0:
        print(f"Page 1 contains {len(page.images)} images.")
    else:
        print("Page 1 has no images.")
        
except Exception as e:
    print(f"Error: {e}")
