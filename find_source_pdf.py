import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

def search_pdfs(directory, search_text):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            with open(pdf_path, "rb") as f:
                pdf_reader = PdfReader(f)
                for page_num, page in enumerate(pdf_reader.pages, start=1):
                    page_text = page.extract_text()
                    if search_text.lower().replace("\n", "") in page_text.lower().replace("\n", ""):  # Case insensitive search
                        return pdf_path, page_num  # Return the path of the PDF and page number if text is found
    return None, None  # Return None for both path and page number if text is not found in any PDF
