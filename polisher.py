"""Talks to the model. Knows nothing about menus or printing, so any app can import it.

Setup:
    pip install google-genai
    pip install python-dotenv
    Put this line in a file named .env next to this file:  GEMINI_API_KEY=your-key
    (free key: https://aistudio.google.com)

Privacy note: on the free tier, Google may use what you send to improve its products.
"""

import json
import time

import httpx  # installed together with google-genai; used to spot timeouts and network errors
from dotenv import load_dotenv  # pip install python-dotenv
from google import genai
from google.genai import errors, types

from prompt import SYSTEM_PROMPT

load_dotenv()  # reads GEMINI_API_KEY from your .env file; must run before the client is created

# Models are tried in order. If a model is "not found" or keeps failing, the next one is used.
# Model names change over time: copy current Flash names from Google AI Studio if needed.
MODELS = [
    # "gemini-3.7-flash",
    # "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]

MAX_RETRIES = 2   # attempts per model; the next model is tried after this
   # attempts per model for temporary errors
TIMEOUT_SECONDS = 30       # a request that takes longer than this is cancelled and retried
TEMPORARY_CODES = (429, 500, 503, 504)  # rate limit / overloaded / server hiccup

client = genai.Client(
    http_options=types.HttpOptions(timeout=TIMEOUT_SECONDS * 1000)  # the library expects milliseconds
)


def _call_model(model, user_prompt):
    """One request to one model. Returns the raw reply text."""
    response = client.models.generate_content(
        model=model,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.4,
        ),
    )
    return (response.text or "").strip()


def _is_temporary(error):
    """True for errors that are worth retrying: busy servers, rate limits, timeouts, network drops."""
    if isinstance(error, errors.APIError):
        return error.code in TEMPORARY_CODES
    return isinstance(error, httpx.TransportError)  # includes timeouts


def _call_with_retries(model, user_prompt):
    """Retry temporary errors with growing waits: 2s, 4s, 8s..."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return _call_model(model, user_prompt)
        except (errors.APIError, httpx.HTTPError) as error:
            if _is_temporary(error) and attempt < MAX_RETRIES:
                wait = 2 ** attempt
                print(f"(No good reply yet, retrying in {wait}s... attempt {attempt}/{MAX_RETRIES})")
                time.sleep(wait)
            else:
                raise


def polish(text, msg_type, tone, length):
    """Return a dict: {"polished": str, "changes": [str], "placeholders": [str]}."""
    user_prompt = (
        f"Message type: {msg_type[0]} ({msg_type[1]})\n"
        f"Tone: {tone}\n"
        f"Length: {length}\n\n"
        f"Rough message:\n<message>\n{text}\n</message>"
    )

    last_error = None
    for model in MODELS:
        try:
            raw = _call_with_retries(model, user_prompt)
            print(model)
            break
        except (errors.APIError, httpx.HTTPError) as error:
            last_error = error  # try the next model in the list
    else:
        raise last_error

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"polished": raw, "changes": [], "placeholders": []}