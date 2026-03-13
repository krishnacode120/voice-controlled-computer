# 🎙️ Voice Controlled Computer System

A Python-based desktop voice assistant for **Windows 10/11** that listens to your voice commands, converts speech to text, and performs real system actions — all while speaking responses back to you.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Running the Project](#-running-the-project)
- [Supported Commands](#-supported-commands)
- [Example Interactions](#-example-interactions)
- [Troubleshooting](#-troubleshooting)
- [Future Improvements](#-future-improvements)

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎤 Voice Input | Captures audio from your microphone and converts it to text |
| 🔊 Voice Output | Speaks back responses using text-to-speech (pyttsx3) |
| 🌐 Web Search | Google and YouTube search via voice |
| 📱 App Launcher | Opens Chrome, Notepad, VS Code, Calculator, File Explorer |
| 📖 Wikipedia | Reads 3-sentence summaries aloud |
| 🎵 Music Player | Plays YouTube videos by voice query |
| 📸 Screenshots | Saves timestamped PNG screenshots |
| 🕐 Time & Date | Speaks the current time and date |
| 🔒 System Control | Shutdown, restart, and lock screen |
| 📜 Command History | JSON log of every command with timestamps |
| 🆘 Help Screen | Says "help" to list all commands in the terminal |

---

## 📁 Project Structure

```
voice_controlled_computer/
│
├── main.py               ← Entry point; starts the assistant and main loop
├── speech_engine.py      ← Microphone input (STT) + voice output (TTS)
├── command_handler.py    ← Parses commands and routes to correct function
├── automation.py         ← Executes system tasks (apps, web, screenshots…)
├── utils.py              ← Helpers: time/date, logging, terminal UI
│
├── requirements.txt      ← Python package dependencies
├── assistant.log         ← Runtime log file (auto-created)
├── command_history.json  ← Command history (auto-created)
│
├── screenshots/          ← Screenshot PNG files saved here
│
└── README.md             ← This file
```

---

## ⚙️ Requirements

### Hardware
- Microphone (built-in or external)
- Speakers or headphones
- Minimum 4 GB RAM

### Software
- **Windows 10 or Windows 11**
- **Python 3.9+** — https://www.python.org/downloads/
- **Visual Studio Code** — https://code.visualstudio.com/ *(recommended)*
- Active internet connection (for speech recognition API and Wikipedia)

---

## 🚀 Installation

### Step 1 — Clone or download the project

Place the `voice_controlled_computer/` folder anywhere on your PC, e.g.:
```
C:\Projects\voice_controlled_computer\
```

### Step 2 — Open in VS Code

```
File → Open Folder → select voice_controlled_computer
```

### Step 3 — Open a terminal inside VS Code

```
Terminal → New Terminal   (or  Ctrl + ` )
```

### Step 4 — (Recommended) Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 5 — Install dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install SpeechRecognition
pip install pyttsx3
pip install pyaudio
pip install pyautogui
pip install wikipedia
pip install pywhatkit
```

> **Note about PyAudio on Windows:**
> If `pip install pyaudio` fails, download the matching `.whl` file from
> https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio and install with:
> ```bash
> pip install PyAudio‑0.2.14‑cp311‑cp311‑win_amd64.whl
> ```
> Make sure the Python version in the filename matches yours (`python --version`).

---

## ▶️ Running the Project

```bash
python main.py
```

The assistant will:
1. Print a startup banner
2. Say *"Voice assistant started. How can I help you?"*
3. Start listening for your commands

Press **Ctrl + C** to stop the assistant at any time.

---

## 🗣️ Supported Commands

| Voice Command | Action |
|---|---|
| `open chrome` | Opens Google Chrome |
| `open youtube` | Opens YouTube in the browser |
| `open notepad` | Opens Notepad |
| `open vs code` | Opens Visual Studio Code |
| `open calculator` | Opens the Windows Calculator |
| `open file explorer` | Opens Windows File Explorer |
| `search <query>` | Google search for `<query>` |
| `google <query>` | Google search for `<query>` |
| `youtube <query>` | YouTube search for `<query>` |
| `play music` | Plays a music playlist on YouTube |
| `play <song/artist>` | Plays a specific song/artist on YouTube |
| `wikipedia <topic>` | Reads a 3-sentence Wikipedia summary |
| `what time is it` | Speaks the current time |
| `what is the date` | Speaks today's date |
| `take screenshot` | Saves a screenshot to `/screenshots/` |
| `shutdown` | Shuts down the PC in 5 seconds |
| `restart` | Restarts the PC in 5 seconds |
| `lock` | Locks the Windows screen |
| `show history` | Displays the command history in the terminal |
| `help` | Lists all commands in the terminal |
| `exit` / `goodbye` | Stops the assistant |

---

## 💬 Example Interactions

```
User:      Open Chrome
Assistant: Opening Google Chrome

User:      Search Python tutorials
Assistant: Searching Google for Python tutorials

User:      What time is it
Assistant: The current time is 10:30 PM

User:      Wikipedia Artificial Intelligence
Assistant: Artificial Intelligence (AI) is intelligence demonstrated by machines...

User:      Play music
Assistant: Playing popular music playlist on YouTube

User:      Take screenshot
Assistant: Screenshot saved as screenshot_20260313_223015.png

User:      Goodbye
Assistant: Goodbye! Have a great day!
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| `PyAudio` install fails | Use the `.whl` file method described in Installation Step 5 |
| Microphone not detected | Check Windows sound settings → Input device |
| Speech not recognised | Speak clearly; check your internet connection |
| Chrome/VS Code not found | Verify the install path or add the app to your system PATH |
| `pywhatkit` opens browser | This is expected — it uses the browser to play YouTube |

---

## 🔮 Future Improvements

- **Wake-word detection** — Activate only when saying *"Hey Assistant"*
- **Custom application paths** — Config file to set paths for any app
- **Email integration** — Read and send emails by voice
- **Weather queries** — *"What's the weather today?"*
- **GUI overlay** — Floating status window showing the current command
- **Offline speech recognition** — Use Vosk or Whisper to work without internet
- **Multi-language support** — Recognise commands in languages other than English
- **Scheduled tasks** — *"Remind me at 5 PM to take a break"*

---

## 📄 License

This project is provided for educational purposes. Feel free to modify and extend it.
