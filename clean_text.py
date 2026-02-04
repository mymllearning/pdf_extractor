
import re

def clean_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    
    # Regex for detecting list items like (1), (૧), 1., etc.
    # Gujarati digits: ૦ ૧ ૨ ૩ ૪ ૫ ૬ ૭ ૮ ૯
    list_item_pattern = re.compile(r'^\s*\(?[\d૧૨૩૪૫૬૭૮૯]+\)[\.\s]')
    
    # Regex for Chapter headers
    chapter_pattern = re.compile(r'^\s*પ્રકરણ\s*[:\-\s]\s*[\d૧૨૩૪૫૬૭૮૯]+', re.IGNORECASE)

    current_paragraph = ""

    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            if current_paragraph:
                cleaned_lines.append(current_paragraph)
                current_paragraph = ""
            continue
            
        # Skip Page markers
        if line.startswith("--- Page") and line.endswith("---"):
            continue
            
        # Check for Headers
        is_header = chapter_pattern.match(line)
        is_list_item = list_item_pattern.match(line)
        
        if is_header or is_list_item:
            # If we have a pending paragraph, save it first
            if current_paragraph:
                cleaned_lines.append(current_paragraph)
                current_paragraph = ""
            
            # Add the header/list item as its own line
            cleaned_lines.append(line)
        else:
            # Regular text line. formatting: 
            # If current_paragraph exists, append to it with space.
            # Else start new.
            if current_paragraph:
                # Heuristic: If previous line ended with valid punctuation, start new paragraph?
                # Usually in OCR, broken lines don't end in punctuation.
                if current_paragraph.endswith(('.', '?', '!', '।', ',')):
                     # Actually, comma might mean continuation, but periods usually mean end.
                     # However, sometimes paragraphs key on newline. 
                     # Let's try to merge unless it looks completely distinct.
                     # But for "Swami ni Vato", it's usually numbered points.
                     # If it's a new point, we handled it above.
                     # If it's just continuation text ...
                     current_paragraph += " " + line
                else:
                    current_paragraph += " " + line
            else:
                current_paragraph = line

    if current_paragraph:
        cleaned_lines.append(current_paragraph)

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in cleaned_lines:
            f.write(line + "\n\n")

    print(f"Cleaned text saved to {output_file}")

if __name__ == "__main__":
    clean_text("extracted_gujarati.txt", "cleaned_gujarati.txt")
