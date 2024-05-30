import os
import requests
import PyPDF2
from io import BytesIO

def get_pdf(zpl_content):
    # i had to remove the index parameter (the 0 index at the end of the URL) in order to request a pdf file with multiple labels 
    url = "http://api.labelary.com/v1/printers/8dpmm/labels/4x7/"
    files = {'file': ('label.zpl', zpl_content)}
    headers = {'Accept': 'application/pdf'}
    response = requests.post(url, headers=headers, files=files, stream=True)

    if response.status_code == 200:
        response.raw.decode_content = True
        return response.content
    else:
        print(f"Error: {response.text}")
        return None

def merge_pdfs(pdf_contents):
    merged_pdf = PyPDF2.PdfWriter()
    for content in pdf_contents:
        if content:
            reader = PyPDF2.PdfReader(BytesIO(content))
            for page in reader.pages:
                merged_pdf.add_page(page)

    return merged_pdf

def merge_zpl_to_pdf(zpl_folder_path):
    # Extract the job number (folder name) from the ZPL folder path
    job_number = os.path.basename(zpl_folder_path)

    base_directory = r'C:\Users\\LabeltoPDF\files'
    output_directory = os.path.join(base_directory, job_number)

    # Create the base directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # List ZPL files in the ZPLfiles folder
    zpl_file_paths = [os.path.join(zpl_folder_path, f) for f in os.listdir(zpl_folder_path) if f.endswith('.zpl')]

    # Convert ZPL files to PDF and collect contents
    pdf_contents = []
    for zpl_file_path in zpl_file_paths:
        try:
            with open(zpl_file_path, 'r') as file:
                zpl_content = file.read()
            pdf_content = get_pdf(zpl_content)
            if pdf_content:
                pdf_contents.append(pdf_content)
        except IOError as e:
            print(f"Failed to read or convert the file {zpl_file_path}: {e}")

    # Merge the PDFs together and save
    merged_pdf = merge_pdfs(pdf_contents)
    output_pdf_path = os.path.join(output_directory, f'{job_number}_labels.pdf')
    
    with open(output_pdf_path, 'wb') as output_file:
        merged_pdf.write(output_file)

    return output_pdf_path

if __name__ == "__main__":
    zpl_folder_path = r'C:\Users\sebas\OneDrive\Documents\LabeltoPDF\ZPLfiles\252949'
    output_pdf_path = merge_zpl_to_pdf(zpl_folder_path)
    print(f"Merged PDF saved to {output_pdf_path}")
