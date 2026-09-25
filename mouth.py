"""Ziggy ki zubaan — text ko awaaz mein badlo.

pyttsx3 = offline, no API key, OS ka built-in TTS.
(Windows pe seedha chalega. Linux pe `sudo apt install espeak` chahiye.)

Upgrade path: edge-tts (Microsoft ki free neural voices, badhiya Hindi
voice 'hi-IN-SwaraNeural') — lekin usme mp3 playback ka jugaad chahiye,
isliye v1 mein pyttsx3.
"""
import pyttsx3


class Mouth:
    def __init__(self, cfg):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", cfg.tts_rate)

    def speak(self, text: str):
        print(f"🤖 Ziggy: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
