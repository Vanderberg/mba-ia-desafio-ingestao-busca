import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "text-embedding-3-small")
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
        self.PDF_PATH = os.getenv("PDF_PATH")
        
        # Google AI Variables (optional based on what embeddings you use, but kept here for completeness)
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")

        self.validate()

    def validate(self):
        # Validate the necessary environment variables
        required_vars = [
            ("OPENAI_API_KEY", self.OPENAI_API_KEY),
            ("DATABASE_URL", self.DATABASE_URL),
            ("PG_VECTOR_COLLECTION_NAME", self.PG_VECTOR_COLLECTION_NAME),
            ("PDF_PATH", self.PDF_PATH)
        ]
        
        for name, value in required_vars:
            if not value:
                raise RuntimeError(f"Environment variable {name} is not set")

config = Config()
