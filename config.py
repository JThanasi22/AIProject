import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
LLM_MODEL = "gpt-3.5-turbo"

DATA_DIR = "data"
ARTICLES_JSON = os.path.join(DATA_DIR, "articles.json")
EMBEDDINGS_FILE = os.path.join(DATA_DIR, "embeddings.npy")
FAISS_INDEX_FILE = os.path.join(DATA_DIR, "faiss_index.index")

HOST = "0.0.0.0"
PORT = 8080
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
