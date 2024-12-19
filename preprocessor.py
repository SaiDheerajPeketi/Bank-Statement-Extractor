from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
import os
import re

def is_valid_date(text):
    date_pattern1 = r'^\d{2}-\d{2}-\d{4}$'
    date_pattern2 = r'^\d{2}-\d{2}-\d{2}$'
    return bool(re.match(date_pattern1, text)) or bool(re.match(date_pattern2, text))

def is_valid_date_or_empty(text):
    date_pattern = r'^\d{2}-\d{2}-\d{4}$'
    return bool(re.match(date_pattern, text)) or text == ''


def extract_opening_balance_info(text):
    pattern = r"Your Opening Balance on (\d{2}-\d{2}-\d{2}):\s*([\d,.]+)"
    match = re.search(pattern, text)
    if match:
        description = f"Your Opening Balance"
        date = match.group(1)
        amount = match.group(2)
        return True, date, description, amount
    else:
        return False, None, None, None


def extract_closing_balance_info(text):
    pattern = r"Your Closing Balance on (\d{2}-\d{2}-\d{2}):([\d,.]+)"
    match = re.search(pattern, text)
    if match:
        date = match.group(1)
        amount = match.group(2)
        converted_text = f"Your Closing Balance on {date}:      {amount}"
        return converted_text
    else:
        return None

def optional_decrypt_pdf(pdf_file, password=None):
    pdf_reader = PdfReader(pdf_file)
    if pdf_reader.is_encrypted and password:
        pdf_reader.decrypt(password)
    pdf_writer = PdfWriter()
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_writer.add_page(page)
    with open(pdf_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)


def pdf_to_images(pdf_file_path, output_folder="extracted_images", dpi=300):
    # Create output folder if it does not exist
    os.makedirs(output_folder, exist_ok=True)

    # Convert PDF to list of images, one per page
    images = convert_from_path(pdf_file_path, dpi=dpi)

    # Save each image to the output folder
    image_paths = []
    for i, image in enumerate(images, start=1):
        image_path = os.path.join(output_folder, f"page_{i}.png")
        image.save(image_path, "PNG")
        image_paths.append(image_path)

    print(f"Saved {len(images)} pages as images in '{output_folder}' folder.")
    return image_paths


if __name__ == "__main__":
    pdf_path = r"test.pdf"
    pdf_to_images(pdf_path)
