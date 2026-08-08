# 📰 AI News Scraper & Summarizer

> Un veilleur d'actualité automatisé qui scrape les dernières news sur l'Intelligence Artificielle, les résume avec un modèle de NLP, et les expose via une API REST accompagnée d'un tableau de bord léger.

## Fonctionnalités principales

- **Scraping intelligent** : Récupère les titres et contenus depuis des sources d'actu tech (via `Requests` & `BeautifulSoup`).
- **Résumé automatique** : Utilise un modèle Transformer (`facebook/bart-large-cnn`) pour synthétiser les articles en quelques phrases.
- **Persistance des données** : Stocke les articles dans une base Postgres.
- **API RESTful** : Construite avec FastAPI, elle expose les articles en JSON avec une documentation interactive générée automatiquement (`/docs`).
- **Frontend minimal** : Une page HTML/CSS/JS statique qui consomme l'API et affiche les résumés sous forme de cartes.
- **Mise à jour automatique** : Un scheduler (APScheduler) lance le scraping en arrière-plan toutes les X heures.

## Stack technique

| Catégorie       | Technologie(s)                                                                 |
|-----------------|--------------------------------------------------------------------------------|
| **Python Package Manager** | [`uv`](https://docs.astral.sh/uv/)     |
| **Backend**     | FastAPI, Uvicorn                                                               |
| **Base de données** | PostgreSQL 16.13                                              |
| **Scraping**    | Requests, BeautifulSoup4                                                       |
| **IA / NLP**    | HuggingFace Transformers (PyTorch)                                             |
| **Tâches planifiées** | APScheduler                                                           |
| **Frontend**    | HTML, CSS vanilla, JavaScript (Fetch API)                                     |

## Installation

Ce projet supporte les versions python `>=3.12`. Pour créer votre environnement et lancer l'interface web, suivre les étapes ci-dessous :

* Intaller le package manager `uv` :
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" # Windows
curl -LsSf https://astral.sh/uv/install.sh | sh # Linux / MacOS
```

* Cloner le dépôt distant :
```bash
git clone https://github.com/Ryane-S/ai-scraper.git
```

* Synchroniser les dépendances (cela créera automatiquement un environnement virtuel avec les dépendances spécifiées dans `pyproject.toml` et `uv.lock`) :
```bash
cd ai-scraper
uv sync
```

* Configurer la base de données PostgreSQL :
    * Assurez-vous que PostgreSQL est installé et lancé sur votre machine.
    * Connectez-vous en tant que superutilisateur pour créer la base et l'utilisateur :
        ```bash
        sudo -u postgres psql
        ```
    * Exécutez les commandes SQL suivantes :
        ```sql
        CREATE USER votre_utilisateur WITH PASSWORD 'votre_mot_de_passe';
        CREATE DATABASE ai_scraper OWNER votre_utilisateur;
        GRANT ALL PRIVILEGES ON DATABASE ai_scraper TO votre_utilisateur;
        \q
        ```
    * Créer le fichier d'environnement .env à la racine du projet et y ajouter votre URL de connexion (en adaptant l'utilisateur, le mot de passe et éventuellement le nom de la base)
        ```env
        DATABASE_URL=postgresql://votre_utilisateur:votre_mot_de_passe@localhost:5432/ai_scraper
        ```

* Lancer l'interface web :
```bash
uv run uvicorn app.main:app --reload
```