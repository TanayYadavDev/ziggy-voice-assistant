"""Ziggy ka dimaag — Muse Spark via Meta Model API (OpenAI-compatible)."""
from openai import OpenAI

from config import Config

SYSTEM_PROMPT = """You are Ziggy, Tanay's personal AI voice companion running on his laptop.
- Talk like a close friend: warm, a little playful, never robotic.
- Default language: Hinglish (Hindi-English mix, Roman script). Match whatever language Tanay uses.
- Keep spoken replies SHORT: 1-3 sentences. This is voice, not an essay.
- If you don't know something, say so honestly. Never invent facts.
- You get a summary of past conversations — refer to it naturally, like you remember."""


class Brain:
    def __init__(self, cfg: Config, memory):
        cfg.check_brain()
        self.cfg = cfg
        self.memory = memory
        self.client = OpenAI(api_key=cfg.meta_api_key, base_url=cfg.meta_base_url)

    def reply(self, user_text: str) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        summary = self.memory.get_summary()
        if summary:
            messages.append({
                "role": "system",
                "content": f"Pichhli baaton ka summary (yaad rakhna): {summary}",
            })
        messages.extend(self.memory.get_history(self.cfg.max_history_turns))
        messages.append({"role": "user", "content": user_text})

        resp = self.client.chat.completions.create(
            model=self.cfg.brain_model,
            messages=messages,
        )
        answer = resp.choices[0].message.content.strip()
        self.memory.log_turn(user_text, answer)
        return answer
