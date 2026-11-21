from django.conf import settings
from django.db import models


class Category(models.Model):
    class Type(models.TextChoices):
        INCOME = 'income', 'Income'
        EXPENSE = 'expense', 'Expense'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
    )
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True)
    is_default = models.BooleanField(default=False)
    type = models.CharField(max_length=7, choices=Type.choices)

    class Meta:
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'name', 'type'),
                name='unique_category_name_and_type_per_user',
            ),
        )

    def __str__(self):
        return self.name
