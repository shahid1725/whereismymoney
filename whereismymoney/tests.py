from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


User = get_user_model()


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
