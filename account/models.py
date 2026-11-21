from django.conf import settings
from django.db import models


class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
    )
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='accounts/', blank=True)

    class Meta:
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'name'),
                name='unique_account_name_per_user',
            ),
        )

    def __str__(self):
        return self.name
