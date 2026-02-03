import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os
from tqdm import tqdm

def load_articles(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    return articles

def create_embeddings(articles, model_name):
    print(f"Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)
    
    texts = [article['full_text'] for article in articles]
    
    print(f"Creating embeddings for {len(texts)} articles...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    
    return embeddings, model

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    
    index = faiss.IndexFlatL2(dimension)
    
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(dimension)
    
    index.add(embeddings.astype('float32'))
    
    return index

def save_index(index, embeddings, articles, index_file, embeddings_file):
    os.makedirs(os.path.dirname(index_file), exist_ok=True)
    
    faiss.write_index(index, index_file)
    print(f"Saved FAISS index to {index_file}")
    
    np.save(embeddings_file, embeddings)
    print(f"Saved embeddings to {embeddings_file}")
    
    metadata_file = embeddings_file.replace('.npy', '_metadata.json')
    metadata = [{"number": a["number"], "text": a["text"]} for a in articles]
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Saved metadata to {metadata_file}")

def main():
    from config import ARTICLES_JSON, EMBEDDINGS_FILE, FAISS_INDEX_FILE, EMBEDDING_MODEL
    
    print("=" * 60)
    print("Creating FAISS Index for Articles")
    print("=" * 60)
    
    if not os.path.exists(ARTICLES_JSON):
        print(f"Error: Articles file not found: {ARTICLES_JSON}")
        print("Please run download_code.py first to create articles.json")
        return
    
    print(f"\nLoading articles from {ARTICLES_JSON}...")
    articles = load_articles(ARTICLES_JSON)
    print(f"Loaded {len(articles)} articles")
    
    embeddings, model = create_embeddings(articles, EMBEDDING_MODEL)
    print(f"\nCreated embeddings with shape: {embeddings.shape}")
    
    print("\nCreating FAISS index...")
    index = create_faiss_index(embeddings)
    print(f"Index created with {index.ntotal} vectors")
    
    save_index(index, embeddings, articles, FAISS_INDEX_FILE, EMBEDDINGS_FILE)
    
    print("\n" + "=" * 60)
    print("Index creation completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
