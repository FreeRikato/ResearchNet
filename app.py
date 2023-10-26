import streamlit as st
import os
from dotenv import load_dotenv
from htmlTemplates import css, bot_template, user_template
from pdf_extractor import get_pdf_text
from text_chunker import get_text_chunks
from generate_embedding import get_vectorstore
from conversation_chain import get_conversation_chain

def handle_userinput(user_question):
    chat_history = st.session_state.get('chat_history', [])
    response = st.session_state.conversation({"question": user_question, "chat_history": chat_history})
    answer = response.get('answer')
    chat_history.append((user_question, answer))
    st.session_state['chat_history'] = chat_history
    for i, message in enumerate(st.session_state.chat_history):
        question, answer = message
        st.write(user_template.replace(
            "{{MSG}}", question), unsafe_allow_html=True)
        st.write(bot_template.replace(
            "{{MSG}}", answer), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    
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
                raw_text = get_pdf_text(pdf_docs)
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