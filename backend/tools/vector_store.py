import numpy as np
import faiss
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.config import Config

class VectorStore:
    def __init__(self):
        pass

    def chunk_data(self, data):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP_SIZE,
            length_function=len
        )

        chunked_documents = []
        for url, content in data.items():
            chunks = text_splitter.create_documents([content], metadatas=[{"url": url}])
            chunked_documents.extend(chunks)
        return chunked_documents
    
    def store_data(self, data):
        # Step 1: Chunk the data
        chunked_documents = self.chunk_data(data)

        # Check if chunked_documents is not empty
        if not chunked_documents:
            raise ValueError("No valid chunks generated. Check the input data.")

        # Step 2: Initialize embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=Config.GOOGLE_API_KEY,
            model=Config.GOOGLE_EMBEDDING_MODEL
        )

        vector_store = FAISS.from_documents(
            chunked_documents, embeddings
        )

        return vector_store