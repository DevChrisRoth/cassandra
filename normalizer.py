from num2words import num2words

#Normalizes the text for tts
def normalize_text(text: str) -> str:
    return num2words(text, lang='de')


print(normalize_text("123"))