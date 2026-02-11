from flask import Flask, render_template, request, jsonify
import os
from chatbot import CriminalCodeAssistant

app = Flask(__name__)

assistant = None

def get_assistant():
    global assistant, assistant_error
    if assistant is None and assistant_error is None:
        try:
            from chatbot import CriminalCodeAssistant
            print("Initializing CriminalCodeAssistant...")
            assistant = CriminalCodeAssistant()
            print("CriminalCodeAssistant initialized successfully")
        except Exception as e:
            error_msg = f"Failed to initialize assistant: {str(e)}"
            print(error_msg)
            print(traceback.format_exc())
            assistant_error = error_msg
            raise
    
    if assistant_error:
        raise Exception(assistant_error)
    
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
        error_msg = str(e)
        print(f"Error in ask_question: {error_msg}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'Gabim: {str(e)}'
        }), 500

@app.route('/health')
def health():
    try:
        get_assistant()
        return jsonify({
            'status': 'ok',
            'assistant_loaded': assistant is not None
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'assistant_loaded': False
        }), 500

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
