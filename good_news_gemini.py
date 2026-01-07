import os
import re
import feedparser
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

# Mots-clés à EXCLURE (simple, ça marche bien)
BLOCKLIST = [
    # guerre / politique violente / sécurité
    "ukraine", "russia", "zelensky", "iran", "protests", "armed", "security forces",
    "attack", "killed", "dead", "violence", "shooting", "terror", "hostage",
    # catastrophes / météo anxiogène
    "verglas", "neige", "tempête", "earthquake", "flood", "storm",
    # fait divers / contenu potentiellement gênant
    "rectum", "porn", "sex", "rape", "anguille",
]

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

2) ...

3) ...

SECTION 2 — ENGLISH
1) Title:
Summary:
Link:

2) ...

3) ...

Liste :
{chr(10).join(news_lines)}
""".strip()

    resp = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt,
    )
    return resp.text.strip()

def main():
    news = fetch_rss_items()
    if len(news) < 8:
        raise RuntimeError("Trop peu d'articles après filtrage. Ajuste la BLOCKLIST ou ajoute des RSS.")

    output = gemini_pick_3(news)
    print(output)

if __name__ == "__main__":
    main()
