import requests

def query_mistral(prompt: str, model: str = "mistral") -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=10
        )
        response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx, 5xx)
        
        # Check if the response contains the expected 'response' field
        response_data = response.json()
        if "response" in response_data:
            return response_data["response"].strip()
        else:
            print("❌ LLM Error: 'response' field missing in response.")
            return "error"
    except requests.exceptions.Timeout:
        print("❌ LLM Request Timeout")
        return "error"
    except requests.exceptions.RequestException as e:
        print(f"❌ LLM Error: {e}")
        return "error"
