def normalize_chars(text: str, chars = ' '):
    chars_ = chars*2
    while chars_ in text:
        text = text.replace(chars_, chars)

def normalize_chars_b(text: [bytes, bytearray], chars = b' '):
    chars_ = chars*2
    while chars_ in text:
        text = text.replace(chars_, chars)
