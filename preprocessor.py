from pdf2image import convert_from_path
import os


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
