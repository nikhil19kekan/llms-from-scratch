import sys

# Colors auto-disable when output is not a terminal (e.g. piped to a file),
# so redirected logs stay clean instead of full of escape codes.
_ENABLED = sys.stdout.isatty()

_RESET = "\033[0m"
_CODES = {
    "black": "30", "red": "31", "green": "32", "yellow": "33",
    "blue": "34", "magenta": "35", "cyan": "36", "white": "37",
    "gray": "90", "bright_red": "91", "bright_green": "92",
    "bright_yellow": "93", "bright_blue": "94", "bright_cyan": "96",
}

# The theme: map a role to (color, bold). Change colors here in one place.
THEME = {
    "header":    ("cyan",   True),
    "step":      ("magenta", False),
    "thought":   ("yellow", False),
    "action":    ("blue",   True),
    "result":    ("green",  False),
    "info":      ("gray",   False),
    "done_ok":   ("bright_green", True),
    "done_fail": ("bright_red",   True),
}


def paint(role, text):
    if not _ENABLED or role not in THEME:
        return text
    name, bold = THEME[role]
    code = _CODES.get(name, "37")
    return f"\033[{'1;' if bold else ''}{code}m{text}{_RESET}"
