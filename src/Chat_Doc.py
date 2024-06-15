import faiss 
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import os 
import time
from groq import Groq 
from typing import List

class Chat_Documents:
    def __init__(self, filepath : str, embedder_name : str, api_key : str):
        self.filepath = filepath
        self.embedder = SentenceTransformer(embedder_name)
        self.vector_store = faiss.IndexFlatL2(self.embedder.get_sentence_embedding_dimension())
        self.client = Groq(api_key=api_key)

    def preprocess(self):
        file_extension = self.filepath.split(".")[-1].lower()
        t0 = time.time()
        if file_extension == 'pdf':
            with open(self.filepath, 'rb') as file:
                pdf_reader = PdfReader(file)
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text()
                print("[INFO] Finshed Extracting data from .pdf")

        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[" ", ",", "\n"],
        )
        self.chunks = text_splitter.split_text(content)
        vectors = self.embedder.encode(self.chunks)
        self.vector_store.add(vectors)
        t1 = time.time()
        print(f"Vectors loaded in {t1 - t0} seconds")

    def chat_doc(self, query : str):
        k = 3 
        t0 = time.time()
        query_vector = self.embedder.encode([query])
        distances , indices = self.vector_store.search(query_vector, k)
        texts = [self.chunks[i] for i in indices[0]]
        chat_completion = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages= [
                    {
                        "role" : "user",
                        "content" : f"You are a helpful assistant, you will be provided with extra information to answer the question. If you cannot answer the question with the data provided just say so, do not generate incorrect answers. This is the extra information {texts}"
                    },
                    {
                        "role" : "user",
                        "content" : f" {query}"
                    }
                ]
            )
        response = chat_completion.choices[0].message.content
        t1 = time.time()
        print(f"Elapsed time {t1 - t0} seconds")
        return response

