import os
from dotenv import load_dotenv

load_dotenv()

print("GEMINI_API_KEY :", "OK" if os.getenv("GEMINI_API_KEY") else "MANQUANTE")
print("SMTP_USER     :", os.getenv("SMTP_USER"))
print("SMTP_PASS    :", "OK" if os.getenv("SMTP_PASS") else "MANQUANTE")
