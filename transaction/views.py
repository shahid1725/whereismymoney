from transaction.models import Transaction
from transaction.serializers import TransactionSerializer
from whereismymoney.views import UserOwnedModelViewSet


class TransactionViewSet(UserOwnedModelViewSet):
    queryset = Transaction.objects.select_related('category', 'account')
    serializer_class = TransactionSerializer
