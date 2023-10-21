import streamlit as st
from dotenv import load_dotenv


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon=":books:")
    
    st.header("Chat with Multiple PDFs :books:")
    st.text_input("Ask a question about your documents")
    
    with st.sidebar:
        st.subheader("Document List")
        st.file_uploader("Upload your PDFs here and click on 'Process' below", accept_multiple_files=True)
        st.button("Process")
        
if __name__ == "__main__":
    main()