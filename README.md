# 📰 AI News Scraper & Summarizer

> Un veilleur d'actualité automatisé qui scrape les dernières news sur l'Intelligence Artificielle, les résume avec un modèle de NLP, et les expose via une API REST accompagnée d'un tableau de bord léger.

## 🚀 Fonctionnalités principales

- **🕷️ Scraping intelligent** : Récupère les titres et contenus depuis des sources d'actu tech (via `Requests` & `BeautifulSoup`).
- **🧠 Résumé automatique** : Utilise un modèle Transformer (`facebook/bart-large-cnn`) pour synthétiser les articles en quelques phrases.
- **💾 Persistance des données** : Stocke les articles dans une base SQLite (évite les doublons grâce aux contraintes d'unicité).
- **⚡ API RESTful** : Construite avec FastAPI, elle expose les articles en JSON avec une documentation interactive générée automatiquement (`/docs`).
- **🖥️ Frontend minimal** : Une page HTML/CSS/JS statique qui consomme l'API et affiche les résumés sous forme de cartes.
- **⏰ Mise à jour automatique** : Un scheduler (APScheduler) lance le scraping en arrière-plan toutes les X heures.

## 🏗️ Stack technique

| Catégorie       | Technologie(s)                                                                 |
|-----------------|--------------------------------------------------------------------------------|
| **Langage**     | Python 3.10+                                                                   |
| **Package Manager** | [`uv`](https://docs.astral.sh/uv/) (ultra-rapide, remplace pip et venv)     |
| **Backend**     | FastAPI, Uvicorn                                                               |
| **Base de données** | SQLite (via SQLAlchemy ORM)                                                 |
| **Scraping**    | Requests, BeautifulSoup4                                                       |
| **IA / NLP**    | HuggingFace Transformers (PyTorch)                                             |
| **Tâches planifiées** | APScheduler                                                           |
| **Frontend**    | HTML, CSS vanilla, JavaScript (Fetch API)                                     |
| **Versioning**  | Git                                                                           |
