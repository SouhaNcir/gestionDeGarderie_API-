# 🚀 Guide Démarrage Rapide - Dashboard Admin

## ⚡ 5 minutes pour commencer

### **Étape 1: Vérifier que le serveur est lancé**

```bash
# Le serveur devrait tourner sur:
http://127.0.0.1:8000/
```

### **Étape 2: Accéder à l'Admin (Interface Web)**

```
URL: http://localhost:8000/admin/
Username: admin
Password: (votre mot de passe admin)
```

### **Étape 3: Explorer la Dashboard Admin**

**Cliquez sur :**
- 📌 **Enfants** → Voir tous les enfants avec filtres, badges, export CSV
- 👥 **Parents** → Voir les parents avec nombre d'enfants
- 👨‍🏫 **Staff** → Voir le personnel avec rôles colorés
- 👤 **Users** → Voir les utilisateurs système

---

## 📊 Utiliser l'API REST

### **1. Obtenir le token (Postman)**

**Request:**
```
POST http://localhost:8000/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "your_password"
}
```

**Copier le token `access` de la réponse.**

### **2. Accéder aux statistiques**

**Request:**
```
GET http://localhost:8000/api/dashboard/stats/
Authorization: Bearer <YOUR_TOKEN>
```

**Réponse :**
```json
{
  "total_enfants": 45,
  "total_parents": 30,
  "total_staff": 8,
  "enfants_by_groupe": { "Groupe A": 12, "Groupe B": 15 },
  ...
}
```

### **3. Filtrer les données**

```
GET http://localhost:8000/api/dashboard/enfants/?groupe=Groupe%20A
Authorization: Bearer <YOUR_TOKEN>
```

---

## 🎯 Les 6 Endpoints Clés

```
1. GET /api/dashboard/               → Info & liste endpoints
2. GET /api/dashboard/stats/         → Statistiques globales
3. GET /api/dashboard/enfants/       → Enfants (filtres: groupe, sexe, parent_id)
4. GET /api/dashboard/parents/       → Parents (filtres: nom, email)
5. GET /api/dashboard/staff/         → Staff (filtres: role, nom)
6. GET /api/dashboard/users/         → Users (filtres: role, username, is_active)
```

---

## 💾 Exporter des données

### **Depuis l'Admin Web**

1. Allez sur **Enfants**
2. Sélectionnez les enfants à exporter
3. Action dropdown → **Exporter en CSV**
4. Cliquez "Go" → Fichier téléchargé

### **Depuis l'API**

```bash
curl -X GET "http://localhost:8000/api/dashboard/enfants/" \
  -H "Authorization: Bearer YOUR_TOKEN" > enfants.json
```

---

## 🔍 Exemples de Requêtes

### **1. Enfants du Groupe A**
```
GET /api/dashboard/enfants/?groupe=Groupe%20A
```

### **2. Enfants garçons**
```
GET /api/dashboard/enfants/?sexe=M
```

### **3. Parents sans enfants**
```
GET /api/dashboard/parents/?nom=
```

### **4. Tous les éducateurs**
```
GET /api/dashboard/users/?role=educateur
```

### **5. Utilisateurs actifs uniquement**
```
GET /api/dashboard/users/?is_active=true
```

---

## 🎨 Interface Admin Personnalisée

### **Enfants**
- 📊 Badge sexe (♂/♀ colorés)
- 🎨 Badge groupe (4 couleurs)
- 🔗 Lien direct vers parent/éducateur
- 🔍 Filtres avancés
- 💾 Export CSV

### **Parents**
- 💚 Badge nombre d'enfants en vert
- 📞 Téléphone visible
- 📧 Email visible
- 🔎 Recherche par nom/email/tel

### **Staff**
- 🎨 Badge rôle coloré
- 📊 Nombre enfants assignés
- 👥 Contact visible
- 🔍 Filtres par rôle

---

## ⚠️ Problèmes Courants

### **Erreur 401 - Unauthorized**
```
Solution: Vérifiez le token JWT, il doit être présent et valide
Authorization: Bearer <TOKEN>
```

### **Erreur 403 - Forbidden**
```
Solution: L'utilisateur n'est pas admin
Vérifiez: user.is_staff = True et user.is_superuser = True
```

### **Pas de données affichées**
```
Solution: Créez d'abord des données depuis l'API
POST /api/parents/ + POST /api/enfants/
```

---

## 📚 Documentation Complète

- 📄 [DASHBOARD.md](DASHBOARD.md) - Tous les endpoints
- 📄 [DASHBOARD_USAGE.md](DASHBOARD_USAGE.md) - Guide complet avec exemples
- 📄 [AUTHENTICATION.md](AUTHENTICATION.md) - JWT & Login
- 📄 [SETUP.md](SETUP.md) - Installation initiale

---

## ✨ Fonctionnalités Clés

✅ **Admin Interface**
- Affichage optimisé avec badges
- Filtres avancés
- Liens de navigation
- Actions groupées
- Export CSV

✅ **API REST**
- 6 endpoints principaux
- Filtres et recherches
- Authentification JWT
- Permissions admin
- JSON structuré

✅ **Sécurité**
- JWT (1h access, 7j refresh)
- Authentification requise
- Admin permissions
- CORS configuré

---

## 🎓 Commandes Utiles

```bash
# Démarrer le serveur
python manage.py runserver

# Créer un superuser admin
python manage.py createsuperuser

# Voir les URLs disponibles
python manage.py show_urls | grep dashboard

# Tests
python manage.py test dashboard

# Shell interactif
python manage.py shell
```

---

## 🎯 Prochaines Étapes

1. ✅ **Explorez l'Admin** - Allez sur /admin/
2. ✅ **Testez les APIs** - Utilisez Postman
3. ✅ **Créez des données** - Ajoutez enfants, parents, staff
4. ✅ **Filtrez les données** - Utilisez les paramètres ?groupe, ?role, etc.
5. ✅ **Exportez les rapports** - CSV depuis l'admin

---

## 💡 Cas d'Usage

**Directeur :**
```
GET /api/dashboard/stats/ 
→ Vue complète du système en temps réel
```

**Admin :**
```
GET /api/dashboard/enfants/?groupe=Groupe%20A
→ Gérer les enfants d'un groupe spécifique
```

**Parent :**
```
GET /api/dashboard/users/?role=educateur
→ Voir les éducateurs disponibles
```

---

## 🚀 C'est tout !

Vous avez maintenant une dashboard complète et fonctionnelle ! 

**Accès :**
- 🌐 Web : http://localhost:8000/admin/
- 🔧 API : http://localhost:8000/api/dashboard/

**Besoin d'aide ?**
- Consultez les fichiers DASHBOARD.md, DASHBOARD_USAGE.md
- Vérifiez les logs du serveur
- Testez avec Postman

**Amusez-vous ! 🎉**
