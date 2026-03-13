"""
main.py
-------
Entry point for the Voice Controlled Computer System.

Run with:
    python main.py

The assistant will greet you, then continuously listen for voice commands
until you say "exit", "goodbye", or a similar exit phrase.
"""

import sys
import logging
from speech_engine import init_tts_engine, speak, listen
from command_handler import handle_command
from utils import print_banner, print_help

# ── Logging configuration ────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("assistant.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    """Initialise the assistant and start the main command loop."""

    # ── Start-up UI ───────────────────────────────────────────────────────────
    print_banner()
    print("  Initialising voice engine…")

    # ── TTS engine ────────────────────────────────────────────────────────────
    engine = init_tts_engine(rate=170)

    # ── Greeting ──────────────────────────────────────────────────────────────
    speak(engine, "Voice assistant started. How can I help you?")
    print_help()

    # ── Main loop ─────────────────────────────────────────────────────────────
    running = True
    while running:
        try:
            command = listen(engine)

            if command:
                running = handle_command(engine, command)
            # If command is empty (timeout / unrecognised) just loop again

        except KeyboardInterrupt:
            print("\n\n  ⚠️  Keyboard interrupt received.")
            speak(engine, "Shutting down. Goodbye!")
            break

        except Exception as exc:
            logger.error("Unexpected error in main loop: %s", exc, exc_info=True)
            speak(engine, "An unexpected error occurred. Please try again.")

    print("\n  👋  Assistant stopped. Goodbye!\n")


if __name__ == "__main__":
    main()
