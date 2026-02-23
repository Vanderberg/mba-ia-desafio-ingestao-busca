import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

for k in ("OPENAI_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")


PDF_PATH = os.getenv("PDF_PATH")

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


provider = os.getenv("ACTIVE_PROVIDER", "openai").lower()

if provider == "openai":
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
elif provider == "gemini":
    embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001"))
else:
    raise ValueError(f"Provedor {provider} não suportado.")

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,
)


# Ingestão em lotes para evitar erro 429 (Rate Limit) do Gemini
batch_size = 5
for i in range(0, len(enriched), batch_size):
    batch = enriched[i : i + batch_size]
    batch_ids = ids[i : i + batch_size]
    
    print(f"Ingerindo lote {i//batch_size + 1} ({len(batch)} documentos)...")
    store.add_documents(documents=batch, ids=batch_ids)
    
    if i + batch_size < len(enriched):
        print("Aguardando 2 segundos para respeitar limite de cota...")
        time.sleep(2)

print("\n*** Ingestão finalizada com sucesso! Vetores armazenados no Postgres/pgvector. ***")