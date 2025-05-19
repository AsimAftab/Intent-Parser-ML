from utils.llm_utils import query_mistral

def parse_intent_with_llm(command: str):
    # Prepare the prompt to extract Intent, Tool, Arguments, and Confidence Score
    system_prompt = f"""
    Extract the following information from the user's command:
    Intent: What does the user want?
    Tool: Which function or module should be invoked?
    Arguments: What parameters are required?
    Confidence Score: How confident is the model in the prediction return values between 0 and 1?

    User Command: {command}
    """

    # Send the prompt to Mistral (via your query_mistral function)
    response = query_mistral(system_prompt)
    
    # Check if the response is a string (plain text)
    if isinstance(response, str):
        # Attempt to parse the response string into a dictionary if it looks like JSON
        try:
            # Assuming Mistral response could be something like {"intent": "...", "tool": "...", etc.}
            import json
            response_dict = json.loads(response)
        except json.JSONDecodeError:
            # If it's not JSON, assume it's just a plain text response
            # Extract intent, tool, arguments, and confidence score from plain text
            response_dict = {
                'intent': 'Unknown',
                'tool': 'Unknown',
                'arguments': 'None',
                'confidence_score': 'N/A'
            }
            print(f"Response parsing failed, raw response: {response}")
    else:
        # If response is not a string, handle it as structured data directly
        response_dict = response
    
    # Return the structured response
    return response_dict

# Example usage
command = "open Spotify and play music"
result = parse_intent_with_llm(command)

if result:
    print("Intent:", result['intent'])
    print("Tool:", result['tool'])
    print("Arguments:", result['arguments'])
    print("Confidence Score:", result['confidence_score'])
else:
    print("Error in processing the query.")
