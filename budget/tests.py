from rest_framework import status

from budget.models import Budget
from category.models import Category
from whereismymoney.tests import AuthenticatedAPITestCase


class BudgetAPITests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(
            user=self.user,
            name='Food',
            type=Category.Type.EXPENSE,
        )

    def test_user_can_create_monthly_and_category_budgets(self):
        monthly_response = self.client.post('/api/budgets/', {
            'amount': '1000.00',
            'month': 11,
            'year': 2026,
        })
        category_response = self.client.post('/api/budgets/', {
            'category': self.category.id,
            'amount': '300.00',
            'month': 11,
            'year': 2026,
        })

        self.assertEqual(monthly_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(category_response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(monthly_response.data['category'])
        self.assertEqual(category_response.data['category'], self.category.id)

    def test_budget_rejects_invalid_month_and_amount(self):
        response = self.client.post('/api/budgets/', {
            'amount': '0.00',
            'month': 13,
            'year': 2026,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)
        self.assertIn('month', response.data)

    def test_user_cannot_access_another_users_budget(self):
        budget = Budget.objects.create(
            user=self.other_user,
            amount='100.00',
            month=11,
            year=2026,
        )

        response = self.client.get(f'/api/budgets/{budget.id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_budget_rejects_another_users_category(self):
        category = Category.objects.create(
            user=self.other_user,
            name='Private',
            type=Category.Type.EXPENSE,
        )

        response = self.client.post('/api/budgets/', {
            'category': category.id,
            'amount': '100.00',
            'month': 11,
            'year': 2026,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('category', response.data)

    def test_duplicate_monthly_budget_is_rejected(self):
        Budget.objects.create(
            user=self.user,
            amount='100.00',
            month=11,
            year=2026,
        )

        response = self.client.post('/api/budgets/', {
            'amount': '200.00',
            'month': 11,
            'year': 2026,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
