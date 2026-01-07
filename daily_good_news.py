import os
import time
from datetime import datetime
import feedparser
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from google import genai

load_dotenv()

RSS_FEEDS = [
    "https://www.francetvinfo.fr/titres.rss",
    "https://www.lemonde.fr/sciences/rss_full.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.sciencedaily.com/rss/top/science.xml",
]

MAX_PER_FEED = 8
MAX_TOTAL = 30

BLOCKLIST = [
    "ukraine", "russia", "zelensky", "iran", "protests", "armed", "security forces",
    "attack", "killed", "dead", "violence", "shooting", "terror", "hostage",
    "verglas", "neige", "tempête", "earthquake", "flood", "storm",
    "rectum", "porn", "sex", "rape", "anguille",
]

MODEL = "models/gemini-flash-latest"


def is_blocked(title: str) -> bool:
    t = title.lower()
    return any(word in t for word in BLOCKLIST)


def fetch_rss_items():
    items = []
    seen_links = set()

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:MAX_PER_FEED]:
            title = getattr(entry, "title", "").strip()
            link = getattr(entry, "link", "").strip()
            if not title or not link:
                continue
            if link in seen_links:
                continue
            seen_links.add(link)

            if is_blocked(title):
                continue

            items.append(f"- {title} — {link}")
            if len(items) >= MAX_TOTAL:
                return items

    return items


def gemini_pick_3(news_lines):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = f"""
Tu es un curateur d'actualités.

À partir de la liste de TITRES + LIENS ci-dessous, choisis 3 "bonnes nouvelles" :
- positives/constructives (progrès, solutions, coopération, santé, science, environnement, éducation)
- pas de faits divers, pas de guerre, pas de catastrophe, pas de sensationnalisme
- variété des thèmes

Pour CHAQUE nouvelle :
- Titre
- Résumé (2–3 phrases max)
- Lien

Format de sortie EXACT :

SECTION 1 — FRANÇAIS
1) Titre :
Résumé :
Lien :

2) Titre :
Résumé :
Lien :

3) Titre :
Résumé :
Lien :

SECTION 2 — ENGLISH
1) Title:
Summary:
Link:

2) Title:
Summary:
Link:

3) Title:
Summary:
Link:

Liste :
{chr(10).join(news_lines)}
""".strip()

    # petit retry simple
    last_err = None
    for _ in range(3):
        try:
            resp = client.models.generate_content(model=MODEL, contents=prompt)
            return resp.text.strip()
        except Exception as e:
            last_err = e
            time.sleep(20)

    raise RuntimeError(f"Gemini failed after retries: {last_err}")


def _parse_recipients(raw: str) -> list[str]:
    # support: "a@x.com,b@y.com" ou "a@x.com, b@y.com"
    return [e.strip() for e in raw.split(",") if e.strip()]


def send_email(subject: str, body: str) -> None:
    host = os.environ["SMTP_HOST"]
    port = int(os.environ["SMTP_PORT"])
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASS"]
    email_from = os.environ["EMAIL_FROM"]

    email_to_raw = os.environ["EMAIL_TO"]
    recipients = _parse_recipients(email_to_raw)
    if not recipients:
        raise ValueError("EMAIL_TO est vide ou invalide. Exemple: EMAIL_TO=alice@gmail.com,bob@yahoo.com")

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = email_from
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP(host, port, timeout=20) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(user, password)
        # IMPORTANT: on envoie bien la liste de destinataires, pas une string unique
        s.sendmail(email_from, recipients, msg.as_string())


def main():
    news = fetch_rss_items()
    if len(news) < 8:
        raise RuntimeError("Trop peu d'articles après filtrage. Ajuste BLOCKLIST ou ajoute des RSS.")

    content = gemini_pick_3(news)
    today = datetime.now().strftime("%Y-%m-%d")
    subject = f"3 bonnes nouvelles du jour — {today}"

    send_email(subject, content)
    print("OK: email quotidien envoyé.")


if __name__ == "__main__":
    main()
