import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.tools import tool
import streamlit as st

load_dotenv()
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

KNOWLEDGE_BASE_DIR = "knowledge_base"
CHROMA_PERSIST_DIR = "chroma_db"

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

def load_and_chunk_documents() -> list:
    """
    Loads every PDF in the knowledge_base folder and splits them into chunks.
    """
    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        if filename.endswith(".pdf"):
            file_path = os.path.join(KNOWLEDGE_BASE_DIR, filename)
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            chunks = splitter.split_documents(pages)
            all_chunks.extend(chunks)

    return all_chunks

def build_vectorstore():
    """
    Builds (or loads, if already built) a persistent Chroma vectorstore
    from the knowledge base PDFs.
    """
    if os.path.exists(CHROMA_PERSIST_DIR):
        vectorstore = Chroma(
            persist_directory=CHROMA_PERSIST_DIR,
            embedding_function=embeddings
        )
    else:
        chunks = load_and_chunk_documents()
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_PERSIST_DIR
        )

    return vectorstore

def search_knowledge_base(query: str, k: int = 2) -> str:
    """
    Searches the knowledge base for chunks relevant to the query,
    and returns them combined as a single context string.
    This is the function the Agent/RAG tool will call.
    """
    vectorstore = build_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k":2})
    results = retriever.invoke(query)
    context = "\n\n".join(doc.page_content for doc in results)
    return context if context else "No relevant information found in the knowledge base."

@tool
def search_knowledge_base_tool(query: str) -> str:
    """
    Searches company policies and FAQs (returns, shipping, payment, warranties, etc.)
    Use this when a customer asks a general informational question about policies
    or how things work — NOT for order status or product availability.
    """
    return search_knowledge_base(query)