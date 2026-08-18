import re

TOKENIZE_CALLS = 0


def reset_stats():
    global TOKENIZE_CALLS
    TOKENIZE_CALLS = 0


def get_stats():
    return {"tokenize_calls": TOKENIZE_CALLS}


def tokenize(source):
    global TOKENIZE_CALLS
    TOKENIZE_CALLS += 1
    parts = re.split(r"(\{\{.*?\}\}|\{%.*?%\})", source)
    tokens = []
    for part in parts:
        if not part:
            continue
        if part.startswith("{{"):
            tokens.append(("var", part[2:-2].strip()))
        elif part.startswith("{%"):
            body = part[2:-2].strip()
            name, _, arg = body.partition(" ")
            tokens.append((name, arg.strip()))
        else:
            tokens.append(("text", part))
    return tokens
