"""Ziggy ke kaan — mic se suno, text mein badlo.

Default: local faster-whisper (tiny model, CPU, offline, free).
Hindi + English auto-detect. Pehli baar ~75MB model download hoga.
"""
import numpy as np
import sounddevice as sd

SAMPLE_RATE = 16000


class Ears:
    def __init__(self, cfg):
        self.provider = cfg.stt_provider
        self.model = None
        if self.provider == "local":
            from faster_whisper import WhisperModel
            print("STT model load ho raha hai (tiny, CPU)...")
            self.model = WhisperModel("tiny", device="cpu", compute_type="int8")
        elif self.provider == "meta":
            print("STT provider: meta (TODO: dev.meta.ai docs se endpoint confirm karo)")

    def listen(self, silence_secs=1.2, max_secs=20) -> str:
        """Bolo — khaamoshi par ruk jayega. Returns transcribed text."""
        print("🎤 Sun raha hun... (bolo)")
        chunks, silent_chunks = [], 0
        chunk_len = int(SAMPLE_RATE * 0.2)
        needed_silent = int(silence_secs / 0.2)
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32") as stream:
            total = 0.0
            while total < max_secs:
                data, _ = stream.read(chunk_len)
                chunks.append(data.copy())
                total += 0.2
                if np.abs(data).mean() < 0.02:
                    silent_chunks += 1
                else:
                    silent_chunks = 0
                if silent_chunks >= needed_silent and total > 1.0:
                    break
        audio = np.concatenate(chunks, axis=0).flatten()
        print("⏳ Samajh raha hun...")
        return self._transcribe(audio)

    def _transcribe(self, audio) -> str:
        if self.provider == "local":
            segments, _ = self.model.transcribe(audio, language=None)  # auto-detect
            return " ".join(s.text.strip() for s in segments).strip()
        raise NotImplementedError(
            "meta STT abhi baaki hai — dev.meta.ai docs mein "
            "'muse-voice-transcribe' ka HTTP endpoint dekh ke yahan implement karo."
        )
