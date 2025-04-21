FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl build-essential gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copier uniquement requirements.txt depuis backend
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Créer un répertoire pour les logs
RUN mkdir -p /app/logs

# Copier tout le code de backend dans le conteneur
COPY . .

# Configurer les variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Exposer le port
EXPOSE 8000

# Lancer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
