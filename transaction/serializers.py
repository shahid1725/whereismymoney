from decimal import Decimal

from rest_framework import serializers

from account.models import Account
from category.models import Category
from transaction.models import Transaction
from whereismymoney.fields import CurrentUserPrimaryKeyRelatedField


class TransactionSerializer(serializers.ModelSerializer):
    category = CurrentUserPrimaryKeyRelatedField(queryset=Category.objects.all())
    account = CurrentUserPrimaryKeyRelatedField(queryset=Account.objects.all())

    class Meta:
        model = Transaction
        fields = (
            'id',
            'category',
            'account',
            'user',
            'type',
            'amount',
            'description',
            'date',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate_amount(self, value):
        if value <= Decimal('0'):
            raise serializers.ValidationError('Amount must be greater than zero.')

        return value

    def validate(self, attrs):
        category = attrs.get('category')
        transaction_type = attrs.get('type')

        if self.instance is not None:
            if category is None:
                category = self.instance.category

            if transaction_type is None:
                transaction_type = self.instance.type

        if category is not None and category.type != transaction_type:
            raise serializers.ValidationError({
                'category': 'Category type must match the transaction type.',
            })

        return attrs
