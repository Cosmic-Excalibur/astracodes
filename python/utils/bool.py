def is_asciiprintable(s):
    if isinstance(s, str):
        return all(32 <= ord(x) <= 126 for x in s)
    else:
        return all(32 <= x <= 126 for x in s)
