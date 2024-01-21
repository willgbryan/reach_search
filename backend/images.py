import os
from typing import Any
from langchain import hub
from langchain.agents import load_tools
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SearxSearchWrapper


class search_images():
    def __init__(self, llm: str, prompt: str):
        self.llm = ChatOpenAI(model=llm, temperature=0)
        self.role_preprompt = hub.pull("hwchase17/openai-functions-agent")
        self.prompt = prompt
        self.api_key = os.environ["OPENAI_API_KEY"]
        self.host = os.environ["SEARX_HOST"]

    def main(self):
        tools = load_tools(
            ["searx-search-results-json"], 
            searx_host="http://localhost:8080",
            engines=["google_images"],
            num_results=10,
        )
        
        # agent = create_openai_tools_agent(self.llm, tools, self.role_preprompt)
        # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

        # agent_response = agent_executor.invoke({'input': self.prompt})
        raw_search = SearxSearchWrapper(searx_host=self.host, engines=["google_images"])
        raw_results = raw_search.results(self.prompt, num_results = 5)

        print(raw_results)
        return raw_results
