from utils.speech_recognizer import SpeechRecognitionAgent, default_callback
import time

def run_single_command_test(agent):
    """
    Test listening to a single voice command.
    """
    print("🧪 Testing single command listening...")
    command = agent.listen_command(timeout=5, phrase_time_limit=10)
    if command:
        print(f"✅ Processing command: {command}")
    else:
        print("⚠️ No command received.")


def run_background_listener(agent):
    """
    Start and manage continuous background listening.
    """
    print("🟢 Starting continuous background listening... Press Ctrl+C to stop.")
    stop_listening = agent.listen_in_background(default_callback)
    try:
        while True:
            time.sleep(0.1)  # Prevent CPU overuse
    except KeyboardInterrupt:
        print("\n🛑 Stopping background listening...")
        stop_listening(wait_for_stop=True)
        print("👋 Program terminated.")


def main():
    agent = SpeechRecognitionAgent(energy_threshold=400, pause_threshold=1.0)

    if agent.adjust_for_ambient_noise(duration=1):
        run_single_command_test(agent)
        run_background_listener(agent)
    else:
        print("❌ Could not calibrate microphone. Exiting.")


if __name__ == "__main__":
    main()
