"""Runs every message in tests.txt through polish() and saves a report you can read.
Run:  python run_tests.py
Then open results.txt and judge each output against the 'check' line.
"""

import time
from polisher import polish
from prompt import MESSAGE_TYPES, TONES, LENGTHS

TEST_FILE = "tests.txt"
RESULT_FILE = "results.txt"
PAUSE_SECONDS = 2  # small gap between calls, to be kind to free-tier rate limits


def load_tests(path):
    tests = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|", 4)]
            if len(parts) < 4:
                print(f"Skipping badly formatted line: {line}")
                continue
            check = parts[4] if len(parts) == 5 else ""
            tests.append((parts[0], parts[1], parts[2], parts[3], check))
    return tests


def main():
    tests = load_tests(TEST_FILE)
    print(f"Running {len(tests)} tests...")
    lines = []
    for number, (t, tone, length, text, check) in enumerate(tests, start=1):
        header = f"=== Test {number} ==="
        print(header)
        try:
            result = polish(text, MESSAGE_TYPES[t], TONES[tone], LENGTHS[length])
            polished = result.get("polished", "")
            changes = result.get("changes", [])
            placeholders = result.get("placeholders", [])
        except Exception as error:
            polished, changes, placeholders = f"ERROR: {error}", [], []

        lines += [
            header,
            f"Type: {MESSAGE_TYPES[t][0]} | Tone: {TONES[tone]} | Length: {LENGTHS[length]}",
            f"ROUGH:    {text}",
            f"POLISHED: {polished}",
            f"CHANGES:  {changes}",
            f"PLACEHOLDERS: {placeholders}",
            f"CHECK:    {check}",
            "SCORE (fill in): meaning kept? [ ]  nothing invented? [ ]  tone right? [ ]  sounds like me? [ ]",
            "",
        ]
        time.sleep(PAUSE_SECONDS)

    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Done. Open {RESULT_FILE} to review.")


if __name__ == "__main__":
    main()