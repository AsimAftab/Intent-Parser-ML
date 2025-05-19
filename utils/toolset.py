from langgraph import Tool

# Define your tools
def play_music(song: str) -> str:
    """Play a song from the library or online."""
    return f"🎵 Playing '{song}'..."

def open_chrome(website: str) -> str:
    """Open a website in Chrome."""
    return f"🌐 Opening Chrome at https://{website}"

def toggle_bluetooth(state: str) -> str:
    """Toggle Bluetooth on or off."""
    state = state.strip().lower()
    if state in ["on", "off"]:
        return f"📶 Bluetooth turned {state}"
    return "❌ Invalid state. Use 'on' or 'off'."

# Create LangGraph tools list
tools = [
    Tool(name="PlayMusic", function=play_music),
    Tool(name="OpenChrome", function=open_chrome),
    Tool(name="ToggleBluetooth", function=toggle_bluetooth),
]
