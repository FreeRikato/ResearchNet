import streamlit as st
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image
import io
import os

from htmlTemplates import css, bot_template, user_template
from pdf_extractor import get_pdf_text
from text_chunker import get_text_chunks
from generate_embedding import get_vectorstore
from conversation_chain import get_conversation_chain
from save_files import save_uploaded_files
from find_source_pdf import search_pdfs
from pdf_to_image import pdf_pages_to_images

def handle_userinput(user_question):
    chat_history = st.session_state.get('chat_history', [])
    response = st.session_state.conversation({"question": user_question, "chat_history": chat_history})
    answer = response.get('answer')
    source_document = response.get('source_documents')
    chat_history.append((user_question, answer))
    st.session_state['chat_history'] = chat_history
    for i, message in enumerate(st.session_state.chat_history):
        question, answer = message
        st.write(user_template.replace(
            "{{MSG}}", question), unsafe_allow_html=True)
        st.write(bot_template.replace(
            "{{MSG}}", answer), unsafe_allow_html=True)
        
    source = str(source_document[0]).split("page_content='", 1)[1].rstrip("'").replace('\\n', '\n').replace('\\t', '\t')

    found_pdf_path, found_page_num = search_pdfs(".\knowledge_base", source)
    
    if found_pdf_path:
        st.sidebar.write(f'Text found in: {found_pdf_path}')
        # Convert the found page, its previous, and its next page to images
        images = pdf_pages_to_images(found_pdf_path, found_page_num)
        for (img, pg_num) in images:  # Unpack the tuple here
            # Save fitz pixmap to a BytesIO buffer as a PNG
            buffer = BytesIO()
            buffer.write(img.tobytes("png"))
            buffer.seek(0)

            # Convert the BytesIO buffer to a PIL Image
            pil_img = Image.open(buffer)

            # Display the image in Streamlit's sidebar
            st.sidebar.image(pil_img, caption=f"Page {pg_num}")
    else:
        print(f'Text not found in any PDF in the knowledge base')
    

def main():
    load_dotenv()
    st.set_page_config(page_title="Research Resonance: A Knowledge-Based Query System",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("Research Resonance: A Knowledge-Based Query System :books:")
    user_question = st.text_input("Ask a question to your knowledge base:")
    
    knowledge_base_path = "./knowledge_base"
    local_pdf_files = [os.path.join(knowledge_base_path, f) for f in os.listdir(knowledge_base_path) if f.endswith('.pdf')]
    
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                
                save_uploaded_files(pdf_docs, "./knowledge_base")
                
                raw_text = "".join(get_pdf_text(local_pdf_files))

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()