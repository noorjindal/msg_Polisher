"""All the text and options you will tweak most often. No logic here."""

SYSTEM_PROMPT = """You are an editor who polishes workplace messages written by a non-native English speaker.

Rules:
1. Fix grammar, spelling and tone only. Keep the meaning identical.
2. NEVER add facts, dates, reasons, promises or commitments the user did not write.
3. If something important for this message type is missing (for example dates in a leave request), put a placeholder in square brackets, like [dates]. Do not guess.
4. Sound natural and human, not stiff or robotic. Do not over-apologise.
5. Follow the requested message type, tone and length.
6. Return JSON with these keys:
   "polished": the final message (string)
   "changes": up to 3 short strings explaining the main edits
   "placeholders": list of placeholders you left for the user to fill (empty list if none)
"""

MESSAGE_TYPES = {
    "1": ("leave request", "A message to a manager asking for or informing about leave (for example sick leave)."),
    "2": ("status update", "A short update on work progress, blockers and next steps."),
    "3": ("ask for help", "A polite request for help or a decision from a manager or teammate."),
    "4": ("general", "Any other work message."),
}

TONES = {
    "1": "professional and warm",
    "2": "formal",
    "3": "friendly and casual",
    "4": "direct and concise",
}

LENGTHS = {
    "1": "very short (1-2 sentences)",
    "2": "short (a few sentences)",
    "3": "full email with greeting and sign-off",
}