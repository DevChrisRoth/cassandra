from num2words import num2words
import re
#Normalizes the text for tts
def normalize_text(text: str) -> str:
    return re.sub(r'(\d+)', lambda m: num2words(m.group(), lang='de'), text)