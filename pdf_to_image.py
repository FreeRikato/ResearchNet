import fitz 

def pdf_pages_to_images(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    images = []

    # Adjust for 0-based indexing in fitz
    zero_based_page_num = page_num - 1

    # List of page numbers to convert: [previous, current, next]
    pages_to_convert = [zero_based_page_num - 1, zero_based_page_num, zero_based_page_num + 1]
    
    for pg_num in pages_to_convert:
        if 0 <= pg_num < len(doc):  # Ensure the page number is valid
            page = doc.load_page(pg_num)
            image = page.get_pixmap()
            images.append((image, pg_num + 1))  # Append the image and its 1-based page number

    return images