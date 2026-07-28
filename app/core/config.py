import os

from dotenv import load_dotenv

# Charger les variables d'environnement depuis env
load_dotenv()

# Lire la connexion string à la base de données
DATABASE_URL = os.getenv("DATABASE_URL")

# Vérifier que DATABASE_URL n'est pas None
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL n'est pas défini dans .env")