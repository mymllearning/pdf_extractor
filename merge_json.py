import json
import os

def merge_files(file1_path, file2_path, output_path):
    if not os.path.exists(file1_path):
        print(f"Error: {file1_path} not found.")
        return
    if not os.path.exists(file2_path):
        print(f"Error: {file2_path} not found.")
        return

    try:
        with open(file1_path, 'r', encoding='utf-8') as f1:
            data1 = json.load(f1)
        
        with open(file2_path, 'r', encoding='utf-8') as f2:
            data2 = json.load(f2)
            
        # Check if basic structure matches
        if 'chapters' not in data1:
             print(f"Error: 'chapters' key not found in {file1_path}")
             return
        if 'chapters' not in data2:
             print(f"Error: 'chapters' key not found in {file2_path}")
             return
             
        # Merge chapters
        merged_chapters = data1['chapters'] + data2['chapters']
        
        # Sort chapters by chapter_number if possible, to have a nice order
        # Assuming chapter_number exists and is integer
        try:
             merged_chapters.sort(key=lambda x: x.get('chapter_number', 0))
        except Exception as e:
             print(f"Warning: Could not sort chapters: {e}")
             
        merged_data = {
            "title": data1.get("title", "Swami Ni Vato"),
            "chapters": merged_chapters
        }
        
        with open(output_path, 'w', encoding='utf-8') as out:
            json.dump(merged_data, out, ensure_ascii=False, indent=2)
            
        print(f"Successfully merged files into {output_path}")
        print(f"Total chapters: {len(merged_chapters)}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    base_path = "/home/krutarth/D/machine_learning/pdf_extractor/"
    file1 = os.path.join(base_path, "swami_ni_vato.json")
    file2 = os.path.join(base_path, "swami_ni_vato1.json")
    output = os.path.join(base_path, "swami_ni_vato_merged.json")
    
    merge_files(file1, file2, output)
