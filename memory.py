"""Ziggy ki yaadashth — JSONL log. Har baat-cheet save, taaki
"yaad hai kal kya bola tha?" kaam kare."""
import json
import os


class Memory:
    def __init__(self, path="memory.jsonl"):
        self.path = path
        self._summary = ""
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    try:
                        obj = json.loads(line)
                        if obj.get("type") == "summary":
                            self._summary = obj["text"]
                    except json.JSONDecodeError:
                        pass

    def log_turn(self, user, assistant):
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(
                {"type": "turn", "user": user, "assistant": assistant},
                ensure_ascii=False) + "\n")

    def get_history(self, n_turns):
        turns = []
        if os.path.exists(self.path):
            with open(self.path, encoding="utf-8") as f:
                for line in f:
                    try:
                        obj = json.loads(line)
                        if obj.get("type") == "turn":
                            turns.append(obj)
                    except json.JSONDecodeError:
                        pass
        msgs = []
        for t in turns[-n_turns:]:
            msgs.append({"role": "user", "content": t["user"]})
            msgs.append({"role": "assistant", "content": t["assistant"]})
        return msgs

    def get_summary(self):
        return self._summary

    def save_summary(self, text):
        self._summary = text
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"type": "summary", "text": text},
                               ensure_ascii=False) + "\n")
