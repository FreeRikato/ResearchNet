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






# directory = "./knowledge_base"  # Replace with the path to your PDF directory
# search_text = "threatens to assault, or obstructs or attempts to obstruct, any public servant in the discharge of his duty as \nsuch public servant, in endeavouring to disperse an unlawful assembly, or to suppress a riot or affray, or \nuses, or threatens , or attempts to use criminal force to such public servant, shall be punished with \nimprisonment of either description for a term which may extend to three years, or with fine, or with both.  \n153. Want only giving provoca tion with intent to cause riot —if rioting be committed; if not \ncommitted. —Whoever malignantly, or wantonly by doing anything which is illegal, gives provocation to \nany person intending or knowing it to be likely that such provocation will cause the offence of rioting to"  # Replace with the text you want to search for
# # Using the function to search for the text
# found_pdf_path, found_page_num = search_pdfs(directory, search_text)

# if found_pdf_path:
#     print(f'Text found in: {found_pdf_path} on page {found_page_num}')
    
#     # Convert the found page, its previous, and its next page to images
#     images = pdf_pages_to_images(found_pdf_path, found_page_num)
#     for (img, pg_num) in images:  # Unpack the tuple here
#         img.save(f"page_{pg_num}.png")  # Saving images as "page_<page_num>.png"
# else:
#     print(f'Text not found in any PDF in the directory {directory}')
