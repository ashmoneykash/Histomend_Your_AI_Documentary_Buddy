# main.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

YOUTUBE_API_KEY = 'your_key_here'

@app.route('/suggest', methods=['POST'])
def suggest():
    user_input = request.json['query']
    response = requests.get(f"https://www.googleapis.com/youtube/v3/search",
                            params={
                                'part': 'snippet',
                                'q': f"{user_input} history documentary",
                                'type': 'video',
                                'key': YOUTUBE_API_KEY,
                                'maxResults': 5
                            })
    results = response.json().get('items', [])
    output = [{
        'title': item['snippet']['title'],
        'thumbnail': item['snippet']['thumbnails']['medium']['url'],
        'videoId': item['id']['videoId']
    } for item in results]
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
