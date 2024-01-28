import os
import json
from langchain import hub
from utils import send_request_to_gpt
# from langchain.agents import load_tools
# from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SearxSearchWrapper


class search_web():
    def __init__ (
            self,
            llm: str,
            prompt: str,
    ):
        # self.llm = ChatOpenAI(model=llm, temperature=0)
        # self.role_preprompt = hub.pull("hwchase17/openai-functions-agent")
        self.prompt = prompt
        self.role_preprompt = "You are a search assistant that takes a user question and search data to produce a meaningful answer."
        self.api_key = os.environ["OPENAI_API_KEY"]
        self.host = os.environ["SEARX_HOST"]
    
    def main(self):
        # # TODO find a smarter way to enable the agent to yield any real value
        # tools = load_tools(
        #     ["searx-search-results-json"], 
        #     searx_host="http://localhost:8080",
        #     engines=["google"],
        #     num_results=10,
        #     )

        # # response quality can be significantly increased by following the sources provided 
        # # and scraping out the text to pass to the agent, currently all we pass is the 
        # # 'snippet' value from th raw_results response
        # agent = create_openai_tools_agent(self.llm, tools, self.role_preprompt)
        # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        raw_search = SearxSearchWrapper(searx_host=self.host)
        search_results = raw_search.results(self.prompt, num_results = 5, engines=['google'])
        raw_results = json.dumps(search_results, default=str)
        print(f'Web engine output: {raw_results}')

        # results = agent_executor.invoke(
        #     {"input": f'Answer the following: {self.prompt}. Use the following information to generate your answer: {raw_results}. IMPORTANT: Cite your sources. If you dont know the answer just say you dont know.'}
        # )

        return_response = send_request_to_gpt(
            role_preprompt = self.role_preprompt,
            prompt = f'Answer the following: {self.prompt}. Use the following information to generate your answer: {raw_results}. IMPORTANT: Cite your sources. If you dont know the answer just say you dont know.',
            context=[{'role': 'user', 'content': raw_results}],
            stream = False
        )

        print(f'web response: {return_response}')
        return return_response