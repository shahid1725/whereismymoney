from rest_framework import status

from account.models import Account
from category.models import Category
from transaction.models import Transaction
from whereismymoney.tests import AuthenticatedAPITestCase


class TransactionAPITests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user, name='Bank')
        self.category = Category.objects.create(
            user=self.user,
            name='Food',
            type=Category.Type.EXPENSE,
        )

    def test_user_can_crud_transaction(self):
        create_response = self.client.post('/api/transactions/', {
            'account': self.account.id,
            'category': self.category.id,
            'type': Transaction.Type.EXPENSE,
            'amount': '25.50',
            'description': 'Lunch',
            'date': '2026-11-21',
        })

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        transaction_id = create_response.data['id']
        transaction = Transaction.objects.get(id=transaction_id)
        self.assertEqual(transaction.user, self.user)

        update_response = self.client.patch(
            f'/api/transactions/{transaction_id}/',
            {'amount': '30.00'},
        )

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['amount'], '30.00')

        delete_response = self.client.delete(
            f'/api/transactions/{transaction_id}/',
        )

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_transaction_rejects_mismatched_category_type(self):
        response = self.client.post('/api/transactions/', {
            'account': self.account.id,
            'category': self.category.id,
            'type': Transaction.Type.INCOME,
            'amount': '25.50',
            'date': '2026-11-21',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('category', response.data)

    def test_transaction_rejects_another_users_relations(self):
        other_account = Account.objects.create(
            user=self.other_user,
            name='Private Bank',
        )

        response = self.client.post('/api/transactions/', {
            'account': other_account.id,
            'category': self.category.id,
            'type': Transaction.Type.EXPENSE,
            'amount': '25.50',
            'date': '2026-11-21',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('account', response.data)

    def test_account_in_use_cannot_be_deleted(self):
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            type=Transaction.Type.EXPENSE,
            amount='25.50',
            date='2026-11-21',
        )

        response = self.client.delete(f'/api/accounts/{self.account.id}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Account.objects.filter(id=self.account.id).exists())
