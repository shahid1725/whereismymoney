from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework import status

from account.models import Account
from whereismymoney.tests import AuthenticatedAPITestCase


@override_settings(STORAGES={
    'default': {
        'BACKEND': 'django.core.files.storage.InMemoryStorage',
    },
})
class AccountAPITests(AuthenticatedAPITestCase):
    def test_user_can_create_update_and_delete_account(self):
        image_data = BytesIO()
        Image.new('RGB', (1, 1)).save(image_data, format='PNG')
        image_data.seek(0)
        image = SimpleUploadedFile(
            'wallet.png',
            image_data.read(),
            content_type='image/png',
        )
        create_response = self.client.post('/api/accounts/', {
            'name': 'Wallet',
            'img': image,
        }, format='multipart')

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        account_id = create_response.data['id']
        account = Account.objects.get(id=account_id)
        self.assertEqual(account.user, self.user)
        self.assertTrue(account.img.name.startswith('accounts/'))

        update_response = self.client.patch(
            f'/api/accounts/{account_id}/',
            {'name': 'Cash Wallet'},
        )

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['name'], 'Cash Wallet')

        delete_response = self.client.delete(f'/api/accounts/{account_id}/')

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Account.objects.filter(id=account_id).exists())

    def test_user_cannot_access_another_users_account(self):
        account = Account.objects.create(user=self.other_user, name='Private')

        detail_response = self.client.get(f'/api/accounts/{account.id}/')
        list_response = self.client.get('/api/accounts/')

        self.assertEqual(detail_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(list_response.data), 0)

    def test_duplicate_account_name_is_rejected(self):
        Account.objects.create(user=self.user, name='Wallet')

        response = self.client.post('/api/accounts/', {'name': 'Wallet'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
