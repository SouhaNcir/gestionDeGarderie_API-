from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserProfile


class AuthenticationTests(TestCase):
    """Tests pour le système d'authentification"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/auth/register/'
        self.login_url = '/auth/login/'
        self.me_url = '/auth/me/'
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPassword123',
            'password_confirm': 'TestPassword123',
            'role': 'parent',
            'telephone': '0123456789'
        }

    def test_user_registration(self):
        """Test l'enregistrement d'un nouvel utilisateur"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_password_mismatch(self):
        """Test l'erreur si les mots de passe ne correspondent pas"""
        data = self.user_data.copy()
        data['password_confirm'] = 'DifferentPassword123'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_username(self):
        """Test que le même username ne peut pas être utilisé deux fois"""
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """Test la connexion d'un utilisateur"""
        self.client.post(self.register_url, self.user_data, format='json')
        
        login_data = {
            'username': 'testuser',
            'password': 'TestPassword123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login(self):
        """Test la connexion avec des identifiants invalides"""
        login_data = {
            'username': 'nonexistent',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_current_user(self):
        """Test la récupération du profil de l'utilisateur actuel"""
        # Créer et connecter l'utilisateur
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'TestPassword123'
        }, format='json')
        
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_unauthorized_access(self):
        """Test que l'accès sans token est refusé"""
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_creation(self):
        """Test que le profil utilisateur est créé automatiquement"""
        self.client.post(self.register_url, self.user_data, format='json')
        user = User.objects.get(username='testuser')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.role, 'parent')
