"""
speech_engine.py
----------------
Handles all voice input (speech-to-text) and voice output (text-to-speech).
"""

import speech_recognition as sr
import pyttsx3
import logging

# ── Logger ──────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ── Text-to-Speech Engine ────────────────────────────────────────────────────

def init_tts_engine(rate: int = 175, volume: float = 1.0) -> pyttsx3.Engine:
    """
    Initialise and return a pyttsx3 TTS engine.

    Args:
        rate:   Speech rate in words per minute (default 175).
        volume: Volume level 0.0 – 1.0 (default 1.0).

    Returns:
        Configured pyttsx3.Engine instance.
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    # Prefer a female voice when available
    voices = engine.getProperty("voices")
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break

    return engine


def speak(engine: pyttsx3.Engine, text: str) -> None:
    """
    Convert *text* to speech and play it through the speakers.

    Args:
        engine: Initialised pyttsx3 engine.
        text:   The string to speak aloud.
    """
    logger.info("Assistant: %s", text)
    print(f"\n🔊  Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


# ── Speech-to-Text (Microphone) ──────────────────────────────────────────────

def listen(engine: pyttsx3.Engine, timeout: int = 5, phrase_limit: int = 10) -> str:
    """
    Listen for a single voice command from the microphone and return it as
    lowercase text.

    Args:
        engine:       TTS engine used to speak error messages back to the user.
        timeout:      Seconds to wait for speech to begin (default 5).
        phrase_limit: Maximum seconds to record a single phrase (default 10).

    Returns:
        Recognised command as a lowercase string, or an empty string on failure.
    """
    recogniser = sr.Recognizer()
    recogniser.pause_threshold = 0.8   # seconds of silence before phrase ends
    recogniser.energy_threshold = 300  # mic sensitivity

    with sr.Microphone() as source:
        print("\n🎤  Listening…  (speak now)")
        recogniser.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recogniser.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        except sr.WaitTimeoutError:
            logger.warning("No speech detected within timeout.")
            return ""

    try:
        command = recogniser.recognize_google(audio).lower()
        print(f"✅  You said: \"{command}\"")
        logger.info("Recognised: %s", command)
        return command

    except sr.UnknownValueError:
        speak(engine, "Sorry, I didn't catch that. Could you please repeat?")
        return ""

    except sr.RequestError as exc:
        speak(engine, "There was a problem connecting to the speech service.")
        logger.error("SpeechRecognition RequestError: %s", exc)
        return ""
