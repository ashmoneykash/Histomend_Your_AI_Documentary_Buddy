from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_youtube(query, max_results=6):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=f"{query} history documentary",
        part="snippet",
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response['items']:
        title = item['snippet']['title']
        desc = item['snippet']['description'][:150] + "..."
        video_id = item['id']['videoId']
        thumb_url = item['snippet']['thumbnails']['high']['url']
        url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append((title, desc, thumb_url, url))  # <--- return as tuple
    return videos

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    suggestions = search_youtube(query)
    return jsonify({"suggestions": suggestions})

@app.route('/')
def home():
    return "Welcome to Histomend: Your AI Documentary Buddy!"

if __name__ == '__main__':
    app.run(debug=True)
