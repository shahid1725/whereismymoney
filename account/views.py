from account.models import Account
from account.serializers import AccountSerializer
from whereismymoney.views import UserOwnedModelViewSet


class AccountViewSet(UserOwnedModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
