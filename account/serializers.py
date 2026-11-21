from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'img')
        read_only_fields = ('id',)

    def validate_name(self, value):
        request = self.context['request']
        queryset = Account.objects.filter(user=request.user, name=value)

        if self.instance is not None:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError(
                'You already have an account with this name.',
            )

        return value
