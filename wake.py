"""Wake word — 'ziggy' sunte hi jaag jao.

Abhi: push-to-talk (Enter dabao). Zero dependency, pehle din se kaam karega.
Phase 2: openwakeword/Porcupine mein custom 'ziggy' wake-word model lagana
hai — neeche TODO dekho.
"""
import numpy as np
import sounddevice as sd


class WakeWord:
    def __init__(self, word="ziggy"):
        self.word = word
        self.available = False
        try:
            from openwakeword.model import Model
            self.oww = Model()  # built-in models auto-download hote hain
            self.available = True
            print("Wake-word model ready hai.")
        except Exception as e:
            print(f"openwakeword nahi mila ({e}) — push-to-talk mode (Enter dabao).")

    def wait(self) -> bool:
        """Tab tak block karo jab tak wake word na sunai de. Returns True."""
        if not self.available:
            input(f"\n[{self.word.upper()} se baat karne ke liye Enter dabao...] ")
            return True
        # TODO (Phase 2): custom 'ziggy' wake-word model ka mic loop:
        #   - openwakeword ke liye custom model train karna padega, ya
        #   - Porcupine (Picovoice) mein custom keyword 'ziggy' banao — free tier mein hota hai
        #   - 16kHz mono stream se chunks lo, score > threshold par return True
        #   Exact API docs/examples se verify kar lena.
        raise NotImplementedError(
            "wake-word mic loop abhi baaki hai — README ka Phase 2 dekho. "
            "Tab tak openwakeword uninstall karke push-to-talk use karo."
        )
