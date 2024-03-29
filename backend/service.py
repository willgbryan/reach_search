import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from videos import search_videos as search_videos
from images import search_images as search_images
from web import search_web as search_web
from search_pdfs import search_pdfs as search_pdfs

import logging
from typing import List

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.config = {
    'UPLOAD_FOLDER': 'C:/Users/willb/OneDrive/Documents/GitHub/reach_search/uploads'
}

@app.post('/upload')
async def upload_files(files: List[UploadFile] = File(...)):
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    uploaded_files = []
    for file in files:
        if file.filename.endswith('.pdf'):
            file_path = os.path.join(upload_folder, file.filename)
            try:
                with open(file_path, 'wb') as f:
                    content = await file.read()
                    f.write(content)
                uploaded_files.append(file.filename)
            except Exception as e:
                logging.error(f'Error saving file: {e}')
                raise HTTPException(status_code=500, detail="Error saving file")
    if not uploaded_files:
        raise HTTPException(status_code=400, detail="No PDF files uploaded")
    return JSONResponse(content={"message": "Files successfully uploaded"})

@app.post('/search')
async def search(request: Request):
    data = await request.json()
    prompt = data.get('prompt')
    
    if not prompt:
        raise HTTPException(status_code=400, detail="No prompt provided")

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

    return JSONResponse(combined_results)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)