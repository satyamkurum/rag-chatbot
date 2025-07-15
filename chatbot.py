import os
import uuid
import re
import PyPDF2
import pinecone
import google.generativeai as genai
from tqdm import tqdm
from dotenv import load_dotenv

# Load API keys from environment
load_dotenv()
GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

# Configure APIs
genai.configure(api_key=GEMINI_API_KEY)
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
INDEX_NAME = "rag-chatbot"
index = pc.Index(INDEX_NAME)

# Unique session namespace (used across app.py)
SESSION_NAMESPACE = str(uuid.uuid4())

# PDF Extraction 
def extract_text_from_pdf(file_path):
    reader = PyPDF2.PdfReader(file_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        text = clean_text(text)
        pages.append({
            "page_number": i + 1,
            "text": text
        })
    return pages

# Text Cleaning 
def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
    lines = text.split('\n')
    return '\n'.join([line.strip() for line in lines if len(line.strip()) > 10])

# Text Chunking 
def chunk_pages(pages, chunk_size=1000, overlap=200):
    chunks = []
    for page in pages:
        text = page['text']
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            chunks.append({
                'page_number': page['page_number'],
                'text': chunk_text
            })
            start += chunk_size - overlap
    return chunks

#  Embed & Store in Pinecone
def embed_and_store_chunks(chunks):
    for chunk in tqdm(chunks, desc="Embedding chunks"):
        try:
            text = chunk['text']
            embedding = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )["embedding"]

            chunk_id = f"chunk-{uuid.uuid4()}"
            index.upsert([
                (
                    chunk_id,
                    embedding,
                    {
                        "text": text,
                        "page_number": chunk['page_number']
                    }
                )
            ], namespace=SESSION_NAMESPACE)
        except Exception as e:
            print(f" Embedding error: {e}")

#  Retrieval 
def get_question_embedding(question):
    return genai.embed_content(
        model="models/embedding-001",
        content=question,
        task_type="retrieval_query"
    )["embedding"]

def retrieve_relevant_chunks(question, top_k=3):
    vector = get_question_embedding(question)
    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True,
        namespace=SESSION_NAMESPACE
    )
    return [match['metadata']['text'] for match in results['matches']]

#  Generate Answer 
def generate_answer_from_context(question, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"""You are a helpful assistant answering questions based on a document.

Use only the context below to answer the question.

Context:
{context}

Question: {question}
Answer:"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    chat = model.start_chat()
    return chat.send_message(prompt).text
