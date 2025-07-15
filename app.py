import streamlit as st
from chatbot import (
    extract_text_from_pdf, chunk_pages,
    embed_and_store_chunks, retrieve_relevant_chunks,
    generate_answer_from_context, index, SESSION_NAMESPACE
)

st.set_page_config(page_title="📄 PDF Chatbot", layout="wide")
st.title("📄 Chat with your PDF")
st.markdown("Upload a PDF file and ask questions about its content using Gemini + Pinecone RAG.")

# File uploader 
uploaded_file = st.file_uploader("📤 Upload your PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("⏳ Processing PDF..."):
        # Save the uploaded file locally
        with open("uploaded.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract and embed PDF content
        pages = extract_text_from_pdf("uploaded.pdf")
        chunks = chunk_pages(pages)
        embed_and_store_chunks(chunks)

    st.success(" PDF processed. You can now ask questions below!")

    #Question input loop 
    question = st.text_input(" Ask a question about the PDF:")

    if question:
        with st.spinner("🧠 Thinking..."):
            chunks = retrieve_relevant_chunks(question)
            answer = generate_answer_from_context(question, chunks)
        st.markdown("### 🤖 Answer:")
        st.success(answer)

    # Cleanup button
    if st.button("🧹 End Session and Clear Memory"):
        index.delete(delete_all=True, namespace=SESSION_NAMESPACE)
        st.success(f"Deleted session namespace: {SESSION_NAMESPACE}")
