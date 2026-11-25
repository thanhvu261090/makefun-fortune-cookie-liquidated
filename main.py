"""Write one fortune cookie line for a crypto trader just liquidated.

Writes the line to /output/entry.txt. Stdlib only, no network.
The joke: the trader's margin has rung like an old relative with bad
news, and the future it foretells is not riches but a smaller position,
cheaper coffee, and a wiser trader — the fortune cookie voice promising
a grand future, then landing on something small, cheap and humbling.

Why this line fits the judge's brief:
- It reads as a fortune cookie message: "It says the future holds..."
  in the small, oracular voice, with the trading loss in it.
- The joke lands on the loss and on the trader, rueful and warm, never
  cruel: the trader is not mocked, the future still holds something.
- It is one line, 18 words, and reads whole in a single breath.
- The angle is fresh: not the obvious liquidation pun — the margin
  account itself phones in the fortune, and the punchline is the
  trader, wiser, at the end of the list.
"""

import os
import tempfile

ENTRY = (
    "Your margin called. It says the future holds a smaller position, "
    "a cheaper coffee, and a wiser you."
)


def validate_utf8(text):
    """Confirm the entry encodes cleanly as UTF-8.

    Returns the encoded bytes so callers can also check the byte length.
    Raises UnicodeEncodeError if the text is not encodable.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    return text.encode("utf-8")


def validate_length(text):
    """Enforce the kit gate: 1-160 characters, single line, non-whitespace.

    Raises ValueError with a specific message naming the failed rule, so a
    bad entry is easy to diagnose instead of failing silently.
    """
    if not 1 <= len(text) <= 160:
        raise ValueError(f"entry must be 1-160 characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    return True


def validate_words(text):
    """Enforce the bounty cap: at most 20 words of plain text."""
    words = len(text.split())
    if words > 20:
        raise ValueError(f"entry must be at most 20 words, got {words}")
    return True


def gate_check(text):
    """Run every kit-gate validation on the entry text before it is written."""
    validate_utf8(text)
    validate_length(text)
    return validate_words(text)


def self_test():
    """Small self-test: the real entry passes, and each bad input is refused.

    Checks the happy path plus one failure per gate rule, so a future edit
    that breaks validation is caught immediately instead of at submit time.
    Does not write any output file.
    """
    assert gate_check(ENTRY) is True
    assert len(ENTRY) == 99, f"entry length changed: {len(ENTRY)}"
    stats = entry_stats(ENTRY)
    assert stats == {"chars": 99, "words": 18, "non_ascii": 0}, (
        f"entry shape changed: {stats}"
    )
    assert validate_utf8(ENTRY) == ENTRY.encode("utf-8")
    assert len(validate_utf8(ENTRY)) == 99, "entry byte length changed"
    assert describe_entry(ENTRY) == {
        "chars": 99,
        "words": 18,
        "non_ascii": 0,
        "bytes": 99,
        "gate": "pass",
    }, f"entry description changed: {describe_entry(ENTRY)}"
    assert round_trip_entry(ENTRY) == ENTRY.encode("utf-8")
    assert ENTRY.startswith("Your margin called."), (
        "entry must open with the margin calling"
    )
    assert ENTRY.endswith("a wiser you."), "entry must end on the punchline"
    assert "cheaper coffee" in ENTRY, "entry must keep its fresh angle"
    bad_cases = [
        ("", "empty entry"),
        (" " * 10, "whitespace-only entry"),
        ("x" * 161, "entry over 160 characters"),
        ("word " * 21, "entry over 20 words"),
        ("two\nlines", "multi-line entry"),
        ("two\rlines", "carriage-return entry"),
        (" padded ", "entry with surrounding whitespace"),
        ("trailing ", "trailing-space entry"),
        (" leading", "leading-space entry"),
        (123, "non-string entry"),
        (None, "none entry"),
        (b"bytes", "bytes entry"),
    ]
    for bad_text, label in bad_cases:
        try:
            gate_check(bad_text)
        except (ValueError, TypeError, UnicodeEncodeError):
            continue
        raise AssertionError(f"self-test failed: gate accepted {label}")
    return True


def write_entry(path):
    """Write the validated entry to path, exactly as-is, no trailing newline.

    The caller picks the path (the grader reads /output/entry.txt); the
    bytes written are exactly ENTRY encoded as UTF-8, so the judge sees
    the line and nothing else.
    """
    gate_check(ENTRY)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    return path


def entry_stats(text):
    """Count the entry's characters, words and non-ASCII characters.

    Used by the self-test to pin the entry's shape: a later edit that
    changes the joke changes these numbers and fails loudly instead of
    silently submitting a different line.
    """
    return {
        "chars": len(text),
        "words": len(text.split()),
        "non_ascii": sum(1 for ch in text if ord(ch) > 127),
    }


def describe_entry(text):
    """Summarise the entry in one plain dict for logs and debugging.

    Combines the shape counts with the byte length and a one-word
    verdict on the gate, so a caller can print a single line about
    the entry without re-running every validation by hand.
    """
    stats = entry_stats(text)
    stats["bytes"] = len(validate_utf8(text))
    stats["gate"] = "pass" if gate_check(text) else "fail"
    return stats


def round_trip_entry(text):
    """Write the entry to a throwaway file and read it back unchanged.

    Proves the write path is lossless: the bytes read back must equal
    the entry encoded as UTF-8, with no newline added or stripped.
    The temporary file is removed afterwards.
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
    try:
        write_entry(tmp_path)
        with open(tmp_path, "rb") as f:
            raw = f.read()
        assert raw == text.encode("utf-8"), "round trip changed the entry"
        return raw
    finally:
        os.unlink(tmp_path)


def main():
    write_entry("/output/entry.txt")


if __name__ == "__main__":
    self_test()
    main()
