import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

class CriminalCodeAssistant:
    def __init__(self):
        from config import (
            ARTICLES_JSON, FAISS_INDEX_FILE, EMBEDDINGS_FILE,
            EMBEDDING_MODEL
        )
        
        print("Loading Criminal Code Assistant...")
        
        with open(ARTICLES_JSON, 'r', encoding='utf-8') as f:
            self.articles = json.load(f)
        
        self.index = faiss.read_index(FAISS_INDEX_FILE)
        
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        
        metadata_file = EMBEDDINGS_FILE.replace('.npy', '_metadata.json')
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = [{"number": a["number"], "text": a["text"]} for a in self.articles]
        
        print(f"Assistant loaded with {len(self.articles)} articles")
    
    def find_relevant_articles(self, question, top_k=3):
        question_embedding = self.embedding_model.encode([question], convert_to_numpy=True)
        
        faiss.normalize_L2(question_embedding)
        
        scores, indices = self.index.search(question_embedding.astype('float32'), top_k)
        
        relevant_articles = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            article = self.articles[idx]
            relevant_articles.append({
                "article_number": article["number"],
                "article_text": article["text"],
                "full_text": article["full_text"],
                "similarity_score": float(score)
            })
        
        return relevant_articles
    
    def generate_answer(self, question, use_llm=False):
        relevant_articles = self.find_relevant_articles(question, top_k=3)
        
        if not relevant_articles:
            return {
                "answer": "Nuk u gjetën artikuj të përshtatshëm për këtë pyetje.",
                "articles": []
            }
        
        if use_llm and os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                
                context = "\n\n".join([
                    f"Artikulli {art['article_number']}: {art['article_text']}"
                    for art in relevant_articles
                ])
                
                prompt = f"""Bazuar në Kodin Penal të Shqipërisë, përgjigju pyetjes në shqip.

Pyetja: {question}

Artikujt relevante:
{context}

Jep një përgjigje të qartë dhe të saktë në shqip, duke cituar numrat e artikujve."""
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Ti je një asistent i specializuar që përgjigjet për Kodin Penal të Shqipërisë."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                
                answer = response.choices[0].message.content
                
            except Exception as e:
                print(f"Error using LLM: {e}")
                answer = self._build_simple_answer(relevant_articles, question)
        else:
            answer = self._build_simple_answer(relevant_articles, question)
        
        return {
            "answer": answer,
            "articles": relevant_articles
        }
    
    def _build_simple_answer(self, relevant_articles, question):
        answer_parts = []
        
        answer_parts.append("Bazuar në Kodin Penal të Shqipërisë, këtu janë informacionet relevante për pyetjen tuaj:\n\n")
        
        if len(relevant_articles) > 1:
            answer_parts.append(f"U gjetën {len(relevant_articles)} artikuj që lidhen me pyetjen tuaj. Këtu janë përmbajtjet e tyre:\n\n")
        else:
            answer_parts.append("Këtu është artikulli që lidhet me pyetjen tuaj:\n\n")
        
        for i, art in enumerate(relevant_articles, 1):
            article_content = art.get('full_text', art.get('article_text', ''))
            
            answer_parts.append(f"**Artikulli {art['article_number']}**\n")
            answer_parts.append(f"{article_content}\n\n")
            
            if i < len(relevant_articles):
                answer_parts.append("---\n\n")
        
        answer_parts.append("\nKëto janë dispozitat e Kodit Penal që lidhen më së shumti me pyetjen tuaj. ")
        answer_parts.append("Për informacion më të detajuar, ju lutem konsultohuni me tekstin e plotë të artikujve të listuar më sipër.")
        
        return "".join(answer_parts)
