# Guide d'installation et de configuration

## ✅ Prérequis
- Python 3.10+
- pip
- Virtual Environment (recommandé)

## 🚀 Installation

### 1. Cloner le projet
```bash
cd gestionDeGarderie_API
```

### 2. Créer un environnement virtuel
```bash
python -m venv env
env\Scripts\activate  # Windows
# ou
source env/bin/activate  # Mac/Linux
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations
```bash
python manage.py migrate
```

### 5. Créer un super utilisateur (admin)
```bash
python manage.py createsuperuser
```
Entrez les informations demandées :
- Username: admin
- Email: admin@example.com
- Password: (saisissez un mot de passe sécurisé)

### 6. Lancer le serveur de développement
```bash
python manage.py runserver
```

Le serveur démarre sur `http://localhost:8000`

---

## 📌 Endpoints principaux

### Authentification
- **POST** `/auth/register/` - S'enregistrer
- **POST** `/auth/login/` - Se connecter et obtenir les tokens
- **POST** `/auth/refresh/` - Renouveler l'access token
- **GET** `/auth/me/` - Récupérer le profil actuel
- **PUT** `/auth/me/update/` - Mettre à jour le profil
- **POST** `/auth/change-password/` - Changer le mot de passe

### API REST (Avec authentification JWT)
- **GET** `/api/enfants/` - Lister les enfants
- **POST** `/api/enfants/` - Créer un enfant
- **GET** `/api/parents/` - Lister les parents
- **POST** `/api/parents/` - Créer un parent
- **GET** `/api/staffs/` - Lister le personnel

### Admin
- **Admin Panel**: `http://localhost:8000/admin/`

---

## 🔐 Test avec Postman

### 1. Enregistrement
```
POST http://localhost:8000/auth/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "SecurePassword123",
  "password_confirm": "SecurePassword123",
  "role": "parent"
}
```

### 2. Connexion
```
POST http://localhost:8000/auth/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePassword123"
}
```

Copier le token `access` de la réponse.

### 3. Utiliser l'API protégée
```
GET http://localhost:8000/api/enfants/
Authorization: Bearer <votre_access_token>
```

---

## 📝 Variables d'environnement (.env)

Créer un fichier `.env` à la racine du projet :

```
DEBUG=True
SECRET_KEY=django-insecure-u5@j#yj@si&unr0ts+79nj6rgyfb(v061*ivo%%6yi_cl%n71o
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=604800
```

---

## 🧪 Tests

Exécuter les tests :
```bash
python manage.py test accounts
python manage.py test enfants
```

---

## 🛠️ Commandes utiles

```bash
# Créer une nouvelle application
python manage.py startapp nom_app

# Faire les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Voir toutes les URL
python manage.py show_urls

# Vider la base de données
python manage.py flush

# Shell Django interactif
python manage.py shell
```

---

## 📚 Structure du projet

```
gestionDeGarderie_API/
├── accounts/              # App d'authentification
│   ├── migrations/
│   ├── models.py          # UserProfile
│   ├── serializers.py     # Sérializers JWT
│   ├── views.py           # Endpoints d'authentification
│   ├── urls.py            # Routes d'authentification
│   ├── admin.py           # Configuration admin
│   └── tests.py           # Tests d'authentification
├── enfants/               # App gestion des enfants
│   ├── models.py          # Enfant, Parent, Staff
│   ├── serializers.py     # Sérializers
│   └── views.py           # Endpoints
├── project/               # Configuration Django
│   ├── settings.py        # Paramètres
│   ├── urls.py            # Routes principales
│   └── wsgi.py
├── manage.py
├── requirements.txt       # Dépendances
├── AUTHENTICATION.md      # Documentation authentification
└── SETUP.md               # Ce fichier
```

---

## ⚠️ Dépannage

### Erreur: "ModuleNotFoundError: No module named 'rest_framework'"
```bash
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
```

### Erreur: "django.core.exceptions.ImproperlyConfigured"
Vérifier que `INSTALLED_APPS` dans `settings.py` contient toutes les apps.

### Erreur: "No such table: auth_user"
```bash
python manage.py migrate
```

### Port 8000 déjà utilisé
```bash
python manage.py runserver 8080
```

---

## 🔒 Sécurité en production

1. **Changer SECRET_KEY** dans settings.py
2. **Mettre DEBUG=False**
3. **Configurer ALLOWED_HOSTS** correctement
4. **Utiliser une base de données PostgreSQL**
5. **Activer HTTPS**
6. **Configurer CORS** pour votre domaine

---

## 📞 Support

Pour des questions ou problèmes, consultez :
- [Documentation Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SimpleJWT Docs](https://django-rest-framework-simplejwt.readthedocs.io/)
