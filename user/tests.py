from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationAPITests(APITestCase):
    def test_register_login_refresh_and_current_user(self):
        register_response = self.client.post('/api/auth/register/', {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'strong-password',
        })

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', register_response.data)

        login_response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'strong-password',
        })

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        self.assertIn('refresh', login_response.data)

        refresh_response = self.client.post('/api/auth/refresh/', {
            'refresh': login_response.data['refresh'],
        })

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {login_response.data["access"]}',
        )
        current_user_response = self.client.get('/api/auth/me/')

        self.assertEqual(current_user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(current_user_response.data['email'], 'test@example.com')

    def test_current_user_requires_authentication(self):
        response = self.client.get('/api/auth/me/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
