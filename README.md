# Bamk - Application Bancaire

Bamk est une application bancaire complète qui permet la gestion des prêts, des actualités, des utilisateurs, et des fonctionnalités de chat en temps réel. Cette application est construite avec Django pour le backend principal et intègre FastAPI pour la modélisation et les services rapides.

## Fonctionnalités

- **Gestion des utilisateurs** : Inscription, connexion, et gestion des rôles (client, conseiller).
- **Gestion des prêts** : Demandes de prêt, suivi des statuts (approuvé/rejeté), et historique des prêts.
- **Actualités** : Création, modification, suppression et affichage des articles d'actualité.
- **Chat en temps réel** : Communication entre les clients et les conseillers.
- **Modélisation avec FastAPI** : Services rapides pour la prédiction et l'analyse des données liées aux prêts.

---

## Structure du Projet

Voici un aperçu de la structure du projet :

```
Bamk/
├── manage.py
├── Bamk/                # Configuration principale de Django
├── chat/                # Application de chat en temps réel
├── loan/                # Application de gestion des prêts
├── news/                # Application de gestion des actualités
├── user/                # Application de gestion des utilisateurs
├── theme/               # Gestion des styles et des templates globaux
├── media/               # Fichiers médias (ex : images des actualités)
├── staticfiles/         # Fichiers statiques collectés
└── fastapi/             # API FastAPI pour la modélisation
```

---

## Installation

### Prérequis

- Python 3.10 ou supérieur
- Node.js (pour gérer les styles avec Tailwind CSS)
- PostgreSQL (ou une autre base de données compatible avec Django)
- FastAPI et Uvicorn

### Étapes d'installation

1. **Cloner le dépôt :**

   ```bash
   git clone git@github.com:RaoufAddeche/Simplon_App_bancaire_Django.git
   cd bamk
   ```

2. **Créer un environnement virtuel et installer les dépendances :**

   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows : env\Scriptsctivate
   pip install -r requirements.txt
   ```

3. **Configurer la base de données :**

   Modifiez le fichier `Bamk/settings.py` pour configurer votre base de données PostgreSQL.

   Exemple de configuration :

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'bamk_db',
           'USER': 'postgres',
           'PASSWORD': 'votre_mot_de_passe',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

4. **Appliquer les migrations :**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Lancer le serveur Django :**

   ```bash
   python manage.py runserver
   ```

6. **Installer et configurer les styles avec Tailwind CSS :**

   ```bash
   cd theme/static_src
   npm install
   npm run build
   ```

7. **Lancer le serveur FastAPI :**

   Naviguez dans le répertoire `fastapi/` et lancez le serveur :

   ```bash
   uvicorn main:app --reload
   ```

---

## Utilisation

### 1. **Démarrage de l'application**

- Accédez à l'interface utilisateur via [http://127.0.0.1:8080](http://127.0.0.1:8080).
- L'API FastAPI est accessible via [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 2. **Fonctionnalités principales**

- **Connexion/Inscription** : Les utilisateurs peuvent s'inscrire et se connecter pour accéder à leurs fonctionnalités respectives.
- **Gestion des prêts** : Les clients peuvent soumettre des demandes de prêt, et les conseillers peuvent les approuver ou les rejeter.
- **Chat en temps réel** : Les clients et les conseillers peuvent communiquer via une interface de chat.
- **Actualités** : Les administrateurs peuvent gérer les articles d'actualité.

### 3. **API FastAPI**

L'API FastAPI est utilisée pour des fonctionnalités avancées comme la modélisation des prêts. Voici un exemple d'endpoint :

- **Endpoint de prédiction :**

  ```http
  POST /predict-loan
  ```

  **Exemple de payload :**

  ```json
  {
      "income": 50000,
      "loan_amount": 20000,
      "credit_score": 700
  }
  ```

  **Réponse :**

  ```json
  {
      "approval_status": "Approved",
      "interest_rate": 5.5
  }
  ```

---

## Tests

Pour exécuter les tests unitaires, utilisez la commande suivante :

```bash
python manage.py test
```

---

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre les étapes suivantes :

1. Forkez le projet.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalite`).
3. Commitez vos modifications (`git commit -m 'Ajout de ma fonctionnalité'`).
4. Poussez votre branche (`git push origin feature/ma-fonctionnalite`).
5. Ouvrez une Pull Request.

---

## Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.
