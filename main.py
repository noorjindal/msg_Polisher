"""The terminal interface: menus, input and printing. Run with: python main.py"""

from polisher import polish
from prompt import MESSAGE_TYPES, TONES, LENGTHS


def pick(title, options):
    """Show a numbered menu and return the chosen value (defaults to the first option)."""
    print(f"\n{title}")
    for key, value in options.items():
        label = value[0] if isinstance(value, tuple) else value
        print(f"  {key}. {label}")
    choice = input("> ").strip()
    return options.get(choice, list(options.values())[0])


def show(result):
    print("\n--- Polished ---")
    print(result.get("polished", ""))
    if result.get("changes"):
        print("\n--- What changed ---")
        for change in result["changes"]:
            print(f"- {change}")
    if result.get("placeholders"):
        print("\n--- Fill these in before sending ---")
        for item in result["placeholders"]:
            print(f"- {item}")
    print("\n" + "=" * 40)


def main():
    print("Message Polisher (Gemini). Press Ctrl+C to quit.")
    while True:
        msg_type = pick("Message type:", MESSAGE_TYPES)
        tone = pick("Tone:", TONES)
        length = pick("Length:", LENGTHS)
        text = input("\nPaste your rough message:\n> ").strip()
        if not text:
            continue
        print("\nPolishing...")
        try:
            result = polish(text, msg_type, tone, length)
        except Exception as error:
            # Common causes: wrong/missing key, wrong model name, or free-tier rate limit (429)
            print(f"\nSomething went wrong: {error}")
            print("Check GEMINI_API_KEY and the MODELS list in polisher.py, or try again in a minute.")
            continue
        show(result)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")