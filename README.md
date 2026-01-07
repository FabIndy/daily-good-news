# Daily Good News — AI-Powered Positive News Digest

## 1. Project Overview (English)

### Motivation

Modern news media tend to focus heavily on negative, alarming, and anxiety-inducing events.  
While this is often justified by their informational role, it can lead to a distorted perception of reality and contribute to chronic stress or pessimism.

The idea behind **Daily Good News** is simple:
> Provide a short, daily, curated selection of *constructive and positive news* to restore a more balanced view of the world.

This project is a lightweight automation that sends **three carefully selected “good news” items every day**, in **both French and English**, directly to the user’s email inbox.

---

### What the Tool Does

Every day (or at the next laptop startup if it was powered off), the tool:

1. Collects recent news headlines from multiple RSS feeds  
2. Filters out:
   - wars, violence, disasters, sensationalism  
   - anxiety-inducing or inappropriate topics  
3. Uses an AI model to:
   - select **three genuinely positive and constructive news items**  
   - summarize them concisely  
   - generate output in **French and English**  
4. Sends the result automatically by email via Gmail  

The entire workflow is fully automated and runs locally on a personal laptop.

---

### Key Features

- RSS-based news collection (no scraping)  
- AI-assisted curation and summarization (Gemini API – free tier)  
- Bilingual output (French / English)  
- Automated email delivery (Gmail SMTP)  
- Laptop-friendly scheduling using *anacron*  
- Secure handling of secrets via environment variables  
- 100% free operation  

---

### Technical Stack

- Python 3  
- RSS feeds (France Info, Le Monde Sciences, BBC, ScienceDaily)  
- Gemini API (`gemini-flash-latest`)  
- Gmail SMTP (application password)  
- anacron  
- python-dotenv  

---

### Why Anacron (and not Cron)?

This project is designed to run on a **personal laptop**, not on a 24/7 server.

- Cron misses executions when the machine is powered off  
- Anacron guarantees:
  - one execution per day  
  - automatic catch-up at next startup  
  - no duplicate emails  

This makes the automation robust and realistic for everyday use.

---

### How to Run

1. Create a virtual environment  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file containing:
   - Gemini API key  
   - Gmail SMTP credentials  
4. Run manually:
   ```bash
   python daily_good_news.py
   ```
5. (Optional) Configure *anacron* for full automation  

---

### Intended Use

This tool is designed for:
- personal well-being  
- daily positive information intake  
- demonstrating automation and AI integration skills  

It is **not intended for mass mailing or commercial use**.

---

## 2. Présentation du projet (Français)

### Origine de l’idée

Les médias d’information ont naturellement tendance à se concentrer sur :
- les crises  
- les conflits  
- les catastrophes  
- les événements anxiogènes  

Cette focalisation peut conduire à une vision excessivement négative du monde.

L’objectif de **Daily Good News** est volontairement simple :
> Offrir chaque jour une courte sélection de nouvelles positives, constructives et porteuses de sens.

Ce mini-projet vise à **rééquilibrer la perception de l’actualité**, sans naïveté, mais avec intention.

---

### Fonctionnement général

Chaque jour (ou au prochain démarrage de l’ordinateur si celui-ci était éteint), le script :

1. Récupère des titres d’actualité via des flux RSS fiables  
2. Élimine automatiquement :
   - les sujets violents ou anxiogènes  
   - les faits divers  
   - le sensationnalisme  
3. Utilise un modèle d’IA pour :
   - sélectionner **trois “bonnes nouvelles”**  
   - produire des résumés courts et clairs  
   - générer une version **française et anglaise**  
4. Envoie le résultat par email  

L’ensemble du processus est entièrement automatisé et s’exécute localement.

---

### Choix techniques

- RSS : sources simples, transparentes et robustes  
- IA générative : utilisée pour la curation et la synthèse, pas comme source d’information  
- Anacron : adapté à un ordinateur personnel  
- Variables d’environnement : aucune donnée sensible dans le code  
- Approche minimaliste : maintenance facile  

---

### Philosophie du projet

Ce projet ne cherche pas à nier la réalité du monde, mais à :
- mettre en lumière les progrès  
- valoriser la recherche scientifique  
- rappeler les dynamiques positives souvent invisibles dans le flux médiatique  

C’est un outil modeste, mais volontairement utile.

---

### Auteur

Projet personnel développé dans une démarche :
- d’apprentissage continu  
- de pratique concrète de l’automatisation  
- d’utilisation raisonnée de l’IA  

---

### Licence

Projet open-source, usage personnel ou éducatif.
