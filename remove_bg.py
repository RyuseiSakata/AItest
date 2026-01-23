import os
from rembg import remove
from PIL import Image
from pathlib import Path

# Paths
source_dir = Path("/Users/sakata/.gemini/antigravity/brain/ca0a797e-07e3-44d5-9f29-f4dabd123ede")
output_dir = Path("/Users/sakata/Desktop/AItest/public")

# Files to process
files = [
    ("char_ai_teacher_1769129691832.png", "char_ai.png"),
    ("char_mai_student_1769129707220.png", "char_mai.png")
]

for src_name, dest_name in files:
    src_path = source_dir / src_name
    dest_path = output_dir / dest_name
    
    print(f"Processing {src_name} -> {dest_name}")
    
    try:
        input_image = Image.open(src_path)
        output_image = remove(input_image)
        output_image.save(dest_path)
        print("Success!")
    except Exception as e:
        print(f"Error processing {src_name}: {e}")
