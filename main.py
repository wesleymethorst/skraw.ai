from flask import Flask, request, jsonify
from flask_cors import CORS
from together import Together
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# CORS configuratie
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:5173", 
    "http://localhost:8080",
    "https://skraw.io",
    "https://www.skraw.io",
    "*"  # Voor development - verwijder dit later voor security
])

# Controleer of API key aanwezig is
if not os.getenv('TOGETHER_API_KEY'):
    print("❌ WARNING: TOGETHER_API_KEY environment variable not set!")

client = Together(api_key=os.getenv('TOGETHER_API_KEY'))

def log_message(message):
    """Hulpfunctie voor console logging met timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

@app.route('/', methods=['GET'])
def health_check():
    log_message("🟢 Health check endpoint accessed")
    return jsonify({
        "status": "OK", 
        "message": "Skraw.ai API is running",
        "has_api_key": bool(os.getenv('TOGETHER_API_KEY'))
    })

@app.route('/evaluate-guess', methods=['POST'])
def evaluate_guess():
    try:
        log_message("🔵 New request received at /evaluate-guess")
        
        data = request.get_json()
        target_word = data.get('target_word')
        user_guess = data.get('user_guess')
        
        log_message(f"📥 Input data: target_word='{target_word}', user_guess='{user_guess}'")
        
        if not target_word or not user_guess:
            log_message("❌ Missing required input data")
            return jsonify({"error": "target_word and user_guess are required"}), 400
        
        log_message("🤖 Sending request to Together AI...")
        
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Je bent een spelmaster. De speler moet een woord raden. "
                        "Beoordeel het gokwoord van de speler ten opzichte van het doelwoord. "
                        "Antwoord uitsluitend met één van deze woorden, en niets anders:\n"
                        "- Juist\n"
                        "- Bijna goed\n"
                        "- Zelfde thema\n"
                        "- Totaal fout"
                    )
                },
                {
                    "role": "user",
                    "content": f"Het doelwoord is '{target_word}'. De speler gokt: '{user_guess}'."
                }
            ]
        )
        
        ai_feedback = response.choices[0].message.content.strip()
        
        log_message(f"🧠 AI Response: '{ai_feedback}'")
        
        result = {
            "target_word": target_word,
            "user_guess": user_guess,
            "feedback": ai_feedback
        }
        
        log_message(f"📤 Sending response: {json.dumps(result, ensure_ascii=False)}")
        
        return jsonify(result)
        
    except Exception as e:
        error_msg = str(e)
        log_message(f"💥 Error occurred: {error_msg}")
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    log_message(f"🚀 Starting Skraw.ai API server on port {port}")
    log_message("🎯 Ready to evaluate guesses!")
    app.run(host='0.0.0.0', port=port, debug=False)