# 🏥 Gestion de Garderie - API Backend

**Système complet de gestion de garderie avec authentification JWT et dashboard admin professionnelle.**

[![Django](https://img.shields.io/badge/Django-5.2.10-darkgreen)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-darkblue)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Installation Rapide](#-installation-rapide)
- [Documentation](#-documentation)
- [API Endpoints](#-api-endpoints)
- [Authentification](#-authentification)
- [Dashboard Admin](#-dashboard-admin)
- [Architecture](#-architecture)
- [Contribution](#-contribution)

---

## ✨ Fonctionnalités

### 🔐 **Authentification & Sécurité**
- ✅ Authentification JWT complète
- ✅ Refresh tokens (7 jours)
- ✅ Système de rôles (Admin, Éducateur, Parent, Directeur)
- ✅ Permissions granulaires

### 📊 **Dashboard Admin**
- ✅ Interface Web Django Admin améliorée
- ✅ 6 Endpoints API dashboard
- ✅ Statistiques en temps réel
- ✅ Filtres et recherches avancées
- ✅ Export CSV

### 👶 **Gestion Enfants**
- ✅ Créer/Modifier/Supprimer enfants
- ✅ Gestion des allergies et remarques médicales
- ✅ Attribution à parents et éducateurs
- ✅ Groupes et calendriers

### 👥 **Gestion Parents & Staff**
- ✅ Gestion des parents
- ✅ Gestion du personnel (éducateurs, directeurs)
- ✅ Affectation des responsabilités

### 📱 **API REST**
- ✅ 15+ endpoints REST
- ✅ Filtres et recherches
- ✅ Pagination
- ✅ Taux de limitation (throttling)

---

## 🚀 Installation Rapide

### **Prérequis**
- Python 3.10+
- pip
- Virtual Environment (recommandé)

### **1. Cloner et installer**
```bash
cd gestionDeGarderie_API
python -m venv env
env\Scripts\activate  # Windows

pip install -r requirements.txt
```

### **2. Configuration**
```bash
python manage.py migrate
python manage.py createsuperuser
```

### **3. Démarrer**
```bash
python manage.py runserver
```

✅ **API disponible sur** : http://localhost:8000/

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| 📄 [QUICK_START.md](QUICK_START.md) | ⚡ Démarrage rapide (5 min) |
| 📄 [SETUP.md](SETUP.md) | 📖 Guide installation complet |
| 📄 [AUTHENTICATION.md](AUTHENTICATION.md) | 🔐 Guide authentification JWT |
| 📄 [DASHBOARD.md](DASHBOARD.md) | 📊 API dashboard détaillée |
| 📄 [DASHBOARD_USAGE.md](DASHBOARD_USAGE.md) | 💡 Exemples d'utilisation |
| 📄 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | 🏗️ Architecture du projet |

---

## 🔗 API Endpoints

### **Authentification** 🔐
```
POST   /auth/register/              → Inscription
POST   /auth/login/                 → Connexion (JWT)
POST   /auth/refresh/               → Renouveler token
GET    /auth/me/                    → Profil utilisateur
PUT    /auth/me/update/             → Mettre à jour profil
POST   /auth/change-password/       → Changer mot de passe
```

### **Dashboard Admin** 👨‍💼 (Authentification + Admin required)
```
GET    /api/dashboard/              → Aperçu
GET    /api/dashboard/stats/        → Statistiques globales
GET    /api/dashboard/enfants/      → Liste enfants
GET    /api/dashboard/parents/      → Liste parents
GET    /api/dashboard/staff/        → Liste personnel
GET    /api/dashboard/users/        → Liste utilisateurs
```

### **API REST Enfants** 👶
```
GET    /api/enfants/                → Liste
POST   /api/enfants/                → Créer
GET    /api/enfants/{id}/           → Détail
PUT    /api/enfants/{id}/           → Modifier
DELETE /api/enfants/{id}/           → Supprimer
```

**Pareillement pour** : `/api/parents/` et `/api/staffs/`

---

## 🔐 Authentification

### **1. S'enregistrer**
```bash
curl -X POST http://localhost:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123",
    "role": "parent"
  }'
```

### **2. Se connecter**
```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123"
  }'
```

**Réponse:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {...}
}
```

### **3. Utiliser l'API**
```bash
curl -X GET http://localhost:8000/api/enfants/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

## 📊 Dashboard Admin

### **Interface Web** 🌐

Accédez à : **http://localhost:8000/admin/**

**Fonctionnalités:**
- 🎨 Interface colorée avec badges
- 🔍 Filtres avancés
- 🔎 Recherche par nom/email/téléphone
- 💾 Export CSV en 1 clic
- 🔗 Liens de navigation rapide

### **API Dashboard** 🔧

```bash
# Authentifiez-vous d'abord
TOKEN="votre_token_ici"

# Statistiques globales
curl -X GET http://localhost:8000/api/dashboard/stats/ \
  -H "Authorization: Bearer $TOKEN"

# Enfants d'un groupe
curl -X GET "http://localhost:8000/api/dashboard/enfants/?groupe=Groupe%20A" \
  -H "Authorization: Bearer $TOKEN"

# Tous les éducateurs
curl -X GET "http://localhost:8000/api/dashboard/users/?role=educateur" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🏗️ Architecture

```
Backend (Django REST)
    ↓
┌───────────────────────────────┐
│   Authentication (JWT)         │
│   • Register / Login           │
│   • Token Management           │
│   • Role-based Permissions     │
└───────────────────────────────┘
    ↓
┌───────────────────────────────┐
│   Dashboard & Statistics       │
│   • Real-time metrics          │
│   • Advanced filters           │
│   • CSV export                 │
└───────────────────────────────┘
    ↓
┌───────────────────────────────┐
│   REST API Endpoints           │
│   • Enfants / Parents / Staff  │
│   • Full CRUD operations       │
│   • Search & Pagination        │
└───────────────────────────────┘
    ↓
┌───────────────────────────────┐
│   Database (SQLite/PostgreSQL) │
│   • Users, Profiles            │
│   • Enfants, Parents, Staff    │
└───────────────────────────────┘
```

---

## 🛠️ Technologies

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 5.2.10 |
| **API** | Django REST Framework 3.16.1 |
| **Auth** | JWT (djangorestframework-simplejwt) |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **CORS** | django-cors-headers |
| **Python** | 3.10+ |

---

## 📋 Configuration

### **settings.py** Highlights
```python
# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'accounts',        # JWT Auth
    'dashboard',       # Admin Dashboard
    'enfants',        # Main App
]

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
]
```

---

## 🔒 Sécurité

✅ **JWT Tokens**
- Access Token : 1 heure
- Refresh Token : 7 jours
- Algorithme : HS256

✅ **Permissions**
- Authentification requise
- Rôles basés sur les permissions
- Admin exclusif pour dashboard

✅ **CORS**
- Domaines whitelist
- Credentials autorisés

✅ **Bonnes Pratiques**
- Mots de passe hashés (PBKDF2)
- SQL injection prévenue
- CSRF protection activée

---

## 📈 Utilisation

### **Cas d'usage**

**Directeur :**
```
GET /api/dashboard/stats/
→ Vue complète du système
```

**Administrateur :**
```
GET /api/dashboard/enfants/?groupe=Groupe%20A
→ Gérer groupe spécifique
```

**Parent :**
```
GET /api/enfants/?parent=1
→ Voir ses enfants
```

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📞 Support

### **Documentation**
- 📄 Voir les fichiers markdown dans le dossier root
- 📚 Collection Postman fournie

### **Dépannage**
- 🔍 Vérifiez `python manage.py runserver` logs
- 🔧 Testez avec `curl` ou Postman
- 📖 Consultez SETUP.md pour les problèmes communs

### **Questions?**
- 📧 Consultez la documentation
- 🐛 Vérifiez les issues
- 💬 Ouvrez une issue

---

## 📜 License

MIT License - Voir [LICENSE](LICENSE) pour plus de détails

---

## 🚀 Démarrage Rapide

```bash
# 1. Installation
git clone <repo>
cd gestionDeGarderie_API
python -m venv env
env\Scripts\activate
pip install -r requirements.txt

# 2. Setup
python manage.py migrate
python manage.py createsuperuser

# 3. Démarrer
python manage.py runserver

# 4. Accès
# - Web: http://localhost:8000/admin/
# - API: http://localhost:8000/api/
# - Docs: Voir QUICK_START.md
```

---

## 📊 Stats du Projet

- 📁 **Apps** : 3 complètes (accounts, dashboard, enfants)
- 🔗 **Endpoints** : 15+
- 📄 **Modèles** : 5
- 📚 **Documentation** : 6 fichiers complets
- 🔐 **Sécurité** : JWT + Permissions
- 🎨 **Interface** : Admin amélioré

---

## ✨ Features Highlights

🎯 **Production Ready**
- ✅ Authentification JWT complète
- ✅ Admin interface professionnelle
- ✅ API REST sécurisée
- ✅ Documentation complète

🚀 **Scalable**
- ✅ Architecture modulaire
- ✅ Permissions granulaires
- ✅ Filtres et recherches
- ✅ Pagination support

📖 **Well Documented**
- ✅ 6 fichiers de documentation
- ✅ Collection Postman
- ✅ Scripts de test
- ✅ Exemples curl

---

## 🎯 Prochaines Étapes

1. ✅ Voir [QUICK_START.md](QUICK_START.md) pour démarrer
2. ✅ Tester avec Postman (Collection fournie)
3. ✅ Créer les premières données
4. ✅ Explorer le Dashboard Admin
5. ✅ Intégrer avec votre frontend

---

## 🙏 Remerciements

Merci à :
- Django & Django REST Framework
- SimpleJWT team
- La communauté Python

---

<div align="center">

**Construit avec ❤️ en Django**

[Star us on GitHub](#) • [Report issues](#) • [Contribute](#)

---

**Prêt à explorer ? [Commencer →](QUICK_START.md)**

</div>
