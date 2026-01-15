# 📊 Documentation Dashboard Admin

## 🎯 Vue d'ensemble

Le système de dashboard fournit une interface complète pour l'administration avec :
- **API REST** pour les statistiques
- **Interface Django Admin améliorée** avec filtres et badges colorés
- **Endpoints protégés** (authentification requise et admin uniquement)

---

## 🔐 Accès au Dashboard

### 1. **Admin Django - Interface Web**

**URL:** `http://localhost:8000/admin/`

**Identifiants:**
- Username: `admin` (créé lors du setup)
- Password: (votre mot de passe admin)

### 2. **API Dashboard REST**

Tous les endpoints requièrent :
- ✅ **Authentification JWT** (token d'accès)
- ✅ **Permission Admin** (user.is_staff = True)

---

## 📍 Endpoints Dashboard API

### 1. **Aperçu Dashboard** - `GET /api/dashboard/`

Affiche la liste des endpoints disponibles.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Bienvenue dans le tableau de bord administrateur",
  "endpoints": {
    "stats": "/api/dashboard/stats/",
    "enfants": "/api/dashboard/enfants/",
    "parents": "/api/dashboard/parents/",
    "staff": "/api/dashboard/staff/",
    "users": "/api/dashboard/users/"
  }
}
```

---

### 2. **Statistiques Globales** - `GET /api/dashboard/stats/`

Récupère toutes les statistiques clés du système.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "total_enfants": 45,
  "total_parents": 30,
  "total_staff": 8,
  "total_users": 40,
  "enfants_by_groupe": {
    "Groupe A": 12,
    "Groupe B": 15,
    "Groupe C": 18
  },
  "enfants_by_sexe": {
    "M": 23,
    "F": 22
  },
  "staff_by_role": {
    "Directeur": 1,
    "Éducateur": 5,
    "Assistant": 2
  },
  "users_by_role": {
    "admin": 2,
    "educateur": 5,
    "parent": 30,
    "directeur": 3
  },
  "enfants_recents": [
    {
      "id": 45,
      "nom": "Dupont",
      "prenom": "Marie",
      "parent_name": "Jean",
      "educateur_name": "Sophie",
      "groupe": "Groupe A",
      "date_inscription": "2026-01-14"
    }
  ]
}
```

---

### 3. **Liste des Enfants** - `GET /api/dashboard/enfants/`

Liste complète des enfants avec filtres optionnels.

**Paramètres optionnels:**
```
?groupe=Groupe%20A
?sexe=M
?parent_id=1
```

**Response (200 OK):**
```json
{
  "count": 45,
  "results": [
    {
      "id": 1,
      "nom": "Dupont",
      "prenom": "Marie",
      "parent_name": "Jean",
      "educateur_name": "Sophie",
      "groupe": "Groupe A",
      "date_inscription": "2026-01-10"
    }
  ]
}
```

---

### 4. **Liste des Parents** - `GET /api/dashboard/parents/`

Liste complète des parents avec nombre d'enfants.

**Paramètres optionnels:**
```
?nom=Dupont
?email=jean@example.com
```

**Response (200 OK):**
```json
{
  "count": 30,
  "results": [
    {
      "id": 1,
      "nom": "Dupont",
      "prenom": "Jean",
      "email": "jean.dupont@example.com",
      "telephone": "0612345678",
      "total_enfants": 2
    }
  ]
}
```

---

### 5. **Liste du Staff** - `GET /api/dashboard/staff/`

Liste complète du personnel avec rôles.

**Paramètres optionnels:**
```
?role=Éducateur
?nom=Sophie
```

**Response (200 OK):**
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "nom": "Martin",
      "prenom": "Sophie",
      "role": "Éducateur",
      "email": "sophie@example.com",
      "telephone": "0698765432"
    }
  ]
}
```

---

### 6. **Liste des Utilisateurs** - `GET /api/dashboard/users/`

Liste complète des utilisateurs système.

**Paramètres optionnels:**
```
?role=parent
?username=john_doe
?is_active=true
```

**Response (200 OK):**
```json
{
  "count": 40,
  "results": [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "parent",
      "is_active": true
    }
  ]
}
```

---

## 🎨 Interface Django Admin Améliorée

### **Page Enfants**

**Colonnes visibles:**
- ✅ Nom complet (avec lien)
- ✅ Sexe (avec icône ♂/♀)
- ✅ Groupe (badge coloré)
- ✅ Parent (lien cliquable)
- ✅ Éducateur (lien cliquable)
- ✅ Date d'inscription
- ✅ Actions rapides

**Filtres disponibles:**
- Sexe (M/F)
- Groupe
- Date d'inscription
- Parent

**Actions:**
- 📥 **Exporter en CSV** - Télécharger les enfants sélectionnés
- 🔔 **Afficher allergies** - Marquer les enfants avec allergies

---

### **Page Parents**

**Colonnes visibles:**
- ✅ Nom complet
- ✅ Téléphone
- ✅ Email
- ✅ Nombre d'enfants (badge vert)
- ✅ Date d'enregistrement

**Filtres disponibles:**
- Nom
- Prénom

**Fonctionnalités:**
- Recherche par nom, email, téléphone
- Affichage du nombre total d'enfants

---

### **Page Staff**

**Colonnes visibles:**
- ✅ Nom complet
- ✅ Rôle (badge coloré)
- ✅ Téléphone
- ✅ Email
- ✅ Nombre d'enfants assignés

**Badge Rôles:**
- 🔴 Directeur (rouge)
- 🔵 Éducateur (bleu)
- 🟢 Assistant (vert)

**Filtres disponibles:**
- Rôle
- Nom
- Prénom

---

## 📊 Utilisation avec Postman

### **Étape 1: Se connecter et obtenir le token**

```
POST http://localhost:8000/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "votre_mot_de_passe"
}
```

Copier le token `access` de la réponse.

### **Étape 2: Accéder aux statistiques**

```
GET http://localhost:8000/api/dashboard/stats/
Authorization: Bearer <votre_access_token>
```

### **Étape 3: Filtrer les données**

```
GET http://localhost:8000/api/dashboard/enfants/?groupe=Groupe%20A
Authorization: Bearer <votre_access_token>
```

---

## 🔒 Sécurité

Tous les endpoints du dashboard sont protégés par :

1. **Authentification JWT requise**
   - L'utilisateur doit être connecté avec un token valide

2. **Permission Admin requise**
   - `user.is_staff = True`
   - `user.is_superuser = True` (recommandé)

3. **CORS configuré**
   - Accès seulement depuis les domaines autorisés

---

## 💡 Exemples de requêtes

### **1. Obtenir le nombre d'enfants par groupe**

```bash
curl -X GET "http://localhost:8000/api/dashboard/stats/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" | jq '.enfants_by_groupe'
```

### **2. Exporter les enfants du Groupe A**

```bash
curl -X GET "http://localhost:8000/api/dashboard/enfants/?groupe=Groupe%20A" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### **3. Lister les parents avec email**

```bash
curl -X GET "http://localhost:8000/api/dashboard/parents/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

---

## 🛠️ Personnalisation

### **Ajouter un nouveau filtre en Admin**

Dans [enfants/admin.py](../enfants/admin.py):

```python
@admin.register(Enfant)
class EnfantAdmin(admin.ModelAdmin):
    list_filter = ['sexe', 'groupe', 'date_inscription', 'parent', 'educateur']
```

### **Ajouter une nouvelle action**

```python
def marquer_groupe_a(self, request, queryset):
    queryset.update(groupe='Groupe A')
marquer_groupe_a.short_description = "Assigner au Groupe A"

actions = ['marquer_groupe_a']
```

---

## 📈 Métriques disponibles

| Métrique | Endpoint | Description |
|----------|----------|-------------|
| Total enfants | `/api/dashboard/stats/` | Nombre total d'enfants |
| Total parents | `/api/dashboard/stats/` | Nombre total de parents |
| Total staff | `/api/dashboard/stats/` | Nombre total du personnel |
| Total utilisateurs | `/api/dashboard/stats/` | Nombre total d'utilisateurs |
| Enfants par groupe | `/api/dashboard/stats/` | Distribution par groupe |
| Enfants par sexe | `/api/dashboard/stats/` | Distribution M/F |
| Staff par rôle | `/api/dashboard/stats/` | Distribution des rôles |
| Utilisateurs par rôle | `/api/dashboard/stats/` | Distribution des rôles système |

---

## ⚠️ Codes d'erreur

| Code | Erreur | Solution |
|------|--------|----------|
| 401 | Unauthorized | Token manquant ou expiré |
| 403 | Forbidden | Utilisateur non admin |
| 404 | Not Found | Endpoint invalide |
| 500 | Server Error | Erreur serveur |

---

## 📞 Support

Pour des questions :
- Consultez la documentation Django Admin
- Vérifiez les logs serveur `python manage.py runserver`
- Testez avec Postman en utilisant la collection fournie
