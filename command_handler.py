"""
command_handler.py
------------------
Parses a recognised voice command string and routes it to the correct
automation function.  Returns True if the assistant should keep running,
False if the user asked to exit.
"""

import logging
import pyttsx3

from speech_engine import speak
from utils import log_command, print_command_received, print_help, print_history
import automation as auto

logger = logging.getLogger(__name__)

# ── Wake-word (optional) ──────────────────────────────────────────────────────
WAKE_WORDS = {"hey assistant", "hello assistant", "ok assistant"}

# ── Exit phrases ──────────────────────────────────────────────────────────────
EXIT_PHRASES = {"exit", "exit assistant", "stop", "stop assistant",
                "goodbye", "bye", "quit"}


def _extract_query(command: str, keyword: str) -> str:
    """
    Strip *keyword* from the start of *command* and return the remainder.

    Example:
        _extract_query("search python tutorials", "search") → "python tutorials"
    """
    return command.replace(keyword, "", 1).strip()


def handle_command(engine: pyttsx3.Engine, command: str) -> bool:
    """
    Route *command* to the appropriate handler function.

    Args:
        engine:  Initialised pyttsx3 TTS engine.
        command: Lowercase recognised voice command string.

    Returns:
        True  – assistant should continue listening.
        False – assistant should exit.
    """
    if not command:
        return True

    # ── Log & display ─────────────────────────────────────────────────────────
    log_command(command)
    print_command_received(command)

    # ── Strip wake words if present ───────────────────────────────────────────
    for wake in WAKE_WORDS:
        if command.startswith(wake):
            command = command[len(wake):].strip()
            break

    if not command:
        speak(engine, "Yes? How can I help you?")
        return True

    # ── Exit ──────────────────────────────────────────────────────────────────
    if command in EXIT_PHRASES:
        speak(engine, "Goodbye! Have a great day!")
        return False

    # ── Help ──────────────────────────────────────────────────────────────────
    if "help" in command:
        print_help()
        speak(engine, "I have displayed the list of available commands on screen.")
        return True

    # ── Command History ───────────────────────────────────────────────────────
    if "show history" in command or "command history" in command:
        print_history()
        speak(engine, "I have displayed the command history on screen.")
        return True

    # ── Open Applications ─────────────────────────────────────────────────────
    if "open chrome" in command or "open google chrome" in command:
        auto.open_chrome(engine)

    elif "open youtube" in command:
        auto.open_youtube(engine)

    elif "open notepad" in command:
        auto.open_notepad(engine)

    elif "open vs code" in command or "open visual studio" in command:
        auto.open_vscode(engine)

    elif "open calculator" in command:
        auto.open_calculator(engine)

    elif "open file explorer" in command or "open explorer" in command:
        auto.open_file_explorer(engine)

    # ── Web Search ────────────────────────────────────────────────────────────
    elif command.startswith("search "):
        query = _extract_query(command, "search")
        auto.search_google(engine, query)

    elif command.startswith("google "):
        query = _extract_query(command, "google")
        auto.search_google(engine, query)

    elif command.startswith("youtube ") and "open" not in command:
        query = _extract_query(command, "youtube")
        auto.search_youtube(engine, query)

    # ── Play Music ────────────────────────────────────────────────────────────
    elif "play music" in command:
        query = _extract_query(command, "play music").strip() or "popular music playlist"
        auto.play_music(engine, query)

    elif command.startswith("play "):
        query = _extract_query(command, "play")
        auto.play_music(engine, query)

    # ── Wikipedia ─────────────────────────────────────────────────────────────
    elif "wikipedia" in command:
        topic = _extract_query(command, "wikipedia")
        auto.search_wikipedia(engine, topic)

    # ── Time & Date ───────────────────────────────────────────────────────────
    elif any(p in command for p in ("what time", "current time", "tell me the time",
                                     "what is the time")):
        auto.tell_time(engine)

    elif any(p in command for p in ("what date", "current date", "tell me the date",
                                     "what is the date", "today's date")):
        auto.tell_date(engine)

    # ── Screenshot ────────────────────────────────────────────────────────────
    elif "take screenshot" in command or "screenshot" in command:
        auto.take_screenshot(engine)

    # ── System Control ────────────────────────────────────────────────────────
    elif "shutdown" in command or "shut down" in command:
        auto.shutdown_computer(engine)
        return False   # exit the loop after shutdown is initiated

    elif "restart" in command or "reboot" in command:
        auto.restart_computer(engine)
        return False

    elif "lock" in command and "computer" in command or command == "lock":
        auto.lock_computer(engine)

    # ── Unknown Command ───────────────────────────────────────────────────────
    else:
        speak(engine, f"Sorry, I don't know how to handle the command: {command}. "
                       "Say 'help' to see a list of available commands.")
        logger.warning("Unrecognised command: %s", command)

    return True
