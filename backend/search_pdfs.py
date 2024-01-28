import os
import json
import chromadb
import pandas as pd
from openai import OpenAI
from utils import send_request_to_gpt
from langchain.document_loaders import PyPDFLoader


class search_pdfs:
    def __init__(
            self,
            collection_name: str,
            llm: str,
            prompt: str,    
        ):
        self.prompt = prompt
        self.role_preprompt = "You are a search assistant that takes a user question and search data to produce a meaningful answer."
        self.collection_name = collection_name
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    def get_embedding(self, text, model="text-embedding-ada-002"):
        return self.client.embeddings.create(input = [text], model=model).data[0].embedding
    
    def parse_pdfs(self):

        uploads_path = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        file_contents = {}

        pdf_files = [f for f in os.listdir(uploads_path) if f.endswith('.pdf')]
        for file in pdf_files:
            loader = PyPDFLoader(os.path.join(uploads_path, file))
            pages = loader.load_and_split()

            for page_counter, page in enumerate(pages):
                file_contents[f'{file}_{page_counter}'] = page

        return file_contents

    def build_contents_table(self):
        table_rows = []

        file_contents = self.parse_pdfs()

        for file_page, document in file_contents.items():
            file_name, page_num = file_page.rsplit('_', 1)
            page_content = document.page_content
            table_rows.append({
                "file_name": file_name,
                "page_num": int(page_num),
                "page_contents": page_content
            })

        contents_table = pd.DataFrame(table_rows)
        contents_table.sort_values(by=["file_name", "page_num"], inplace=True)
        contents_table.reset_index(drop=True, inplace=True)

        return contents_table

    def row_chunking(self, row):
            page_contents = row['page_contents']

            if '  ' in page_contents:
                page_contents = page_contents.replace(' ', '')
                page_contents = page_contents.replace('  ', ' ')
            chunks = page_contents.split('\n')

            return chunks

    def create_embeddings_by_chunk(self, df):
            new_table = []
            for index, row in df.iterrows():
                chunks = self.row_chunking(row)
                chunk_embeddings = {chunk: self.get_embedding(chunk) for chunk in chunks if chunk}
                new_row = {
                    'chunk_embeddings': chunk_embeddings,
                    'file_name': row['file_name'],
                    'page_num': row['page_num']
                }
                new_table.append(new_row)
            return pd.DataFrame(new_table)

    def add_to_collection(self, df, embeddings_col, collection):

            app_count = 0
            for _, row in df.iterrows():
                embeddings_dict = row[embeddings_col]
                for key, value in embeddings_dict.items():

                    file = row['file_name']
                    page_num = row['page_num']
                    metadata = f'{file}_page_number:{page_num}'
                
                    collection.add(
                        embeddings=[value],
                        documents=[key],
                        metadatas=[{"file": metadata}],
                        ids=[f'app_{app_count}: {file}']
                    )

                    app_count += 1
    def main(self):
        vdb_client = chromadb.Client()
        if not vdb_client.list_collections():
            collection = vdb_client.create_collection(name=self.collection_name)
            pdf_info_df = self.build_contents_table()
            embedding_df = self.create_embeddings_by_chunk(pdf_info_df)
            self.add_to_collection(embedding_df, 'chunk_embeddings', collection)
        else:
            collection = vdb_client.get_collection(name=self.collection_name)
            print(f'Available collections: {vdb_client.list_collections()}')
            pass
            
        query_embedding = self.get_embedding(self.prompt)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=10
        )
        
        context_friendly_results = json.dumps(results, default=str)
        
        print(f'PDF search results: {context_friendly_results}')

        return_response = send_request_to_gpt(
            role_preprompt=self.role_preprompt,
            prompt=f'Answer the following: {self.prompt}. Use the following information to generate your answer: {context_friendly_results}. IMPORTANT: Cite your sources. If you dont know the answer just say you dont know.',
            context=[{'role': 'user', 'content': context_friendly_results}],
            stream=False,
            )

        print(f'Search response: {return_response}')

        return return_response
