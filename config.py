"""Ziggy configuration — sab settings .env file se aati hain."""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    # --- Meta Model API (dev.meta.ai se API key lao, signup pe $20 free credits) ---
    meta_api_key: str = field(default_factory=lambda: os.getenv("META_API_KEY", ""))
    # Base URL aur model ID dev.meta.ai ke docs se confirm karke .env mein daalo.
    # Maine guess nahi daala — galat URL se bekaar debugging hogi.
    meta_base_url: str = field(default_factory=lambda: os.getenv("META_BASE_URL", ""))
    brain_model: str = field(default_factory=lambda: os.getenv("BRAIN_MODEL", ""))

    # --- Voice pipeline ---
    wake_word: str = field(default_factory=lambda: os.getenv("WAKE_WORD", "ziggy"))
    stt_provider: str = field(default_factory=lambda: os.getenv("STT_PROVIDER", "local"))  # local | meta
    language: str = field(default_factory=lambda: os.getenv("LANGUAGE", "hi"))  # hi = Hinglish mode
    tts_rate: int = field(default_factory=lambda: int(os.getenv("TTS_RATE", "175")))

    # --- Memory ---
    memory_file: str = field(default_factory=lambda: os.getenv("MEMORY_FILE", "memory.jsonl"))
    max_history_turns: int = field(default_factory=lambda: int(os.getenv("MAX_HISTORY_TURNS", "12")))

    def check_brain(self):
        missing = []
        if not self.meta_api_key:
            missing.append("META_API_KEY")
        if not self.meta_base_url:
            missing.append("META_BASE_URL")
        if not self.brain_model:
            missing.append("BRAIN_MODEL")
        if missing:
            raise RuntimeError(
                f".env mein ye missing hain: {', '.join(missing)} "
                "(dev.meta.ai ke docs se lao)"
            )
