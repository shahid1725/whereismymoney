from rest_framework import serializers

from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'icon', 'is_default', 'type')
        read_only_fields = ('id', 'is_default')

    def validate(self, attrs):
        name = attrs.get('name')
        category_type = attrs.get('type')

        if self.instance is not None:
            if name is None:
                name = self.instance.name

            if category_type is None:
                category_type = self.instance.type

        request = self.context['request']
        queryset = Category.objects.filter(
            user=request.user,
            name=name,
            type=category_type,
        )

        if self.instance is not None:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError(
                'You already have this category for the selected type.',
            )

        return attrs
