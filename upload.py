import requests
import multiplePDF
import os


def get_token(token_file_path):
    # Reads the token from the specified file
    with open(token_file_path, 'r') as file:
        return file.read().strip()


def upload_pdf_to_intellievent(file_path, token):
    # Constants
    URL = "https://webapi1.ielightning.net/api/v1/Jobs/JobFiles/Files"
    headers = {'Authorization': f'Bearer {token}'}
    params = {'refId': '252949'}

    # Opens the file in binary mode and upload
    with open(file_path, 'rb') as f:
        # The 'Name' is not specified in this code snippet but would be something like 'document'.
        files = {'file': (os.path.basename(file_path), f, 'application/pdf')}

        response = requests.post(URL, headers=headers, params=params, files=files)
    

        if response.status_code in [200, 201]:
            print("File uploaded successfully")
            return response.json()
        else:
            print(f"Failed to upload file: {response.status_code}, {response.headers}")
            return None


if __name__ == "__main__":

    TOKEN_FILE = r'C:\Users\LabeltoPDF\TOKEN.TXT'
    token = get_token(TOKEN_FILE)

    # Define the ZPL folder path
    zpl_folder_path = r'C:\Users\LabeltoPDF\ZPLfiles\252949'

    # Use multiplePDF to merge ZPL files into a PDF and get the path of the merged PDF
    merged_pdf_path = multiplePDF.merge_zpl_to_pdf(zpl_folder_path)

    # Upload the merged PDF
    upload_pdf_to_intellievent(TOKEN_FILE, token)
