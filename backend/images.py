import os
from langchain import hub
from langchain.agents import load_tools
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_models import ChatOpenAI


class search_web():
    def __init__ (
            self,
            llm: str,
            prompt: str,
    ):
        self.llm = ChatOpenAI(model=llm, temperature=0)
        self.tools = load_tools(
            ["searx-search-results-json"], 
            searx_host="http://localhost:8080",
            engines=["google_images"],
            num_results=10,
            ),
        self.role_preprompt = hub.pull("hwchase17/openai-functions-agent")
        self.prompt = prompt
        self.api_key = os.environ["OPENAI_API_KEY"]
        self.host = os.environ["SEARX_HOST"]
    
    def main(self):
        agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        results = agent_executor.invoke(
            {"input": self.prompt}
        )

        return results