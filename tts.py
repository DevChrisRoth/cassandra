import pyttsx3
import normalizer

# Engine initialisieren
engine = pyttsx3.init('nsss')  # nsss = Apple Mac OS Speechlib
engine.setProperty("rate", 175)  # Geschwindigkeit der Sprachausgabe (Standard: 200)

# Text-to-Speech Ausgabe
def speak(text: str) -> None:
    text = normalizer.normalize_text(text)
    engine.say(text)
    engine.runAndWait()
    engine.stop()