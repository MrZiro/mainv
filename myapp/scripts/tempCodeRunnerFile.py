

import fitz  # PyMuPDF
import os
import sys

def split_pdf(pdf_path, output_folder, max_pages=20):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    pdf_document = fitz.open(pdf_path)
    num_pages = pdf_document.page_count
    
    for start_page in range(0, num_pages, max_pages):
        end_page = min(start_page + max_pages - 1, num_pages - 1)
        pdf_writer = fitz.open()
        pdf_writer.insert_pdf(pdf_document, from_page=start_page, to_page=end_page)
        
        part_number = start_page // max_pages + 1
        output_path = os.path.join(output_folder, f"part_{part_number:02}.pdf")
        
        pdf_writer.save(output_path)
        pdf_writer.close()
        print(f"Saved part {part_number:02} with pages {start_page + 1} to {end_page + 1} to {output_path}")
    
    pdf_document.close()

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    output_folder = sys.argv[2]
    max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    split_pdf(pdf_path, output_folder, max_pages)
