
import io
import os
from google.cloud import vision
import logging
import time
import sys
# Configure logging
logging.basicConfig(level=logging.INFO)

# Replace with the path to your downloaded key file
credentials_path = os.path.join(os.path.dirname(__file__), 'crested-guru-429911-g4-08e1001da7cd.json')

# Initialize the Google Cloud Vision client with the service account key file
vision_client = vision.ImageAnnotatorClient.from_service_account_json(credentials_path)
logging.info("Google Cloud Vision API initialized")

# Function to perform OCR using Google Cloud Vision API
def extract_text_from_image(image_path):
    try:
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        image_context = vision.ImageContext(language_hints=["ar"])
        response = vision_client.text_detection(image=image, image_context=image_context)
        texts = response.text_annotations
        if texts:
            logging.info(f"Extracted text from image {image_path}")
            return texts[0].description
        else:
            logging.warning(f"No text found in image {image_path}")
            return ''
    except Exception as e:
        logging.error(f"Problem with {image_path}: {e}")
        return ''

# Main function
def main(image_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # start_time = time.time()
    # print("Started the time")

    # Walk through all directories and files within the specified image directory
    for root, dirs, files in os.walk(image_dir):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for PNG, JPG, and JPEG files
                image_path = os.path.join(root, filename)
                if os.path.isfile(image_path):  # Check if the file exists
                    text = extract_text_from_image(image_path)
                    
                    # Create a subdirectory for each part in the output directory
                    relative_path = os.path.relpath(root, image_dir)
                    part_output_dir = os.path.join(output_dir, relative_path)
                    if not os.path.exists(part_output_dir):
                        os.makedirs(part_output_dir)
                    
                    # Save text to a separate file named after the image
                    output_txt_path = os.path.join(part_output_dir, f"{os.path.splitext(filename)[0]}.txt")
                    with open(output_txt_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    logging.info(f"Text saved to {output_txt_path}")
                else:
                    logging.warning(f"File not found: {filename}")

    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Conversion completed in {elapsed_time:.2f} seconds")

# Replace with your image directory
# image_dir = 'imgoutput_test2\part_01'
# image_dir = input("Enter the path to the image directory: ")
# output_dir = 'from_vision'
if __name__ == "__main__":

    image_dir = sys.argv[1]
    output_dir = sys.argv[2]
    main(image_dir, output_dir)
