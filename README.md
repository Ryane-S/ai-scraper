# 📰 SIFT - News Scraper & Summarizer

> Un veilleur d'actualité automatisé qui agrège plusieurs sources (tech, science, politique, géopolitique,...), résume les articles avec un modèle NLP (BART) et les catégorise automatiquement. Le tout est exposé via une API REST.

## Fonctionnalités principales

- **Scraping intelligent** : récupère les titres et contenus depuis des sources d'actualités variées via `Requests`, `Feedparser` et `BeautifulSoup`.
- **Résumé automatique** : utilise un modèle Transformer (`facebook/bart-large-cnn`) pour synthétiser les articles en quelques phrases.
- **Catégorisation automatique** : classe les articles par thème à l'aide d'un modèle d'embeddings (`all-MiniLM-L6-v2`).
- **Persistance des données** : stocke les articles dans une base de données PostgreSQL.
- **API RESTful** : construite avec FastAPI, elle expose les articles au format JSON et propose une documentation interactive générée automatiquement.
- **Frontend minimal** : une interface web statique en HTML, CSS et JavaScript qui consomme l'API et affiche les résumés sous forme de cartes.
- **Mise à jour automatique** : un scheduler (APScheduler) lance le scraping et le nettoyage des données en arrière-plan chaque nuit.

## Stack technique

| Catégorie | Technologies |
|---|---|
| **Gestion des dépendances** | [uv](https://docs.astral.sh/uv/) |
| **Backend** | FastAPI, Uvicorn |
| **Base de données** | PostgreSQL 16.13 |
| **Scraping** | Requests, Feedparser, BeautifulSoup4, Trafilatura |
| **IA / NLP** | Hugging Face Transformers, Sentence Transformers, PyTorch |
| **Tâches planifiées** | APScheduler |
| **Frontend** | HTML, CSS, JavaScript (Fetch API) |
| **Conteneurisation** | Docker, Docker Compose |
| **Déploiement et infrastructure** | AWS EC2 (ARM Graviton), Nginx |

## Installation

Le projet nécessite Python `>=3.12`.

### 1. Installer `uv`

**Windows (PowerShell)**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux / macOS**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Cloner le dépôt

```bash
git clone https://github.com/Ryane-S/sift.git
cd sift
```

### 3. Installer les dépendances

La commande suivante crée automatiquement un environnement virtuel et installe les dépendances spécifiées dans `pyproject.toml` et `uv.lock`.

```bash
uv sync
```

### 4. Configurer PostgreSQL

Assurez-vous que PostgreSQL est installé et en cours d'exécution sur votre machine.

Connectez-vous à PostgreSQL en tant que superutilisateur :

```bash
sudo -u postgres psql
```

Créez ensuite un utilisateur et une base de données :

```sql
CREATE USER votre_utilisateur WITH PASSWORD 'votre_mot_de_passe';
CREATE DATABASE ai_scraper OWNER votre_utilisateur;
GRANT ALL PRIVILEGES ON DATABASE ai_scraper TO votre_utilisateur;
\q
```

### 5. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet et renseignez votre URL de connexion PostgreSQL :

```env
DATABASE_URL=postgresql://votre_utilisateur:votre_mot_de_passe@localhost:5432/ai_scraper
```

Adaptez les identifiants et le nom de la base de données à votre configuration.

### 6. Lancer l'application

```bash
uv run uvicorn app.main:app --reload
```

L'API est accessible à l'adresse `http://localhost:8000`.

La documentation interactive des endpoints est disponible à l'adresse `http://localhost:8000/docs`.

### Lancement local avec Docker Compose

```bash
docker compose up -d --build
```

L'application est alors accessible à l'adresse `http://localhost:8000`.

> **Note :** Au premier démarrage, les modèles Hugging Face sont téléchargés. Ils représentent environ 1,6 Go. Les démarrages suivants sont plus rapides grâce au cache des modèles.