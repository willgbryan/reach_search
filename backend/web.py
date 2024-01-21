import os
from langchain import hub
from langchain.agents import load_tools
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SearxSearchWrapper


class search_web():
    def __init__ (
            self,
            llm: str,
            prompt: str,
    ):
        self.llm = ChatOpenAI(model=llm, temperature=0)
        self.role_preprompt = hub.pull("hwchase17/openai-functions-agent")
        self.prompt = prompt
        self.api_key = os.environ["OPENAI_API_KEY"]
        self.host = os.environ["SEARX_HOST"]
    
    def main(self):
        tools = load_tools(
            ["searx-search-results-json"], 
            searx_host="http://localhost:8080",
            engines=["google"],
            num_results=10,
            )

        agent = create_openai_tools_agent(self.llm, tools, self.role_preprompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        raw_search = SearxSearchWrapper(searx_host=self.host)
        raw_results = raw_search.results(self.prompt, num_results = 5)

        results = agent_executor.invoke(
            {"input": f'Answer the following: {self.prompt}. Ground your results in {raw_results} and cite your sources. If you dont know the answer just say you dont know.'}
        )

        return results