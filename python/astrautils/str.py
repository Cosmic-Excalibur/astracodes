from functools import reduce

def normalize_chars(text: str, chars = ' '):
    chars_ = chars*2
    while chars_ in text:
        text = text.replace(chars_, chars)

def normalize_chars_b(text: [bytes, bytearray], chars = b' '):
    chars_ = chars*2
    while chars_ in text:
        text = text.replace(chars_, chars)

def strip_word(text: str, word: str):
    if text.startswith(word):
        text = text[len(word):]
    if text.endswith(word):
        text = text[:-len(word)]
    return text

def lstrip_word(text: str, word: str):
    if text.startswith(word):
        text = text[len(word):]
    return text

def rstrip_word(text: str, word: str):
    if text.endswith(word):
        text = text[:-len(word)]
    return text

def strip_word_b(text: [bytes, bytearray], word: [bytes, bytearray]):
    if text.startswith(word):
        text = text[len(word):]
    if text.endswith(word):
        text = text[:-len(word)]
    return text

def lstrip_word(text: [bytes, bytearray], word: [bytes, bytearray]):
    if text.startswith(word):
        text = text[len(word):]
    return text

def rstrip_word(text: [bytes, bytearray], word: [bytes, bytearray]):
    if text.endswith(word):
        text = text[:-len(word)]
    return text

def print_no_prompt(text: str, prompts = ["sage: ", "....: ", ">>> ", "... "]):
    print('\n'.join(reduce(lambda a, b: lstrip_word(a, b), prompts, line) for line in text.splitlines()))
