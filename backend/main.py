from flask import Flask, request, jsonify
from googleapiclient.discovery import build

app = Flask(__name__)

# 🔑 Replace this with your actual API key
YOUTUBE_API_KEY = "AIzaSyB0W8aYkkLfKa9ZacjKX0nO4HFWBmJXogs"

def search_youtube(query, max_results=5):
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
        video_id = item['id']['videoId']
        url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append(f"{title} - {url}")
    return videos

@app.route('/')
def home():
    return "Welcome to Histomend: Your AI Documentary Buddy!"

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    query = data.get("query", "").lower()

    try:
        suggestions = search_youtube(query)
        return jsonify({"suggestions": suggestions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
