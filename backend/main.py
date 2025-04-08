from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Mock historical database (we'll later replace this with an API)
documentaries = {
    "world war": ["The War (2007)", "World War II in Colour", "Apocalypse: The Second World War"],
    "ancient egypt": ["Secrets of the Pharaohs", "Egypt's Lost Queens", "The Story of Egypt"],
    "cold war": ["The Cold War - CNN", "The Fog of War", "Commanding Heights"],
    "india": ["The Story of India", "Gandhi (1982)", "Indus: The Unvoiced Civilization"]
}

@app.route('/')
def home():
    return "Welcome to Histomend: Your AI Documentary Buddy!"

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    query = data.get("query", "").lower()

    # Find suggestions
    suggestions = []
    for topic, films in documentaries.items():
        if topic in query:
            suggestions = films
            break

    if not suggestions:
        suggestions = random.choice(list(documentaries.values()))

    return jsonify({"suggestions": suggestions})

if __name__ == '__main__':
    app.run(debug=True)
