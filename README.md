# RAG PDF Chatbot – Ask Your PDF Anything!

A Streamlit-based chatbot that allows you to upload a PDF file and ask questions about its content. Built using:

-  Retrieval-Augmented Generation (RAG)
-  Google Gemini (via `google-generativeai`)
-  Pinecone vector database
-  Streamlit for user interface

---

##  How It Works

1. Upload any PDF file
2. The app extracts and chunks the text
3. Each chunk is embedded using Gemini Embeddings
4. Chunks are stored in a temporary session namespace in Pinecone
5. When you ask a question:
   - It is embedded and matched to relevant chunks
   - The matched context is sent to Gemini (RAG)
   - You get an accurate, context-aware answer
6. Session data is automatically deleted when you're done 

---

##  Example Use Cases

- Understanding long research papers
- Quickly reviewing resumes
- Extracting insights from business documents
- Q&A over lecture notes or reports

---

##  Tech Stack

  UI             Streamlit (in Docker) 
  LLM            Gemini 2.5 Flash (via API) 
  Embeddings     Gemini `models/embedding-001` 
  Vector DB      Pinecone (cosine similarity) 
  Deployment     Hugging Face Spaces |

---

##  API Keys Required

Before running locally, make sure to set your environment variables:

```bash
GOOGLE_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
```
## Author

**Satyam Kurum**  
_Machine Learning & Web Enthusiast_  
[LinkedIn](https://linkedin.com/in/satyamkurum) | [GitHub](https://github.com/satyamkurum)

> Feel free to ⭐️ this repo and fork it for your own projects!
