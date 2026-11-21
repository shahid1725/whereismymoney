from django.contrib.auth import get_user_model
from django.test import SimpleTestCase
from rest_framework.test import APITestCase


User = get_user_model()


class HealthCheckTests(SimpleTestCase):
    def test_root_returns_success_for_deployed_backend_host(self):
        response = self.client.get(
            '/',
            HTTP_HOST='whereismymoney-xsg2.vercel.app',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'status': 'success',
            'message': 'Backend API is running',
        })


class AuthenticatedAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='owner@example.com',
            name='Owner',
            password='strong-password',
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            name='Other',
            password='strong-password',
        )
        self.client.force_authenticate(self.user)
