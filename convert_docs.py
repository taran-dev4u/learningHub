import os
import glob
from markitdown import MarkItDown

def convert_pdfs():
    md = MarkItDown()
    resources_dir = os.path.join(os.path.dirname(__file__), 'Resources')
    output_dir = os.path.join(os.path.dirname(__file__), 'ConvertedDocs')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Find all PDFs in Resources directory and subdirectories
    pdf_files = glob.glob(os.path.join(resources_dir, '**', '*.pdf'), recursive=True)

    for pdf_path in pdf_files:
        print(f"Processing {pdf_path}...")
        try:
            result = md.convert(pdf_path)

            # Create a corresponding markdown file
            rel_path = os.path.relpath(pdf_path, resources_dir)
            out_file = os.path.join(output_dir, rel_path.replace('.pdf', '.md'))

            # Ensure output directory exists for this file
            os.makedirs(os.path.dirname(out_file), exist_ok=True)

            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(result.text_content)

            print(f"Successfully converted to {out_file}")
        except Exception as e:
            print(f"Failed to convert {pdf_path}: {e}")

if __name__ == "__main__":
    convert_pdfs()
