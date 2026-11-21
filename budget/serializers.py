from decimal import Decimal

from rest_framework import serializers

from budget.models import Budget
from category.models import Category
from whereismymoney.fields import CurrentUserPrimaryKeyRelatedField


class BudgetSerializer(serializers.ModelSerializer):
    category = CurrentUserPrimaryKeyRelatedField(
        allow_null=True,
        queryset=Category.objects.all(),
        required=False,
    )

    class Meta:
        model = Budget
        fields = (
            'id',
            'user',
            'category',
            'amount',
            'month',
            'year',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate_amount(self, value):
        if value <= Decimal('0'):
            raise serializers.ValidationError('Amount must be greater than zero.')

        return value

    def validate_month(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError('Month must be between 1 and 12.')

        return value

    def validate(self, attrs):
        category = attrs.get('category')
        month = attrs.get('month')
        year = attrs.get('year')

        if self.instance is not None:
            if 'category' not in attrs:
                category = self.instance.category

            if month is None:
                month = self.instance.month

            if year is None:
                year = self.instance.year

        request = self.context['request']
        queryset = Budget.objects.filter(
            user=request.user,
            category=category,
            month=month,
            year=year,
        )

        if self.instance is not None:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError(
                'A budget already exists for this period and category.',
            )

        return attrs
