import json
import re
from pathlib import Path
import emoji

# Friendly names for some common emojis
FRIENDLY = {
    "face with tears of joy": "laughing hard",
    "red heart": "love",
    "smiling face with heart eyes": "love it",
    "thumbs up": "thumbs up",
    "fire": "fire",
    "pizza": "pizza",
}

def load_combos(path: str = "combos.json") -> dict:
    """Load custom multi-emoji combos from a JSON file."""
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}

def _normalize_spaces(s: str) -> str:
    """Clean up extra spaces."""
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([.,!?;:])", r"\1", s)
    return s.strip()

def _apply_combo_rules(text: str, combos: dict) -> tuple[str, bool]:
    """Replace multi-emoji combos first."""
    changed = False
    for combo, meaning in sorted(combos.items(), key=lambda kv: len(kv[0]), reverse=True):
        if combo in text:
            text = text.replace(combo, f" [{meaning}] ")
            changed = True
    return text, changed

def _replace_single_emojis(text: str, friendly: bool = True) -> tuple[str, bool]:
    """Replace single emojis using emoji.replace_emoji (modern API)."""
    had_emoji = emoji.demojize(text) != text

    def _rep(e: str, data: dict = None) -> str:
        # e = actual emoji character
        name = emoji.demojize(e).strip(":").replace("_", " ")
        if friendly and name in FRIENDLY:
            name = FRIENDLY[name]
        return f" [{name}] "

    replaced = emoji.replace_emoji(text, _rep)
    return replaced, had_emoji

def convert(text: str, combos: dict, friendly: bool = True) -> str:
    """Convert text with emojis into human-readable form."""
    original = text

    # 1) Apply combo rules (🍕❤️ -> [I love pizza])
    text, combo_changed = _apply_combo_rules(text, combos)

    # 2) Replace single emojis
    text, had_emoji = _replace_single_emojis(text, friendly=friendly)

    # 3) If nothing changed, return original text
    if not combo_changed and not had_emoji:
        return original

    # 4) Normalize spacing
    return _normalize_spaces(text)
