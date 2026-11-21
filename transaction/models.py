from django.conf import settings
from django.db import models

from account.models import Account
from category.models import Category


class Transaction(models.Model):
    class Type(models.TextChoices):
        INCOME = 'income', 'Income'
        EXPENSE = 'expense', 'Expense'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    type = models.CharField(max_length=7, choices=Type.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date', '-created_at')

    def __str__(self):
        return f'{self.type}: {self.amount}'
