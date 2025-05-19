# # utils/intent_parser.py

# from utils.agent_executor import agent

# def parse_and_execute(command: str) -> str:
#     try:
#         return agent.run(command)
#     except Exception as e:
#         return f"❌ Failed to process command: {str(e)}"

# from langgraph.messages import HumanMessage
# from utils.agent_graph import graph  # Import the graph we built
# Second Iteration
# def parse_and_execute(command: str) -> str:
#     try:
#         # Pass the command to the graph and get the response
#         result = graph.invoke({"messages": [HumanMessage(content=command)]})
#         messages = result.get("messages", [])
#         if messages:
#             return messages[-1].content  # Return the latest message from the graph
#         return "🤖 No response generated."  # Default response if no message generated
#     except Exception as e:
#         return f"❌ Error: {str(e)}"  # Handle errors gracefully

from utils.agent_graph import graph  # Import the graph we built

def parse_and_execute(command: str) -> str:
    try:
        # Pass the command as a string (no need for HumanMessage, unless LangGraph expects a specific object)
        result = graph.invoke({"input": command})  # We pass the command directly to the graph
        
        # Assuming the response is in the form of a dictionary, with the result in "output"
        response = result.get("output", "🤖 No response generated.")  # Default response if no output
        return response
    except Exception as e:
        return f"❌ Error: {str(e)}"  # Handle any errors gracefully
