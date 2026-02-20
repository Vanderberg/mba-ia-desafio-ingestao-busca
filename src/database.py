from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from config import config

def get_embeddings():
    return OpenAIEmbeddings(model=config.OPENAI_MODEL)

def get_vector_store():
    return PGVector(
        embeddings=get_embeddings(),
        collection_name=config.PG_VECTOR_COLLECTION_NAME,
        connection=config.DATABASE_URL,
        use_jsonb=True,
    )


