import hashlib
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.constants import openai_api_key, azure_endpoint, openai_api_version, openai_api_type, embedding_deployment_name

persist_directory = "chroma_db"
embeddings = AzureOpenAIEmbeddings(openai_api_key=openai_api_key, openai_api_type=openai_api_type, deployment=embedding_deployment_name, model=embedding_deployment_name, openai_api_version=openai_api_version, azure_endpoint=azure_endpoint, chunk_size=512)

db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings,
    collection_metadata={"hnsw:space": "cosine"},
)

def documents_count():
    return len(db.get()['documents'])

def is_duplicate(doc_hash):
    collection = db.get()
    metadatas = collection.get("metadatas", [])
    for meta in metadatas:
        if meta.get("hash") == doc_hash:
            return True
    return False

def get_document_hash(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def save_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    unique_docs = []
    
    for doc in documents:
        doc_hash = get_document_hash(doc.page_content)
        if not is_duplicate(doc_hash):
            doc.metadata["hash"] = doc_hash
            unique_docs.append(doc)

    if not unique_docs:
          return

    docs = splitter.split_documents(unique_docs)
    Chroma.from_documents(
        documents=docs, embedding=embeddings, persist_directory=persist_directory
    )


def get_similarity(question):
    context = db.similarity_search(question)
    return context
