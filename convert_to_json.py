
import json
import re

def parse_swami_ni_vato(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {
        "title": "Swami Ni Vato",
        "chapters": []
    }

    # Split content by "પ્રકરણ :" tags, but keep the delimiter
    # The first part will be introductory/front matter
    # Regex to find chapter headers of the form "પ્રકરણ : <number> <Title>"
    # Note: text might be scattered with newlines.
    
    # We will iterate line by line to build state
    lines = content.split('\n')
    
    current_chapter = None
    current_item = None
    
    # Regex checks for Prakaran (Chapter)
    # Handling OCR error where 'Prekaran' might be 'Grakaran' (પ્ર/ગ્ર)
    # Ensure number is separated from title by space or is at end of line to avoid matching references like 'પ્રકરણ-૧૬માં'
    chapter_pattern = re.compile(r'^\s*[ગપ]્રકરણ\s*[:\-\s]\s*(\d+)(?:\s+|$)(.*)', re.IGNORECASE)
    item_pattern = re.compile(r'^\s*\((\d+)\)\s*(.*)')
    
    # Text accumulator
    buffer_text = []

    # Special handling for front matter (before any chapter)
    front_matter = []
    
    mode = "front_matter" 
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        chap_match = chapter_pattern.match(line)
        item_match = item_pattern.match(line)
        
        if chap_match:
            try:
                new_chapter_num = int(chap_match.group(1))
            except ValueError:
                # Fallback if int conversion fails somehow
                buffer_text.append(line)
                continue

            if current_chapter and current_chapter['chapter_number'] == new_chapter_num:
                # This is a running header for the same chapter (e.g. on a new page)
                # Ignore it so text continues merging.
                continue

            # Save previous item/chapter work
            if current_item:
                current_item['text'] = "\n".join(buffer_text).strip()
                current_chapter['items'].append(current_item)
                current_item = None
                buffer_text = []
            elif current_chapter and buffer_text:
                # If we had text in a chapter but no item started yet, it's chapter intro
                current_chapter['intro_text'] = "\n".join(buffer_text).strip()
                buffer_text = []

            # Start new chapter
            chapter_title = chap_match.group(2).strip().strip('.')
            
            current_chapter = {
                "chapter_number": new_chapter_num,
                "chapter_title": chapter_title,
                "intro_text": "",
                "items": []
            }
            data['chapters'].append(current_chapter)
            mode = "chapter_intro"
            
        elif item_match:
            # Found a new item (Vat)
            if current_chapter is None:
                # If we find an item but no chapter has started yet, treat it as front matter
                front_matter.append(line)
                continue

            # Save previous item if exists
            if current_item:
                current_item['text'] = "\n".join(buffer_text).strip()
                current_chapter['items'].append(current_item)
                buffer_text = []
            elif current_chapter and mode == "chapter_intro":
                 # We were in chapter intro, save that text
                 current_chapter['intro_text'] = "\n".join(buffer_text).strip()
                 buffer_text = []
            
            # Start new item
            item_id = int(item_match.group(1))
            item_text_start = item_match.group(2).strip()
            
            current_item = {
                "id": item_id,
                "text": "" # will fill later
            }
            buffer_text = [item_text_start]
            mode = "item_text"
            
        else:
            # Just normal text line
            if mode == "front_matter":
                front_matter.append(line)
            else:
                buffer_text.append(line)

    # End of loop: save last item
    if current_item:
        current_item['text'] = "\n".join(buffer_text).strip()
        current_chapter['items'].append(current_item)
    elif current_chapter and buffer_text:
        # If we had text but no items (unlikely for final chapter, but possible)
        current_chapter['intro_text'] = "\n".join(buffer_text).strip()

    data['metadata'] = "\n".join(front_matter)

    # Post-cleanup: Sometimes "Chapter 1" text comes from OCR noise. 
    # Let's filter out empty chapters if any.
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully converted to {output_file}")

if __name__ == "__main__":
    parse_swami_ni_vato("cleaned_gujarati.txt", "swami_ni_vato1.json")
