"""
utils.py
--------
Utility helpers: time/date, command history logging, and terminal UI.
"""

import datetime
import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR       = Path(__file__).parent.resolve()
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
HISTORY_FILE    = BASE_DIR / "command_history.json"

SCREENSHOTS_DIR.mkdir(exist_ok=True)


# ── Time & Date ───────────────────────────────────────────────────────────────

def get_current_time() -> str:
    """Return the current time as a human-readable string (e.g. '10:30 PM')."""
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")


def get_current_date() -> str:
    """Return the current date as a human-readable string (e.g. 'Friday, 13 March 2026')."""
    now = datetime.datetime.now()
    return now.strftime("%A, %d %B %Y")


# ── Command History ───────────────────────────────────────────────────────────

def log_command(command: str) -> None:
    """
    Append *command* with a timestamp to the JSON history file.

    Args:
        command: The voice command string to record.
    """
    history: list = []

    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            history = []

    entry = {
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "command": command,
    }
    history.append(entry)

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except IOError as exc:
        logger.error("Could not write history file: %s", exc)


# ── Terminal UI ───────────────────────────────────────────────────────────────

def print_banner() -> None:
    """Print a decorative banner when the assistant starts."""
    banner = r"""
╔══════════════════════════════════════════════════════════╗
║       Voice Controlled Computer System  🎙️              ║
║                  Powered by Python                       ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_command_received(command: str) -> None:
    """Display the recognised command in the terminal with formatting."""
    print(f"\n{'─'*55}")
    print(f"  📝  Command received: \"{command}\"")
    print(f"{'─'*55}")


def print_help() -> None:
    """Print a list of supported commands to the terminal."""
    commands = [
        ("open chrome",           "Open Google Chrome"),
        ("open youtube",          "Open YouTube in the browser"),
        ("open notepad",          "Open Notepad"),
        ("open vs code",          "Open Visual Studio Code"),
        ("search <query>",        "Search Google for <query>"),
        ("youtube <query>",       "Search YouTube for <query>"),
        ("play music",            "Play a music video on YouTube"),
        ("what time is it",       "Speak the current time"),
        ("what is the date",      "Speak today's date"),
        ("wikipedia <topic>",     "Read a Wikipedia summary"),
        ("take screenshot",       "Capture and save a screenshot"),
        ("shutdown",              "Shut down the computer"),
        ("restart",               "Restart the computer"),
        ("lock",                  "Lock the screen"),
        ("show history",          "Display command history"),
        ("help",                  "Show this help list"),
        ("exit / stop / goodbye", "Exit the assistant"),
    ]
    print("\n" + "═" * 55)
    print("  📋  Available Commands")
    print("═" * 55)
    for cmd, desc in commands:
        print(f"  • {cmd:<30} → {desc}")
    print("═" * 55 + "\n")


def print_history() -> None:
    """Print the command history stored in the JSON log file."""
    if not HISTORY_FILE.exists():
        print("  ℹ️  No command history found.")
        return

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except (json.JSONDecodeError, IOError):
        print("  ⚠️  Could not read history file.")
        return

    print("\n" + "═" * 55)
    print("  📜  Command History")
    print("═" * 55)
    for entry in history[-20:]:   # show last 20
        print(f"  [{entry['timestamp']}]  {entry['command']}")
    print("═" * 55 + "\n")
