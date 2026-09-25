"""Wake word — 'ziggy' sunte hi jaag jao, hands-free.

Providers (WAKE_PROVIDER in .env):
  - porcupine : real always-on detection via Picovoice Porcupine.
                100% on-device, no audio leaves the laptop.
                Setup: free account at console.picovoice.ai -> train the
                "ziggy" wake word -> download the .ppn file -> set
                PICOVOICE_ACCESS_KEY + PORCUPINE_KEYWORD_PATH in .env.
  - push      : push-to-talk fallback (press Enter). Default, zero setup.
"""
import os

import numpy as np
import sounddevice as sd


class WakeWord:
    def __init__(self, cfg):
        self.provider = cfg.wake_provider
        self.word = cfg.wake_word
        self._porcupine = None

        if self.provider == "porcupine":
            import pvporcupine
            if not cfg.picovoice_access_key:
                raise RuntimeError(".env mein PICOVOICE_ACCESS_KEY missing hai "
                                   "(console.picovoice.ai se free mein milti hai)")
            if not os.path.exists(cfg.porcupine_keyword_path):
                raise RuntimeError(
                    f"Wake-word model file nahi mili: {cfg.porcupine_keyword_path}\n"
                    "console.picovoice.ai par 'ziggy' train karke .ppn download karo "
                    "aur repo folder mein rakho (README mein steps hain).")
            self._porcupine = pvporcupine.create(
                access_key=cfg.picovoice_access_key,
                keyword_paths=[cfg.porcupine_keyword_path],
                sensitivities=[cfg.wake_sensitivity],
            )
            print(f"Wake word '{self.word}' armed "
                  f"(Porcupine, sensitivity {cfg.wake_sensitivity}).")
        else:
            print(f"Wake word: push-to-talk mode "
                  f"('{self.word}' ke liye Enter dabao).")

    def wait(self) -> bool:
        """Block until the wake word is heard. Returns True."""
        if self._porcupine is None:
            input(f"\n[{self.word.upper()} se baat karne ke liye Enter dabao...] ")
            return True

        p = self._porcupine
        print(f"😴 '{self.word}' ka intezaar... (Ctrl+C se band karo)")
        with sd.InputStream(samplerate=p.sample_rate, channels=1,
                            dtype="int16") as stream:
            while True:
                pcm, _ = stream.read(p.frame_length)
                pcm = np.asarray(pcm, dtype=np.int16).flatten()
                if len(pcm) != p.frame_length:
                    continue
                if p.process(pcm) >= 0:
                    print(f"⚡ '{self.word}' suna!")
                    return True

    def close(self):
        if self._porcupine is not None:
            self._porcupine.delete()
            self._porcupine = None
