"""Prints the model names your API key can use for text generation.
Run:  python list_models.py
Copy a few 'flash' names into the MODELS list in polisher.py (leave out the 'models/' prefix).
"""

from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

for model in client.models.list():
    actions = getattr(model, "supported_actions", None) or []
    if "generateContent" in actions:
        print(model.name)