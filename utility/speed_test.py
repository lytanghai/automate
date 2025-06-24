import time
import random

sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing is a skill that improves with practice.",
    "Python is an amazing programming language.",
    "OpenAI creates powerful AI tools."
]

def typing_test():
    text = random.choice(sentences)
    print("\nType the following:")
    print(f">>> {text}")
    input("Press Enter when ready...")

    start = time.time()
    typed = input("Start typing: ")
    end = time.time()

    elapsed = end - start
    words = len(text.split())
    wpm = (words / elapsed) * 60
    accuracy = sum(1 for a, b in zip(text, typed) if a == b) / len(text) * 100

    print(f"\n⏱ Time: {elapsed:.2f}s")
    print(f"💨 WPM: {wpm:.2f}")
    print(f"🎯 Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    typing_test()
