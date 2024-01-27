import os
from backend.web import search_web
from backend.images import search_images
from backend.search_pdfs import search_pdfs
import streamlit as st

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SEARX_HOST"] = "http://localhost:8080"

uploads_dir = 'uploads'
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

web = st.checkbox('Perform web search')

with st.sidebar:
    uploaded_files = st.file_uploader('Choose a folder to upload', accept_multiple_files=True)

for uploaded_file in uploaded_files:
    file_path = os.path.join(uploads_dir, uploaded_file.name)
    with open(file_path, 'wb') as f:
        content = uploaded_file.read()
        f.write(content)

prompt = st.chat_input()
with st.status('Processing Input Params', expanded=True) as status:
    if prompt:
        if web:
            # image_searcher = search_images(llm='gpt-4-1106-preview', prompt=prompt)
            web_searcher = search_web(llm='gpt-4-1106-preview', prompt=prompt)

            # image_results = image_searcher.main()
            st.write('Beginning web search...')
            web_results = web_searcher.main()
            st.write('Web search complete...')

            with st.chat_message('user'):
                st.write(f'Web Search Results: {web_results}')

        pdf_files_exist = any(f.endswith('.pdf') for f in os.listdir('uploads'))
        if pdf_files_exist:
            st.write('Beginning PDF processing and search. This can take some time...')
            pdf_searcher = search_pdfs(collection_name='hold2', llm='gpt-4-1106-preview', prompt=prompt)
            pdf_results = pdf_searcher.main()
            st.write('PDF search complete...')

            with st.chat_message('user'):
                st.write(f'PDF Search Results: {pdf_results}')
        
        status.update(label='All processes complete...', state='complete', expanded=True)