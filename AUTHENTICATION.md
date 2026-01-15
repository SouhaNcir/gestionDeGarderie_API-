# Documentation API - Authentification

## 📋 Vue d'ensemble

Le système d'authentification utilise **JWT (JSON Web Tokens)** avec Django REST Framework SimpleJWT. Cela permet une authentification sécurisée et stateless pour l'API.

## 🔐 Endpoints d'authentification

### 1. **Inscription** - `POST /auth/register/`

Créer un nouvel utilisateur avec un profil.

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "SecurePassword123",
  "password_confirm": "SecurePassword123",
  "role": "parent",
  "telephone": "0123456789"
}
```

**Paramètres:**
- `username` (string, required): Nom d'utilisateur unique
- `email` (string, required): Adresse email unique
- `first_name` (string, optional): Prénom
- `last_name` (string, optional): Nom
- `password` (string, required): Mot de passe (min 8 caractères)
- `password_confirm` (string, required): Confirmation du mot de passe
- `role` (string, optional): Rôle utilisateur
  - `parent` (défaut)
  - `educateur`
  - `directeur`
  - `admin`
- `telephone` (string, optional): Numéro de téléphone

**Response (201 Created):**
```json
{
  "message": "Utilisateur créé avec succès",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "profile": {
      "id": 1,
      "role": "parent",
      "telephone": "0123456789",
      "is_active": true,
      "created_at": "2026-01-14T10:30:00Z"
    }
  }
}
```

---

### 2. **Connexion (Login)** - `POST /auth/login/`

Obtenir les tokens JWT pour accéder à l'API.

**Request:**
```json
{
  "username": "john_doe",
  "password": "SecurePassword123"
}
```

**Response (200 OK):**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "profile": {
      "id": 1,
      "role": "parent",
      "telephone": "0123456789",
      "is_active": true,
      "created_at": "2026-01-14T10:30:00Z"
    }
  }
}
```

---

### 3. **Renouveler le Token** - `POST /auth/refresh/`

Générer un nouveau token d'accès à partir du refresh token.

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 4. **Récupérer le Profil** - `GET /auth/me/`

Obtenir les informations de l'utilisateur actuellement connecté.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "profile": {
    "id": 1,
    "role": "parent",
    "telephone": "0123456789",
    "is_active": true,
    "created_at": "2026-01-14T10:30:00Z"
  }
}
```

---

### 5. **Mettre à jour le Profil** - `PUT /auth/me/update/`

Mettre à jour les informations du profil utilisateur.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request:**
```json
{
  "first_name": "Jonathan",
  "last_name": "Doe",
  "email": "jonathan@example.com",
  "telephone": "0987654321"
}
```

**Response (200 OK):**
```json
{
  "message": "Profil mis à jour avec succès",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "jonathan@example.com",
    "first_name": "Jonathan",
    "last_name": "Doe",
    "profile": {
      "id": 1,
      "role": "parent",
      "telephone": "0987654321",
      "is_active": true,
      "created_at": "2026-01-14T10:30:00Z"
    }
  }
}
```

---

### 6. **Changer le Mot de passe** - `POST /auth/change-password/`

Changer le mot de passe de l'utilisateur.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request:**
```json
{
  "old_password": "SecurePassword123",
  "new_password": "NewSecurePassword456",
  "new_password_confirm": "NewSecurePassword456"
}
```

**Response (200 OK):**
```json
{
  "message": "Mot de passe modifié avec succès"
}
```

---

### 7. **Déconnexion (Logout)** - `POST /auth/logout/`

Terminer la session (optionnel).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Logout réussi"
}
```

---

## 🔄 Flux d'authentification

```
1. Utilisateur s'inscrit → POST /auth/register/
2. Utilisateur se connecte → POST /auth/login/
   (Reçoit access_token et refresh_token)
3. Utilisateur utilise access_token → Header: Authorization: Bearer {access_token}
4. Access token expire (1h) → POST /auth/refresh/ pour un nouveau token
5. Utilisateur se déconnecte → POST /auth/logout/
```

---

## 💾 Utilisation avec Postman

### Étape 1: Inscription
```
POST http://localhost:8000/auth/register/
Content-Type: application/json

{
  "username": "test_user",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "password": "TestPass123",
  "password_confirm": "TestPass123",
  "role": "parent",
  "telephone": "0123456789"
}
```

### Étape 2: Connexion
```
POST http://localhost:8000/auth/login/
Content-Type: application/json

{
  "username": "test_user",
  "password": "TestPass123"
}
```

**Copier le `access` token de la réponse.**

### Étape 3: Utiliser l'API protégée
```
GET http://localhost:8000/auth/me/
Authorization: Bearer <votre_access_token>
```

---

## 🔑 Variables d'environnement recommandées

```env
# settings.py
SECRET_KEY = 'your-secret-key'
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# JWT
JWT_ACCESS_TOKEN_LIFETIME = 60  # minutes
JWT_REFRESH_TOKEN_LIFETIME = 7  # days

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://yourdomain.com'
]
```

---

## ⚠️ Codes d'erreur

| Code | Erreur | Description |
|------|--------|-------------|
| 400 | Bad Request | Les données envoyées sont invalides |
| 401 | Unauthorized | Token absent ou invalide |
| 403 | Forbidden | Accès refusé (permissions insuffisantes) |
| 404 | Not Found | Ressource non trouvée |
| 409 | Conflict | Username ou email déjà existant |

---

## 🛡️ Bonnes pratiques de sécurité

1. **Stockez les tokens de manière sécurisée** (localStorage, sessionStorage)
2. **Utilisez HTTPS en production**
3. **Renouvelez régulièrement les refresh tokens**
4. **Validez toujours les inputs côté serveur**
5. **Utilisez des mots de passe forts** (min 8 caractères)
6. **Configurez CORS correctement** pour votre domaine

---

## 📚 Ressources utiles

- [Django REST Framework](https://www.django-rest-framework.org/)
- [SimpleJWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
- [JWT.io](https://jwt.io/)
