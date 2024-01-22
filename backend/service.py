import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.videos import search_videos as search_videos
from backend.images import search_images as search_images
from backend.web import search_web as search_web
from backend.search_pdfs import search_pdfs as search_pdfs
from werkzeug.utils import secure_filename
import logging


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'C:/Users/willb/OneDrive/Documents/GitHub/reach_search/uploads'

os.environ["OPENAI_API_KEY"] = ""
os.environ["SEARX_HOST"] = "http://localhost:8080"

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    files = request.files.getlist('files')
    for file in files:
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(file_path)
            except Exception as e:
                app.logger.error(f'Error saving file: {e}')
                return jsonify({"error": "Error saving file"}), 500

    return jsonify({"message": "Files successfully uploaded"}), 200

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
        'web': web_results,
    }

    pdf_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.pdf')]
    if pdf_files:
        print('PDF files found:', pdf_files)
        pdf_searcher = search_pdfs(collection_name='hold2', llm='gpt-4-1106-preview', prompt=prompt)
        pdf_results = pdf_searcher.main()
        combined_results['pdf'] = pdf_results

    return jsonify(combined_results)

if __name__ == '__main__':
    app.run(debug=True)