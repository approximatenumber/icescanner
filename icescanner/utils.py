import re

def parse_string_to_secs(time: str) -> int:
    """Parse time string to seconds."""
    time, suffix = re.match(r"([0-9]+)([a-z]+|)", str(time), re.I).groups()
    if suffix in ['hours', 'h']:
        return int(time) * 60 * 60
    elif suffix in ['minutes', 'min', 'm']:
        return int(time) * 60
    elif suffix in ['s', 'sec'] or not suffix:
        return int(time)
    else:
        raise Exception(f"Cannot detect time measurement suffix: {suffix}")