from pdf2image import convert_from_path
from PIL import Image, ImageOps  # Import the Python Imaging Library for image processing
import os
import time
import sys

poppler_path = r'D:\Downloads\Release-24.02.0-0\poppler-24.02.0\bin'

def pdf_to_images(pdf_path, output_folder, start_page, dpi=500, timeout=4800):
    try:
        # Create directory for output images if it does not exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # print(f"Starting conversion for: {pdf_path}")

        # # Record the start time
        # start_time = time.time()
        # print("Conversion started...")

        # Convert PDF to list of images
        images = convert_from_path(
            pdf_path, 
            dpi=dpi, 
            poppler_path=poppler_path, 
            timeout=timeout
        )

        # # Record the end time and calculate the elapsed time
        # end_time = time.time()
        # elapsed_time = end_time - start_time
        # print(f"Conversion completed in {elapsed_time:.2f} seconds")
        
        # Save images and print progress
        image_paths = []
        total_pages = len(images)
        for i, img in enumerate(images):
            # Convert the image to grayscale
            img = img.convert('L')
            
            # Convert grayscale image to strictly black and white
            # threshold = 50  # You can adjust the threshold value as needed
            # img = img.point(lambda p: 255 if p > threshold else 0)

            page_number = start_page + i
            output_path = os.path.join(output_folder, f"page_{page_number:03}.png")
            img.save(output_path, 'PNG')
            image_paths.append(output_path)
            # Print progress every 10 pages
            if (i + 1) % 10 == 0 or i + 1 == total_pages:
                print(f"Saved image {page_number}/{start_page + total_pages - 1}: {output_path}")

        return total_pages  # Return the number of pages processed

    except Exception as e:
        print(f"An error occurred: {e}")
        # Additional debug information
        import traceback
        traceback.print_exc()
        return 0

def process_all_pdfs(input_folder, output_folder, dpi=500, timeout=4800):
    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # # Record the main start time
    # main_start_time = time.time()
    # print("Main conversion started...")

    # List all PDF files in the input directory
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]
    
    current_page_number = 1  # Start page number

    # Process each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_output_folder = os.path.join(output_folder, os.path.splitext(pdf_file)[0])
        print(f"Processing {pdf_file}...")
        pages_processed = pdf_to_images(pdf_path, pdf_output_folder, start_page=current_page_number, dpi=dpi, timeout=timeout)
        current_page_number += pages_processed  # Update the starting page number for the next PDF

    # print("All PDFs processed successfully.")
    # main_end_time = time.time()
    # main_elapsed_time = main_end_time - main_start_time
    # print(f"Main conversion completed in {main_elapsed_time:.2f} seconds")

if __name__ == "__main__":
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    odpi = sys.argv[3]
    process_all_pdfs(input_folder, output_folder, odpi, timeout=4800)
