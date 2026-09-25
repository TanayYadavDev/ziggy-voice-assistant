# Ziggy 🎙️ — 24/7 Voice Assistant

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Status](https://img.shields.io/badge/status-active_development-green.svg)

A hands-free, always-on voice companion that runs on your laptop.
Say the wake word, talk naturally, get spoken responses — with conversation
memory, so it remembers what you told it yesterday.

**Design principle:** silence is free. Wake-word detection runs locally, and
API tokens are consumed only while you're actively talking.

## ✨ Features

- **Wake-word activation** — always listening locally, wakes on "ziggy"
- **Speech-to-text** — local Whisper (tiny), auto-detects Hindi & English, works offline
- **Conversational brain** — powered by Muse Spark via the Meta Model API
- **Text-to-speech** — offline voice output, no API key needed
- **Conversation memory** — every exchange is logged locally; the assistant recalls past context
- **Privacy-first** — your API key and memory never leave your machine (`.env` and `memory.jsonl` are git-ignored)

## 🏗️ Architecture

```
 🎤 microphone (24/7, local)
      │
      ▼
 ┌───────────┐   wake word detected   ┌──────────┐
 │  wake.py  │ ─────────────────────▶ │ ears.py  │  audio → text (faster-whisper)
 └───────────┘                        └──────────┘
                                            │ text
                                            ▼
                                      ┌──────────┐
                                      │ brain.py │  Muse Spark (Meta Model API)
                                      └──────────┘
                                            │ text
                                            ▼
 ┌──────────┐                         ┌──────────┐
 │ memory.py│ ◀── every turn logged ── │ mouth.py │  text → speech (pyttsx3)
 └──────────┘                         └──────────┘
```

| Component | Role | Cost |
|---|---|---|
| `wake.py` | Local wake-word detection | Free |
| `ears.py` | Speech → text (Whisper tiny, CPU) | Free, offline |
| `brain.py` | Reasoning & replies (Muse Spark) | ~10–15k tokens / hour of active chat |
| `mouth.py` | Text → speech | Free, offline |
| `memory.py` | JSONL conversation log + recall | Free |

## 🚀 Quick Start

**Requirements:** Python 3.10+, a microphone and speakers.

```bash
git clone https://github.com/TanayYadavDev/ziggy-voice-assistant.git
cd ziggy-voice-assistant
pip install -r requirements.txt
cp .env.example .env
# fill in META_API_KEY, META_BASE_URL, BRAIN_MODEL (see Configuration)
```

```bash
# First run — text mode, no microphone needed (tests brain + memory):
python ziggy.py --text

# Full voice mode (press Enter, speak, hear the reply):
python ziggy.py
```

Say **"band karo"** (or press Ctrl+C) to shut down.

> On Linux, if text-to-speech fails: `sudo apt install espeak`

## ⚙️ Configuration

All settings live in `.env` (copy from `.env.example`):

| Variable | Description |
|---|---|
| `META_API_KEY` | Your Meta Model API key — get one at [dev.meta.ai](https://dev.meta.ai) (free $20 credits on signup) |
| `META_BASE_URL` | API base URL from the Meta Model API docs |
| `BRAIN_MODEL` | Model ID from the Meta Model API docs |
| `WAKE_WORD` | Wake word (default: `ziggy`) |
| `STT_PROVIDER` | `local` (Whisper) or `meta` (Meta voice-transcribe API) |
| `TTS_RATE` | Speech rate for TTS output |

## 📁 Project Structure

```
ziggy-voice-assistant/
├── ziggy.py         # main loop: wake → listen → think → speak
├── config.py        # configuration (.env loader)
├── brain.py         # LLM client (Meta Model API, OpenAI-compatible)
├── ears.py          # microphone capture + speech-to-text
├── mouth.py         # text-to-speech output
├── wake.py          # wake-word detection (push-to-talk fallback for now)
├── memory.py        # conversation log + context recall
├── requirements.txt
├── .env.example     # configuration template (no secrets)
└── LICENSE
```

## 🗺️ Roadmap

- **Phase 1** — Text mode + push-to-talk voice loop ✅
- **Phase 2** — True hands-free wake word (custom "ziggy" model via training or Porcupine keyword)
- **Phase 3** — Tool use: tell the time, set reminders, control the laptop
- **Phase 4** — Meta `muse-voice-transcribe` as the STT backend (higher accuracy)
- **Phase 5** — Neural TTS (e.g. edge-tts) for a more natural Hindi voice

## 🤝 Contributing

This is a personal project, but suggestions and PRs are welcome —
open an issue first to discuss what you'd like to change.

## 📄 License

MIT — see [LICENSE](LICENSE).

## 👤 Author

**Tanay Singh Yadav**
- GitHub: [@TanayYadavDev](https://github.com/TanayYadavDev)
- LinkedIn: [tanay-yadav-dev](https://www.linkedin.com/in/tanay-yadav-dev)
