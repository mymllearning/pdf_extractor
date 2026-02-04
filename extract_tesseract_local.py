
import os
import subprocess
from pdf2image import convert_from_path, pdfinfo_from_path

def get_pdf_page_count(pdf_path):
    try:
        info = pdfinfo_from_path(pdf_path)
        return info["Pages"]
    except Exception as e:
        print(f"Error getting PDF info: {e}")
        return None

def extract_text_with_local_tesseract(pdf_path, output_file):
    # Determine total pages
    total_pages = get_pdf_page_count(pdf_path)
    if total_pages is None:
        # Fallback if we can't get page count: just try a large number or error out?
        # Let's try to just process without count if failed, but usually this works.
        print("Could not determine page count. Proceeding with risk of failing blindly.")
        total_pages = 1000 # arbitrary limit
    else:
        print(f"Total pages in PDF: {total_pages}")

    # Define paths
    tesseract_binary =  os.path.abspath("./tesseract")
    tessdata_dir = os.path.abspath("./tessdata")
    
    # Ensure binary is executable
    if not os.access(tesseract_binary, os.X_OK):
        print("Making tesseract binary executable...")
        os.chmod(tesseract_binary, 0o755)

    # Initialize output file (clear it)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("")

    batch_size = 5
    for start_page in range(1, total_pages + 1, batch_size):
        end_page = min(start_page + batch_size - 1, total_pages)
        print(f"\nProcessing batch: Pages {start_page} to {end_page}...")
        
        try:
            images = convert_from_path(pdf_path, first_page=start_page, last_page=end_page)
        except Exception as e:
            print(f"Error converting pages {start_page}-{end_page}: {e}")
            break

        batch_text = ""
        for i, image in enumerate(images):
            page_num = start_page + i
            print(f"  - OCR Page {page_num}...", end="", flush=True)
            
            # Save temporary image
            temp_img_path = f"temp_page_{page_num}.png"
            image.save(temp_img_path, "PNG")
            
            output_base = f"temp_output_{page_num}"
            
            # Run tesseract command
            cmd = [
                tesseract_binary,
                temp_img_path,
                output_base,
                "-l", "guj",
                "--tessdata-dir", tessdata_dir
            ]
            
            try:
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode == 0:
                    # Read result
                    txt_file = output_base + ".txt"
                    if os.path.exists(txt_file):
                        with open(txt_file, "r", encoding="utf-8") as f:
                            page_text = f.read()
                        
                        char_count = len(page_text.strip())
                        print(f" Done. Extracted {char_count} chars.")
                        
                        batch_text += f"\n--- Page {page_num} ---\n{page_text}\n"
                        # Cleanup
                        os.remove(txt_file)
                    else:
                        print(f" Warning: Output file {txt_file} not found.")
                else:
                    print(f" Failed: {result.stderr}")
            except Exception as e:
                print(f" Error: {e}")
            finally:
                 if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)

        # Write batch to file
        if batch_text:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(batch_text)
            print(f"  -> Batch saved to {output_file}")

if __name__ == "__main__":
    pdf_file = "Swami ni vato 10 - 16.pdf"
    output_file = "extracted_gujarati.txt"
    
    if os.path.exists(pdf_file):
        extract_text_with_local_tesseract(pdf_file, output_file)
        print("\nExtraction complete.")
    else:
        print(f"File {pdf_file} not found.")
