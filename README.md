# Ziggy 🎙️ — Tanay ka personal voice assistant

24x7 active rehne wala voice companion — ab awaaz mein bhi Ziggy. 💖

24x7 active rehne wala voice companion. Design principle: **khaamoshi free hai** —
wake word local detect hota hai, API tokens sirf tab jalte hain jab tum baat karte ho.

## Architecture

```
 🎤 mic (24x7 local)
      │
      ▼
 ┌───────────┐   "ziggy" sunte hi     ┌──────────┐
 │ wake.py   │ ─────────────────────▶ │ ears.py  │  mic → text (faster-whisper, local)
 └───────────┘                        └──────────┘
                                            │ text
                                            ▼
                                      ┌──────────┐
                                      │ brain.py │  Muse Spark (Meta Model API)
                                      └──────────┘
                                            │ text
                                            ▼
 ┌──────────┐                         ┌──────────┐
 │memory.py │ ◀── har turn log ────── │ mouth.py │  text → awaaz (pyttsx3, offline)
 └──────────┘                         └──────────┘
```

| Hissa | Kya karta hai | Cost |
|---|---|---|
| wake word | Local "ziggy" detection (custom model, Phase 2) | Free, zero tokens |
| STT (faster-whisper tiny) | Bol → text, Hindi/English auto | Free, offline |
| Brain (Muse Spark API) | Soch → jawab | ~10-15k tokens/ghanta active baat |
| TTS (pyttsx3) | Text → awaaz | Free, offline |
| Memory (memory.jsonl) | Baat-cheet ka log | Free |

## Setup

```bash
cd ~/workspace/ziggy
pip install -r requirements.txt
cp .env.example .env
# .env mein META_API_KEY, META_BASE_URL, BRAIN_MODEL bharo (neeche dekho)
```

Linux pe agar TTS error de: `sudo apt install espeak`

## Tera ek kaam 🔑

1. **dev.meta.ai** pe signup kar (free $20 credits milte hain)
2. API key bana → `.env` mein `META_API_KEY=` ke aage daal
3. Unke docs se **base URL** aur **model ID** confirm karke `.env` mein daal —
   maine guess nahi daala, galat URL pe debugging bekaar jaayegi

## Chalana

```bash
# Pehla test — mic ke bina, keyboard se (brain + memory test):
python ziggy.py --text

# Full voice mode (Enter dabao → bolo → jawab suno):
python ziggy.py
```

Band karne ke liye "band karo" bolo ya Ctrl+C.

## Roadmap

- **Phase 1 (abhi):** text mode + push-to-talk voice loop ✅ scaffold ready
- **Phase 2:** wake word 'ziggy' ka mic loop `wake.py` mein wire karo (custom model train ya Porcupine custom keyword) → sach mein 24x7 hands-free
- **Phase 3:** brain ko tools do — time batao, reminder lagao, laptop control (volume, etc.)
- **Phase 4:** Meta ka `muse-voice-transcribe` API STT ke liye (zyaada accurate, $0.18/ghanta — sirf baat karte waqt)
- **Phase 5:** edge-tts pe switch → natural Hindi voice

## Khule TODOs (docs se confirm karne hain)

- `META_BASE_URL` aur `BRAIN_MODEL` ka exact value — dev.meta.ai docs
- Meta STT ka HTTP endpoint — `ears.py` mein `NotImplementedError` wali jagah
- Custom 'ziggy' wake-word model (train ya Porcupine keyword) — `wake.py` mein TODO
