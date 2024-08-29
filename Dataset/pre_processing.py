import re
import os
import json
from utils import *

# Company names to mask
company_names = ['삼성SDS','삼성 SDS', '삼성', 'SDS', '삼성전자']

# Directory containing the files
input_dir = r'C:\\TailorCV\\Dataset\\삼성'
output_dir = r'C:\\TailorCV\\Dataset\\Thebe_processed'
remove_duplicate_files(input_dir)
delete_empty_files(input_dir)

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)



# Process each file in the directory
for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):
        file_path = os.path.join(input_dir, filename)

        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Mask the company names
        masked_text = mask_company_names(text, company_names)

        # Split text into questions and answers
        qa_dict = parse_text(masked_text)

        # Save the masked text to a JSON file
        output_filename = f"{os.path.splitext(filename)[0]}.json"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(qa_dict, json_file, ensure_ascii=False, indent=4)

        print(f"Processed and saved: {output_filename}")

# Optionally, rename files in order if needed
rename_files_in_order(output_dir)
print("All files processed.")

