from budget.models import Budget
from budget.serializers import BudgetSerializer
from whereismymoney.views import UserOwnedModelViewSet


class BudgetViewSet(UserOwnedModelViewSet):
    queryset = Budget.objects.select_related('category')
    serializer_class = BudgetSerializer
