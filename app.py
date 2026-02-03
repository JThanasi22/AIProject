from flask import Flask, render_template, request, jsonify
import os
from chatbot import CriminalCodeAssistant

app = Flask(__name__)

assistant = None

def get_assistant():
    global assistant
    if assistant is None:
        assistant = CriminalCodeAssistant()
    return assistant

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'error': 'Ju lutem shkruani një pyetje.'
            }), 400
        
        assistant = get_assistant()
        result = assistant.generate_answer(question, use_llm=False)
        
        return jsonify({
            'answer': result['answer'],
            'articles': result['articles']
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Gabim: {str(e)}'
        }), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    from config import HOST, PORT
    
    from config import FAISS_INDEX_FILE, ARTICLES_JSON
    
    if not os.path.exists(FAISS_INDEX_FILE) or not os.path.exists(ARTICLES_JSON):
        print("Warning: Index or articles file not found!")
        print("Please run:")
        print("  1. python download_code.py")
        print("  2. python create_index.py")
        print("before starting the web server.")
    
    app.run(host=HOST, port=PORT, debug=True)
