from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.documents import Document
from database import get_vector_store

from config import config

PDF_PATH = config.PDF_PATH

loader = PyPDFLoader(PDF_PATH)
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    add_start_index=False
)

chunks = splitter.split_documents(documents)

if not chunks:
    raise SystemError(0)


enriched = [
    Document(
        page_content=d.page_content,
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
    )
    for d in chunks
]    

ids = [f"doc-{i}" for i in range(len(enriched))]



store = get_vector_store()

store.add_documents(documents=enriched, ids=ids)

print("*** Ingestão finalizada com sucesso! Vetores armazenados no Postgres/pgvector. ***")