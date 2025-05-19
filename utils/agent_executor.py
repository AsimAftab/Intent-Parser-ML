# utils/agent_executor.py

from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, AgentType
from utils.toolset import tools

# Initialize the Mistral LLM (make sure `ollama run mistral` is running)
llm = Ollama(model="mistral")

# Agent setup using tools
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)
