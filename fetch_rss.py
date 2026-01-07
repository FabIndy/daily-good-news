import feedparser

RSS_FEEDS = [
    "https://www.francetvinfo.fr/titres.rss",
    "https://www.lemonde.fr/sciences/rss_full.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.sciencedaily.com/rss/top/science.xml",
]

def fetch_titles(limit_per_feed=5):
    news = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:limit_per_feed]:
            title = entry.title.strip()
            link = entry.link.strip()
            news.append(f"- {title} — {link}")
    return news

if __name__ == "__main__":
    items = fetch_titles()
    print("\n".join(items))
