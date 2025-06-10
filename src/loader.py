import os
import tempfile
import PyPDF2
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from src.rag_engine import save_documents

def upload_files(uploaded_files):
    for uploaded_file in uploaded_files:
        suffix = os.path.splitext(uploaded_file.name)[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        if uploaded_file.name.endswith(".txt"):
            loader = TextLoader(tmp_path, encoding="utf-8")
        elif uploaded_file.name.endswith(".pdf"):
            loader = PyPDFLoader(tmp_path)

        documents = loader.load()
        save_documents(documents)

def extract_text(file):
    if file.type == "text/plain":
        return file.read().decode("utf-8")

    elif file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text

    else:
        return "Unsupported file type"