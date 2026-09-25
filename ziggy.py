"""Ziggy — main loop.

Usage:
    python ziggy.py --text    # mic ke bina, keyboard se (pehla test yehi karo)
    python ziggy.py           # full voice mode (push-to-talk until wake word wired)

Band karne ke liye: "band karo" bolo, ya Ctrl+C.
"""
import argparse

from config import Config
from memory import Memory
from brain import Brain
from ears import Ears
from mouth import Mouth
from wake import WakeWord

STOP_WORDS = {"band karo", "shutdown", "exit", "quit", "bye ziggy"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", action="store_true",
                    help="mic ke bina, keyboard se baat karo")
    args = ap.parse_args()

    cfg = Config()
    memory = Memory(cfg.memory_file)
    brain = Brain(cfg, memory)   # yahan .env check hota hai — key nahi to error
    mouth = Mouth(cfg)
    ears = None if args.text else Ears(cfg)
    wake = None if args.text else WakeWord(cfg)

    mouth.speak("Ziggy online. Bolo Tanay, kya kaam hai?")

    while True:
        try:
            if args.text:
                user_text = input("\nTum: ").strip()
            else:
                wake.wait()
                user_text = ears.listen()
                print(f"📝 Tumne kaha: {user_text}")

            if not user_text:
                continue
            if user_text.lower() in STOP_WORDS:
                mouth.speak("Theek hai, main yahin hun jab zaroorat ho. Bye!")
                if wake:
                    wake.close()
                break

            answer = brain.reply(user_text)
            mouth.speak(answer)

        except KeyboardInterrupt:
            print("\nBand ho raha hun. Bye! 👋")
            if wake:
                wake.close()
            break


if __name__ == "__main__":
    main()
