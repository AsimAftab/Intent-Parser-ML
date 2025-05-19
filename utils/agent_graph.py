# Assuming the latest version requires a different approach for building the graph

from langchain_community.chat_models import ChatOllama
from langgraph import ToolNode  # Check if ToolNode exists in the current version
from utils.toolset import tools

# Initialize the LLM (ensure Ollama is running with Mistral model)
llm = ChatOllama(model="mistral")

# Define the tool node if ToolNode is available
tool_node = ToolNode(tools)

# Example function to process commands and interact with the tools
def process_command(command: str):
    # Simulate tool interaction (assuming LangGraph now uses a different structure)
    result = tool_node.invoke({"command": command})
    return result.get("message", "No valid response")

# Call the function with a sample command
response = process_command("Play music")
print(response)
