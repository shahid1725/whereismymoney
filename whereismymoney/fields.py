from rest_framework import serializers


class CurrentUserPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.context.get('request')

        if request is None or not request.user.is_authenticated:
            return queryset.none()

        return queryset.filter(user=request.user)
