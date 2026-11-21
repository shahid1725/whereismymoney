from django.conf import settings
from django.db import models
from django.db.models import Q

from category.models import Category


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='budgets',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='budgets',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-year', '-month', 'category__name')
        constraints = (
            models.CheckConstraint(
                condition=Q(month__gte=1, month__lte=12),
                name='budget_month_between_1_and_12',
            ),
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name='budget_amount_greater_than_zero',
            ),
            models.UniqueConstraint(
                condition=Q(category__isnull=False),
                fields=('user', 'category', 'month', 'year'),
                name='unique_category_budget_per_month',
            ),
            models.UniqueConstraint(
                condition=Q(category__isnull=True),
                fields=('user', 'month', 'year'),
                name='unique_monthly_budget',
            ),
        )

    def __str__(self):
        return f'{self.month}/{self.year}: {self.amount}'
