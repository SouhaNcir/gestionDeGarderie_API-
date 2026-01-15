#!/bin/bash

# Script de test pour la Dashboard Admin API
# Utilisation: ./test_dashboard.sh

BASE_URL="http://localhost:8000"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="your_password_here"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Test Dashboard Admin API ===${NC}\n"

# Étape 1: Authentification
echo -e "${YELLOW}[1] Obtention du token JWT...${NC}"
AUTH_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login/" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$ADMIN_USERNAME\", \"password\": \"$ADMIN_PASSWORD\"}")

ACCESS_TOKEN=$(echo "$AUTH_RESPONSE" | grep -o '"access":"[^"]*' | cut -d'"' -f4)

if [ -z "$ACCESS_TOKEN" ]; then
  echo -e "${RED}Erreur d'authentification${NC}"
  echo "$AUTH_RESPONSE"
  exit 1
fi

echo -e "${GREEN}✓ Token obtenu avec succès${NC}\n"

# Fonction pour tester un endpoint
test_endpoint() {
  local method=$1
  local endpoint=$2
  local description=$3
  local params=${4:-""}
  
  echo -e "${YELLOW}[$((++COUNTER))] $description${NC}"
  echo "URL: $BASE_URL$endpoint$params"
  
  RESPONSE=$(curl -s -X "$method" "$BASE_URL$endpoint$params" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json")
  
  echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
  echo ""
}

COUNTER=1

# Tests des endpoints
test_endpoint "GET" "/api/dashboard/" "" "Aperçu Dashboard"
test_endpoint "GET" "/api/dashboard/stats/" "" "Statistiques Globales"
test_endpoint "GET" "/api/dashboard/enfants/" "" "Liste des Enfants"
test_endpoint "GET" "/api/dashboard/enfants/" "?groupe=Groupe%20A" "Enfants du Groupe A"
test_endpoint "GET" "/api/dashboard/parents/" "" "Liste des Parents"
test_endpoint "GET" "/api/dashboard/staff/" "" "Liste du Staff"
test_endpoint "GET" "/api/dashboard/users/" "" "Liste des Utilisateurs"
test_endpoint "GET" "/api/dashboard/users/" "?role=parent" "Utilisateurs Parents"

echo -e "${GREEN}=== Tests terminés ===${NC}"
