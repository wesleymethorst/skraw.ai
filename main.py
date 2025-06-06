from flask import Flask, request, jsonify
from together import Together
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Together(api_key=os.getenv('TOGETHER_API_KEY'))

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "message": "Skraw.ai API is running"})

@app.route('/evaluate-guess', methods=['POST'])
def evaluate_guess():
    try:
        data = request.get_json()
        target_word = data.get('target_word')
        user_guess = data.get('user_guess')
        
        if not target_word or not user_guess:
            return jsonify({"error": "target_word and user_guess are required"}), 400
        
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Je bent een spelmaster. De speler moet een woord raden. "
                        "Beoordeel het gokwoord van de speler ten opzichte van het doelwoord. "
                        "Antwoord uitsluitend met één van deze woorden, en niets anders:\n"
                        "- juist\n"
                        "- bijna goed\n"
                        "- zelfde thema\n"
                        "- totaal fout"
                    )
                },
                {
                    "role": "user",
                    "content": f"Het doelwoord is '{target_word}'. De speler gokt: '{user_guess}'."
                }
            ]
        )
        
        ai_feedback = response.choices[0].message.content.strip()
        
        return jsonify({
            "target_word": target_word,
            "user_guess": user_guess,
            "feedback": ai_feedback
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)