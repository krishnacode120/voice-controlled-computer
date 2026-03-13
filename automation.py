"""
automation.py
-------------
Low-level task execution: opening apps, screenshots, system control, etc.
All functions accept a pyttsx3 engine so they can provide voice feedback.
"""

import os
import subprocess
import webbrowser
import datetime
import logging
import pyautogui
import pyttsx3
import wikipedia
import pywhatkit

from pathlib import Path
from speech_engine import speak
from utils import get_current_time, get_current_date, SCREENSHOTS_DIR

logger = logging.getLogger(__name__)

# ── Application Paths (Windows defaults) ─────────────────────────────────────

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

VSCODE_PATHS = [
    os.path.join(os.getenv("LOCALAPPDATA", ""), r"Programs\Microsoft VS Code\Code.exe"),
    r"C:\Program Files\Microsoft VS Code\Code.exe",
]


def _open_exe(engine: pyttsx3.Engine, paths: list, fallback_cmd: str, app_name: str) -> None:
    """
    Try to launch an executable from a list of candidate *paths*.
    Falls back to *fallback_cmd* if none of the paths exist.
    """
    for path in paths:
        if os.path.exists(path):
            os.startfile(path)  # type: ignore[attr-defined]
            speak(engine, f"Opening {app_name}")
            return
    # Fallback: rely on PATH
    try:
        subprocess.Popen(fallback_cmd, shell=True)
        speak(engine, f"Opening {app_name}")
    except Exception as exc:
        logger.error("Could not open %s: %s", app_name, exc)
        speak(engine, f"Sorry, I could not find {app_name} on your system.")


# ── Application Launchers ─────────────────────────────────────────────────────

def open_chrome(engine: pyttsx3.Engine) -> None:
    """Open Google Chrome."""
    _open_exe(engine, CHROME_PATHS, "chrome", "Google Chrome")


def open_youtube(engine: pyttsx3.Engine) -> None:
    """Open YouTube in the default browser."""
    speak(engine, "Opening YouTube")
    webbrowser.open("https://www.youtube.com")


def open_notepad(engine: pyttsx3.Engine) -> None:
    """Open Notepad."""
    speak(engine, "Opening Notepad")
    os.system("notepad.exe")


def open_vscode(engine: pyttsx3.Engine) -> None:
    """Open Visual Studio Code."""
    _open_exe(engine, VSCODE_PATHS, "code", "Visual Studio Code")


def open_calculator(engine: pyttsx3.Engine) -> None:
    """Open the Windows Calculator."""
    speak(engine, "Opening Calculator")
    os.system("calc.exe")


def open_file_explorer(engine: pyttsx3.Engine) -> None:
    """Open Windows File Explorer."""
    speak(engine, "Opening File Explorer")
    os.system("explorer.exe")


# ── Web Search ────────────────────────────────────────────────────────────────

def search_google(engine: pyttsx3.Engine, query: str) -> None:
    """
    Perform a Google search for *query* in the default browser.

    Args:
        engine: TTS engine.
        query:  Search query string.
    """
    if not query.strip():
        speak(engine, "What would you like me to search for?")
        return
    speak(engine, f"Searching Google for {query}")
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)


def search_youtube(engine: pyttsx3.Engine, query: str) -> None:
    """
    Search YouTube for *query*.

    Args:
        engine: TTS engine.
        query:  Search query string.
    """
    if not query.strip():
        speak(engine, "What would you like me to search on YouTube?")
        return
    speak(engine, f"Searching YouTube for {query}")
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)


def play_music(engine: pyttsx3.Engine, query: str = "popular music playlist") -> None:
    """
    Play a YouTube music video matching *query* using pywhatkit.

    Args:
        engine: TTS engine.
        query:  Song / artist name (default is a generic music playlist).
    """
    speak(engine, f"Playing {query} on YouTube")
    try:
        pywhatkit.playonyt(query)
    except Exception as exc:
        logger.error("pywhatkit error: %s", exc)
        # Fallback: direct YouTube search
        search_youtube(engine, query)


# ── Information Commands ──────────────────────────────────────────────────────

def tell_time(engine: pyttsx3.Engine) -> None:
    """Speak the current time."""
    time_str = get_current_time()
    speak(engine, f"The current time is {time_str}")


def tell_date(engine: pyttsx3.Engine) -> None:
    """Speak today's date."""
    date_str = get_current_date()
    speak(engine, f"Today is {date_str}")


def search_wikipedia(engine: pyttsx3.Engine, topic: str) -> None:
    """
    Fetch a short Wikipedia summary for *topic* and speak it aloud.

    Args:
        engine: TTS engine.
        topic:  Subject to look up on Wikipedia.
    """
    if not topic.strip():
        speak(engine, "Please tell me what topic to look up on Wikipedia.")
        return

    speak(engine, f"Searching Wikipedia for {topic}. Please wait.")
    try:
        wikipedia.set_lang("en")
        summary = wikipedia.summary(topic, sentences=3, auto_suggest=True)
        speak(engine, summary)
    except wikipedia.exceptions.DisambiguationError as exc:
        options = ", ".join(exc.options[:3])
        speak(engine, f"That topic is ambiguous. Did you mean: {options}?")
    except wikipedia.exceptions.PageError:
        speak(engine, f"I could not find a Wikipedia page for {topic}.")
    except Exception as exc:
        logger.error("Wikipedia error: %s", exc)
        speak(engine, "There was an error fetching Wikipedia data.")


# ── Screenshot ────────────────────────────────────────────────────────────────

def take_screenshot(engine: pyttsx3.Engine) -> None:
    """Capture the screen and save it to the screenshots folder."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = SCREENSHOTS_DIR / f"screenshot_{timestamp}.png"

    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        speak(engine, f"Screenshot saved as screenshot_{timestamp}.png")
        logger.info("Screenshot saved: %s", filename)
    except Exception as exc:
        logger.error("Screenshot error: %s", exc)
        speak(engine, "Sorry, I could not take a screenshot.")


# ── System Control ────────────────────────────────────────────────────────────

def shutdown_computer(engine: pyttsx3.Engine) -> None:
    """Shut down the Windows computer after a 5-second delay."""
    speak(engine, "Shutting down the computer in 5 seconds. Goodbye!")
    os.system("shutdown /s /t 5")


def restart_computer(engine: pyttsx3.Engine) -> None:
    """Restart the Windows computer after a 5-second delay."""
    speak(engine, "Restarting the computer in 5 seconds.")
    os.system("shutdown /r /t 5")


def lock_computer(engine: pyttsx3.Engine) -> None:
    """Lock the Windows screen immediately."""
    speak(engine, "Locking your computer.")
    os.system("rundll32.exe user32.dll,LockWorkStation")
