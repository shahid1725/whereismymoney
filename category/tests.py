from rest_framework import status

from category.models import Category
from whereismymoney.tests import AuthenticatedAPITestCase


class CategoryAPITests(AuthenticatedAPITestCase):
    def test_user_can_crud_category(self):
        create_response = self.client.post('/api/categories/', {
            'name': 'Salary',
            'icon': 'wallet',
            'type': Category.Type.INCOME,
            'is_default': True,
        })

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        category_id = create_response.data['id']
        category = Category.objects.get(id=category_id)
        self.assertEqual(category.user, self.user)
        self.assertFalse(category.is_default)

        update_response = self.client.patch(
            f'/api/categories/{category_id}/',
            {'icon': 'briefcase'},
        )

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['icon'], 'briefcase')

        delete_response = self.client.delete(f'/api/categories/{category_id}/')

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_access_another_users_category(self):
        category = Category.objects.create(
            user=self.other_user,
            name='Private',
            type=Category.Type.EXPENSE,
        )

        response = self.client.get(f'/api/categories/{category.id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_duplicate_category_name_and_type_is_rejected(self):
        Category.objects.create(
            user=self.user,
            name='Food',
            type=Category.Type.EXPENSE,
        )

        response = self.client.post('/api/categories/', {
            'name': 'Food',
            'type': Category.Type.EXPENSE,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
