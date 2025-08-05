from ingest import extract_text
import os

file_list = os.listdir()
supported_extensions = (".pdf", ".docx", ".eml")

for file_name in file_list:
    if file_name.endswith(supported_extensions):
        try:
            text = extract_text(file_name)

            if text.strip():
                print(text[:1000])
            else:
                print(f"No readable text in: {file_name}")

        except Exception as e:
            print(f"Error reading {file_name}: {e}")