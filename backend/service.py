import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.videos import search_videos as search_videos
from backend.images import search_images as search_images
from backend.web import search_web as search_web

app = Flask(__name__)
CORS(app)

os.environ["OPENAI_API_KEY"] = "redact"
os.environ["SEARX_HOST"] = "http://localhost:8080"

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # video_searcher = search_videos(llm='gpt-4-1106-preview', prompt=prompt)
    image_searcher = search_images(llm='gpt-4-1106-preview', prompt=prompt)
    web_searcher = search_web(llm='gpt-4-1106-preview', prompt=prompt)

    # video_results = video_searcher.main()
    image_results = image_searcher.main()
    web_results = web_searcher.main()

    combined_results = {
        # 'videos': video_results,
        'images': image_results,
        'web': web_results
    }

    return jsonify(combined_results)

if __name__ == '__main__':
    app.run(debug=True)