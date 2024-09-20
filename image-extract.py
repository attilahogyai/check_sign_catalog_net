import os
import unicodedata

import pymupdf
from enum import Enum
import subprocess



path_to_pdf_alto = '/home/hati/stuff/brickz/insura/pdfalto/pdfalto'

directory_path = '/home/hati/stuff/brickz/insura/pdf/'
extracted_images_path = '/home/hati/stuff/brickz/insura/images_pdfimages/'
os.makedirs(extracted_images_path, exist_ok=True)

class Method(Enum):
    pymupdf = 1
    pdfalto = 2
    pdfimages = 3

def replace_non_ascii_characters(filename: str) -> str:
    # Normalize the filename to NFKD form and encode to ASCII bytes, ignoring errors
    normalized_filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    return normalized_filename

def extract_all (method: Method = Method.pymupdf) -> None:
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            new_filename = replace_non_ascii_characters(filename)
            if new_filename != filename:
                old_file_path = os.path.join(directory_path, filename)
                new_file_path = os.path.join(directory_path, new_filename)
                os.rename(old_file_path, new_file_path)
                filename = new_filename
                print(f"Renamed '{filename}' to '{new_filename}'")
            file_path = os.path.join(directory_path, filename)
            extract_images_from_pdf(file_path, filename, method)

def extract_images_from_pdf(pdf_path: str, filename: str, method: Method = Method.pymupdf) -> None:
    if method == Method.pymupdf:
        extract_images_from_pdf_pymupdf(pdf_path, filename)
    elif method == Method.pdfalto:
        extract_images_from_pdf_pdfalto(pdf_path, filename)
    elif method == Method.pdfimages:
        extract_images_from_pdf_pdfimages(pdf_path, filename)

def extract_images_from_pdf_pymupdf(pdf_path: str, filename: str) -> None:
    doc = pymupdf.open(pdf_path)
    for page in doc:
        list_of_image = page.get_images()
        for image in list_of_image:
            img = doc.extract_image(image[0])
            img_data = img["image"]
            img_ext = img["ext"]
            img_path = os.path.join(extracted_images_path, f"{filename}_{page.number}.{img_ext}")
            with open(img_path, "wb") as img_file:
                img_file.write(img_data)
            print(img_path)

    doc.close()


def extract_images_from_pdf_pdfalto(pdf_path: str, filename: str) -> None:
    output_path = os.path.join(extracted_images_path, f"{filename}_alto.xml")
    command = [path_to_pdf_alto, pdf_path, output_path]
    subprocess.run(command, check=True)
    print(f"{pdf_path} Images extracted to {output_path}")

def extract_images_from_pdf_pdfimages(pdf_path: str, filename: str) -> None:
    output_path = os.path.join(extracted_images_path, f"{filename}")
    command = ["pdfimages", pdf_path, output_path]
    subprocess.run(command, check=True)
    print(f"Images extracted to {output_path}")


extract_all(Method.pdfimages)