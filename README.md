## Pokémon Microservices Platform

Plateforme Pokémon basée sur des microservices, utilisant la PokeAPI et une base PostgreSQL pour gérer un Pokédex, les favoris et un leaderboard de popularité.

### Architecture

- **frontend** : interface web simple pour parcourir les Pokémon, gérer les favoris et consulter le leaderboard.
- **gateway** : API gateway qui expose une API unifiée pour le frontend.
- **backend** : microservice qui proxy la PokeAPI et normalise les réponses.
- **favorites-service** : microservice qui persiste les favoris des utilisateurs et calcule les statistiques.
- **database (PostgreSQL)** : stockage des favoris.

### Stack technique

- **Backend / Microservices** : Python + FastAPI
- **Base de données** : PostgreSQL
- **Conteneurisation** : Docker, Docker Compose
- **Orchestration** : Kubernetes (manifests dans `deploy/`)
- **CI/CD** : GitHub Actions (workflows dans `.github/workflows/`)

### Lancement en développement (Docker Compose)

1. Construire et lancer les services :

```bash
docker compose up --build
```

2. Accéder au frontend :

- Naviguer sur `http://localhost:8080`

### Lancement sur Kubernetes (exemple)

1. Appliquer les ConfigMap/Secrets et la base de données :

```bash
kubectl apply -f deploy/configmap.yaml
kubectl apply -f deploy/secret.yaml
kubectl apply -f deploy/postgres-pv-pvc.yaml
kubectl apply -f deploy/postgres-deployment.yaml
```

2. Déployer les microservices :

```bash
kubectl apply -f deploy/backend-deployment.yaml
kubectl apply -f deploy/favorites-deployment.yaml
kubectl apply -f deploy/gateway-deployment.yaml
kubectl apply -f deploy/frontend-deployment.yaml
```

3. Vérifier :

```bash
kubectl get pods,svc,deploy
```

### Utilisation de l’IA

Ce projet utilise un assistant IA pour :

- **Générer la structure du projet et les templates de code** (services FastAPI, Dockerfiles, manifests Kubernetes).
- **Proposer un pipeline CI/CD GitHub Actions**.

Tout le code généré est relu, simplifié et adapté au contexte du projet. En soutenance, il faudra être capable d’expliquer :

- L’architecture globale (services, base, gateway).
- Les principaux endpoints FastAPI.
- Le rôle de Docker, Docker Compose et Kubernetes.
- Le fonctionnement du pipeline CI/CD.

