import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

models = client.models.list()
for m in models:
    name = getattr(m, "name", "")
    # Certains renvoient supported_actions, d'autres supported_generation_methods
    methods = getattr(m, "supported_generation_methods", None) or getattr(m, "supported_actions", None)
    print(name, "-", methods)
