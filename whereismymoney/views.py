import logging

from django.db.models.deletion import ProtectedError
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response


logger = logging.getLogger(__name__)


class UserOwnedModelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
        except ProtectedError:
            logger.exception(
                'Unable to delete protected %s instance.',
                instance._meta.label,
            )
            return Response(
                {'detail': 'This item is in use and cannot be deleted.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
