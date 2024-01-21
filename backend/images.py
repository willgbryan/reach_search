import os
import requests
from bs4 import BeautifulSoup
from langchain import hub
from langchain.agents import load_tools
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SearxSearchWrapper

class search_images():
    def __init__(self, llm: str, prompt: str):
        self.llm = ChatOpenAI(model=llm, temperature=0)
        self.role_preprompt = hub.pull("hwchase17/openai-functions-agent")
        self.prompt = prompt
        self.api_key = os.environ["OPENAI_API_KEY"]
        self.host = os.environ["SEARX_HOST"]

    def extract_image_url(self, page_url):
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            og_image = soup.find('meta', property='og:image')
            if og_image:
                return og_image['content']
        return None  # Fallback if no image is found

    def main(self):
        raw_search = SearxSearchWrapper(searx_host=self.host, engines=["google_images"])
        raw_results = raw_search.results(
            self.prompt, 
            num_results=5, 
            image_proxy=True, 
            engines=["google images"]
        )
        print(f'Raw output from engine: {raw_results}')
        results_with_images = []
        for result in raw_results:
            image_url = self.extract_image_url(result['link'])
            if image_url:
                results_with_images.append({
                    'pageUrl': result['link'],
                    'imageUrl': image_url
                })

        print(results_with_images)
        return results_with_images