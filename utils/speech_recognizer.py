import speech_recognition as sr
from utils.intent_parser_test import parse_intent_with_llm

# from utils.intent_parser import parse_and_execute

WAKE_WORD = "hey jarvis"

def is_wake_word(text: str) -> bool:
    """Checks if the wake word is present in the speech."""
    return WAKE_WORD in text.lower()

class SpeechRecognitionAgent:
    """A modular speech recognition agent for capturing and processing voice commands."""
    
    def __init__(self, api_key=None, energy_threshold=300, pause_threshold=0.8):
        """
        Initialize the speech recognition agent with customizable settings.
        
        Args:
            api_key (str, optional): Google Speech Recognition API key. Defaults to None (uses default key).
            energy_threshold (int): Energy level for detecting speech (default: 300).
            pause_threshold (float): Seconds of silence before stopping recording (default: 0.8).
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.api_key = api_key
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold
        self.recognizer.dynamic_energy_threshold = True  # Automatically adjust for ambient noise

    def adjust_for_ambient_noise(self, duration=1):
        """
        Calibrate the recognizer to filter out ambient noise.
        
        Args:
            duration (float): Seconds to analyze ambient noise (default: 1).
        
        Returns:
            bool: True if calibration succeeded, False otherwise.
        """
        try:
            with self.microphone as source:
                print(f"🔊 Adjusting for ambient noise ({duration}s)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
                print("✅ Ambient noise adjustment complete.")
                return True
        except Exception as e:
            print(f"❌ Failed to adjust for ambient noise: {e}")
            return False

    def listen_command(self, timeout=5, phrase_time_limit=10):
        """
        Listen for a single voice command and return the recognized text.
        
        Args:
            timeout (float): Seconds to wait for speech to start (default: 5).
            phrase_time_limit (float): Maximum seconds for a single phrase (default: 10).
        
        Returns:
            str or None: Recognized text if successful, None if failed.
        """
        with self.microphone as source:
            print("🎤 Listening for your command...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            except sr.WaitTimeoutError:
                print("❌ No speech detected within timeout.")
                return None

        return self._recognize_audio(audio)

    def listen_in_background(self, callback):
        """
        Start continuous background listening with the provided callback function.
        
        Args:
            callback (callable): Function to process recognized audio (takes recognizer and audio args).
        
        Returns:
            callable: Function to stop background listening.
        """
        print("🎤 Starting background listening...")
        return self.recognizer.listen_in_background(self.microphone, callback)

    def _recognize_audio(self, audio):
        """
        Recognize speech from audio data using Google Speech Recognition.
        
        Args:
            audio (AudioData): Audio data to recognize.
        
        Returns:
            str or None: Recognized text if successful, None if failed.
        """
        try:
            if self.api_key:
                text = self.recognizer.recognize_google(audio, key=self.api_key)
            else:
                text = self.recognizer.recognize_google(audio)
            print(f"🗣️ Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition service error: {e}")
            return None

def default_callback(recognizer, audio):
    """
    Callback function for background listening that checks for wake word and parses the command.
    
    Args:
        recognizer (Recognizer): The recognizer instance.
        audio (AudioData): Captured audio data.
    """
    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ Heard: {text}")
        
        if is_wake_word(text):
            print("✅ Wake word detected. Listening for command...")
            # Capture the command after the wake word
            command = text.lower().replace(WAKE_WORD, "").strip()
            if not command:
                # If the command is empty, listen again
                print("⏸️ No command detected. Listening again...")
                with sr.Microphone() as source:  # Use the microphone properly
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio)

            # Parsing the command's intent using the LLM
            intent = parse_intent_with_llm(command)
            # intent=parse_and_execute(command)
            print(f"🎯 Intent parsed: {intent}")
            
            # Call a handler based on the parsed intent
            handle_intent(intent, command)

        else:
            print("⏸️ Wake word not detected.")
    
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError as e:
        print(f"❌ Recognition error: {e}")


def handle_intent(intent, command):
    """
    Handle the action based on the recognized intent.

    Args:
        intent (str): The parsed intent from LLM.
        command (str): The voice command that was processed.
    """
    print(f"🔧 Handling intent: {intent} with command: '{command}'")
    # You can add specific intent handlers here, for example:
    if intent == "play_music":
        print("🎵 Playing music...")
    elif intent == "turn_on_lights":
        print("💡 Turning on lights...")
    else:
        print("❓ Unknown intent.")
